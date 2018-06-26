
from mintools.ormin import Domain

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.stats import Blockstats
from explorer.models.stats import Mempoolstats
from explorer.models.transaction import Input, Output, Tx

ORMIN_DOMAIN = Domain([
    Block,
    Blockstats,
    Chaininfo,
    Input,
    Mempoolstats,
    Output,
    Tx,
])
