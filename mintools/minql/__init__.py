
class MinqlException(BaseException):
    pass

class TableNotFoundError(MinqlException):
    pass

class NotFoundError(MinqlException):
    def __init__(self, table_name, id, *args, **kwargs):
        self.errors = {'Error:': '%s %s not found.' % (table_name, id)}
        super(NotFoundError, self).__init__(*args, **kwargs)

class AlreadyExistsError(MinqlException):
    def __init__(self, table_name, id, *args, **kwargs):
        self.errors = {'Error:':'The %s %s already exists.' % (table_name, id)}
        super(AlreadyExistsError, self).__init__(*args, **kwargs)

def MinqlClientFactory(db):

    if db == 'zmq':
        from .impl.zmq import ZmqMinqlClient
        return ZmqMinqlClient
    elif db == 'dummy':
        from .impl.dummy import DummyMinqlClient
        return DummyMinqlClient
    elif db == 'hyperdex':
        from .impl.hyperdex import HyperdexMinqlClient
        return HyperdexMinqlClient
    elif db == 'postgres':
        from .impl.postgresql import PostgresqlMinqlClient
        return PostgresqlMinqlClient
    else:
        raise NotImplementedError

def MinqlClient(db, address):
    return MinqlClientFactory(db)(address)

class MinqlFactory(object):

    def __init__(self,
                 db_type,
                 db_adr,
                 db_name,
                 db_user,
                 db_pass,
                 *args, **kwargs):

        self.db_type = db_type
        self.db_adr = db_adr
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        super(MinqlFactory, self).__init__(
            *args, **kwargs)

    def create(self):
        return MinqlClientFactory(self.db_type)(self.db_adr, self.db_name, self.db_user, self.db_pass)


import json
def read_json(path):
    with open(path, 'r') as infile:
        return json.load(infile)

def write_json(path, value, ugly=False):
    with open(path, 'w') as outfile:
        if ugly:
            json.dump(value, outfile)
        else:
            json.dump(value, outfile, sort_keys=True, indent=2)

from .impl.zmq import ZmqMinqlServer

from .migration import get_migration_schema, Migration
