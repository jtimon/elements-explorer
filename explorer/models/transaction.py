
import json

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Output(ormin.Model):
    n = ormin.IntField()

    value = ormin.StringField(required=False)
    value_minimum = ormin.StringField(required=False)
    value_maximum = ormin.StringField(required=False)
    ct_exponent = ormin.StringField(required=False)
    ct_bits = ormin.StringField(required=False)

    asset = ormin.StringField(required=False)
    assetcommitment = ormin.StringField(required=False)
    amountcommitment = ormin.StringField(required=False)

    scriptpubkey_asm = ormin.StringField()
    scriptpubkey_hex = ormin.StringField()
    scriptpubkey_type = ormin.StringField()
    scriptpubkey_reqsigs = ormin.IntField(required=False)
    scriptpubkey_addresses = ormin.BlobField(required=False)

    pegout_chain = ormin.StringField(required=False)
    pegout_scriptpubkey_asm = ormin.StringField(required=False)
    pegout_scriptpubkey_hex = ormin.StringField(required=False)
    pegout_scriptpubkey_type = ormin.StringField(required=False)
    pegout_scriptpubkey_reqsigs = ormin.IntField(required=False)
    pegout_scriptpubkey_addresses = ormin.BlobField(required=False)

    def __init__(self, json_dict=None, *args, **kwargs):

        if 'value-minimum' in json_dict:
            json_dict['value_minimum'] = json_dict['value-minimum']

        if 'value-maximum' in json_dict:
            json_dict['value_maximum'] = json_dict['value-maximum']

        if 'ct-exponent' in json_dict:
            json_dict['ct_exponent'] = json_dict['ct-exponent']

        if 'ct-bits' in json_dict:
            json_dict['ct_bits'] = json_dict['ct-bits']

        if 'scriptPubKey' in json_dict:
            json_dict['scriptpubkey_asm'] = json_dict['scriptPubKey']['asm']
            json_dict['scriptpubkey_hex'] = json_dict['scriptPubKey']['hex']
            json_dict['scriptpubkey_type'] = json_dict['scriptPubKey']['type']
            if 'reqSigs' in json_dict['scriptPubKey']:
                json_dict['scriptpubkey_reqsigs'] = json_dict['scriptPubKey']['reqSigs']
            if 'addresses' in json_dict['scriptPubKey']:
                json_dict['scriptpubkey_addresses'] = json.dumps(json_dict['scriptPubKey']['addresses'])

            if 'pegout_asm' in json_dict['scriptPubKey']:
                json_dict['pegout_scriptpubkey_asm'] = json_dict['scriptPubKey']['pegout_asm']
            if 'pegout_hex' in json_dict['scriptPubKey']:
                json_dict['pegout_scriptpubkey_hex'] = json_dict['scriptPubKey']['pegout_hex']
            if 'pegout_type' in json_dict['scriptPubKey']:
                json_dict['pegout_scriptpubkey_type'] = json_dict['scriptPubKey']['pegout_type']
            if 'pegout_reqSigs' in json_dict['scriptPubKey']:
                json_dict['pegout_scriptpubkey_reqsigs'] = json_dict['scriptPubKey']['pegout_reqSigs']
            if 'pegout_addresses' in json_dict['scriptPubKey']:
                json_dict['pegout_scriptpubkey_addresses'] = json.dumps(json_dict['scriptPubKey']['pegout_addresses'])

        super(Output, self).__init__(json_dict=json_dict, *args, **kwargs)

    def new_id(self):
        self.id = "%s_%s" % (self.tx_id, self.n)


class Tx(RpcCachedModel):
    blockhash = ormin.StringField(index=True)
    time = ormin.IntField(required=False)
    hex = ormin.TextField()
    size = ormin.IntField()
    vsize = ormin.IntField()
    version = ormin.IntField()
    locktime = ormin.BigIntField()

    vin = ormin.BlobField()
    vout = ormin.OneToManyField(Output, 'tx_id', cascade=True)

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

# TODO remove this patch, necessary for OneToManyField relation to
# appear in the related ManyToOne Model schema from the beginning
Tx._init_fields()
