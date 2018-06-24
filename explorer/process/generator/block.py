
from explorer.process.base import CronCacher

class BlockGenerator(CronCacher):

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(BlockGenerator, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

    def _cron_loop(self):
        try:
            block_hashes = self.rpccaller.RpcCall('generate', {'nblocks': 1})
            print('Generated block', block_hashes)
        except Exception as e:
            print("Error in BlockGenerator._cron_loop:", type(e), e)
