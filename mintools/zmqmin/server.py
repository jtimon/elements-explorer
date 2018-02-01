
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
