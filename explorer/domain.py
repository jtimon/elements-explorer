
from mintools import ormin

from explorer.model import *
from explorer import models

ORMIN_DOMAIN = ormin.Domain([
    Chaininfo,
    Block,
    Tx,
    models.stats.Blockstats,
    models.stats.Mempoolstats,
])
