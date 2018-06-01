
import json

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

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
