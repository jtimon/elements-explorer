#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"bitcoin",
                     u"Chain to subscribe to for caching mempool stats")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

import time

from explorer.process.mempoolsaver import MempoolSaver
from explorer.process.mempoolstats import MempoolStatsCacher

from explorer import env_config

chain = FLAGS.chain

# Wait for db to start
time.sleep(12)

mempool_cacher_params = [chain, env_config.AVAILABLE_RPCS[chain], env_config.DB_FACTORY.create()]
mempool_cacher_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['mempool_cacher'])
mempool_cacher = MempoolStatsCacher(*mempool_cacher_params)
mempool_cacher.start()

if 'mempool_saver' in env_config.AVAILABLE_CHAINS[chain]:
    mempool_saver_params = [chain, env_config.AVAILABLE_RPCS[chain]]
    mempool_saver_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['mempool_saver'])
    mempool_saver = MempoolSaver(*mempool_saver_params)
    mempool_saver.start()
