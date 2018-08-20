# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import multiprocessing

import pyzmq

class Device(multiprocessing.Process):

    def __init__(self, frontend_address, backend_address, 
                 gevent=False, 
                 *args, **kwargs):

        self.frontend_address = frontend_address
        self.backend_address = backend_address
        self.gevent = gevent

        super(Device, self).__init__(*args, **kwargs)

    def _create_frontend(self):
        raise NotImplementedError
    def _create_backend(self):
        raise NotImplementedError

    def run(self):
        self.context = pyzmq.Context(self.gevent)

        self._create_frontend()
        self.frontend.bind(self.frontend_address)
        self._create_backend()
        self.backend.bind(self.backend_address)
        print("%s connecting %s to %s" % (
            self.__class__.__name__, 
            self.frontend_address, 
            self.backend_address
        ))

        pyzmq.device(self.device_type, self.frontend, self.backend, self.gevent)

class Forwarder(Device):

    def __init__(self, *args, **kwargs):

        self.device_type = pyzmq.FORWARDER

        super(Forwarder, self).__init__(*args, **kwargs)

    def _create_frontend(self):
        self.frontend = self.context.socket(pyzmq.SUB)
        self.frontend.setsockopt(pyzmq.SUBSCRIBE, "")

    def _create_backend(self):
        self.backend = self.context.socket(pyzmq.PUB)

class Streamer(Device):

    def __init__(self, *args, **kwargs):

        self.device_type = pyzmq.STREAMER

        super(Streamer, self).__init__(*args, **kwargs)

    def _create_frontend(self):
        self.frontend = self.context.socket(pyzmq.PULL)

    def _create_backend(self):
        self.backend = self.context.socket(pyzmq.PUSH)

class Queue(Device):

    def __init__(self, *args, **kwargs):

        self.device_type = pyzmq.QUEUE

        super(Queue, self).__init__(*args, **kwargs)

    def _create_frontend(self):
        self.frontend = self.context.socket(pyzmq.XREP)

    def _create_backend(self):
        self.backend = self.context.socket(pyzmq.XREQ)
