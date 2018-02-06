
from mintools import ormin

from .model import *

ORMIN_DOMAIN = ormin.Domain([
    Chaininfo,
    Block,
    Tx,
    Blockstats,
    Mempoolstats,
])
