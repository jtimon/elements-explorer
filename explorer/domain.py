
from mintools import ormin

from explorer.model import *

ORMIN_DOMAIN = ormin.Domain([
    Chaininfo,
    Block,
    Tx,
    Blockstats,
    Mempoolstats,
])
