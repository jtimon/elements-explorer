# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.process.generator.sidechain import SidechainGenerator

class PegoutGenerator(SidechainGenerator):

    def __init__(self, chain, rpccaller, parent_rpccaller, parent_chain_has_CT, wait_time, initial_wait_time,
                 *args, **kwargs):

        self.parent_chain_has_CT = parent_chain_has_CT

        super(PegoutGenerator, self).__init__(chain, rpccaller, parent_rpccaller, wait_time, initial_wait_time,
                                              *args, **kwargs)

    def _cron_loop(self):
        try:
            address = self.parent_rpccaller.RpcCall('getnewaddress', {})
            if self.parent_chain_has_CT:
                address = self.parent_rpccaller.RpcCall('validateaddress', {'address': address})['unconfidential']
            txid = self.rpccaller.RpcCall('sendtomainchain', {'address': address, 'amount': 0.01})
            print('Generated pegout', txid)
        except Exception as e:
            print("Error in PegoutGenerator._cron_loop:", type(e), e)
