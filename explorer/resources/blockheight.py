# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.services.blockheight import GetBlockByHeight

from .chain import UnknownChainError, ChainResource

class BlockheightResource(ChainResource):

    def __init__(self, *args, **kwargs):
        super(BlockheightResource, self).__init__(*args, **kwargs)

        self.resource = 'blockheight'

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'id' in request:
            return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}, 400

        response = GetBlockByHeight(self.rpccaller, request['id'])
        if isinstance(response, dict) and 'error' in response:
            return {'error': response['error']}, 400

        response = response.json()
        if isinstance(response, dict) and 'errors' in response:
            return {'error': response['errors']}, 400

        return response, 200
