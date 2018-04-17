#!/usr/bin/env python
if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

import gflags

gflags.DEFINE_string('chain', u"elementsregtest",
                     u"Chain to for which to generate txs and/or Blocks")

try:
    import sys
    argv = gflags.FLAGS(sys.argv)
except gflags.FlagsError, e:
    print('%s\n\nUsage %s ARGS \n%s' % (e, sys.argv[0], gflags.FLAGS))
    sys.exit(0)
FLAGS = gflags.FLAGS

# ===----------------------------------------------------------------------===

from explorer.daemon_subscriber import BlockGenerator, TxGenerator, PegoutGenerator, PeginGenerator
from explorer.env_config import AVAILABLE_CHAINS

chain = FLAGS.chain

if 'block_gen' in AVAILABLE_CHAINS[chain]['proc']:
    block_gen_params = [chain, AVAILABLE_CHAINS[chain]['rpc']]
    block_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['block_gen'])
    block_generator = BlockGenerator(*block_gen_params)
    block_generator.start()

if 'tx_gen' in AVAILABLE_CHAINS[chain]['proc']:
    tx_gen_params = [chain, AVAILABLE_CHAINS[chain]['rpc']]
    tx_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['tx_gen'])
    tx_generator = TxGenerator(*tx_gen_params)
    tx_generator.start()

if 'pegin_gen' in AVAILABLE_CHAINS[chain]['proc'] and 'parent_chain' in AVAILABLE_CHAINS[chain]:
    parent_chain_rpccaller = AVAILABLE_CHAINS[ AVAILABLE_CHAINS[chain]['parent_chain'] ]['rpc']
    pegin_gen_params = [chain, AVAILABLE_CHAINS[chain]['rpc'], parent_chain_rpccaller]
    pegin_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['pegin_gen'])
    pegin_generator = PeginGenerator(*pegin_gen_params)
    pegin_generator.start()

if 'pegout_gen' in AVAILABLE_CHAINS[chain]['proc'] and 'parent_chain' in AVAILABLE_CHAINS[chain]:
    parent_chain_rpccaller = AVAILABLE_CHAINS[ AVAILABLE_CHAINS[chain]['parent_chain'] ]['rpc']
    pegout_gen_params = [chain, AVAILABLE_CHAINS[chain]['rpc'], parent_chain_rpccaller]
    pegout_gen_params.extend(AVAILABLE_CHAINS[chain]['proc']['pegout_gen'])
    pegout_generator = PegoutGenerator(*pegout_gen_params)
    pegout_generator.start()