
from mintools import ormin

class RpcCachedModel(ormin.CachedModel):

    @classmethod
    def set_rpccaller(cls, value):
        cls._rpccaller = value


class Chaininfo(RpcCachedModel):
    bestblockhash = ormin.StringField()
    blocks = ormin.IntField()
    mediantime = ormin.IntField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Chaininfo, cls)._rpccaller.RpcCall('getblockchaininfo', {})
        if 'error' in json_result:
            return json_result

        chaininfo = cls(json=json_result)
        chaininfo.id = req_id
        chaininfo.save()
        return chaininfo

class Block(ormin.Model):
    height = ormin.IntField(index=True, unique=True)
    blob = ormin.TextField()

class Tx(ormin.Model):
    blockhash = ormin.StringField(index=True)
    blob = ormin.TextField()

class Blockstats(ormin.Model):
    height = ormin.IntField(index=True)
    blob = ormin.TextField()

class Mempoolstats(ormin.Model):
    time = ormin.IntField(index=True)
    blob = ormin.TextField()
