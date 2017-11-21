
import os

from lib import minql

from lib.explorer.rpcdaemon import RpcCaller

CONFIG = {
    'DB_TYPE': os.environ.get('DB_TYPE'),
    'DB_ADR': os.environ.get('DB_ADR'),
    'DB_NAME': os.environ.get('DB_NAME'),
    'DB_USER': os.environ.get('DB_USER'),
    'DB_PASS': os.environ.get('DB_PASS'),
}

DB_FACTORY = minql.MinqlFactory(CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'])
DB_CLIENT = DB_FACTORY.create()

AVAILABLE_CHAINS = {
    "bitcoin": {
        'rpc': RpcCaller(os.environ.get('BITCOIN_ADR'),
                         os.environ.get('BITCOIN_RPCUSER'),
                         os.environ.get('BITCOIN_RPCPASSWORD')
        ),
        'zmq': os.environ.get('BITCOIN_ZMQ'),
    },
    "testnet3": {
        'rpc': RpcCaller(os.environ.get('TESTNET3_ADR'),
                         os.environ.get('TESTNET3_RPCUSER'),
                         os.environ.get('TESTNET3_RPCPASSWORD')
        ),
        'zmq': os.environ.get('TESTNET3_ZMQ'),
    },
    "elementsregtest": {
        'rpc': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                         os.environ.get('ELEMENTS_RPCUSER'),
                         os.environ.get('ELEMENTS_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSREGTEST_ZMQ'),
    },
}

SUBSCRIBER_PARAMS = {
    'bitcoin': [AVAILABLE_CHAINS['bitcoin']['zmq'], 'bitcoin', AVAILABLE_CHAINS['bitcoin']['rpc'], DB_FACTORY],
    'testnet3': [AVAILABLE_CHAINS['testnet3']['zmq'], 'testnet3', AVAILABLE_CHAINS['testnet3']['rpc'], DB_FACTORY],
    'elementsregtest': [AVAILABLE_CHAINS['elementsregtest']['zmq'], 'elementsregtest', AVAILABLE_CHAINS['elementsregtest']['rpc'], DB_FACTORY],
}
