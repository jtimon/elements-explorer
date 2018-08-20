# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import ormin

class Faucetsent(ormin.Model):
    address = ormin.StringField(index=True, unique=True)
    amount = ormin.StringField()
    ip = ormin.StringField(index=True)
    time = ormin.IntField(index=True)
    txid = ormin.StringField()

    def new_id(self):
        self.id = self.address
    
