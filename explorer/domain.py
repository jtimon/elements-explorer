
from mintools import ormin

from explorer.model import Block
from explorer import models

ORMIN_DOMAIN = ormin.Domain([
    models.Chaininfo,
    Block,
    models.transaction.Tx,
    models.stats.Blockstats,
    models.stats.Mempoolstats,
])
