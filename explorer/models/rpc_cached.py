
from mintools.ormin.model import CachedModel

class RpcCachedModel(CachedModel):

    @classmethod
    def set_rpccaller(cls, value):
        cls._rpccaller = value
