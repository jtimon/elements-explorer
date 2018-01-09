
import json
import datetime

from lib import minql

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'tx',
    'blockstats',
    'chaininfo',
    'blockhash',
]

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        return rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        return rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        return rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
    elif resource == 'chaininfo':
        return rpccaller.RpcCall('getblockchaininfo', {})
    elif resource == 'blockhash':
        return rpccaller.RpcCall('getblockhash', {'height': req_id})
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
    elif resource == 'blockhash':
        CacheBlockhashResult(db_client, chain, resource, json_result, req_id)
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

def GetById(db_client, rpccaller, chain, resource, req_id):
    if resource == 'blockhash':
        criteria = {'height': req_id}
        count_by_height = db_client.search(chain + "_" + 'block', criteria)
        if len(count_by_height) > 1:
            return {'error': {'message': 'More than one block cached for height %s' % req_id}}
        if len(count_by_height) == 1:
            return {'result': count_by_height[0]['id']}

        json_result = RpcFromId(rpccaller, resource, req_id)
        if 'error' in json_result:
            return json_result
        json_result = GetByIdBase(db_client, rpccaller, chain, 'block', json_result['result'])
        if 'error' in json_result:
            return json_result
        return {'result': json_result['hash']}

    return GetByIdBase(db_client, rpccaller, chain, resource, req_id)

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
        elif self.resource == 'mempoolstats':
            try:
                if not 'hours_ago' in request:
                    return {'error': {'message': 'No hours_ago specified to get %s in request %s' % (self.resource, request)}}
                seconds_ago = request['hours_ago'] * 60 * 60
                min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
                db_result = self.db_client.search(self.chain + "_" + self.resource, {'time': {'ge': min_epoch}})
                if not db_result:
                    return {'error': {'message': 'No result db for %s.' % self.resource}}
                json_result = {}
                for db_elem in db_result:
                    json_result[db_elem['id']] = json.loads(db_elem['blob'])
                return json_result
            except:
                return {'error': {'message': 'Error getting %s from db.' % (self.resource)}}
        else:
            json_result = self.rpccaller.RpcCall(self.resource, request)
            if self.resource == 'getrawmempool':
                json_result['result'] = json_result['result'][:8]

        # If there's errors, only return the errors
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}
        return json_result
