# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Blockstats(RpcCachedModel):
    height = ormin.IntField(index=True)

    subsidy = ormin.BigIntField()
    total_out = ormin.BigIntField()

    avgfee = ormin.BigIntField()
    avgfeerate = ormin.IntField()
    avgtxsize = ormin.IntField()
    feerate_percentiles_10 = ormin.IntField(required=False)
    feerate_percentiles_25 = ormin.IntField(required=False)
    feerate_percentiles_50 = ormin.IntField(required=False)
    feerate_percentiles_75 = ormin.IntField(required=False)
    feerate_percentiles_90 = ormin.IntField(required=False)
    ins = ormin.IntField()
    maxfee = ormin.BigIntField()
    maxfeerate = ormin.IntField()
    maxtxsize = ormin.IntField()
    medianfee = ormin.BigIntField()
    mediantime = ormin.IntField()
    mediantxsize = ormin.IntField()
    minfee = ormin.BigIntField()
    minfeerate = ormin.IntField()
    mintxsize = ormin.IntField()
    outs = ormin.IntField()
    swtotal_size = ormin.IntField()
    swtotal_weight = ormin.IntField()
    swtxs = ormin.IntField()
    time = ormin.IntField()
    total_size = ormin.IntField()
    total_weight = ormin.IntField()
    totalfee = ormin.BigIntField()
    txs = ormin.IntField()
    utxo_increase = ormin.IntField()
    utxo_size_inc = ormin.IntField()

    def __init__(self, json_dict=None, *args, **kwargs):

        if 'feerate_percentiles' in json_dict and len(json_dict['feerate_percentiles']) == 5:
            json_dict['feerate_percentiles_10'] = json_dict['feerate_percentiles'][0]
            json_dict['feerate_percentiles_25'] = json_dict['feerate_percentiles'][1]
            json_dict['feerate_percentiles_50'] = json_dict['feerate_percentiles'][2]
            json_dict['feerate_percentiles_75'] = json_dict['feerate_percentiles'][3]
            json_dict['feerate_percentiles_90'] = json_dict['feerate_percentiles'][4]
            del json_dict['feerate_percentiles']
        
        super(Blockstats, self).__init__(json_dict=json_dict, *args, **kwargs)
    
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
    stat_type = ormin.StringField(index=True)
    
    blob = ormin.BlobField()

    def new_id(self):
        self.id = '%s_%s' % (self.time, self.stat_type)
