import os

from lib import minql

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

DB_CLIENT = minql.MinqlClientFactory(os.environ.get('DB_TYPE'))(os.environ.get('DB_ADR'))

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "bitcoin": "bitcoin:8532",
    "testnet3": "bitcoin:18532",
    "elementsregtest": "elements:7041",
    # "elements": "elements:9042",
}

WEB_ALLOWED_CALLS = [
    'block',
    'tx',
    'blockstats',
    "getblockchaininfo",
    "getblockhash",
    "getmempoolinfo",
    "getrawmempool",
    "getmempoolentry",
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
