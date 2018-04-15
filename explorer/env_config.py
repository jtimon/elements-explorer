
import os

from mintools import minql

from explorer.rpcdaemon import RpcCaller

DEFAULT_CHAIN = 'bitcoin'

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
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
        },
        'proc': {
            'reorg_cron': [60, 60 * 5], # every 1 min after 5 min
            'mempool_cacher': [60, 60], # every 1 min after 1 min
            'mempool_saver': [60 * 20, 60 * 5], # every 20 min after 5 min
            'greedy_cacher': [60, 60 * 60, True], # every 1 min after 1 hour, cache txs
        },
    },

    "testnet3": {
        'rpc': RpcCaller(os.environ.get('TESTNET3_ADR'),
                         os.environ.get('TESTNET3_RPCUSER'),
                         os.environ.get('TESTNET3_RPCPASSWORD')
        ),
        'zmq': os.environ.get('TESTNET3_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206',
        },
        'proc': {
            'reorg_cron': [60, 60 * 5], # every 1 min after 5 min
            'mempool_cacher': [60, 60], # every 1 min after 1 min
            'mempool_saver': [60 * 20, 60 * 5], # every 20 min after 5 min
            'greedy_cacher': [60, 60 * 15, True], # every 1 min after 15 min, cache txs
        },
    },

    "elementsregtest": {
        'rpc': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                         os.environ.get('ELEMENTS_RPCUSER'),
                         os.environ.get('ELEMENTS_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSREGTEST_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': False,
            'chain_id': 'elementsregtest_genesis_hash',
        },
        'proc': {
            'reorg_cron': [60, 60], # every 1 min after 1 min
            'mempool_cacher': [60, 60], # every 1 min after 1 min
            'greedy_cacher': [60, 60 * 10, True], # every 1 min after 10 min, cache txs
            'block_gen': [60 * 5, 60], # every 5 min after 1 min
            'tx_gen': [30, 60], # every 30 secs after 1 min
        },
    },

}
