
import json

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        rpc_result = rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        rpc_result = rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        rpc_result = rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})

    return rpc_result

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
        if not 'blob' in db_result:
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = json.loads(db_result['blob'])
    except:
        json_result = RpcFromId(rpccaller, resource, req_id)
        if not json_result:
            return {'error': {'message': 'No rpc result for %s.' % resource}}
        CacheResultAsBlob(db_client, chain, resource, json_result, req_id)

    return json_result
