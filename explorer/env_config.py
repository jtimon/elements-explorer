# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import os

from mintools.minql import MinqlFactory

from explorer.services.rpcdaemon import RpcCaller

print('Importing env_config.py')

AVAILABLE_API = json.loads(open('/build_docker/docker/conf/API_AVAILABLE.json', 'r').read())['api_available']
AVAILABLE_CHAINS = json.loads(open('/build_docker/docker/conf/AVAILABLE_CHAINS.json', 'r').read())
DEFAULT_CHAIN = os.environ.get('DEFAULT_CHAIN')

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
    return os.environ.get('%s_ZMQ' % chain.upper())
