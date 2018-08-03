
from mintools import ormin

class Faucetsent(ormin.Model):
    address = ormin.StringField(index=True, unique=True)
    amount = ormin.StringField()
    time = ormin.IntField(index=True)
    txid = ormin.StringField()

    def new_id(self):
        self.id = self.address
    
