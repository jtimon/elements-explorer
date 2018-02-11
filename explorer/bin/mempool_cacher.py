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

from explorer.daemon_subscriber import MempoolStatsCacher, MempoolSaver
from explorer.env_config import mempool_cacher_params, mempool_saver_params

mempool_cacher = MempoolStatsCacher(*mempool_cacher_params(FLAGS.chain))
mempool_cacher.start()

mempool_saver = MempoolSaver(*mempool_saver_params(FLAGS.chain))
mempool_saver.start()
