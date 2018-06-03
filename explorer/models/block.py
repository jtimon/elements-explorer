
import json

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Block(RpcCachedModel):
    height = ormin.IntField(index=True, unique=True)
    previousblockhash = ormin.StringField(index=True, required=False)

    # For chains with pow (optional)
    bits = ormin.StringField(required=False)
    chainwork = ormin.StringField(required=False)
    difficulty = ormin.BigIntField(required=False)
    nonce = ormin.BigIntField(required=False)

    # For chains with signed blocks (optional)
    signblock_witness_asm = ormin.StringField(required=False)
    signblock_witness_hex = ormin.StringField(required=False)

    mediantime = ormin.IntField()
    merkleroot = ormin.StringField()
    size = ormin.IntField()
    # strippedsize = ormin.IntField()
    time = ormin.IntField()
    # version = ormin.IntField()
    # versionhex = ormin.StringField()
    weight = ormin.IntField()

    tx = ormin.BlobField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Block, cls)._rpccaller.RpcCall('getblock', {'blockhash': req_id})
        if 'error' in json_result:
            return json_result

        block = Block(json_dict=json_result)
        block.id = req_id
        block.save()
        return block
