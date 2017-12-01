
import binascii
import json
import multiprocessing
import time

from lib import zmqmin
from lib import minql

from lib.explorer.explorer_server import GetById

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

def IncrementStats(stats, interval, tx_fee, tx_size):
    stats['count'][interval] = stats['count'][interval] + 1
    stats['fee'][interval] = stats['fee'][interval] + BtcStrToSatInt(tx_fee)
    stats['vsize'][interval] = stats['vsize'][interval] + tx_size

class MempoolStatsCacher(ChainCacher, multiprocessing.Process):

    def __init__(self, chain, rpccaller, db_client, wait_time=60,
                 *args, **kwargs):

        super(MempoolStatsCacher, self).__init__(chain, rpccaller, db_client, *args, **kwargs)

        self.wait_time = wait_time
        self.initial_wait_time = 5
        self.stats_types = ['count', 'fee', 'vsize']
        self.stats_intervals = range(1, 6) + range(10, 100, 10) + range(100, 1100, 100)

    def __loop(self):
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

    def run(self):
        time.sleep(self.initial_wait_time)
        while True:
            self.__loop()
            time.sleep(self.wait_time)

class DaemonReorgManager(ChainCacher):

    def __init__(self, chain, rpccaller, db_client):

        super(DaemonReorgManager, self).__init__(chain, rpccaller, db_client)

    def delete_from_height(self, block_height):
        criteria = {'height': {'ge': block_height}}
        blocks_to_delete = self.db_client.search(self.chain + "_" + 'block', criteria)
        for block in blocks_to_delete:
            blockhash = block['id']
            print('delete txs with blockhash %s' % blockhash)
            print('to_delete_block', block)
            tx_criteria = {'blockhash': blockhash}
            self.db_client.delete(self.chain + "_" + 'tx', tx_criteria)

        self.db_client.delete(self.chain + "_" + 'block', criteria)
        self.db_client.delete(self.chain + "_" + 'blockstats', criteria)

    def update_tip(self, block_hash):
        json_result = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)
        block_height = json_result['height']
        block_mediantime = json_result['mediantime']

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
            print('FAILED HANDLING REORG WITH %s in chain %s' % ('blockstats', self.chain), criteria)
            return

        try:
            json_result = GetById(self.db_client, self.rpccaller, self.chain, 'blockstats', block_height)
        except:
            print('FAILED GREEDY CACHE %s in chain %s for height %s' % ('blockstats', self.chain, block_height))

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
