
class TableNotFoundError(BaseException):
    pass

class NotFoundError(BaseException):
    def __init__(self, table_name, id, *args, **kwargs):
        self.errors = {'Error:': '%s %s not found.' % (table_name, id)}
        super(NotFoundError, self).__init__(*args, **kwargs)

class AlreadyExistsError(BaseException):
    def __init__(self, table_name, id, *args, **kwargs):
        self.errors = {'Error:':'The %s %s already exists.' % (table_name, id)}
        super(AlreadyExistsError, self).__init__(*args, **kwargs)

def MinqlClient(db, address):

    if db == 'zmq':
        from .impl.zmq import ZmqMinqlClient
        return ZmqMinqlClient(address)
    elif db == 'dummy':
        from .impl.dummy import DummyMinqlClient
        return DummyMinqlClient(address)
    elif db == 'hyperdex':
        from .impl.hyperdex import HyperdexMinqlClient
        return HyperdexMinqlClient(address)
    elif db == 'postgres':
        from .impl.postgresql import PostgresqlMinqlClient
        return PostgresqlMinqlClient(address)
    else:
        raise NotImplementedError

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
