
from mintools import ormin

from explorer.model import Chaininfo, Block
from explorer import models

ORMIN_DOMAIN = ormin.Domain([
    Chaininfo,
    Block,
    models.transaction.Tx,
    models.stats.Blockstats,
    models.stats.Mempoolstats,
])
