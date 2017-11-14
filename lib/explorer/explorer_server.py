
import json

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'tx',
    'blockstats',
    'chaininfo',
    'blockhash',
]

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        rpc_result = rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        rpc_result = rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        rpc_result = rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
    elif resource == 'chaininfo':
        rpc_result = rpccaller.RpcCall('getblockchaininfo', {})
    elif resource == 'blockhash':
        rpc_result = rpccaller.RpcCall('getblockhash', {'height': req_id})
    else:
        raise NotImplementedError

    return rpc_result

def CacheChainInfoResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['bestblockhash'] = json_result['bestblockhash']
    db_cache['blocks'] = json_result['blocks']
    db_cache['mediantime'] = json_result['mediantime']
    db_client.put(chain + "_" + resource, db_cache)

def CacheBlockhashResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = json_result['result']
    db_cache['height'] = req_id
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

def GetById(db_client, rpccaller, chain, resource, req_id):
    try:
        db_result = db_client.get(chain + "_" + resource, req_id)
        if not db_result:
            return {'error': {'message': 'No result db for %s.' % resource}}
        if resource == 'chaininfo':
            return db_result
        if not 'blob' in db_result:
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = json.loads(db_result['blob'])
    except:
        json_result = RpcFromId(rpccaller, resource, req_id)
        if not json_result:
            return {'error': {'message': 'No rpc result for %s.' % resource}}
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}
        if resource == 'chaininfo':
            CacheChainInfoResult(db_client, chain, resource, json_result, req_id)
        elif resource == 'blockhash':
            CacheBlockhashResult(db_client, chain, resource, json_result, req_id)
        elif resource == 'block':
            CacheBlockResult(db_client, chain, resource, json_result, req_id)
        elif resource == 'blockstats':
            CacheBlockResult(db_client, chain, resource, json_result, req_id)
        else:
            CacheResultAsBlob(db_client, chain, resource, json_result, req_id)

    return json_result

class BetterNameResource(object):

    def __init__(self,
                 db_client,
                 rpccaller,
                 chain,
                 resource,
                 **kwargs):

        self.db_client = db_client
        self.rpccaller = rpccaller
        self.chain = chain
        self.resource = resource

        super(BetterNameResource, self).__init__(**kwargs)

    def resolve_request(self, request):
        print('request', request)
        if self.resource in RESOURCES_FOR_GET_BY_ID:
            if not 'id' in request:
                return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}

            json_result = GetById(self.db_client, self.rpccaller, self.chain, self.resource, request['id'])
        else:
            json_result = self.rpccaller.RpcCall(self.resource, request)

        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}
        return json_result
