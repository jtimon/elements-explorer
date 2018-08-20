# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.process.base import CronCacher

class MempoolSaver(CronCacher):

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
