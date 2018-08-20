# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import pyzmq

from .messenger import Messenger

class Receiver(Messenger):

    def _init_socket(self):
        self.socket = self.context.socket(pyzmq.PULL)
