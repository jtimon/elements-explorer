
import multiprocessing
import time

from mintools.ormin import Form as ormin_form
from mintools.ormin import Model as ormin_model

from explorer.models.rpc_cached import RpcCachedModel

class RpcCacher(object):

    def __init__(self, rpccaller, db_client):
        super(RpcCacher, self).__init__()

        self.rpccaller = rpccaller
        RpcCachedModel.set_rpccaller(rpccaller)
        self.db_client = db_client
        ormin_model.set_db(db_client)


class ChainCacher(RpcCacher):

    def __init__(self, chain, rpccaller, db_client):

        super(ChainCacher, self).__init__(rpccaller, db_client)

        self.chain = chain
        ormin_form.set_namespace(self.chain)


class CronCacher(ChainCacher, multiprocessing.Process):

    def __init__(self, chain, rpccaller, db_client, wait_time, initial_wait_time):

        super(CronCacher, self).__init__(chain, rpccaller, db_client)

        self.wait_time = wait_time
        self.initial_wait_time = initial_wait_time

    def run(self):
        time.sleep(self.initial_wait_time)
        while True:
            self._cron_loop()
            time.sleep(self.wait_time)
