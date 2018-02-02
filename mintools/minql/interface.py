
from . import TableNotFoundError, NotFoundError, AlreadyExistsError, read_json

class MinqlBaseClient(object):

    def create_table(self, table_name, schema):
        raise NotImplementedError

    def _drop_table(self, table_name):
        raise NotImplementedError

    def drop_table(self, table_name):
        print('drop_table %s' % table_name)
        try:
            self._drop_table(table_name)
        except:
            print('WARNING: trying to drop unkown table %s' % table_name)

    def search(self, table_name, criteria={}):
        raise NotImplementedError

    def delete(self, table_name, criteria):
        raise NotImplementedError

    def _get(self, table_name, id):
        raise NotImplementedError

    def put(self, table_name, row):
        raise NotImplementedError

    def get(self, table_name, id):
        obj = self._get(table_name, id)
        if obj is None:
            raise NotFoundError(table_name, id)
        return obj

    def delete_single(self, table_name, id):
        obj = self._get(table_name, id)
        if obj is None:
            raise NotFoundError(table_name, id)
        self.delete(table_name, {'id': id})

    def update(self, table_name, row):
        obj = self.get(table_name, row['id'])
        return self.put(table_name, row)

    def insert(self, table_name, row):
        try:
            obj = self.get(table_name, row['id'])
            raise AlreadyExistsError(table_name, row['id'])
        except NotFoundError:
            return self.put(table_name, row)

    def put_table(self, table_name, schema):
        self.drop_table(table_name)
        print('create_table %s' % table_name)
        self.create_table(table_name, schema)

    def put_schema(self, schema={}):
        print('put_schema...')
        for table_name, s in schema.iteritems():
            self.put_table(table_name, s)

    def put_schema_from_file(self, path):
        print('put_schema_from_file...')
        self.put_schema(read_json(path))

    def put_table_data(self, table_name, rows):
        print('put_table_data %s' % table_name)
        for row in rows:
            self.put(table_name, row)

    def put_dataset(self, dataset):
        print('put_dataset...')
        for table_name, rows in dataset.iteritems():
            self.put_table_data(table_name, rows)

    def put_dataset_from_file(self, path):
        print('put_dataset_from_file...')
        self.put_dataset(read_json(path))

    def reset_db(self, table_names=[]):
        for tn in table_names:
            self.drop_table(tn)
