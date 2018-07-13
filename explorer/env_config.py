
import json
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

AVAILABLE_RPCS = {

    'bitcoin': RpcCaller(os.environ.get('BITCOIN_ADR'),
                         os.environ.get('BITCOIN_RPCUSER'),
                         os.environ.get('BITCOIN_RPCPASSWORD')
    ),

    'testnet3': RpcCaller(os.environ.get('TESTNET3_ADR'),
                          os.environ.get('TESTNET3_RPCUSER'),
                          os.environ.get('TESTNET3_RPCPASSWORD')
    ),

    'regtest': RpcCaller(os.environ.get('REGTEST_ADR'),
                         os.environ.get('REGTEST_RPCUSER'),
                         os.environ.get('REGTEST_RPCPASSWORD')
    ),

    'elementsregtest': RpcCaller(os.environ.get('ELEMENTSREGTEST_ADR'),
                                 os.environ.get('ELEMENTSREGTEST_RPCUSER'),
                                 os.environ.get('ELEMENTSREGTEST_RPCPASSWORD')
    ),

    'elementsparent': RpcCaller(os.environ.get('ELEMENTSPARENT_ADR'),
                                os.environ.get('ELEMENTSPARENT_RPCUSER'),
                                os.environ.get('ELEMENTSPARENT_RPCPASSWORD')
    ),

    'elementside': RpcCaller(os.environ.get('ELEMENTSIDE_ADR'),
                             os.environ.get('ELEMENTSIDE_RPCUSER'),
                             os.environ.get('ELEMENTSIDE_RPCPASSWORD')
    ),
}

file = open('/root/conf/AVAILABLE_CHAINS.json', 'r').read()
AVAILABLE_CHAINS = json.loads(file)
