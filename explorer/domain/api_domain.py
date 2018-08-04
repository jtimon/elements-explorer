
import time

from mintools.ormin import Model as ormin_model
from mintools.restmin import Domain as restmin_domain
from mintools.restmin.resources import FunctionResource

from explorer import env_config

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.stats import Blockstats
from explorer.models.transaction import Tx

from explorer.resources.address import AddressResource
from explorer.resources.blockheight import BlockheightResource
from explorer.resources.faucet import FaucetInfoResource
from explorer.resources.faucet import FreeCoinsResource
from explorer.resources.generic import GetByIdResource
from explorer.resources.mempoolstats import MempoolStatsResource
from explorer.resources.rpccaller import RpcCallerResource

def get_default_chain(**kwargs):
    return env_config.DEFAULT_CHAIN

def get_available_chains(**kwargs):
    available_chains = {}
    for k, v in env_config.AVAILABLE_CHAINS.iteritems():
        available_chains[k] = v['properties']
    return available_chains, 200

class ExplorerApiDomain(restmin_domain):

    def __init__(self, domain, db_factory, *args, **kwargs):

        # Wait for db to start
        time.sleep(12)
        ormin_model.set_db( db_factory.create() )

        super(ExplorerApiDomain, self).__init__(domain, *args, **kwargs)

API_DOMAIN = ExplorerApiDomain(
{
    # never cached, always hits the node if the request not rejected before
    'getmempoolentry': RpcCallerResource('getmempoolentry'),
    'getrawmempool': RpcCallerResource('getrawmempool', limit_array_result=4),
    'faucetinfo': FaucetInfoResource(),
    'freecoins': FreeCoinsResource(),

    # cached in server and gui
    'block': GetByIdResource('block', Block),
    'blockheight': BlockheightResource(),
    'tx': GetByIdResource('tx', Tx),
    'blockstats': GetByIdResource('blockstats', Blockstats, ['stats_support']),
    # TODO currently goes throught the whole block
    'address': AddressResource(),
    # TODO handle reorgs from gui (ie use websockets)
    'chaininfo': GetByIdResource('chaininfo', Chaininfo),

    # Data const or from db, independent from reorgs or caching
    'default_chain': FunctionResource(get_default_chain),
    'available_chains': FunctionResource(get_available_chains),
    'mempoolstats': MempoolStatsResource(),

}, env_config.DB_FACTORY)
