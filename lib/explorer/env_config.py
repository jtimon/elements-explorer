
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

WEB_ALLOWED_CALLS = [
    'block', # cached in server and gui
    'blockheight', # cached in server and gui
    'tx', # cached in server and gui
    'blockstats', # cached in server and gui
    # cached in gui (TODO handle reorgs from gui)
    'chaininfo', # cached in server, reorgs handled with zmq subscription to node
    "blockhash", # cached in server, reorgs handled with zmq subscription to node
    'mempoolstats', # Data from db, independent from reorgs
    "getmempoolentry", # never cached, always hits the node
    "getrawmempool", # never cached, always hits the node (limited to 5 results)
]

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
    },
    "testnet3": {
        'rpc': RpcCaller(os.environ.get('TESTNET3_ADR'),
                         os.environ.get('TESTNET3_RPCUSER'),
                         os.environ.get('TESTNET3_RPCPASSWORD')
        ),
        'zmq': os.environ.get('TESTNET3_ZMQ'),
        'db': DB_FACTORY,
    },
    "elementsregtest": {
        'rpc': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                         os.environ.get('ELEMENTS_RPCUSER'),
                         os.environ.get('ELEMENTS_RPCPASSWORD')
        ),
        'zmq': os.environ.get('ELEMENTSREGTEST_ZMQ'),
        'db': DB_FACTORY,
    },
}

def subscriber_params(chain):
    return [AVAILABLE_CHAINS[chain]['zmq'], chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db']]

def reorg_cron_params(chain):
    return [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create(), 60, 300] # 5 min

def mempool_cacher_params(chain):
    return [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create(), 60, 60] # 1 min

def mempool_saver_params(chain):
    # 2 hours before starting, change after https://github.com/bitcoin/bitcoin/issues/12142 is fixed
    return [chain, AVAILABLE_CHAINS[chain]['rpc'], 60, 7200] # 2 hours

def greedy_cacher_params(chain):
    return [chain, AVAILABLE_CHAINS[chain]['rpc'], AVAILABLE_CHAINS[chain]['db'].create(), 60, 3600] # 1 hour
