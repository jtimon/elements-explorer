
import binascii

from lib import zmqmin
from lib import minql

from lib.explorer.explorer_server import GetById

class DaemonSubscriber(zmqmin.Subscriber, zmqmin.Process):

    def __init__(self, address,
                 db_type,
                 db_adr,
                 db_name,
                 db_user,
                 db_pass,
                 chain,
                 rpccaller,
                 worker_id='DaemonSubscriber',
                 *args, **kwargs):

        self.db_type = db_type
        self.db_adr = db_adr
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.chain = chain
        self.rpccaller = rpccaller
        self.resource = 'chaininfo'

        super(DaemonSubscriber, self).__init__(
            address=address,
            context=None, single=False,
            worker_id=worker_id,
            json=False,
            topic='hashblock',
            multipart=True,
            *args, **kwargs)

    def _init_process(self):
        super(DaemonSubscriber, self)._init_process()
        self.db_client = minql.MinqlClientFactory(self.db_type)(self.db_adr, self.db_name, self.db_user, self.db_pass)

    def _loop(self):
        while True:
            msg_parts = self.receive_message()
            block_hash = binascii.hexlify(msg_parts[1])

            json_result = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)

            entry = {}
            entry['id'] = self.chain
            entry['bestblockhash'] = block_hash
            entry['blocks'] = json_result['height']
            entry['mediantime'] = json_result['mediantime']
            print('put entry', self.chain, self.resource, entry)
            try:
                db_result = self.db_client.put(self.chain + "_" + self.resource, entry)
            except:
                print('FAILED ENTRY', self.chain, self.resource, entry)
                continue
            if not db_result:
                print('FAILED ENTRY: No db result', self.chain, self.resource, entry)
                continue
