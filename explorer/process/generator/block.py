# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from explorer.process.base import CronCacher

class BlockGenerator(CronCacher):

    def import_keys_if_any(self, chain, rpccaller):
        # Load private keys for block-signing if any
        try:
            with open('/build_docker/keys/%s.wif' % chain, 'r') as f:
                wif_list = f.read().splitlines()
                for wif in wif_list:
                    result = self.rpccaller.RpcCall('importprivkey', {'privkey': wif})
                    print('BlockGenerator.import_keys_if_any: Rpc importprivkey result', result)
        except IOError:
            print('File /build_docker/keys/%s.wif not found' % chain)

    def __init__(self, chain, rpccaller, wait_time, initial_wait_time, generate_type,
                 *args, **kwargs):

        super(BlockGenerator, self).__init__(chain, rpccaller, None, wait_time, initial_wait_time,
                                                 *args, **kwargs)

        self.generate_type = generate_type
        self.import_keys_if_any(chain, rpccaller)

    def generate_regtestlike(self):
        try:
            block_hashes = self.rpccaller.RpcCall('generate', {'nblocks': 1})
            print('Generated %s block' % self.generate_type, block_hashes)
        except Exception as e:
            print("Error in BlockGenerator.generate_regtestlike:", type(e), e)

    def generate_onesigner(self):
        try:
            blockhex = self.rpccaller.RpcCall('getnewblockhex', {})
            sig = self.rpccaller.RpcCall('signblock', {'blockhex': blockhex})
            print('combineblocksigs', {'signatures': [sig]})
            blockresult = self.rpccaller.RpcCall('combineblocksigs', {'blockhex': blockhex, 'signatures': [sig]})

            if 'complete' in blockresult and blockresult['complete']:
                self.rpccaller.RpcCall('submitblock', {'hexdata': blockresult['hex']})
                print('Generated %s block' % self.generate_type)
            else:
                print('ERROR: Block not generated', {x: blockresult[x] for x in blockresult if x != 'hex'})

        except Exception as e:
            print("Error in BlockGenerator.generate_onesigner:", type(e), e)

    def _cron_loop(self):
        if self.generate_type == 'regtestlike':
            self.generate_regtestlike()
        elif self.generate_type == 'onesigner':
            self.generate_onesigner()
        else:
            raise Exception("BlockGenerator doesn't support generate_type %s" % self.generate_type)
