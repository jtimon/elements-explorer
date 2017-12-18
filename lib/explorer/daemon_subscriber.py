
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

    def cache_blockhash(self, blockhash):
        try:
            block = GetById(self.db_client, self.rpccaller, self.chain, 'block', blockhash)
            blockstats = GetById(self.db_client, self.rpccaller, self.chain, 'blockstats', block['height'])
        except:
            print('FAILED cache_blockhash %s' % blockhash)
            return None
        return block

    def _cron_loop(self):
        chaininfo = GetById(self.db_client, self.rpccaller, self.chain, 'chaininfo', self.chain)
        if 'error' in chaininfo:
            return
        height = chaininfo['blocks']
        blockhash = chaininfo['bestblockhash']
        while height > self.last_cached_height:
            block = self.cache_blockhash(blockhash)
            if block and 'previousblockhash' in block:
                blockhash = block['previousblockhash']
            elif block and height == 0:
                # the genesis block doesn't have a previous block
                break
            else:
                print('FAILED no block %s' % blockhash)
                return
            height = height - 1

        self.last_cached_height = chaininfo['blocks']


class DaemonReorgManager(GreedyCacher):

    def __init__(self, chain, rpccaller, db_client):

        super(DaemonReorgManager, self).__init__(chain, rpccaller, db_client)

        self.prev_reorg_height = -1
        self.prev_reorg_hash = None
        self.print_delete_tx = False

    def update_chainfo(self, block):
        entry = {}
        entry['id'] = self.chain
        entry['bestblockhash'] = block['hash']
        entry['blocks'] = block['height']
        entry['mediantime'] = block['mediantime']
        try:
            db_result = self.db_client.put(self.chain + "_" + 'chaininfo', entry)
        except:
            print('FAILED UPDATE TIP in chain %s' % (self.chain), entry)
            return False

        return True


    def delete_txs_from_blockheight(self, criteria):
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
            txs_to_delete = self.db_client.search(self.chain + "_" + 'tx', criteria)
            if txs_to_delete:
                self.db_client.delete(self.chain + "_" + 'tx', tx_criteria)

    def delete_from_height(self, block_height):
        criteria = {'height': {'ge': block_height}}
        self.delete_txs_from_blockheight(criteria)
        self.db_client.delete(self.chain + "_" + 'block', criteria)
        self.db_client.delete(self.chain + "_" + 'blockstats', criteria)

    def commit_new_prev(self, block):
        self.prev_reorg_hash = block['hash']
        self.prev_reorg_height = block['height']
        self.cache_blockhash(self.prev_reorg_hash)

        if not self.update_chainfo(block):
            print('FAILED update_chainfo in commit_new_prev', block)
            return False

        return True

    def get_ascendant(self, block, target_height):

        if not block or not 'hash' in block or not 'height' in block or target_height < 0:
            return None

        block_height = block['height']
        block_hash = block['hash']

        if target_height > block_height:
            return None

        while target_height < block_height:
            print('get_ascendant loop height %s hash %s', block_height, block_hash)

            if not 'previousblockhash' in block:
                return None
            block_hash = block['previousblockhash']
            block_height = block_height - 1
            try:
                block = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)
            except:
                print('FAILED get_ascendant block.get(%s)' % block_hash, block)
                return None

        return block

    def manage_reorg(self, block):
        block_height = block['height']
        block_hash = block['hash']
        print('REORG DETECTED at height %s hash %s previous height %s hash %s' % (
            block_height, block_hash, self.prev_reorg_height, self.prev_reorg_hash))

        try:
            self.delete_from_height(block_height)
            print('HANDLING REORG SUCCESS delete_from_height %s' % block_height)
        except:
            print('FAILED HANDLING REORG calling delete_from_height %s' % block_height)
            return False

        if not self.commit_new_prev(block):
            print('FAILED update_chainfo in commit_new_prev in manage_reorg', block)
            return False

        return True

    def update_tip(self, block_hash):
        print('update_tip from reorg height %s hash %s to %s', self.prev_reorg_height, self.prev_reorg_hash, block_hash)

        try:
            block = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)
            assert(block and 'hash' in block and block['hash'] == block_hash and
                   'height' in block and 'mediantime' in block)
        except:
            print('FAILED update_tip block.get(%s)' % block_hash, block)
            return

        block_height = block['height']

        if not self.prev_reorg_hash:
            # Only commit new tip if the first call
            if not self.commit_new_prev(block):
                print('FAILED update_chainfo in commit_new_prev in update_tip', block)
                return

            print('START update_tip with block', block_height, block_hash)
            return

        if self.prev_reorg_hash == block_hash:
            # Don't do anything if we're already on the tip
            return

        if self.prev_reorg_height >= block_height:
            if not self.manage_reorg(block):
                return
            return

        ascendant = self.get_ascendant(block, self.prev_reorg_height)
        if ascendant and 'hash' in ascendant and ascendant['hash'] == self.prev_reorg_hash:
            self.commit_new_prev(block)
        else:
            if not self.manage_reorg(block):
                return

    def _cron_loop(self):
        chaininfo = self.rpccaller.RpcCall('getblockchaininfo', {})
        if 'bestblockhash' in chaininfo:
            self.update_tip(chaininfo['bestblockhash'])


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
