
import binascii
import datetime
import json
import multiprocessing
import time

from mintools import zmqmin, minql, ormin

from explorer import model

MEMPOOL_STATS_INTERVALS = (
    range(1, 5) + range(5, 30, 5) + range(30, 100, 10) +
    range(100, 200, 20) + range(200, 500, 50) + range(500, 1000, 100) + range(1000, 2000, 500))

CURRENCY_UNIT_FLOAT = 100000000

def BtcStrToSatInt(btc_str):
    sat_float = float(btc_str) * CURRENCY_UNIT_FLOAT
    return int(sat_float)

def FeerateFromBtcFeeStrAndVsize(btc_str, vsize):
    fee_sat = BtcStrToSatInt(btc_str)
    return int(fee_sat / vsize)

class RpcCacher(object):

    def __init__(self, rpccaller, db_client):
        super(RpcCacher, self).__init__()

        self.rpccaller = rpccaller
        model.RpcCachedModel.set_rpccaller(rpccaller)
        self.db_client = db_client
        ormin.Model.set_db(db_client)

class ChainCacher(RpcCacher):

    def __init__(self, chain, rpccaller, db_client):

        super(ChainCacher, self).__init__(rpccaller, db_client)

        self.chain = chain
        ormin.Form.set_namespace(self.chain)

class CronCacher(ChainCacher, multiprocessing.Process):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(CronCacher, self).__init__(chain, rpccaller, db_client)

        self.wait_time = wait_time
        self.initial_wait_time = initial_wait_time

    def run(self):
        time.sleep(self.initial_wait_time)
        while True:
            self._cron_loop()
            time.sleep(self.wait_time)

class MempoolSaver(CronCacher):

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(MempoolSaver, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

    def _cron_loop(self):
        try:
            self.rpccaller.RpcCall('savemempool', {})
            print('Success saving mempool...')
        except Exception as e:
            print("Error in MempoolSaver._cron_loop:", type(e), e)


def IncrementStats(stats, interval, tx_fee, tx_size):
    stats['count'][interval] = stats['count'][interval] + 1
    stats['fee'][interval] = stats['fee'][interval] + BtcStrToSatInt(tx_fee)
    stats['vsize'][interval] = stats['vsize'][interval] + tx_size

class MempoolStatsCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(MempoolStatsCacher, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time,
                                                 *args, **kwargs)

        self.stats_types = ['count', 'fee', 'vsize']
        self.stats_intervals = MEMPOOL_STATS_INTERVALS

    def _cron_loop(self):
        mempool_state = self.rpccaller.RpcCall('getrawmempool', {'verbose': True})
        if 'error' in mempool_state and mempool_state['error']:
            return

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

        int_time = int((datetime.datetime.now()).strftime('%s'))
        mempoolstats = model.Mempoolstats(json={
            'id': int_time,
            'time': int_time,
            'blob': json.dumps(stats),
        })
        try:
            mempoolstats.insert()
            print('SUCCESS caching %s in chain %s' % ('mempoolstats', self.chain))
        except Exception as e:
            print("Error in MempoolStatsCacher._cron_loop:", type(e), e)
            print('FAILED caching %s in chain %s %s' % ('mempoolstats', self.chain, json.dumps(mempoolstats.json())))

class GreedyCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time, cache_txs):

        super(GreedyCacher, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time)

        self.last_cached_height = -1
        self.cache_txs = cache_txs

    def cache_blockhash(self, blockhash):
        try:
            block = model.Block.get(blockhash)
            if not isinstance(block, model.Block):
                print("Error in GreedyCacher.cache_blockhash: wrong type for block", blockhash, block)
                return None

            model.Block.get(block.height)
            blockblob = json.loads(block.blob)
            if self.cache_txs and 'tx' in blockblob:
                for txid in blockblob['tx']:
                    tx = model.Tx.get(txid)
            return block.json()
        except Exception as e:
            print("Error in GreedyCacher.cache_blockhash:", blockhash, type(e), e)
            return None

    def _cron_loop(self):
        chaininfo = model.Chaininfo.get(self.chain)
        if not isinstance(chaininfo, model.Chaininfo):
            print("Error in GreedyCacher._cron_loop: wrong type for chaininfo", chaininfo)
            return

        height = chaininfo.blocks
        blockhash = chaininfo.bestblockhash
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

        self.last_cached_height = chaininfo.blocks


class DaemonReorgManager(GreedyCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time=60, initial_wait_time=60, cache_txs=False):

        super(DaemonReorgManager, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time, cache_txs)

        self.prev_reorg_height = -1
        self.prev_reorg_hash = None

    def update_chainfo(self, block):
        chaininfo = model.Chaininfo(json={
            'bestblockhash': block['hash'],
            'blocks': block['height'],
            'mediantime': block['mediantime'],
        })
        chaininfo.id = self.chain
        try:
            chaininfo.save()
            if chaininfo.errors:
                print("Validation errors saving chaininfo:", chaininfo.errors)
        except Exception as e:
            print("Error in DaemonReorgManager.update_chainfo:", type(e), e)
            print('FAILED UPDATE TIP in chain %s %s' % (self.chain, entry), json.dumps(chaininfo.json()))
            return False

        return True


    def delete_txs_from_blocks(self, blocks_to_delete):

        for block in blocks_to_delete:
            blockhash = block.id
            print('delete txs with blockhash %s' % blockhash)

            tx_criteria = {'blockhash': blockhash}
            try:
                txs_to_delete = model.Tx.search(tx_criteria)
                print('txs_to_delete', txs_to_delete)
                if txs_to_delete:
                    model.Tx.delete(tx_criteria)
            except minql.NotFoundError:
                pass

    def delete_from_height(self, block_height):

        criteria = {'height': {'ge': block_height}}
        try:
            blocks_to_delete = model.Block.search(criteria)
            if blocks_to_delete:
                try:
                    self.delete_txs_from_blocks(blocks_to_delete)
                except Exception as e:
                    print("Error in DaemonReorgManager.delete_from_height:", type(e), e)
                    print('ERROR with blocks_to_delete', len(blocks_to_delete))
                    # return False
                model.Block.delete(criteria)
        except minql.NotFoundError:
            pass

        try:
            stats_to_delete = model.Blockstats.search(criteria)
            print('stats_to_delete', len(stats_to_delete))
            if stats_to_delete:
                model.Blockstats.delete(criteria)
        except minql.NotFoundError:
            pass

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
                orm_block = model.Block.get(block_hash)
                if not isinstance(orm_block, model.Block):
                    print('Error in DaemonReorgManager.get_ascendant: wrong type for block', block_hash, orm_block)
                    return None
                block = json.loads(orm_block.blob)
            except Exception as e:
                print('FAILED DaemonReorgManager.get_ascendant: block.get(%s)' % block_hash, type(e), e, block)
                return None

        return block

    def check_basic_block(self, block):
        return block and 'hash' in block and 'height' in block and 'previousblockhash' in block

    def find_common_ancestor(self, block_A, block_B):
        if not self.check_basic_block(block_A):
            if not self.check_basic_block(block_B):
                return None
            else:
                return block_B
        elif not self.check_basic_block(block_B):
            return block_A

        try:
            if block_A['hash'] == block_B['hash']:
                return block_A
            elif block_A['height'] > block_B['height']:
                return self.find_common_ancestor(block_B, block_A)
            elif block_A['height'] < block_B['height']:
                ascendant = self.get_ascendant(block_B, block_A['height'])
                if not ascendant:
                    print('FAILED calling get_ascendant in find_common_ancestor A: %s %s B: %s %s' % (
                        block_A['height'], block_A['hash'], block_B['height'], block_B['hash']))
                    return None
                return self.find_common_ancestor(block_A, ascendant)
            elif block_A['height'] == block_B['height']:
                ascendantA = self.get_ascendant(block_A, block_A['height'] - 1)
                ascendantB = self.get_ascendant(block_B, block_A['height'] - 1)
                if not ascendantA or not ascendantB:
                    print('FAILED finding common_ancestor A: %s %s B: %s %s' % (
                        block_A['height'], block_A['hash'], block_B['height'], block_B['hash']))
                    return None
                return self.find_common_ancestor(ascendantA, ascendantB)

        except Exception as e:
            print("Error in DaemonReorgManager.find_common_ancestor:", type(e), e)
            print('FAILED calling find_common_ancestor A: %s %s B: %s %s' % (
                block_A['height'], block_A['hash'], block_B['height'], block_B['hash']))

        return None

    def manage_reorg(self, block):
        print('REORG DETECTED at previous height %s and hash %s' % (self.prev_reorg_height, self.prev_reorg_hash))
        if isinstance(block, dict) and 'height' in block and 'hash' in block:
            print('new height %s and hash %s' % (block['height'], block['hash']))

        orm_block = model.Block.get(self.prev_reorg_hash)
        if not isinstance(orm_block, model.Block):
            print('Error in DaemonReorgManager.manage_reorg: wrong type for block', self.prev_reorg_hash, orm_block)
            return False
        self.prev_reorg_block = json.loads(orm_block.blob)
        common_ancestor = self.find_common_ancestor(self.prev_reorg_block, block)
        if not common_ancestor or not self.check_basic_block(common_ancestor):
            print('FAILED HANDLING REORG calling find_common_ancestor %s' % block['height'], common_ancestor)
            common_ancestor = self.get_ascendant(block, block['height'] - 100)
            print('Reorging to new common ancestor, old common ancestor:', self.prev_reorg_block)
            print('new common ancestor:', common_ancestor)

        try:
            block_height = common_ancestor['height'] + 1
            self.delete_from_height(block_height)
            print('HANDLING REORG SUCCESS for delete_from_height %s' % block_height)
        except Exception as e:
            print("Error in DaemonReorgManager.manage_reorg:", type(e), e)
            print('FAILED HANDLING REORG calling delete_from_height')
            return False

        if not self.commit_new_prev(common_ancestor):
            print('FAILED update_chainfo in commit_new_prev in manage_reorg', common_ancestor)
            return False

        print('HANDLING REORG SUCCESS at previous height %s and hash %s, new height %s and hash %s' % (
            self.prev_reorg_block['height'], self.prev_reorg_block['hash'], block['height'], block['hash']))
        return True

    def update_tip(self, block_hash):
        print('update_tip from reorg height %s hash %s to %s' % (self.prev_reorg_height, self.prev_reorg_hash, block_hash))

        try:
            orm_block = model.Block.get(block_hash)
            if not isinstance(orm_block, model.Block):
                print('Error in DaemonReorgManager.update_tip: wrong type for block', block_hash, orm_block)
                return
            block = json.loads(orm_block.blob)
            assert(block and 'hash' in block and block['hash'] == block_hash and
                   'height' in block and 'mediantime' in block)
        except Exception as e:
            print("Error in DaemonReorgManager.update_tip:", type(e), e)
            print('FAILED update_tip block.get(%s)' % block_hash)
            return

        if not block:
            print('FAILED update_tip block.get(%s) returned empty block' % block_hash)
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
            if not self.manage_reorg(ascendant):
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
