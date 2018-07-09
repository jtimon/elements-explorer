
import json
import time

from explorer.process.base import CronCacher

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.stats import Blockstats
from explorer.models.transaction import Tx

class GreedyCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time, cache_txs, cache_stats, wait_time_greedy=1):

        super(GreedyCacher, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time)

        self.cache_txs = cache_txs
        self.cache_stats = cache_stats
        self.wait_time_greedy = wait_time_greedy

    def cache_blockhash(self, blockhash):
        try:
            block = Block.get(blockhash)
            if not isinstance(block, Block):
                print("Error in GreedyCacher.cache_blockhash: wrong type for block", blockhash, block)
                return None

            if self.cache_stats:
                Blockstats.get(block.height)

            if self.cache_txs:
                tx_ids = json.loads(block.tx)
                for txid in tx_ids:
                    tx = Tx.get(txid)
                    time.sleep(self.wait_time_greedy)

            return block

        except Exception as e:
            print("Error in GreedyCacher.cache_blockhash:", blockhash, type(e), e)
            return None

    def _cron_loop(self):
        chaininfo = Chaininfo.get(self.chain)
        if not isinstance(chaininfo, Chaininfo):
            print("Error in GreedyCacher._cron_loop: wrong type for chaininfo", chaininfo)
            return

        if chaininfo.caching_first == -1 or chaininfo.caching_last == -1 or chaininfo.caching_blockhash == '':
            height = chaininfo.blocks
            blockhash = chaininfo.bestblockhash
            chaininfo.caching_first = height
            chaininfo.caching_blockhash = blockhash
            chaininfo.caching_last = height
            chaininfo.save()
        else:
            height = chaininfo.caching_first
            blockhash = chaininfo.caching_blockhash

        next_cached_blocks = chaininfo.caching_last
        while height > chaininfo.cached_blocks:
            block = self.cache_blockhash(blockhash)
            if not block:
                print('Error in GreedyCacher._cron_loop: no block %s %s' % (height, blockhash))
                return
            elif block.previousblockhash:
                blockhash = block.previousblockhash
            elif height == 0:
                # the genesis block doesn't have a previous block
                break
            else:
                print('Error in GreedyCacher._cron_loop: no previousblockhash in block %s %s' % (height, blockhash), block)
                return

            height = height - 1
            chaininfo = Chaininfo.get(self.chain)
            if not isinstance(chaininfo, Chaininfo):
                print("Error in GreedyCacher._cron_loop: wrong type for chaininfo", chaininfo)
                return

            chaininfo.caching_first = height
            chaininfo.caching_blockhash = blockhash
            chaininfo.save()

        chaininfo = Chaininfo.get(self.chain)
        if not isinstance(chaininfo, Chaininfo):
            print("Error in GreedyCacher._cron_loop: wrong type for chaininfo", chaininfo)
            return
        chaininfo.cached_blocks = next_cached_blocks
        chaininfo.clean_caching_progress_fields()
        chaininfo.save()
