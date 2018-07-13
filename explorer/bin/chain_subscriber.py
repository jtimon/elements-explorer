#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"bitcoin",
                     u"Chain to subscribe to")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from explorer.process.subscriber import DaemonSubscriber
from explorer.env_config import AVAILABLE_CHAINS, DB_FACTORY

chain = FLAGS.chain

daemon_subscriber = DaemonSubscriber(AVAILABLE_CHAINS[chain]['zmq'],
                                     chain, AVAILABLE_CHAINS[chain]['rpc'],
                                     DB_FACTORY, cache_stats=AVAILABLE_CHAINS[chain]['properties']['stats_support'])
daemon_subscriber.start()
