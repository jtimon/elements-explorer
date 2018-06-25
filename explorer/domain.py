
from mintools import ormin

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.stats import Blockstats
from explorer.models.stats import Mempoolstats
from explorer.models.transaction import Tx

ORMIN_DOMAIN = ormin.Domain([
    Block,
    Blockstats,
    Chaininfo,
    Mempoolstats,
    Tx,
])
