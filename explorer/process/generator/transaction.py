
from explorer.process.base import CronCacher

class TxGenerator(CronCacher):

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        super(TxGenerator, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

    def _cron_loop(self):
        try:
            address = self.rpccaller.RpcCall('getnewaddress', {})
            txid = self.rpccaller.RpcCall('sendtoaddress', {'address': address, 'amount': 0.01})
            print('Generated tx', txid)
        except Exception as e:
            print("Error in TxGenerator._cron_loop:", type(e), e)
