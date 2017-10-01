
import hyperdex.client
import hyperdex.admin

from ...interface import MinqlBaseClient

class HyperdexMinqlClient(MinqlBaseClient):

    def __init__(self, address, *args, **kwargs):

        url, port = address.split(':')
        self.db_client = hyperdex.client.Client(url, int(port))
        self.db_admin = hyperdex.admin.Admin(url, int(port))

        super(HyperdexMinqlClient, self).__init__(*args, **kwargs)

    def create_table(self, table_name, schema):
        print 'Creating hyperdex space %s' % table_name

        attrs = []
        indexes = []
        for k, v in schema.iteritems():
            attrs.append(v['type'] + ' ' + k)
            if 'index' in v and v['index']:
                indexes.append(k)

        space = '''
        space %s
        key id
        ''' % table_name
        if attrs:
            space += '\n attributes ' + ', '.join(attrs)
        if indexes:
            space += '\n subspace ' + ', '.join(indexes)

        self.db_admin.add_space(space.encode('utf8'))

    def _drop_table(self, table_name):
        self.db_admin.rm_space(table_name.encode('utf8'))

    def search(self, table_name, criteria={}):

        if isinstance(table_name, basestring):
            table_name = table_name.encode('utf8')

        crit = {}
        for attr, value in criteria.iteritems():

            if isinstance(value, basestring):
                crit[ attr ] = value.encode('utf8')
            elif isinstance(value, int):
                crit[ attr ] = value
            elif isinstance(value, float):
                crit[ attr ] = value
            elif type(value) is dict and 'ge' in value:
                crit[ attr ] = hyperdex.client.GreaterEqual(float(value['ge']))
            elif type(value) is dict and 'le' in value:
                crit[ attr ] = hyperdex.client.LessEqual(float(value['le']))
            else:
                raise TypeError

        return [x for x in self.db_client.search(table_name, crit)]

    def put(self, table_name, row):
        assert 'id' in row and row['id'], 'The row needs an id field.'

        id = row['id'].encode('utf8')
        del row ['id']

        if isinstance(table_name, basestring):
            table_name = table_name.encode('utf8')

        for attr, value in row.iteritems():
            if isinstance(value, basestring):
                row[ attr ] = value.encode('utf8')
            elif isinstance(value, int):
                row[ attr ] = value
            elif isinstance(value, float):
                row[ attr ] = value
            else:
                raise TypeError

        # TODO remove waiting (without breaking)
        import time
        import random
        time.sleep (random.uniform(0.001, 0.0011))

        self.db_client.put(table_name, id, row)
        row['id'] = id
        return row

    def _get(self, table_name, id):

        if isinstance(table_name, basestring):
            table_name = table_name.encode('utf8')

        elem = self.db_client.get(table_name, id.encode('utf8'))
        if elem is not None:
            elem.update({'id': id})
        return elem
