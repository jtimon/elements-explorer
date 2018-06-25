
from explorer.process.base import CronCacher

class GreedyCacher(CronCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time, cache_txs, cache_stats, wait_time_greedy=2):

        super(GreedyCacher, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time)

        self.last_cached_height = -1
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

            return block

        except Exception as e:
            print("Error in GreedyCacher.cache_blockhash:", blockhash, type(e), e)
            return None

    def _cron_loop(self):
        chaininfo = Chaininfo.get(self.chain)
        if not isinstance(chaininfo, Chaininfo):
            print("Error in GreedyCacher._cron_loop: wrong type for chaininfo", chaininfo)
            return

        height = chaininfo.blocks
        blockhash = chaininfo.bestblockhash
        while height > self.last_cached_height:
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
            time.sleep(self.wait_time_greedy)

        self.last_cached_height = chaininfo.blocks
