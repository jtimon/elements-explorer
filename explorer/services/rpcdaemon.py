
import requests
import json
import time

RPC_ALLOWED_CALLS = [
    'getblockchaininfo',
    'getblock',
    'getblockhash',
    'getrawtransaction',
    'getblockstats',
    'getrawmempool',
    'getmempoolentry',
    'savemempool',
    'getbalance',
    'generate',
    'getnewaddress',
    'validateaddress',
    'sendtoaddress',
    'sendtomainchain',
    'getpeginaddress',
    'gettxoutproof',
    'claimpegin',
    # Exclusively for 1-of-1 multisig support in process.generator.block
    'importprivkey',
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
        response = None
        counter = 0
        while response == None:
            try:
                response = requests.request('post', 'http://' + self.address,
                                            data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
                # response.raise_for_status()
            except Exception as e:
                print("Error in RpcCaller.RpcCall:", type(e), e)
                if counter == 5:
                    return {'error': {'message': 'Rpc connection error for method %s' % method}}
                time.sleep(2)
                counter = counter + 1
                continue

        json_result = response.json()
        if not json_result:
            return {'error': {'message': 'No rpc result for method %s' % method}}
        # If there's errors, only return the errors
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}

        if ('result' in json_result):
            json_result = json_result['result']

        return json_result
