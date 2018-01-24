
import json
import datetime

from lib import minql
from lib import restmin
from lib.explorer.env_config import DB_CLIENT, AVAILABLE_CHAINS, DEFAULT_CHAIN, WEB_ALLOWED_CALLS

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'blockheight',
    'tx',
    'blockstats',
    'chaininfo',
]

class RpcCacher(object):

    def __init__(self, rpccaller, db_client):
        super(RpcCacher, self).__init__()

        self.rpccaller = rpccaller
        self.db_client = db_client

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        return rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        return rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        return rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
    elif resource == 'chaininfo':
        return rpccaller.RpcCall('getblockchaininfo', {})
    else:
        raise NotImplementedError

def CacheChainInfoResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['bestblockhash'] = json_result['bestblockhash']
    db_cache['blocks'] = json_result['blocks']
    db_cache['mediantime'] = json_result['mediantime']
    db_client.put(chain + "_" + resource, db_cache)

def CacheTxResult(db_client, chain, resource, json_result, req_id):
    if 'blockhash' in json_result and json_result['blockhash']:
        # Don't cache mempool txs
        db_cache = {}
        db_cache['id'] = req_id
        db_cache['blockhash'] = json_result['blockhash']
        db_cache['blob'] = json.dumps(json_result)
        db_client.put(chain + "_" + resource, db_cache)

def CacheBlockResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['height'] = json_result['height']
    db_cache['blob'] = json.dumps(json_result)
    db_client.put(chain + "_" + resource, db_cache)

def CacheResultAsBlob(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['blob'] = json.dumps(json_result)
    db_client.put(chain + "_" + resource, db_cache)

def TryRpcAndCacheFromId(db_client, rpccaller, chain, resource, req_id):
    json_result = RpcFromId(rpccaller, resource, req_id)
    if 'error' in json_result:
        return json_result

    if resource == 'chaininfo':
        CacheChainInfoResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'block':
        CacheBlockResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'blockstats':
        CacheBlockResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'tx':
        CacheTxResult(db_client, chain, resource, json_result, req_id)
    else:
        CacheResultAsBlob(db_client, chain, resource, json_result, req_id)

    return json_result

def GetByIdBase(db_client, rpccaller, chain, resource, req_id):
    try:
        db_result = db_client.get(chain + "_" + resource, req_id)
        if not db_result:
            return {'error': {'message': 'No result db for %s.' % resource}}
        if resource == 'chaininfo':
            return db_result
        if not 'blob' in db_result:
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = json.loads(db_result['blob'])
    except minql.NotFoundError:
        json_result = TryRpcAndCacheFromId(db_client, rpccaller, chain, resource, req_id)
    except:
        return {'error': {'message': 'Error getting %s from db by id %s.' % (resource, req_id)}}

    return json_result

def GetBlockByHeight(db_client, rpccaller, chain, height):
    criteria = {'height': height}
    count_by_height = db_client.search(chain + "_" + 'block', criteria)
    if len(count_by_height) > 1:
        return {'error': {'message': 'More than one block cached for height %s' % height}}
    if len(count_by_height) == 1:
        return json.loads(count_by_height[0]['blob'])

    json_result = rpccaller.RpcCall('getblockhash', {'height': height})
    if 'error' in json_result:
        return json_result
    return GetByIdBase(db_client, rpccaller, chain, 'block', json_result)

def GetById(db_client, rpccaller, chain, resource, req_id):
    if resource == 'blockheight':
        return GetBlockByHeight(db_client, rpccaller, chain, req_id)

    return GetByIdBase(db_client, rpccaller, chain, resource, req_id)

class UnknownChainError(BaseException):
    pass

class ChainResource(restmin.resources.Resource):

    def update_chain(self, request_data):
        if 'chain' in request_data:
            self.chain = request_data['chain']
            del request_data['chain']
        else:
            self.chain = DEFAULT_CHAIN
        if not self.chain in AVAILABLE_CHAINS:
            raise UnknownChainError

        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']

        return request_data


class RpcCallerResource(ChainResource):
    def __init__(self, resource, limit_array_result=0):
        self.resource = resource
        self.limit_array_result = limit_array_result

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % chain}}, 400

        json_result = self.rpccaller.RpcCall(self.resource, req['json'])
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}, 400

        if self.limit_array_result:
            return {'result': json_result[:self.limit_array_result]}, 200
        else:
            return {'result': json_result}, 200


class BetterNameResource(RpcCacher):

    def __init__(self, db_client, rpccaller, chain, resource):

        self.chain = chain
        self.resource = resource

        super(BetterNameResource, self).__init__(rpccaller, db_client)

    def resolve_mempoolstats(self, request):
        if not 'hours_ago' in request:
            return {'error': {'message': 'No hours_ago specified to get %s in request %s' % (self.resource, request)}}

        json_result = {}
        try:
            seconds_ago = request['hours_ago'] * 60 * 60
            min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
            db_result = self.db_client.search(self.chain + "_" + self.resource, {'time': {'ge': min_epoch}})
            if not db_result:
                return {'error': {'message': 'No result db for %s.' % self.resource}}
            for db_elem in db_result:
                json_result[db_elem['id']] = json.loads(db_elem['blob'])
        except:
            return {'error': {'message': 'Error getting %s from db.' % (self.resource)}}

        return json_result

    def resolve_request(self, request):
        print('request', request)

        if self.resource == 'blockstats' and not AVAILABLE_CHAINS[self.chain]['properties']['stats_support']:
                return {'error': {'message': 'API resource %s is not supported by chain %s' % ('blockstats', self.chain)}}

        if self.resource in RESOURCES_FOR_GET_BY_ID:
            if not 'id' in request:
                return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}

            json_result = GetById(self.db_client, self.rpccaller, self.chain, self.resource, request['id'])
        elif self.resource == 'mempoolstats':
            json_result = self.resolve_mempoolstats(request)
        else:
            return {'error': {'message': 'Resource "%s" not supported.' % resource}}

        return json_result

def get_available_chains(**kwargs):
    available_chains = {}
    for k, v in AVAILABLE_CHAINS.iteritems():
        available_chains[k] = v['properties']
    return available_chains, 200

RESOURCES = {
    'available_chains': restmin.resources.FunctionResource(get_available_chains),
    # never cached, always hits the node
    'getmempoolentry': RpcCallerResource('getmempoolentry'),
    'getrawmempool': RpcCallerResource('getrawmempool', limit_array_result=4),
}

def explorer_request_processor(app, req):
    request_data = req['json']
    resource = req['resource']

    if resource in RESOURCES:
        return restmin.domain.Domain(RESOURCES).resolve_request(req)

    if not resource in WEB_ALLOWED_CALLS:
        return {'status': 404, 'error': {'message': 'Resource "%s" not supported.' % resource}}

    chain = DEFAULT_CHAIN
    if 'chain' in request_data:
        chain = request_data['chain']
        if not chain in AVAILABLE_CHAINS:
            return {'status': 400, 'error': {'message': 'Chain "%s" not supported.' % chain}}
        del request_data['chain']

    json_result = BetterNameResource(DB_CLIENT, AVAILABLE_CHAINS[chain]['rpc'], chain, resource).resolve_request(request_data)

    if not json_result:
        return {'status': 400, 'error': {'message': 'No result for %s.' % resource}}
    # If there's errors, only return the errors
    if 'error' in json_result and json_result['error']:
        return {'status': 400, 'error': json_result['error']}

    result = {}
    if 'status' in json_result:
        result['status'] = json_result['status']
        del json_result['status']
    else:
        result['status'] = 200
    result['json'] = json_result
    return result
