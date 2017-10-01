
import pyzmq

from .messenger import Messenger

class Receiver(Messenger):

    def _init_socket(self):
        self.socket = self.context.socket(pyzmq.PULL)
