# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

from explorer.models.chaininfo import Chaininfo
from explorer.models.transaction import Tx
from explorer.services.blockheight import GetBlockByHeight

from .chain import UnknownChainError, ChainResource

class AddressResource(ChainResource):

    def search_by_address(self, height, addresses):

        block = GetBlockByHeight(self.rpccaller, height)
        if isinstance(block, dict) and 'error' in block:
            return block

        receipts = []
        expenditures = []
        tx_ids = json.loads(block.tx)
        for txid in tx_ids:
            orm_tx = Tx.get(txid)
            if isinstance(orm_tx, dict) and 'error' in orm_tx:
                return orm_tx
            elif not isinstance(orm_tx, Tx):
                print('Error in AddressResource.search_by_address: wrong type for tx', txid, orm_tx)
                return {'error': {'message': 'Error getting tx %s (address)' % txid}}
            tx = orm_tx.json()

            for output in tx['vout']:
                for address in addresses:
                    if 'scriptpubkey_addresses' in output and address in output['scriptpubkey_addresses']:
                        receipts.append({'output': output, 'txid': txid, 'height': height})

            for tx_input in tx['vin']:
                pegin_witness = []
                if 'pegin_witness' in tx_input and tx_input['pegin_witness']:
                    if isinstance(tx_input['pegin_witness'], basestring):
                        pegin_witness = json.loads(tx_input['pegin_witness'])
                    else:
                        pegin_witness = tx_input['pegin_witness']

                if 'txid' in tx_input and 'vout' in tx_input and len(pegin_witness) == 0:
                    orm_tx_in = Tx.get(tx_input['txid'])
                    if isinstance(orm_tx_in, dict) and 'error' in orm_tx_in:
                        return orm_tx_in
                    elif not isinstance(orm_tx_in, Tx):
                        print('Error in AddressResource.search_by_address_ascendant: wrong type for tx', tx_input['txid'], orm_tx_in)
                        return {'error': {'message': 'Error getting tx %s (address)' % tx_input['txid']}}
                    tx_in = orm_tx_in.json()
                    if tx_input['vout'] < len(tx_in['vout']):
                        output = tx_in['vout'][ tx_input['vout'] ]
                        for address in addresses:
                            if 'scriptpubkey_addresses' in output and address in output['scriptpubkey_addresses']:
                                expenditures.append({'input': tx_input, 'prev_output': output, 'txid': tx['id'], 'height': height})
                    else:
                        print('Error in search by address, index out of range', tx_input, tx_in)

        return {'expenditures': expenditures, 'receipts': receipts}

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'addresses' in request:
            return {'error': {'message': '%s: No addresses specified in request %s' % ('address', request)}}, 400
        if not 'start_height' in request:
            return {'error': {'message': '%s: No start_height specified in request %s' % ('address', request)}}, 400
        if not 'end_height' in request:
            return {'error': {'message': '%s: No end_height specified in request %s' % ('address', request)}}, 400

        if request['start_height'] < 1 or request['end_height'] < 1:
            return {'error': {'message': '%s: Minimum height is 1 for %s' % ('address')}}, 400

        if request['start_height'] > request['end_height']:
            return {'error': {'message': '%s: start_height cannot be grater than end_height' % ('address')}}, 400

        chaininfo = Chaininfo.get(self.chain)
        if not isinstance(chaininfo, Chaininfo):
            print("Error in AddressResource.resolve_request: wrong type for chaininfo", chaininfo)
            return {'error': {'message': '%s: Error getting chaininfo for chain %s' % ('address', self.chain)}}, 400

        if request['end_height'] > chaininfo.cached_blocks and (
                chaininfo.caching_first == chaininfo.caching_last
                or request['start_height'] < chaininfo.caching_first
                or request['end_height'] < chaininfo.caching_first
                or request['end_height'] > chaininfo.caching_last):
            return {'error': {'message': '%s: end_height (%s) cannot be grater than chaininfo.cached_blocks (%s). Currently caching from %s to %s in chain %s' % (
                'address',
                request['end_height'],
                chaininfo.cached_blocks,
                chaininfo.caching_first,
                chaininfo.caching_last,
                self.chain,
            )}}, 400

        json_result = {'expenditures': [], 'receipts': []}
        for height in xrange(request['start_height'], request['end_height'] + 1):
            address_block_result = {}
            try:
                address_block_result = self.search_by_address(height, request['addresses'])
            except Exception as e:
                print("Error in AddressResource.resolve_request:", type(e), e)
                return {'error': {'message': 'Error while searching by address'}}, 400
            if 'error' in address_block_result:
                return {'error': address_block_result['error']}, 400
            if 'expenditures' in address_block_result:
                json_result['expenditures'].extend(address_block_result['expenditures'])
            if 'receipts' in address_block_result:
                json_result['receipts'].extend(address_block_result['receipts'])

        return json_result, 200
