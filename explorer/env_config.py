
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
        },
    },
}

REORG_CRON_PARAMS = {
    "bitcoin": [60, 300], # every 1 min after 5 min
    "testnet3": [60, 60 * 60], # every 1 min after 1 hour
    "elementsregtest": [60, 60 * 5], # every 1 min after 5 min
}

MEMPOOL_CACHER_PARAMS = {
    "bitcoin": [60, 60], # every 1 min after 1 min
    "testnet3": [60, 60], # every 1 min after 1 min
    "elementsregtest": [60 * 20, 60], # every 20 min after 1 min
}

# 2 hours before starting, change after https://github.com/bitcoin/bitcoin/issues/12142 is fixed
SECONDS_FIX_12142 = 60 * 60 * 2 # 2 hours
MEMPOOL_SAVER_PARAMS = {
    "bitcoin": [60, SECONDS_FIX_12142], # every 1 min after SECONDS_FIX_12142 seconds
    "testnet3": [60, SECONDS_FIX_12142], # every 1 min after SECONDS_FIX_12142 seconds
    "elementsregtest": [60 * 60 * 24 * 7, SECONDS_FIX_12142], # every 1 week after SECONDS_FIX_12142 seconds
}

GREEDY_CACHER_PARAMS = {
    "bitcoin": [60, 60 * 60 * 24, True], # every 1 min after 1 day, cache txs
    "testnet3": [60, 60 * 60, True], # every 1 min after 1 hour, cache txs
    "elementsregtest": [60 * 60, 60 * 60, True], # every 1 hour after 1 hour, cache txs
}

def subscriber_params(chain):
    return [AVAILABLE_CHAINS[chain]['zmq'], chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db']]

def reorg_cron_params(chain):
    to_return = [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create()]
    to_return.extend(REORG_CRON_PARAMS[chain])
    return to_return

def mempool_cacher_params(chain):
    to_return = [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create()]
    to_return.extend(MEMPOOL_CACHER_PARAMS[chain])
    return to_return

def mempool_saver_params(chain):
    to_return = [chain, AVAILABLE_CHAINS[chain]['rpc']]
    to_return.extend(MEMPOOL_SAVER_PARAMS[chain])
    return to_return

def greedy_cacher_params(chain):
    to_return = [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create()]
    to_return.extend(GREEDY_CACHER_PARAMS[chain])
    return to_return
