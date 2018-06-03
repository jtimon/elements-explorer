
from mintools import ormin

from explorer import models

ORMIN_DOMAIN = ormin.Domain([
    models.Chaininfo,
    models.Block,
    models.transaction.Tx,
    models.stats.Blockstats,
    models.stats.Mempoolstats,
])
