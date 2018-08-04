#!/usr/bin/env python

# Copyright (c) 2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

if __name__ != '__main__':
    raise ImportError(u"%s may only be run as a script" % __file__)

print('Running %s' % (__file__))

# ===----------------------------------------------------------------------===

from explorer.resources.faucet import FaucetInfoResource, FreeCoinsResource

from explorer.test_tools.test_prototypes import RepeatPerAvailableChainTest

class FaucetTest(RepeatPerAvailableChainTest):

    def assert_faucet_info(self, faucet_info, status):
        print('faucet_info', faucet_info)
        assert status == 200
        assert 'amount' in faucet_info
        assert 'balance' in faucet_info
        assert 'time' in faucet_info
        assert 'donation_address' in faucet_info

    def assert_free_coins(self, faucet_result, status):
        assert status == 200
        assert 'amount' in faucet_result
        assert 'txid' in faucet_result
        assert 'time' in faucet_result
        assert 'address' in faucet_result

    def run_tests_for_chain(self, chain):

        print('Running %s for chain %s' % (self.__class__.__name__, chain))
        faucet_info_resource = FaucetInfoResource()
        freecoins_resource = FreeCoinsResource()

        req = {}
        try:
            faucet_info = faucet_info_resource.resolve_request(req)
            raise Exception("Expected exception KeyError('json')")
        except KeyError as e:
            assert str(e) == "'json'"

        # Should work without json.chain thanks to DEFAULT_CHAIN
        req = {'json': {},}
        faucet_info, status = faucet_info_resource.resolve_request(req)
        self.assert_faucet_info(faucet_info, status)

        # Should also work with an explicit json.chain
        req = {
            'json': {
                'chain': chain,
            },
        }
        faucet_info, status = faucet_info_resource.resolve_request(req)
        self.assert_faucet_info(faucet_info, status)
        
        req = {
            'json': {
                'chain': chain,
            },
        }
        faucet_result = freecoins_resource.resolve_request(req)
        print('faucet_result', faucet_result)
        assert faucet_result == ({'error': {'message': 'No address specified to get freecoins in request {}'}}, 400)

        req = {
            'json': {
                'chain': chain,
                'address': faucet_info['donation_address'],
            },
        }
        faucet_result, status = freecoins_resource.resolve_request(req)
        print('faucet_result', faucet_result, req)
        if self.needs_101(chain):
            assert faucet_result == {'error': {'message': u'freecoins: Not enough funds for chain %s' % chain}}

            self.do_101(chain)

            req = {
                'json': {
                    'chain': chain,
                    'address': faucet_info['donation_address'],
                },
            }
            faucet_result, status = freecoins_resource.resolve_request(req)
            self.assert_free_coins(faucet_result, status)
        else:
            self.assert_free_coins(faucet_result, status)

        # Test that reusing addresses isn't allowed
        req = {
            'json': {
                'chain': chain,
                'address': faucet_info['donation_address'],
            },
        }
        faucet_result, status = freecoins_resource.resolve_request(req)
        assert status == 400
        assert faucet_result == {'error': {'message': "freecoins: Don't reuse address %s (chain %s)" % (
            faucet_info['donation_address'], chain)}}
            
        req = {
            'json': {
                'chain': chain,
                'address': 'AAA',
            },
        }
        faucet_result = freecoins_resource.resolve_request(req)
        print('faucet_result', faucet_result)
        assert (
            faucet_result == ({'error': {u'message': u'Invalid address', u'code': -5}}, 400) or
            faucet_result == ({'error': {u'message': u'Invalid Bitcoin address', u'code': -5}}, 400)
        )
            
FaucetTest().run_tests()
