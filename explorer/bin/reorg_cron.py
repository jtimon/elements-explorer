#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"bitcoin",
                     u"Chain to manage reorgs for")

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
from explorer.process.subscriber import DaemonReorgManager

chain = FLAGS.chain

# Wait for db to start
time.sleep(12)

reorg_cron_params = [chain, env_config.AVAILABLE_RPCS[chain], env_config.DB_FACTORY.create()]
reorg_cron_params.extend(env_config.AVAILABLE_CHAINS[chain]['proc']['reorg_cron'])
daemon_reorg_cron = DaemonReorgManager(*reorg_cron_params)
daemon_reorg_cron.start()
