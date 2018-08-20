# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import ormin
from explorer.models.rpc_cached import RpcCachedModel

class Chaininfo(RpcCachedModel):
    bestblockhash = ormin.StringField()
    blocks = ormin.IntField()
    mediantime = ormin.IntField()
    cached_blocks = ormin.IntField()
    caching_first = ormin.IntField()
    caching_blockhash = ormin.StringField()
    caching_last = ormin.IntField()
    signblock_asm = ormin.StringField(required=False)
    signblock_hex = ormin.StringField(required=False)

    @classmethod
    def truth_src_get(cls, req_id):
        json_result = super(Chaininfo, cls)._rpccaller.RpcCall('getblockchaininfo', {})
        if 'error' in json_result:
            return json_result

        chaininfo = cls(json_dict=json_result)
        chaininfo.id = req_id
        chaininfo.start_caching_progress()
        chaininfo.save()
        return chaininfo

    def clean_caching_progress_fields(self):
        self.caching_first = -1
        self.caching_blockhash = ''
        self.caching_last = -1

    def start_caching_progress(self):
        self.cached_blocks = -1
        self.clean_caching_progress_fields()
