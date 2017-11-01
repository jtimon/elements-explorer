import os

from lib import minql

from lib.explorer.rpcdaemon import RpcCaller

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

DB_CLIENT = minql.MinqlClientFactory(os.environ.get('DB_TYPE'))(
    os.environ.get('DB_ADR'), os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'))

WEB_ALLOWED_CALLS = [
    'block', # cached in server and gui
    'tx', # cached in server and gui
    'blockstats', # cached in server and gui
    "getblockchaininfo", # cached in gui (TODO subscribe from gui)
    "getblockhash", # never cached, always hits the node
    "getmempoolinfo", # never cached, always hits the node
    "getrawmempool", # never cached, always hits the node
    "getmempoolentry", # never cached, always hits the node
]

RPC_ALLOWED_CALLS = [
    "getblockchaininfo",
    "getblock",
    "getblockhash",
    "getrawtransaction",
    "getblockstats",
    "getmempoolinfo",
    "getrawmempool",
    "getmempoolentry",
]

AVAILABLE_CHAINS = {
    "bitcoin": RpcCaller(os.environ.get('BITCOIN_ADR'),
                         os.environ.get('BITCOIN_RPCUSER'),
                         os.environ.get('BITCOIN_RPCPASSWORD'),
                         RPC_ALLOWED_CALLS),
    "testnet3": RpcCaller(os.environ.get('TESTNET3_ADR'),
                          os.environ.get('TESTNET3_RPCUSER'),
                          os.environ.get('TESTNET3_RPCPASSWORD'),
                          RPC_ALLOWED_CALLS),
    "elementsregtest": RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                                 os.environ.get('ELEMENTS_RPCUSER'),
                                 os.environ.get('ELEMENTS_RPCPASSWORD'),
                                 RPC_ALLOWED_CALLS),
}
