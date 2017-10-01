
from ...interface import MinqlBaseClient

class DummyMinqlClient(MinqlBaseClient):

    def __init__(self, address=None, *args, **kwargs):

        self.tables = {}
        self.schemas = {}

        super(DummyMinqlClient, self).__init__(*args, **kwargs)

    def create_table(self, table_name, schema):
        assert table_name not in self.tables, "Table '%s' already exists." % table_name

        self.tables[ table_name ] = {}
        self.schemas[ table_name ] = schema
        return {'success': "Table '%s' created." % table_name}

    def _drop_table(self, table_name):
        if table_name in self.tables:
            del self.tables[ table_name ]
        if table_name in self.schemas:
            del self.schemas[ table_name ]

    def put(self, table_name, row):
        assert table_name in self.tables, "Table '%s' doesn't exist." % table_name
        assert 'id' in row, 'A field "id" is required for put.'

        # TODO remove waiting (without breaking)
        import time
        import random
        time.sleep (random.uniform(0.001, 0.0011))

        self.tables[ table_name ][ row['id'] ] = row
        return row

    def search(self, table_name, criteria):
        assert table_name in self.tables, "Table '%s' doesn't exist." % table_name

        rows = self.tables[ table_name ].values()
        for field, value in criteria.iteritems():
            selected_rows = []
            for row in rows:
                if type(value) is dict:
                    if ('ge' in value and 
                        float(row[field]) >= float(value['ge']) ):

                        selected_rows.append(row)
                    elif ('le' in value and 
                          float(row[field]) <= float(value['le']) ):
                        selected_rows.append(row)
                elif row[field] == value:
                    selected_rows.append(row)
            rows = selected_rows

        return rows

    def _get(self, table_name, id):
        assert table_name in self.tables, "Table '%s' doesn't exist." % table_name

        if id not in self.tables[ table_name ]:
            return None
        return self.tables[ table_name ][id]
