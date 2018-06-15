
import datetime

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Faucetinfo(RpcCachedModel):
    time = ormin.IntField(index=True)

    balance = ormin.IntField()
    donation_address = ormin.StringField()
    giveaway_amount = ormin.IntField()

    @classmethod
    def truth_src_get(cls, req_id):

        newaddress = super(Faucetinfo, cls)._rpccaller.RpcCall('getnewaddress')
        if 'error' in newaddress:
            return newaddress

        balance = super(Faucetinfo, cls)._rpccaller.RpcCall('getbalance')
        if 'error' in balance:
            return balance
        giveaway_amount = balance / 100

        faucetinfo = Faucetinfo(json_dict={
            'time': datetime.datetime.now(),
            'donation_address': donation_address,
            'giveaway_amount': giveaway_amount,
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
