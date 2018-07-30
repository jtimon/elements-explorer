#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

print('Running %s' % (__file__))

# ===----------------------------------------------------------------------===

from explorer.env_config import AVAILABLE_CHAINS, AVAILABLE_RPCS
from explorer.process.generator.block import BlockGenerator
from explorer.process.generator.pegin import PeginGenerator
from explorer.process.generator.pegout import PegoutGenerator
from explorer.process.generator.transaction import TxGenerator
from explorer.process.greedy import GreedyCacher
from explorer.process.subscriber import DaemonReorgManager

from explorer.test_tools.test_prototypes import RepeatPerAvailableChainTest

class ExampleTest(RepeatPerAvailableChainTest):

    def run_tests_for_chain(self, chain):

        block_gen_params = [chain, AVAILABLE_RPCS[chain]]
        block_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['block_gen'])
        self.block_generator = BlockGenerator(*block_gen_params)

        tx_gen_params = [chain, AVAILABLE_RPCS[chain]]
        tx_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['tx_gen'])
        self.tx_generator = TxGenerator(*tx_gen_params)

        greedy_cacher_params = [chain, AVAILABLE_RPCS[chain], self.DB_CLIENT]
        greedy_cacher_params.extend(AVAILABLE_CHAINS[chain]['proc']['greedy_cacher'])
        self.greedy_cacher = GreedyCacher(*greedy_cacher_params, wait_time_greedy=0)

        reorg_cron_params = [chain, AVAILABLE_RPCS[chain], self.DB_CLIENT]
        reorg_cron_params.extend(AVAILABLE_CHAINS[chain]['proc']['reorg_cron'])
        self.daemon_reorg_cron = DaemonReorgManager(*reorg_cron_params)

        if self.needs_101(chain):
            self.do_101(chain)

        self.greedy_cacher._cron_loop()

        for i in xrange(5):
            for j in xrange(5):
                self.tx_generator._cron_loop()
            self.block_generator._cron_loop()

        # Shouldn't cache anything else because greedy_cacher doesn't handle tip changes
        self.greedy_cacher._cron_loop()

        self.daemon_reorg_cron._cron_loop()

        # After calling reorg cron, it should cache more things again
        self.greedy_cacher._cron_loop()

ExampleTest().run_tests()
