# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from .chain import UnknownChainError, ChainResource

class RpcCallerResource(ChainResource):
    def __init__(self, resource, limit_array_result=0):
        self.resource = resource
        self.limit_array_result = limit_array_result

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        json_result = self.rpccaller.RpcCall(self.resource, req['json'])
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}, 400

        if self.limit_array_result:
            return {'result': json_result[:self.limit_array_result]}, 200
        else:
            return {'result': json_result}, 200
