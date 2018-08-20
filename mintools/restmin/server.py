# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import zmqmin

class Server(zmqmin.Server):

    def __init__(self, resource, 
                 address,
                 single=False, worker_id='RestminServer', 
                 *args, **kwargs):

        self._resource = resource

        super(Server, self).__init__(address, single, worker_id, True, 
                                     *args, **kwargs)

    def _init_process(self):
        super(Server, self)._init_process()

        self._resource._init()

    def calculate_response(self, request):
        return self._resource.resolve_request(request)
