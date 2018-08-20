#!/usr/bin/env python

# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"bitcoin",
                     u"Chain to greedy cache for")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

import time

from explorer import env_config
from explorer.process.greedy import GreedyCacher

chain = FLAGS.chain

# Wait for db to start
time.sleep(12)

greedy_cacher_params = [chain, env_config.rpccaller_for_chain(chain), env_config.DB_FACTORY.create()]
greedy_cacher_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['greedy_cacher'])
greedy_cacher = GreedyCacher(*greedy_cacher_params)
greedy_cacher.start()
