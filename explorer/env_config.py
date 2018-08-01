
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

def node_zmq_for_chain(chain):
    # TODO Move AVAILABLE_CHAINS[chain]['zmq'] to os.environ.get('%s_ZMQ' % CHAIN_UPPER)
    return AVAILABLE_CHAINS[chain]['zmq']
