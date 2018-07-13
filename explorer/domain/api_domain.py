
from mintools.ormin import Model as ormin_model
from mintools.restmin import Domain as restmin_domain
from mintools.restmin.resources import FunctionResource

from explorer.env_config import DB_FACTORY, AVAILABLE_CHAINS

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

def get_available_chains(**kwargs):
    available_chains = {}
    for k, v in AVAILABLE_CHAINS.iteritems():
        if k == 'DEFAULT_CHAIN':
            continue
        available_chains[k] = v['properties']
    return available_chains, 200

class ExplorerApiDomain(restmin_domain):

    def __init__(self, domain, db_client, *args, **kwargs):

        ormin_model.set_db( db_client )

        super(ExplorerApiDomain, self).__init__(domain, *args, **kwargs)

API_DOMAIN = ExplorerApiDomain({
    'available_chains': FunctionResource(get_available_chains),
    # never cached, always hits the node
    'getmempoolentry': RpcCallerResource('getmempoolentry'),
    'getrawmempool': RpcCallerResource('getrawmempool', limit_array_result=4),
    'faucetinfo': FaucetInfoResource(),
    'freecoins': FreeCoinsResource(),
    # Data from db, independent from reorgs
    'mempoolstats': MempoolStatsResource(),
    # currently goes throught the whole block
    'address': AddressResource(),
    # cached in server and gui
    'block': GetByIdResource('block', Block),
    'blockheight': BlockheightResource(),
    'tx': GetByIdResource('tx', Tx),
    'blockstats': GetByIdResource('blockstats', Blockstats, ['stats_support']),
    # TODO handle reorgs from gui (ie use websockets)
    'chaininfo': GetByIdResource('chaininfo', Chaininfo),
}, DB_FACTORY.create())
