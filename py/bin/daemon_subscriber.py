#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

from lib.explorer.daemon_subscriber import DaemonSubscriber
from lib.explorer.env_config import SUBSCRIBER_PARAMS

daemon_subscriber = DaemonSubscriber(*SUBSCRIBER_PARAMS['bitcoin'])
daemon_subscriber.start()
daemon_subscriber2 = DaemonSubscriber(*SUBSCRIBER_PARAMS['testnet3'])
daemon_subscriber2.start()
daemon_subscriber3 = DaemonSubscriber(*SUBSCRIBER_PARAMS['elementsregtest'])
daemon_subscriber3.start()
