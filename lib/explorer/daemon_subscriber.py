
import binascii
import json
import multiprocessing
import time

from lib import zmqmin
from lib import minql

from lib.explorer.explorer_server import GetById

MEMPOOL_STATS_INTERVALS = range(1, 10) + range(10, 20, 2) + range(20, 100, 10) + range(100, 300, 20) + range(300, 1100, 100)
CURRENCY_UNIT_FLOAT = 100000000

def BtcStrToSatInt(btc_str):
    sat_float = float(btc_str) * CURRENCY_UNIT_FLOAT
    return int(sat_float)

def FeerateFromBtcFeeStrAndVsize(btc_str, vsize):
    fee_sat = BtcStrToSatInt(btc_str)
    return int(fee_sat / vsize)

class ChainCacher(object):

    def __init__(self, chain, rpccaller, db_client, *args, **kwargs):

        super(ChainCacher, self).__init__(*args, **kwargs)

        self.chain = chain
        self.rpccaller = rpccaller
        self.db_client = db_client

class CronCacher(ChainCacher, multiprocessing.Process):

    def __init__(self, chain, rpccaller, db_client, wait_time=60,
                 *args, **kwargs):

        super(CronCacher, self).__init__(chain, rpccaller, db_client, *args, **kwargs)

        self.wait_time = wait_time
        self.initial_wait_time = 5

    def run(self):
        time.sleep(self.initial_wait_time)
        while True:
            self._cron_loop()
            time.sleep(self.wait_time)


def IncrementStats(stats, interval, tx_fee, tx_size):
    stats['count'][interval] = stats['count'][interval] + 1
    stats['fee'][interval] = stats['fee'][interval] + BtcStrToSatInt(tx_fee)
    stats['vsize'][interval] = stats['vsize'][interval] + tx_size

class MempoolStatsCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time=60,
                 *args, **kwargs):

        super(MempoolStatsCacher, self).__init__(chain, rpccaller, db_client, wait_time,
                                                 *args, **kwargs)

        self.stats_types = ['count', 'fee', 'vsize']
        self.stats_intervals = MEMPOOL_STATS_INTERVALS

    def _cron_loop(self):
        mempool_state = self.rpccaller.RpcCall('getrawmempool', {'verbose': True})
        if 'error' in mempool_state and mempool_state['error']:
            return
        # TODO remove special case for getrawmempool
        mempool_state = mempool_state['result']

        stats = {}
        for stats_type in self.stats_types:
            stats[stats_type] = {}
            stats[stats_type]['total'] = 0
            for stats_interval in self.stats_intervals:
                stats[stats_type][stats_interval] = 0

        for txid, tx_entry in mempool_state.iteritems():
            tx_fee = tx_entry['fee']
            tx_size = tx_entry['size']
            tx_feerate = FeerateFromBtcFeeStrAndVsize(tx_fee, tx_size)
            max_interval = self.stats_intervals[-1]

            for stats_interval in self.stats_intervals:
                if tx_feerate <= stats_interval:
                    max_interval = stats_interval

            for stats_interval in self.stats_intervals:
                if tx_feerate <= stats_interval:
                    IncrementStats(stats, stats_interval, tx_fee, tx_size)

            IncrementStats(stats, 'total', tx_fee, tx_size)

        entry = {}
        entry['id'] = int(time.time())
        entry['blob'] = json.dumps(stats)
        try:
            db_result = self.db_client.put(self.chain + "_" + 'mempoolstats', entry)
        except:
            print('FAILED caching %s in chain %s' % ('mempoolstats', self.chain))
            return

class GreedyCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time=60,
                 *args, **kwargs):

        super(GreedyCacher, self).__init__(chain, rpccaller, db_client, wait_time,
                                                 *args, **kwargs)

        self.last_cached_height = -1

    def cache_height(self, height):
        try:
            blockstats = GetById(self.db_client, self.rpccaller, self.chain, 'blockstats', height)
            blockhash = GetById(self.db_client, self.rpccaller, self.chain, 'blockhash', height)['result']
            block = GetById(self.db_client, self.rpccaller, self.chain, 'block', blockhash)
            print('cache_height', height, blockhash)
        except:
            print('FAILED GREEDY CACHE height %s in chain %s' % (height, self.chain))

    def _cron_loop(self):
        chaininfo = GetById(self.db_client, self.rpccaller, self.chain, 'chaininfo', self.chain)
        if 'error' in chaininfo:
            return
        next_cached_height = chaininfo['blocks']
        height = next_cached_height
        while height > self.last_cached_height:
            self.cache_height(height)
            height = height - 1
        self.last_cached_height = next_cached_height


class DaemonReorgManager(GreedyCacher):

    def __init__(self, chain, rpccaller, db_client):

        super(DaemonReorgManager, self).__init__(chain, rpccaller, db_client)

        self.prev_reorg_height = -1
        self.prev_reorg_hash = None
        self.print_delete_tx = False


    def delete_from_height(self, block_height):
        criteria = {'height': {'ge': block_height}}
        blocks_to_delete = self.db_client.search(self.chain + "_" + 'block', criteria)
        for block in blocks_to_delete:
            blockhash = block['id']
            print('delete txs with blockhash %s' % blockhash)
            if self.print_delete_tx:
                print(block)
            else:
                to_delete_block = block
                del to_delete_block['tx']
                print('to_delete_block', to_delete_block)

            tx_criteria = {'blockhash': blockhash}
            self.db_client.delete(self.chain + "_" + 'tx', tx_criteria)

        self.db_client.delete(self.chain + "_" + 'block', criteria)
        self.db_client.delete(self.chain + "_" + 'blockstats', criteria)

    def is_descendant(self, block_height, block_hash):
        if self.prev_reorg_height >= block_height:
            return False

        return True

    def manage_reorg(self, block_height, block_hash):
        print('REORG DETECTED at height %s hash %s previous height %s hash %s' % (
            block_height, block_hash, self.prev_reorg_height, self.prev_reorg_hash))
    
    def update_tip(self, block_hash):
        json_result = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)
        block_height = json_result['height']
        block_mediantime = json_result['mediantime']

        if not self.prev_reorg_hash:
            self.prev_reorg_hash = block_hash
            self.prev_reorg_height = block_height

        if self.prev_reorg_hash == block_hash:
            # Don't do anything on first call or when the tip is the same
            return

        if not self.is_descendant(block_height, block_hash):
            self.manage_reorg(block_height, block_hash)

        self.prev_reorg_hash = block_hash
        self.prev_reorg_height = block_height

        entry = {}
        entry['id'] = self.chain
        entry['bestblockhash'] = block_hash
        entry['blocks'] = block_height
        entry['mediantime'] = block_mediantime
        try:
            db_result = self.db_client.put(self.chain + "_" + 'chaininfo', entry)
        except:
            print('FAILED GREEDY CACHE %s in chain %s' % ('chaininfo', self.chain), entry)
            return

        try:
            self.delete_from_height(block_height)
        except:
            print('FAILED HANDLING REORG calling delete_from_height %s' % block_height)
            return

        self.cache_height(block_height)


class DaemonSubscriber(zmqmin.Subscriber, zmqmin.Process):

    def __init__(self,
                 address,
                 chain,
                 rpccaller,
                 db_factory,
                 silent=False,
                 worker_id='DaemonSubscriber',
                 *args, **kwargs):

        self.chain = chain
        self.rpccaller = rpccaller
        self.db_factory = db_factory

        if (silent):
            import sys
            import os
            sys.stdout = open(os.devnull, 'w')

        super(DaemonSubscriber, self).__init__(
            address=address,
            context=None, single=False,
            worker_id=worker_id,
            json=False,
            topic='hashblock',
            multipart=True,
            *args, **kwargs)

    def _init_process(self):
        super(DaemonSubscriber, self)._init_process()
        self.reorg_man = DaemonReorgManager(self.chain, self.rpccaller, self.db_factory.create())

    def _loop(self):
        while True:
            msg_parts = self.receive_message()
            block_hash = binascii.hexlify(msg_parts[1])
            self.reorg_man.update_tip(block_hash)
