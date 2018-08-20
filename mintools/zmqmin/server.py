# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from  multiprocessing import Process

import pyzmq
from .process import Process

class Server(Process):

    def _init_socket(self):
        self.socket = self.context.socket(pyzmq.REP)

    def _loop(self):
        while True:
            request = self.receive_message()
            response = self.calculate_response(request)
            self.send_message(response)
