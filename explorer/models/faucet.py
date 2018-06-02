
from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Faucetinfo(RpcCachedModel):
    time = ormin.IntField(index=True)

    amount = ormin.IntField()
    balance = ormin.IntField()

    @classmethod
    def truth_src_get(cls, req_id):
        balance = super(Faucetinfo, cls)._rpccaller.RpcCall('getbalance', {'blockhash': req_id})
        if 'error' in balance:
            return balance

        faucetinfo = Faucetinfo(json_dict={
            'time': time,
            'amount': amount,
            'balance': balance,
        })
        faucetinfo.id = req_id
        faucetinfo.save()
        return faucetinfo

class Faucetsent(ormin.Model):
    time = ormin.IntField(index=True)
    amount = ormin.IntField()
    txid = ormin.StringField()
    address = ormin.StringField()
