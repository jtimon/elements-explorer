# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.process.generator.sidechain import SidechainGenerator

class PeginGenerator(SidechainGenerator):

    def __init__(self, chain, rpccaller, parent_rpccaller, wait_time, initial_wait_time,
                 *args, **kwargs):

        self.ptxi_set = []
        super(PeginGenerator, self).__init__(chain, rpccaller, parent_rpccaller, wait_time, initial_wait_time,
                                                 *args, **kwargs)
    def _cron_loop(self):
        try:
            pegin_address = self.rpccaller.RpcCall('getpeginaddress', {})['mainchain_address']
            txid = self.parent_rpccaller.RpcCall('sendtoaddress', {'address': pegin_address, 'amount': 0.01})
            if 'error' in txid:
                print('Error Generating pegin candidate:', txid['error'])
            else:
                self.ptxi_set.append(txid)
                print('Generated pegin candidate: pegin_address %s txid %s' % (pegin_address, txid))
        except Exception as e:
            print("Error in PeginGenerator._cron_loop (1, candidate):", type(e), e)

        try:
            print('PeginGenerator._cron_loop: Looping among %s pending pegins' % len(self.ptxi_set))
            for txid in self.ptxi_set:
                proof = self.parent_rpccaller.RpcCall('gettxoutproof', {'txids': [txid]})
                if 'error' in proof:
                    continue
                raw = self.parent_rpccaller.RpcCall('getrawtransaction', {'txid': txid})
                claimtxid = self.rpccaller.RpcCall('claimpegin', {'bitcoinT': raw, 'txoutproof': proof})
                if 'error' in claimtxid:
                    print('Error claiming pegin:', claimtxid['error'])
                else:
                    self.ptxi_set.remove(txid)
                    print('Generated pegin claim: txid %s claimtxid %s' % (txid, claimtxid))
        except Exception as e:
            print("Error in PeginGenerator._cron_loop (2, claim):", type(e), e)

        if len(self.ptxi_set) > 1000:
            self.ptxi_set = self.ptxi_set[:1000]

