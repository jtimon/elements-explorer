
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

def rpccaller_for_chain(chain):
    CHAIN_UPPER = chain.upper()
    return RpcCaller(os.environ.get('%s_ADR' % CHAIN_UPPER),
                     os.environ.get('%s_RPCUSER' % CHAIN_UPPER),
                     os.environ.get('%s_RPCPASSWORD' % CHAIN_UPPER)
    )
    
AVAILABLE_RPCS = {}
for chain in AVAILABLE_CHAINS:
    if chain == 'DEFAULT_CHAIN':
        continue
    AVAILABLE_RPCS[chain] = rpccaller_for_chain(chain)
