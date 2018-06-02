
from mintools import restmin, ormin

from explorer import models, resources
from explorer.env_config import DB_CLIENT, AVAILABLE_CHAINS

def get_available_chains(**kwargs):
    available_chains = {}
    for k, v in AVAILABLE_CHAINS.iteritems():
        available_chains[k] = v['properties']
    return available_chains, 200

class ExplorerApiDomain(restmin.Domain):

    def __init__(self, domain, db_client, *args, **kwargs):

        ormin.Model.set_db( db_client )

        super(ExplorerApiDomain, self).__init__(domain, *args, **kwargs)

API_DOMAIN = ExplorerApiDomain({
    'available_chains': restmin.resources.FunctionResource(get_available_chains),
    # never cached, always hits the node
    'getmempoolentry': resources.rpccaller.RpcCallerResource('getmempoolentry'),
    'getrawmempool': resources.rpccaller.RpcCallerResource('getrawmempool', limit_array_result=4),
    # Data from db, independent from reorgs
    'mempoolstats': resources.mempoolstats.MempoolStatsResource(),
    # currently goes throught the whole block
    'address': resources.address.AddressResource(),
    # cached in server and gui
    'block': resources.generic.GetByIdResource('block', models.Block),
    'blockheight': resources.blockheight.BlockheightResource(),
    'tx': resources.generic.GetByIdResource('tx', models.transaction.Tx, uses_blob=True),
    'blockstats': resources.generic.GetByIdResource('blockstats', models.stats.Blockstats, ['stats_support']),
    # TODO handle reorgs from gui (ie use websockets)
    'chaininfo': resources.generic.GetByIdResource('chaininfo', models.Chaininfo),
    'faucetinfo': resources.generic.GetByIdResource('faucetinfo', models.faucet.Faucetinfo),
}, DB_CLIENT)
