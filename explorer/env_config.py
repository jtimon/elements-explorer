
import os

from mintools.minql import MinqlFactory

from explorer.services.rpcdaemon import RpcCaller

DEFAULT_CHAIN = 'bitcoin'

CONFIG = {
    'DB_TYPE': os.environ.get('DB_TYPE'),
    'DB_ADR': os.environ.get('DB_ADR'),
    'DB_NAME': os.environ.get('DB_NAME'),
    'DB_USER': os.environ.get('DB_USER'),
    'DB_PASS': os.environ.get('DB_PASS'),
}

DB_FACTORY = MinqlFactory(CONFIG['DB_TYPE'], CONFIG['DB_ADR'], CONFIG['DB_NAME'], CONFIG['DB_USER'], CONFIG['DB_PASS'])
DB_CLIENT = DB_FACTORY.create()

INIT_DB_TIME = 120
INIT_NODES_TIME = 120
def InitTime(init_time):
    return max(INIT_DB_TIME, INIT_NODES_TIME) + init_time

AVAILABLE_CHAINS = {

    'bitcoin': {
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
            'reorg_cron': [60, InitTime(60 * 5), False, True], # every 1 min after 5 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'mempool_saver': [60 * 20, InitTime(60 * 5)], # every 20 min after 5 min
            'greedy_cacher': [60, InitTime(60 * 60 * 2), True, True], # every 1 min after 2 hours, cache txs, cache stats
        },
    },

    'testnet3': {
        'rpc': RpcCaller(os.environ.get('TESTNET3_ADR'),
                         os.environ.get('TESTNET3_RPCUSER'),
                         os.environ.get('TESTNET3_RPCPASSWORD')
        ),
        'zmq': os.environ.get('TESTNET3_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '000000000933ea01ad0ee984209779baaec3ced90fa3f408719526f8d77f4943',
        },
        'proc': {
            'reorg_cron': [60, InitTime(60 * 5), False, True], # every 1 min after 5 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'mempool_saver': [60 * 20, InitTime(60 * 5)], # every 20 min after 5 min
            'greedy_cacher': [60, InitTime(60 * 60), True, True], # every 1 min after 1 hour, cache txs, cache stats
        },
    },

    'regtest': {
        'rpc': RpcCaller(os.environ.get('REGTEST_ADR'),
                         os.environ.get('REGTEST_RPCUSER'),
                         os.environ.get('REGTEST_RPCPASSWORD')
        ),
        'zmq': os.environ.get('REGTEST_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206',
        },
        'proc': {
            'reorg_cron': [60, InitTime(60), False, True], # every 1 min after 1 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'greedy_cacher': [60, InitTime(60 * 5), True, True], # every 1 min after 5 mins, cache txs, cache stats
            'block_gen': [60, InitTime(60 * 2)], # every 2 min after 1 min
            'tx_gen': [50, InitTime(60)], # every 50 secs after 1 min
        },
    },

    'elementsregtest': {
        'rpc': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                         os.environ.get('ELEMENTSREGTEST_RPCUSER'),
                         os.environ.get('ELEMENTSREGTEST_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSREGTEST_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': 'b69af98be45cf3fb1d992b716a1d6156835c059f6944620d81dcc2487bb5cc8c',
            'parent_chain': 'regtest',
            'parent_chain_has_CT': False,
        },
        'proc': {
            'reorg_cron': [60, InitTime(60), False, True], # every 1 min after 1 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'greedy_cacher': [60, InitTime(60 * 10), True, True], # every 1 min after 10 min, cache txs, cache stats
            'block_gen': [60 * 5, InitTime(60)], # every 5 min after 1 min
            'tx_gen': [30, InitTime(60)], # every 30 secs after 1 min
            'pegin_gen': [60, InitTime(60)], # every 1 min after 1 min
            'pegout_gen': [40, InitTime(60)], # every 40 secs after 1 min
        },
    },

    'elementsparent': {
        'rpc': RpcCaller(os.environ.get('ELEMENTSPARENT_ADR'),
                         os.environ.get('ELEMENTSPARENT_RPCUSER'),
                         os.environ.get('ELEMENTSPARENT_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSPARENT_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '5d5e0aefb7734b1371ff236f5c6b5c8cfbcc4f156795d3d23849610202aac6c9',
        },
        'proc': {
            'reorg_cron': [60, InitTime(60), False, True], # every 1 min after 1 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'greedy_cacher': [60, InitTime(60 * 5), True, True], # every 1 min after 5 mins, cache txs, cache stats
            'block_gen': [60, InitTime(60 * 2)], # every 2 min after 1 min
            'tx_gen': [50, InitTime(60)], # every 50 secs after 1 min
        },
    },

    'elementside': {
        'rpc': RpcCaller(os.environ.get('ELEMENTSIDE_ADR'),
                         os.environ.get('ELEMENTSIDE_RPCUSER'),
                         os.environ.get('ELEMENTSIDE_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSIDE_ZMQ'),
        'db': DB_FACTORY,
        'properties': {
            'stats_support': True,
            'chain_id': '8d497636488f8ea97d51cf23de95d888009f672a00ba79c8758373fc47c2cdf3',
            'parent_chain': 'elementsparent',
            'parent_chain_has_CT': True,
        },
        'proc': {
            'reorg_cron': [60, InitTime(60), False, True], # every 1 min after 1 min, don't cache txs, cache stats
            'mempool_cacher': [60, InitTime(60)], # every 1 min after 1 min
            'greedy_cacher': [60, InitTime(60 * 10), True, True], # every 1 min after 10 min, cache txs, cache stats
            'block_gen': [60 * 5, InitTime(60)], # every 5 min after 1 min
            'tx_gen': [30, InitTime(60)], # every 30 secs after 1 min
            'pegin_gen': [60, InitTime(60)], # every 1 min after 1 min
            'pegout_gen': [40, InitTime(60)], # every 40 secs after 1 min
        },
    },
    
}
