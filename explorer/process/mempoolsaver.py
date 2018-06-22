
from explorer.process import base

class MempoolSaver(base.CronCacher):

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(MempoolSaver, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

    def _cron_loop(self):
        try:
            self.rpccaller.RpcCall('savemempool', {})
            print('Success saving mempool...')
        except Exception as e:
            print("Error in MempoolSaver._cron_loop:", type(e), e)
