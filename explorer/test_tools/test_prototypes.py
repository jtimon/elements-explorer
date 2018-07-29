#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.env_config import AVAILABLE_CHAINS, DB_FACTORY

class DbTest(object):
    
    def __init__(self):
        super(DbTest, self).__init__()

        self.DB_CLIENT = DB_FACTORY.create()

class RepeatPerAvailableChainTest(DbTest):

    def run_tests(self):
        for chain, chain_properties in AVAILABLE_CHAINS.items():
            if chain == 'DEFAULT_CHAIN':
                continue
            print('Running %s for chain %s' % (__file__, chain))
            self.run_tests_for_chain(chain)
