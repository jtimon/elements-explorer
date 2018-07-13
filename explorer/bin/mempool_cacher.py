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

from explorer.process.mempoolsaver import MempoolSaver
from explorer.process.mempoolstats import MempoolStatsCacher

from explorer.env_config import AVAILABLE_CHAINS, DB_FACTORY, AVAILABLE_RPCS

chain = FLAGS.chain

mempool_cacher_params = [chain, AVAILABLE_RPCS[chain], DB_FACTORY.create()]
mempool_cacher_params.extend(AVAILABLE_CHAINS[chain]['proc']['mempool_cacher'])
mempool_cacher = MempoolStatsCacher(*mempool_cacher_params)
mempool_cacher.start()

if 'mempool_saver' in AVAILABLE_CHAINS[chain]:
    mempool_saver_params = [chain, AVAILABLE_RPCS[chain]]
    mempool_saver_params.extend(AVAILABLE_CHAINS[chain]['proc']['mempool_saver'])
    mempool_saver = MempoolSaver(*mempool_saver_params)
    mempool_saver.start()
