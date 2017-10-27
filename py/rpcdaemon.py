
import requests
import json

from settings import RPC_ALLOWED_CALLS

class RpcCaller(object):

    def __init__(self, address, 
                 **kwargs):

        self.address = address

        super(FunctionResource, self).__init__(**kwargs)

    def RpcCall(method, params):
        if not method in RPC_ALLOWED_CALLS:
            return {'error': {'message': 'Method "%s" not supported.' % method}}

        requestData = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': self.address + '_' + method,
        }
        rpcAuth = ('user1', 'password1')
        rpcHeaders = {'content-type': 'application/json'}
        response = requests.request('post', 'http://' + self.address, data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
        # response.raise_for_status()

        json_result = response.json()
        # TODO remove special case for getrawmempool and getblockhash
        if ('result' in json_result and method != 'getrawmempool' and method != 'getblockhash'):
            json_result = json_result['result']
        return json_result
