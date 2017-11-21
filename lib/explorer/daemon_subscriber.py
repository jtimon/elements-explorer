
import binascii

from lib import zmqmin
from lib import minql

from lib.explorer.explorer_server import GetById

class DaemonSubscriber(zmqmin.Subscriber, zmqmin.Process):

    def __init__(self,
                 address,
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

        self.chain = chain
        self.rpccaller = rpccaller
        self.db_factory = minql.MinqlFactory(db_type, db_adr, db_name, db_user, db_pass)

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
        self.db_client = self.db_factory.create()

    def delete_from_height(self, block_height):
        criteria = {'height': {'ge': block_height}}
        blocks_to_delete = self.db_client.search(self.chain + "_" + 'block', criteria)
        for block in blocks_to_delete:
            blockhash = block['id']
            print('delete txs with blockhash %s' % blockhash)
            print('to_delete_block', block)
            tx_criteria = {'blockhash': blockhash}
            self.db_client.delete(self.chain + "_" + 'tx', tx_criteria)

        self.db_client.delete(self.chain + "_" + 'block', criteria)
        self.db_client.delete(self.chain + "_" + 'blockstats', criteria)

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
            self.delete_from_height(block_height)
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
