# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

from mintools.minql import NotFoundError

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.stats import Blockstats
from explorer.models.transaction import Tx

from explorer.process.greedy import GreedyCacher

class DaemonReorgManager(GreedyCacher):

    def __init__(self, chain, rpccaller, db_client, wait_time=60, initial_wait_time=60, cache_txs=False, cache_stats=True):

        super(DaemonReorgManager, self).__init__(chain, rpccaller, db_client, wait_time, initial_wait_time, cache_txs, cache_stats)

        self.prev_reorg_height = -1
        self.prev_reorg_hash = None

    def update_chainfo(self, block):

        chaininfo = Chaininfo.get(self.chain)
        if not isinstance(chaininfo, Chaininfo):
            chaininfo = Chaininfo()
            chaininfo.id = self.chain
            chaininfo.start_caching_progress()

        chaininfo.bestblockhash = block.id
        chaininfo.blocks = block.height
        if chaininfo.blocks < chaininfo.cached_blocks:
            chaininfo.cached_blocks = chaininfo.blocks
            chaininfo.clean_caching_progress_fields()
        chaininfo.mediantime = block.mediantime
        try:
            chaininfo.save()
            if chaininfo.errors:
                print("Validation errors saving chaininfo:", chaininfo.errors)
        except Exception as e:
            print("Error in DaemonReorgManager.update_chainfo:", type(e), e)
            print('FAILED UPDATE TIP in chain %s' % self.chain, json.dumps(chaininfo.json()))
            return False

        return True


    def delete_txs_from_blocks(self, blocks_to_delete):

        for block in blocks_to_delete:
            blockhash = block.id
            print('delete txs with blockhash %s' % blockhash)

            tx_criteria = {'blockhash': blockhash}
            try:
                txs_to_delete = Tx.search(tx_criteria)
                print('txs_to_delete', txs_to_delete)
                if txs_to_delete:
                    Tx.delete(tx_criteria)
            except NotFoundError:
                pass

    def delete_from_height(self, block_height):

        criteria = {'height': {'ge': block_height}}
        try:
            blocks_to_delete = Block.search(criteria)
            if blocks_to_delete:
                try:
                    self.delete_txs_from_blocks(blocks_to_delete)
                except Exception as e:
                    print("Error in DaemonReorgManager.delete_from_height:", type(e), e)
                    print('ERROR with blocks_to_delete', len(blocks_to_delete))
                    # return False
                Block.delete(criteria)
        except NotFoundError:
            pass

        try:
            stats_to_delete = Blockstats.search(criteria)
            print('stats_to_delete', len(stats_to_delete))
            if stats_to_delete:
                Blockstats.delete(criteria)
        except NotFoundError:
            pass

    def commit_new_prev(self, block):
        self.prev_reorg_hash = block.id
        self.prev_reorg_height = block.height
        self.cache_blockhash(self.prev_reorg_hash)

        if not self.update_chainfo(block):
            print('FAILED update_chainfo in commit_new_prev', block)
            return False

        return True

    def get_ascendant(self, block, target_height):

        if not block or not block.id or not block.height or target_height < 0:
            return None

        block_height = block.height
        block_hash = block.id

        if target_height > block_height:
            return None

        while target_height < block_height:
            print('get_ascendant loop height %s hash %s', block_height, block_hash)

            if not block.previousblockhash:
                return None
            block_hash = block.previousblockhash
            block_height = block_height - 1
            try:
                block = Block.get(block_hash)
                if not isinstance(block, Block):
                    print('Error in DaemonReorgManager.get_ascendant: wrong type for block', block_hash, block)
                    return None
            except Exception as e:
                print('FAILED DaemonReorgManager.get_ascendant: block.get(%s)' % block_hash, type(e), e, block.json())
                return None

        return block

    def check_basic_block(self, block):
        return block and block.id and block.height and block.previousblockhash

    def find_common_ancestor(self, block_A, block_B):
        if not self.check_basic_block(block_A):
            if not self.check_basic_block(block_B):
                return None
            else:
                return block_B
        elif not self.check_basic_block(block_B):
            return block_A

        try:
            if block_A.id == block_B.id:
                return block_A
            elif block_A.height > block_B.height:
                return self.find_common_ancestor(block_B, block_A)
            elif block_A.height < block_B.height:
                ascendant = self.get_ascendant(block_B, block_A.height)
                if not ascendant:
                    print('FAILED calling get_ascendant in find_common_ancestor A: %s %s B: %s %s' % (
                        block_A.height, block_A.id, block_B.height, block_B.id))
                    return None
                return self.find_common_ancestor(block_A, ascendant)
            elif block_A.height == block_B.height:
                ascendantA = self.get_ascendant(block_A, block_A.height - 1)
                ascendantB = self.get_ascendant(block_B, block_A.height - 1)
                if not ascendantA or not ascendantB:
                    print('FAILED finding common_ancestor A: %s %s B: %s %s' % (
                        block_A.height, block_A.id, block_B.height, block_B.id))
                    return None
                return self.find_common_ancestor(ascendantA, ascendantB)

        except Exception as e:
            print("Error in DaemonReorgManager.find_common_ancestor:", type(e), e)
            print('FAILED calling find_common_ancestor A: %s %s B: %s %s' % (
                block_A.height, block_A.id, block_B.height, block_B.id))

        return None

    def manage_reorg(self, block):
        print('REORG DETECTED at previous height %s and hash %s' % (self.prev_reorg_height, self.prev_reorg_hash))
        if isinstance(block, Block) and block.id and block.height:
            print('new height %s and hash %s' % (block.height, block.id))

        prev_reorg_block = Block.get(self.prev_reorg_hash)
        if not isinstance(prev_reorg_block, Block):
            print('Error in DaemonReorgManager.manage_reorg: wrong type for block', self.prev_reorg_hash, prev_reorg_block)
            return False
        common_ancestor = self.find_common_ancestor(prev_reorg_block, block)
        if not common_ancestor or not self.check_basic_block(common_ancestor):
            print('FAILED HANDLING REORG calling find_common_ancestor %s' % block.height, common_ancestor)
            common_ancestor = self.get_ascendant(block, block.height - 100)
            print('Reorging to new common ancestor, old common ancestor:', prev_reorg_block)
            print('new common ancestor:', common_ancestor)

        try:
            block_height = common_ancestor.height + 1
            self.delete_from_height(block_height)
            print('HANDLING REORG SUCCESS for delete_from_height %s' % block_height)
        except Exception as e:
            print("Error in DaemonReorgManager.manage_reorg:", type(e), e)
            print('FAILED HANDLING REORG calling delete_from_height')
            return False

        if not self.commit_new_prev(common_ancestor):
            print('FAILED update_chainfo in commit_new_prev in manage_reorg', common_ancestor)
            return False

        print('SUCCESS HANDLING REORG')
        if isinstance(block, Block) and block.id and block.height:
            print('new height %s and hash %s' % (block.height, block.id))
        if isinstance(prev_reorg_block, Block) and prev_reorg_block.id and prev_reorg_block.height:
            print('previous height %s and hash %s' % (prev_reorg_block.height, prev_reorg_block.id))
        return True

    def update_tip(self, block_hash):
        print('update_tip from reorg height %s hash %s to %s' % (self.prev_reorg_height, self.prev_reorg_hash, block_hash))

        try:
            block = Block.get(block_hash)
            if not isinstance(block, Block):
                print('Error in DaemonReorgManager.update_tip: wrong type for block', block_hash, block)
                return
            assert(block and block.id and block.id == block_hash and block.height != None and block.mediantime)
        except Exception as e:
            print("Error in DaemonReorgManager.update_tip:", type(e), e)
            print('FAILED update_tip block.get(%s)' % block_hash)
            return

        if not block:
            print('FAILED update_tip block.get(%s) returned empty block' % block_hash)
            return

        block_height = block.height

        if not self.prev_reorg_hash:
            # Only commit new tip if the first call
            if not self.commit_new_prev(block):
                print('FAILED update_chainfo in commit_new_prev in update_tip', block.json())
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
        if ascendant and ascendant.id and ascendant.id == self.prev_reorg_hash:
            self.commit_new_prev(block)
        else:
            if not self.manage_reorg(ascendant):
                return

    def _cron_loop(self):
        try:
            chaininfo = self.rpccaller.RpcCall('getblockchaininfo', {})
            if 'bestblockhash' in chaininfo:
                self.update_tip(chaininfo['bestblockhash'])
        except Exception as e:
            print("Error in DaemonReorgManager._cron_loop:", type(e), e)
