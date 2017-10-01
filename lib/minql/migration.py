
class Migration(object):
    
    def __init__(self, client, schema, *args, **kwargs):

        self.client = client
        self.schema = schema

        super(Migration, self).__init__(*args, **kwargs)

    def migrate(to_client=None, to_schema=None):

        if to_client:

            if not to_schema:
                migrate_basic(to_client)
            else:
                migrate_changes(to_client, to_schema)

        elif to_schema:

            from .impl.dummy.client import DummyMinqlClient
            middle_client = DummyMinqlClient(url, port)
            self.migrate_basic(middle_client)
            aux_mig = Migration(middle_client, self.schema)
            aux_mig.migrate_changes(self.client, to_schema)

    def migrate_basic(self, to_schema):

        for table_name, s in schema.iteritems():

            try:
                to_client.drop_table(table_name)
            except TableNotFoundError:
                pass
            to_client.create_table(table_name, s)

            rows = self.client.search(table_name)
            for row in rows:
                self.client.put(table_name, row)

    def migrate_changes(self, to_client, to_schema):

        raise NotImplementedError
