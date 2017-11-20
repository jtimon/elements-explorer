
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
                 silent=False,
                 worker_id='DaemonSubscriber',
                 *args, **kwargs):

        self.db_type = db_type
        self.db_adr = db_adr
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.chain = chain
        self.rpccaller = rpccaller

        if (silent):
            import sys
            import os
            sys.stdout = open(os.devnull, 'w')
        
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

    def update_tip(self, block_hash):
        json_result = GetById(self.db_client, self.rpccaller, self.chain, 'block', block_hash)
        block_height = json_result['height']
        block_mediantime = json_result['mediantime']

        entry = {}
        entry['id'] = self.chain
        entry['bestblockhash'] = block_hash
        entry['blocks'] = block_height
        entry['mediantime'] = block_mediantime
        try:
            db_result = self.db_client.put(self.chain + "_" + 'chaininfo', entry)
        except:
            print('FAILED GREEDY CACHE %s in chain %s' % ('chaininfo', self.chain), entry)
            return

        try:
            criteria = {'height': {'ge': block_height}}
            to_delete = self.db_client.search(self.chain + "_" + 'block', criteria)
            print('to_delete', to_delete)
            self.db_client.delete(self.chain + "_" + 'block', criteria)
            self.db_client.delete(self.chain + "_" + 'blockstats', criteria)
        except:
            print('FAILED HANDLING REORG WITH %s in chain %s' % ('blockstats', self.chain), criteria)
            return

        try:
            json_result = GetById(self.db_client, self.rpccaller, self.chain, 'blockstats', block_height)
        except:
            print('FAILED GREEDY CACHE %s in chain %s for height %s' % ('blockstats', self.chain, block_height))

    def _loop(self):
        while True:
            msg_parts = self.receive_message()
            block_hash = binascii.hexlify(msg_parts[1])
            self.update_tip(block_hash)
