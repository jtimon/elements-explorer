#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import time

from explorer import env_config

class BenchmarkTest(object):

    def init_chrono(self):
        self._init_time = time.time()

    def stop_chrono(self):
        self._final_time = time.time()

    def print_chrono(self, chrono_name):
        print('---------------------------------------------------')
        print('%s INIT TIME: %s' % (chrono_name, self._init_time))
        print('%s FINAL TIME: %s' % (chrono_name, self._final_time))
        print('%s DIFF TIME: %s' % (chrono_name, self._final_time - self._init_time))
        print('---------------------------------------------------')

class DbTest(BenchmarkTest):
    
    def __init__(self):
        super(DbTest, self).__init__()

        self.DB_CLIENT = env_config.DB_FACTORY.create()

class RepeatPerAvailableChainTest(DbTest):

    def needs_101(self, chain):
        return chain in ['regtest']

    def do_101(self, chain):
        block_hashes = env_config.rpccaller_for_chain(chain).RpcCall('generate', {'nblocks': 101})
    
    def run_tests(self):
        for chain, chain_properties in env_config.AVAILABLE_CHAINS.items():
            if chain == 'DEFAULT_CHAIN':
                continue
            print('Running %s for chain %s' % (self.__class__.__name__, chain))
            self.init_chrono()
            self.run_tests_for_chain(chain)
            self.stop_chrono()
            self.print_chrono('%s_%s' % (self.__class__.__name__, chain))
