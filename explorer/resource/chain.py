
from mintools import restmin, ormin

from explorer import models
from explorer.env_config import AVAILABLE_CHAINS, DEFAULT_CHAIN

class UnknownChainError(BaseException):
    pass

class ChainResource(restmin.resources.Resource):

    def update_chain(self, request_data):
        self.chain = None
        if request_data and 'chain' in request_data:
            self.chain = request_data['chain']
            del request_data['chain']
        else:
            self.chain = DEFAULT_CHAIN
        if not self.chain in AVAILABLE_CHAINS:
            raise UnknownChainError

        ormin.Form.set_namespace(self.chain)
        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']
        models.RpcCachedModel.set_rpccaller(self.rpccaller)

        return request_data
