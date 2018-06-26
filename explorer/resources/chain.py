
from mintools.ormin import Form as ormin_form
from mintools.restmin.resources import Resource as restmin_resource

from explorer.env_config import AVAILABLE_CHAINS, DEFAULT_CHAIN
from explorer.models.rpc_cached import RpcCachedModel

class UnknownChainError(BaseException):
    pass

class ChainResource(restmin_resource):

    def update_chain(self, request_data):
        self.chain = None
        if request_data and 'chain' in request_data:
            self.chain = request_data['chain']
            del request_data['chain']
        else:
            self.chain = DEFAULT_CHAIN
        if not self.chain in AVAILABLE_CHAINS:
            raise UnknownChainError

        ormin_form.set_namespace(self.chain)
        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']
        RpcCachedModel.set_rpccaller(self.rpccaller)

        return request_data
