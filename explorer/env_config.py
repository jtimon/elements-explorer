
import json
import os

from mintools.minql import MinqlFactory

from explorer.services.rpcdaemon import RpcCaller

file = open('/root/conf/AVAILABLE_CHAINS.json', 'r').read()
AVAILABLE_CHAINS = json.loads(file)

DB_FACTORY = MinqlFactory(
    os.environ.get('DB_TYPE'),
    os.environ.get('DB_ADR'),
    os.environ.get('DB_NAME'),
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASS')
)

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
