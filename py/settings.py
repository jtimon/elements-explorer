import os

from lib import minql

from rpcdaemon import RpcCaller

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

DB_CLIENT = minql.MinqlClientFactory(os.environ.get('DB_TYPE'))(os.environ.get('DB_ADR'))

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

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'tx',
    'blockstats',
]

AVAILABLE_CHAINS = {
    "bitcoin": RpcCaller("bitcoin:8532", 'user1', 'password1', RPC_ALLOWED_CALLS),
    "testnet3": RpcCaller("bitcoin:18532", 'user1', 'password1', RPC_ALLOWED_CALLS),
    "elementsregtest": RpcCaller("elements:7041", 'user1', 'password1', RPC_ALLOWED_CALLS),
}
