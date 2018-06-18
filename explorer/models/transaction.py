
import json

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Tx(RpcCachedModel):
    blockhash = ormin.StringField(index=True)
    time = ormin.IntField(required=False)
    hex = ormin.TextField()
    size = ormin.IntField()
    vsize = ormin.IntField()
    version = ormin.IntField()
    locktime = ormin.BigIntField()

    vin = ormin.BlobField()
    vout = ormin.BlobField()

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Tx, cls)._rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
        if 'error' in json_result:
            return json_result

        tx = Tx(json_dict=json_result)
        tx.id = req_id

        # Don't cache mempool txs
        if 'blockhash' in json_result and json_result['blockhash']:
            tx.save()

        return tx
