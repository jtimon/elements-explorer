
import json

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
                        receipts.append({'output': output, 'txid': txid, 'height': block.height})

            for tx_input in tx['vin']:
                if 'txid' in tx_input and 'vout' in tx_input:
                    orm_tx_in = Tx.get(tx_input['txid'])
                    if isinstance(orm_tx_in, dict) and 'error' in orm_tx_in:
                        return orm_tx_in
                    elif not isinstance(orm_tx_in, Tx):
                        print('Error in AddressResource.search_by_address_ascendant: wrong type for tx', tx_input['txid'], orm_tx_in)
                        return {'error': {'message': 'Error getting tx %s (address)' % tx_input['txid']}}
                    tx_in = orm_tx_in.json()
                    print('tx_in', tx_in, "tx_input['vout']", tx_input['vout'])
                    output = tx_in['vout'][ tx_input['vout'] ]
                    for address in addresses:
                        if 'scriptpubkey_addresses' in output and address in output['scriptpubkey_addresses']:
                            expenditures.append({'input': tx_input, 'prev_output': output, 'txid': tx['txid'], 'height': block.height})

        return {'expenditures': expenditures, 'receipts': receipts}

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'addresses' in request:
            return {'error': {'message': 'No addresses specified for %s with request %s' % ('address', request)}}, 400
        if not 'start_height' in request:
            return {'error': {'message': 'No start_height specified for %s with request %s' % ('address', request)}}, 400
        if not 'end_height' in request:
            return {'error': {'message': 'No end_height specified for %s with request %s' % ('address', request)}}, 400

        if request['start_height'] < 1 or request['end_height'] < 1:
            return {'error': {'message': 'Minimum height is 1 for %s' % ('address')}}, 400

        json_result = {'expenditures': [], 'receipts': []}
        for height in xrange(request['start_height'], request['end_height'] + 1):
            address_block_result = self.search_by_address(height, request['addresses'])
            if 'error' in address_block_result:
                return {'error': address_block_result['error']}, 400
            if 'expenditures' in address_block_result:
                json_result['expenditures'].extend(address_block_result['expenditures'])
            if 'receipts' in address_block_result:
                json_result['receipts'].extend(address_block_result['receipts'])

        return json_result, 200
