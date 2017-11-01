#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import os

from lib.explorer.daemon_subscriber import DaemonSubscriber
from lib.explorer.rpcdaemon import RpcCaller

# TODO unify with settings
AVAILABLE_CHAINS = {
    "bitcoin": RpcCaller(os.environ.get('BITCOIN_ADR'),
                         os.environ.get('BITCOIN_RPCUSER'),
                         os.environ.get('BITCOIN_RPCPASSWORD')
    ),
    "testnet3": RpcCaller(os.environ.get('TESTNET3_ADR'),
                          os.environ.get('TESTNET3_RPCUSER'),
                          os.environ.get('TESTNET3_RPCPASSWORD')
    ),
    "elementsregtest": RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                                 os.environ.get('ELEMENTS_RPCUSER'),
                                 os.environ.get('ELEMENTS_RPCPASSWORD')
    ),
}

daemon_subscriber = DaemonSubscriber(os.environ.get('BITCOIN_ZMQ'), os.environ.get('DB_TYPE'), os.environ.get('DB_ADR'), os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'), 'bitcoin', AVAILABLE_CHAINS['bitcoin'])
daemon_subscriber.start()
daemon_subscriber2 = DaemonSubscriber(os.environ.get('TESTNET3_ZMQ'), os.environ.get('DB_TYPE'), os.environ.get('DB_ADR'), os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'), 'testnet3', AVAILABLE_CHAINS['testnet3'])
daemon_subscriber2.start()
daemon_subscriber3 = DaemonSubscriber(os.environ.get('ELEMENTSREGTEST_ZMQ'), os.environ.get('DB_TYPE'), os.environ.get('DB_ADR'), os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'), 'elementsregtest', AVAILABLE_CHAINS['elementsregtest'])
daemon_subscriber3.start()
