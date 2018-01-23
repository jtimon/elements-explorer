
from mintools import restmin
from mintools import minql

from ..model import Model

class Domain(restmin.Domain):

    def __init__(self, domain,
                 db_address, db_type='zmq',
                 *args, **kwargs):

        self.db_address = db_address
        self.db_type = db_type

        super(Domain, self).__init__(domain, *args, **kwargs)

    def _init(self):
        print 'connecting to', self.db_type, self.db_address
        Model.set_db( minql.MinqlClient(self.db_type, self.db_address) )

        super(Domain, self)._init()
