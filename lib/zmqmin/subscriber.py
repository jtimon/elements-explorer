
import pyzmq

from .messenger import Messenger

class Subscriber(Messenger):

    # topicfilter blank to get all messages
    def __init__(self, address, 
                 context=pyzmq.Context(), single=False,
                 worker_id='Subscriber', 
                 json=True, topic='', 
                 *args, **kwargs):

        self.topic = topic

        super(Subscriber, self).__init__(
            address=address, context=context, 
            single=single, worker_id=worker_id, json=json, 
            *args, **kwargs)

    def _init_socket(self):
        self.socket = self.context.socket(pyzmq.SUB)
        self.socket.setsockopt(pyzmq.SUBSCRIBE, self.topic)
