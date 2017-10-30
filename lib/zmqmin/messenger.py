
from . import pyzmq, ForceReceiveError

class Messenger(object):

    def __init__(self, address,
                 context=False, single=False,
                 worker_id='Messenger',
                 json=True,
                 gevent=False,
                 multipart=False,
                 *args, **kwargs):

        self.address = address
        self.single = single
        self.worker_id = worker_id
        self.json = json
        self.multipart = multipart
        self.context = context
        self.gevent = gevent

        self._connect_socket()

        super(Messenger, self).__init__(*args, **kwargs)

    def _init_socket(self):
        raise NotImplementedError

    def _connect_socket(self):
        if not self.context:
            self.context = pyzmq.Context(self.gevent)
        self._init_socket()

        if self.single:
            self.socket.bind(self.address)
        else:
            self.socket.connect(self.address)
        print '%s connected to %s' % (self.worker_id, self.address)

    def send_message(self, message):
        if self.json:
            self.socket.send_json(message)
        elif self.multipart:
            self.socket.send_multipart(message)
        else:
            self.socket.send(message)

    def receive_message(self, force=False):
        if force:
            try:
                if self.json:
                    return self.socket.recv_json(pyzmq.DONTWAIT)
                elif self.multipart:
                    return self.socket.recv_multipart(pyzmq.DONTWAIT)
                else:
                    return self.socket.recv(pyzmq.DONTWAIT)
            except pyzmq.ZMQError:
                raise ForceReceiveError
        else:
            if self.json:
                return self.socket.recv_json()
            elif self.multipart:
                return self.socket.recv_multipart()
            return self.socket.recv()
