
import requests
import json

class RpcCaller(object):

    def __init__(self, address, user, password, RPC_ALLOWED_CALLS,
                 **kwargs):

        self.address = address
        self.RPC_ALLOWED_CALLS = RPC_ALLOWED_CALLS
        self.user = user
        self.password = password

        super(RpcCaller, self).__init__(**kwargs)

    def RpcCall(self, method, params):
        if not method in self.RPC_ALLOWED_CALLS:
            return {'error': {'message': 'Method "%s" not supported.' % method}}

        requestData = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': self.address + '_' + method,
        }
        rpcAuth = (self.user, self.password)
        rpcHeaders = {'content-type': 'application/json'}
        response = requests.request('post', 'http://' + self.address, data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
        # response.raise_for_status()

        json_result = response.json()
        # TODO remove special case for getrawmempool and getblockhash
        if ('result' in json_result and method != 'getrawmempool' and method != 'getblockhash'):
            json_result = json_result['result']
        return json_result
