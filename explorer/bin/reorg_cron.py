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

from explorer.process.subscriber import DaemonReorgManager
from explorer.env_config import AVAILABLE_CHAINS, DB_FACTORY

chain = FLAGS.chain

reorg_cron_params = [chain, AVAILABLE_CHAINS[chain]['rpc'], DB_FACTORY.create()]
reorg_cron_params.extend(AVAILABLE_CHAINS[chain]['proc']['reorg_cron'])
daemon_reorg_cron = DaemonReorgManager(*reorg_cron_params)
daemon_reorg_cron.start()
