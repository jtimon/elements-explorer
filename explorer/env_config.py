
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
    },
}

REORG_CRON_PARAMS = {
    "bitcoin": [60, 60 * 5], # every 1 min after 5 min
    "testnet3": [60, 60 * 5], # every 1 min after 5 min
    "elementsregtest": [60, 60 * 5], # every 1 min after 5 min
}

MEMPOOL_CACHER_PARAMS = {
    "bitcoin": [60, 60], # every 1 min after 1 min
    "testnet3": [60, 60], # every 1 min after 1 min
    "elementsregtest": [60 * 20, 60], # every 20 min after 1 min
}

MEMPOOL_SAVER_PARAMS = {
    "bitcoin": [60 * 20, 60 * 5], # every 20 min after 5 min
    "testnet3": [60 * 20, 60 * 5], # every 20 min after 5 min
    "elementsregtest": [60 * 60 * 24 * 7, 60 * 5], # every 1 week after 5 min
}

GREEDY_CACHER_PARAMS = {
    "bitcoin": [60, 60 * 60 * 2, True], # every 1 min after 2 hours, cache txs
    "testnet3": [60, 60 * 60, True], # every 1 min after 1 hour, cache txs
    "elementsregtest": [60 * 60, 60, True], # every 1 hour after 1 min, cache txs
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
