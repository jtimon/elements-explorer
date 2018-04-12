
import requests
import json

RPC_ALLOWED_CALLS = [
    'getblockchaininfo',
    'getblock',
    'getblockhash',
    'getrawtransaction',
    'getblockstats',
    'getrawmempool',
    'getmempoolentry',
    'savemempool',
    # Only for testing regtests
    'generate',
    'getnewaddress',
    'sendtoaddress',
    'sendtomainchain',
]

class RpcCaller(object):

    def __init__(self, address, user, password,
                 **kwargs):

        self.address = address
        self.user = user
        self.password = password

        super(RpcCaller, self).__init__(**kwargs)

    def RpcCall(self, method, params):
        if not method in RPC_ALLOWED_CALLS:
            return {'error': {'message': 'Daemon RPC method "%s" not supported.' % method}}

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
        if not json_result:
            return {'error': {'message': 'No rpc result for method %s' % method}}
        # If there's errors, only return the errors
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}

        if ('result' in json_result):
            json_result = json_result['result']

        return json_result
