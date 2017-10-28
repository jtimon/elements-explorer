
from lib import restmin
from lib import zmqmin

from ... import MinqlClientFactory

class ZmqMinqlServer(zmqmin.Server):

    def __init__(self, client_class, 
                 single, address, db_address,
                 db_name, db_user, db_pass,
                 worker_id='ZmqMinqlServer',
                 *args, **kwargs):

        self.client_class = client_class
        self.db_address = db_address
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        super(ZmqMinqlServer, self).__init__(
            address, single, worker_id, True, 
            *args, **kwargs)

    def _init_process(self):
        super(ZmqMinqlServer, self)._init_process()
        
        client = MinqlClientFactory(self.client_class)(self.db_address, self.db_name, self.db_user, self.db_pass)
        self._resource = restmin.ClassResource(
            client, 
            ['create_table', 'drop_table', 'search', '_get', 'put'])

    def calculate_response(self, request):
        return self._resource.resolve_request(request)
