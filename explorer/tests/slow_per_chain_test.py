#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

print('Running %s for' % (__file__))

# ===----------------------------------------------------------------------===

from explorer.env_config import AVAILABLE_CHAINS, AVAILABLE_RPCS, DB_FACTORY
from explorer.process.generator.block import BlockGenerator
from explorer.process.generator.pegin import PeginGenerator
from explorer.process.generator.pegout import PegoutGenerator
from explorer.process.generator.transaction import TxGenerator
from explorer.process.greedy import GreedyCacher
from explorer.process.subscriber import DaemonReorgManager

class ExampleTest(object):

    def __init__(self):
        super(ExampleTest, self).__init__()

    def run_test(self, chain):

        DB_CLIENT = DB_FACTORY.create()

        block_gen_params = [chain, AVAILABLE_RPCS[chain]]
        block_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['block_gen'])
        self.block_generator = BlockGenerator(*block_gen_params)

        tx_gen_params = [chain, AVAILABLE_RPCS[chain]]
        tx_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['tx_gen'])
        self.tx_generator = TxGenerator(*tx_gen_params)

        greedy_cacher_params = [chain, AVAILABLE_RPCS[chain], DB_CLIENT]
        greedy_cacher_params.extend(AVAILABLE_CHAINS[chain]['proc']['greedy_cacher'])
        self.greedy_cacher = GreedyCacher(*greedy_cacher_params, wait_time_greedy=0)

        reorg_cron_params = [chain, AVAILABLE_RPCS[chain], DB_CLIENT]
        reorg_cron_params.extend(AVAILABLE_CHAINS[chain]['proc']['reorg_cron'])
        self.daemon_reorg_cron = DaemonReorgManager(*reorg_cron_params)

        for i in xrange(101):
            self.block_generator._cron_loop()

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

def run_test_across_chains(_ExampleTest, AVAILABLE_CHAINS_ITEMS):
    print('Testing %s chains' % (len(AVAILABLE_CHAINS_ITEMS)))
    for chain, chain_properties in AVAILABLE_CHAINS_ITEMS:
        if chain == 'DEFAULT_CHAIN':
            continue
        _ExampleTest().run_test(chain)

run_test_across_chains(ExampleTest, AVAILABLE_CHAINS.items())
