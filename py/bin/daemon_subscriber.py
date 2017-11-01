#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import os

from lib.explorer.daemon_subscriber import DaemonSubscriber
from lib.explorer.rpcdaemon import RpcCaller
from lib.explorer.env_config import CONFIG, AVAILABLE_CHAINS

daemon_subscriber = DaemonSubscriber(os.environ.get('BITCOIN_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'bitcoin', AVAILABLE_CHAINS['bitcoin'])
daemon_subscriber.start()
daemon_subscriber2 = DaemonSubscriber(os.environ.get('TESTNET3_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'testnet3', AVAILABLE_CHAINS['testnet3'])
daemon_subscriber2.start()
daemon_subscriber3 = DaemonSubscriber(os.environ.get('ELEMENTSREGTEST_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'elementsregtest', AVAILABLE_CHAINS['elementsregtest'])
daemon_subscriber3.start()
