
import requests
import json

from settings import RPC_ALLOWED_CALLS, AVAILABLE_CHAINS

def RpcCall(chain, method, params):
    if not method in RPC_ALLOWED_CALLS:
        return {'error': {'message': 'Method "%s" not supported.' % method}}

    requestData = {
        'method': method,
        'params': params,
        'jsonrpc': '2.0',
        'id': chain + '_' + method,
    }
    rpcAuth = ('user1', 'password1')
    rpcHeaders = {'content-type': 'application/json'}
    response = requests.request('post', 'http://' + AVAILABLE_CHAINS[chain], data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
    # response.raise_for_status()

    json_result = response.json()
    # TODO remove special case for getrawmempool and getblockhash
    if ('result' in json_result and method != 'getrawmempool' and method != 'getblockhash'):
        json_result = json_result['result']
    return json_result
