# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools.ormin import Domain

from explorer.models.block import Block
from explorer.models.chaininfo import Chaininfo
from explorer.models.faucet import Faucetsent
from explorer.models.stats import Blockstats
from explorer.models.stats import Mempoolstats
from explorer.models.transaction import Input, Output, Tx

ORMIN_DOMAIN = Domain([
    Block,
    Blockstats,
    Chaininfo,
    Faucetsent,
    Input,
    Mempoolstats,
    Output,
    Tx,
])
