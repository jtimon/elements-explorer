
import json

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

        chaininfo = cls(json_dict=json_result)
        chaininfo.id = req_id
        chaininfo.save()
        return chaininfo

class Block(RpcCachedModel):
    height = ormin.IntField(index=True, unique=True)
    blob = ormin.TextField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Block, cls)._rpccaller.RpcCall('getblock', {'blockhash': req_id})
        if 'error' in json_result:
            return json_result

        block = Block()
        block.height = json_result['height']
        block.blob = json.dumps(json_result)
        block.id = req_id
        block.save()
        return block

class Tx(RpcCachedModel):
    blockhash = ormin.StringField(index=True)
    blob = ormin.TextField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Tx, cls)._rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
        if 'error' in json_result:
            return json_result

        tx = Tx()
        tx.blob = json.dumps(json_result)
        tx.id = req_id
        if 'blockhash' in json_result and json_result['blockhash']:
            # Don't cache mempool txs
            tx.blockhash = json_result['blockhash']
            tx.save()

        return tx

class Blockstats(RpcCachedModel):
    height = ormin.IntField(index=True)
    blob = ormin.TextField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Blockstats, cls)._rpccaller.RpcCall('getblockstats', {'height': req_id})
        if 'error' in json_result:
            return json_result

        blockstats = Blockstats()
        blockstats.height = json_result['height']
        blockstats.blob = json.dumps(json_result)
        blockstats.id = req_id
        blockstats.save()
        return blockstats

class Mempoolstats(ormin.Model):
    time = ormin.IntField(index=True)
    blob = ormin.TextField()
