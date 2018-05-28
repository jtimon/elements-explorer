
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

    subsidy = ormin.BigIntField()
    total_out = ormin.BigIntField()

    avgfee = ormin.IntField()
    avgfeerate = ormin.IntField()
    avgtxsize = ormin.IntField()
    ins = ormin.IntField()
    maxfee = ormin.IntField()
    maxfeerate = ormin.IntField()
    maxtxsize = ormin.IntField()
    medianfee = ormin.IntField()
    medianfeerate = ormin.IntField()
    mediantime = ormin.IntField()
    mediantxsize = ormin.IntField()
    minfee = ormin.IntField()
    minfeerate = ormin.IntField()
    mintxsize = ormin.IntField()
    outs = ormin.IntField()
    swtotal_size = ormin.IntField()
    swtotal_weight = ormin.IntField()
    swtxs = ormin.IntField()
    time = ormin.IntField()
    total_size = ormin.IntField()
    total_weight = ormin.IntField()
    totalfee = ormin.IntField()
    txs = ormin.IntField()
    utxo_increase = ormin.IntField()
    utxo_size_inc = ormin.IntField()
    
    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Blockstats, cls)._rpccaller.RpcCall('getblockstats', {'hash_or_height': req_id})
        if 'error' in json_result:
            return json_result

        # TODO Use call by blockhash or this field to keep stats for orphan/stalled branches
        del json_result['blockhash']
        blockstats = Blockstats(json_dict=json_result)
        blockstats.id = blockstats.height # TODO Use block hash for id
        blockstats.save()
        return blockstats

class Mempoolstats(ormin.Model):
    time = ormin.IntField(index=True)
    blob = ormin.TextField()
