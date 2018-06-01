
import json

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Chaininfo(RpcCachedModel):
    bestblockhash = ormin.StringField()
    blocks = ormin.IntField()
    mediantime = ormin.IntField()
    signblock_asm = ormin.StringField(required=False)
    signblock_hex = ormin.StringField(required=False)

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Chaininfo, cls)._rpccaller.RpcCall('getblockchaininfo', {})
        if 'error' in json_result:
            return json_result

        chaininfo = cls(json_dict=json_result)
        chaininfo.id = req_id
        chaininfo.save()
        return chaininfo

class Block(RpcCachedModel):
    height = ormin.IntField(index=True, unique=True)
    previousblockhash = ormin.StringField(index=True, required=False)
    # bits = ormin.IntField(required=False) TODO don't show the challenge in bits in elements
    # chainwork = ormin.StringField(required=False)
    # difficulty = ormin.IntField(required=False)
    signblock_witness_asm = ormin.StringField(required=False)
    signblock_witness_hex = ormin.StringField(required=False)
    mediantime = ormin.IntField()
    merkleroot = ormin.StringField()
    # nonce = ormin.IntField(required=False)
    size = ormin.IntField()
    # strippedsize = ormin.IntField()
    time = ormin.IntField()
    # version = ormin.IntField()
    # versionhex = ormin.StringField()
    weight = ormin.IntField()
    tx = ormin.TextField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Block, cls)._rpccaller.RpcCall('getblock', {'blockhash': req_id})
        if 'error' in json_result:
            return json_result

        json_result['tx'] = json.dumps(json_result['tx'])
        block = Block(json_dict=json_result)
        block.id = req_id
        block.save()
        return block
