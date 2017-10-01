
from lib import restmin
from lib import zmqmin

from ... import MinqlClient

class ZmqMinqlServer(zmqmin.Server):

    def __init__(self, client_class, 
                 single, address, db_address,
                 worker_id='ZmqMinqlServer',
                 *args, **kwargs):

        self.client_class = client_class
        self.db_address = db_address

        super(ZmqMinqlServer, self).__init__(
            address, single, worker_id, True, 
            *args, **kwargs)

    def _init_process(self):
        super(ZmqMinqlServer, self)._init_process()
        
        client = MinqlClient(self.client_class, self.db_address)
        self._resource = restmin.ClassResource(
            client, 
            ['create_table', 'drop_table', 'search', '_get', 'put'])

    def calculate_response(self, request):
        return self._resource.resolve_request(request)
