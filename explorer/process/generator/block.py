
from explorer.process.base import CronCacher

class BlockGenerator(CronCacher):

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(BlockGenerator, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

        # Load private keys for block-signing if any
        try:
            with open('/root/keys/%s.wif' % chain, 'r') as f:
                wif_list = f.read().splitlines() 
                for wif in wif_list:
                    result = self.rpccaller.RpcCall('importprivkey', {'privkey': wif})
                    print('BlockGenerator.import_keys_if_any: Rpc importprivkey result', result)
        except IOError:
            print('File /root/keys/%s.wif not found' % chain)

    def _cron_loop(self):
        try:
            block_hashes = self.rpccaller.RpcCall('generate', {'nblocks': 1})
            print('Generated block', block_hashes)
        except Exception as e:
            print("Error in BlockGenerator._cron_loop:", type(e), e)
