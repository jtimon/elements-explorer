
import multiprocessing

import pyzmq
from .messenger import Messenger

class Process(Messenger, multiprocessing.Process):

    def __init__(self, address, 
                 single=True, 
                 worker_id='Process', 
                 json=True, 
                 *args, **kwargs):
 
        super(Process, self).__init__(
            address=address, 
            single=single, worker_id=worker_id, json=json, 
            *args, **kwargs)

    def _connect_socket(self):
        pass

    def _init_process(self):
        self.context = pyzmq.Context()
        super(Process, self)._connect_socket()

    def _loop(self):
        raise NotImplementedError

    def run(self):
        self._init_process()
        self._loop()
