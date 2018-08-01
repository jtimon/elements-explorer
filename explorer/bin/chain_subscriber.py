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

import time

from explorer import env_config
from explorer.process.subscriber import DaemonSubscriber

chain = FLAGS.chain

# Wait for db to start
time.sleep(12)

daemon_subscriber = DaemonSubscriber(env_config.node_zmq_for_chain(chain),
                                     chain, env_config.rpccaller_for_chain(chain),
                                     env_config.DB_FACTORY, cache_stats=env_config.AVAILABLE_CHAINS[chain]['properties']['stats_support'])
daemon_subscriber.start()
