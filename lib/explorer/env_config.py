
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

DB_CLIENT = minql.MinqlClientFactory(CONFIG['DB_TYPE'])(
    CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'])

AVAILABLE_CHAINS = {
    "bitcoin": {
        'rpc': RpcCaller(os.environ.get('BITCOIN_ADR'),
                         os.environ.get('BITCOIN_RPCUSER'),
                         os.environ.get('BITCOIN_RPCPASSWORD')
        ),
    },
    "testnet3": {
        'rpc': RpcCaller(os.environ.get('TESTNET3_ADR'),
                         os.environ.get('TESTNET3_RPCUSER'),
                         os.environ.get('TESTNET3_RPCPASSWORD')
        ),
    },
    "elementsregtest": {
        'rpc': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                         os.environ.get('ELEMENTS_RPCUSER'),
                         os.environ.get('ELEMENTS_RPCPASSWORD')
        ),
    },
}

SUBSCRIBER_PARAMS = {
    'bitcoin': [os.environ.get('BITCOIN_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'bitcoin', AVAILABLE_CHAINS['bitcoin']['rpc']],
    'testnet3': [os.environ.get('TESTNET3_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'testnet3', AVAILABLE_CHAINS['testnet3']['rpc']],
    'elementsregtest': [os.environ.get('ELEMENTSREGTEST_ZMQ'), CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'], 'elementsregtest', AVAILABLE_CHAINS['elementsregtest']['rpc']],
}

