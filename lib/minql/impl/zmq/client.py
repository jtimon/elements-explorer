
from lib import zmqmin

from ...interface import MinqlBaseClient

class ZmqMinqlClient(MinqlBaseClient):

    def __init__(self, address, *args, **kwargs):

        self.client = zmqmin.Client(address)

        super(ZmqMinqlClient, self).__init__(*args, **kwargs)

    def create_table(self, table_name, schema):

        return self.client.send_request({
            'method': 'create_table',
            'table_name': table_name,
            'schema': schema,
        })

    def _drop_table(self, table_name):

        return self.client.send_request({
            'method': 'drop_table',
            'table_name': table_name,
        })

    def search(self, table_name, criteria={}):

        return self.client.send_request({
            'method': 'search',
            'table_name': table_name,
            'criteria': criteria,
        })

    def put(self, table_name, row):

        return self.client.send_request({
            'method': 'put',
            'table_name': table_name,
            'row': row,
        })

    def _get(self, table_name, id):

        return self.client.send_request({
            'method': '_get',
            'table_name': table_name,
            'id': id,
        })
