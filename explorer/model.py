
from mintools import ormin

class Chaininfo(ormin.Model):
    bestblockhash = ormin.StringField()
    blocks = ormin.IntField()
    mediantime = ormin.IntField()

class Block(ormin.Model):
    height = ormin.IntField(index=True, unique=True)
    blob = ormin.TextField()

class Tx(ormin.Model):
    blockhash = ormin.StringField(index=True)
    blob = ormin.TextField()

class Blockstats(ormin.Model):
    height = ormin.IntField(index=True)
    blob = ormin.TextField()

class Mempoolstats(ormin.Model):
    time = ormin.IntField(index=True)
    blob = ormin.TextField()
