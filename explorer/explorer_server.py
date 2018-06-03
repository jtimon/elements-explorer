
import json
import datetime

from mintools import minql, restmin, ormin

from explorer import model
from explorer import models
from explorer.env_config import DB_CLIENT, AVAILABLE_CHAINS, DEFAULT_CHAIN

def GetBlockByHeight(rpccaller, height):
    try:
        block_by_height = model.Block.search({'height': height})
    except minql.NotFoundError:
        block_by_height = []
    except Exception as e:
        print("Error in GetBlockByHeight:", type(e), e)
        return {'error': {'message': 'Error getting block from db by height %s' % height}}
    if len(block_by_height) > 1:
        return {'error': {'message': 'More than one block cached for height %s' % height}}
    if len(block_by_height) == 1:
        return block_by_height[0]

    blockhash = rpccaller.RpcCall('getblockhash', {'height': height})
    if 'error' in blockhash:
        return blockhash
    block = model.Block.get(blockhash)
    if isinstance(block, dict) and 'error' in block:
        return block
    elif not isinstance(block, model.Block):
        print('Error in GetBlockByHeight: wrong type for block', blockhash, block)
        return {'error': {'message': 'Error getting block %s (by height %s)' % (blockhash, height)}}
    return block

class UnknownChainError(BaseException):
    pass

class ChainResource(restmin.resources.Resource):

    def update_chain(self, request_data):
        self.chain = None
        if request_data and 'chain' in request_data:
            self.chain = request_data['chain']
            del request_data['chain']
        else:
            self.chain = DEFAULT_CHAIN
        if not self.chain in AVAILABLE_CHAINS:
            raise UnknownChainError

        ormin.Form.set_namespace(self.chain)
        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']
        models.RpcCachedModel.set_rpccaller(self.rpccaller)

        return request_data


class RpcCallerResource(ChainResource):
    def __init__(self, resource, limit_array_result=0):
        self.resource = resource
        self.limit_array_result = limit_array_result

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        json_result = self.rpccaller.RpcCall(self.resource, req['json'])
        if 'error' in json_result and json_result['error']:
            return {'error': json_result['error']}, 400

        if self.limit_array_result:
            return {'result': json_result[:self.limit_array_result]}, 200
        else:
            return {'result': json_result}, 200


class MempoolStatsResource(ChainResource):
    ALLOWED_MEMPOOL_STATS_TYPES = ['count', 'fee', 'vsize']

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'hours_ago' in request:
            return {'error': {'message': 'No hours_ago specified to get %s in request %s' % ('mempoolstats', request)}}, 400
        if not 'stat_type' in request:
            return {'error': {'message': 'No stat_type specified to get %s in request %s' % ('mempoolstats', request)}}, 400
        if request['stat_type'] not in self.ALLOWED_MEMPOOL_STATS_TYPES:
            return {'error': {'message':
                              'No stat_type=%s not allowed in request %s, allowed values %s' % (
                                  'mempoolstats', request, self.ALLOWED_MEMPOOL_STATS_TYPES)}}, 400

        seconds_ago = request['hours_ago'] * 60 * 60
        min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
        try:
            db_result = {}
            db_result = models.stats.Mempoolstats.search({'stat_type': request['stat_type'], 'time': {'ge': min_epoch}})
        except minql.NotFoundError:
            return {'error': {'message': 'No mempoolstats in the last %s hours.' % hours_ago}}, 400
        except Exception as e:
            print("Error in MempoolStatsResource.resolve_request:", type(e), e)
            return {'error': {'message': 'Error getting %s from db.' % ('mempoolstats')}}, 400

        if not db_result:
            return {'error': {'message': 'No result db for %s type %s' % ('mempoolstats', request['stat_type'])}}, 400

        json_result = {}
        for mempoolstats in db_result:
            json_result[mempoolstats.time] = json.loads(mempoolstats.blob)

        return json_result, 200


class BlockheightResource(ChainResource):

    def __init__(self, *args, **kwargs):
        super(BlockheightResource, self).__init__(*args, **kwargs)

        self.resource = 'blockheight'

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'id' in request:
            return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}, 400

        response = GetBlockByHeight(self.rpccaller, request['id'])
        if isinstance(response, dict) and 'error' in response:
            return {'error': response['error']}, 400

        response = response.json()
        if isinstance(response, dict) and 'errors' in response:
            return {'error': response['errors']}, 400

        return response, 200


class GetByIdResource(ChainResource):

    def __init__(self, resource, model, chain_required_properties=[], uses_blob=False, *args, **kwargs):
        super(GetByIdResource, self).__init__(*args, **kwargs)

        self.resource = resource
        self.model = model
        self.chain_required_properties = chain_required_properties
        self.uses_blob = uses_blob

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        for required_property in self.chain_required_properties:
            if not AVAILABLE_CHAINS[self.chain]['properties'][required_property]:
                return {'error': {'message': 'API resource %s is not supported by chain %s' % (self.resource, self.chain)}}, 400

        request = req['json']
        if not 'id' in request:
            return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}, 400

        try:
            db_result = self.model.get(request['id'])
        except Exception as e:
            print("Error in GetByIdResource.resolve_request (resource=%s):" % self.resource, type(e), e)
            return {'error': {'message': 'Error getting %s from db by id %s.' % (self.resource, request['id'])}}, 400

        if not db_result:
            return {'error': {'message': 'No result db for %s %s.' % (self.resource, request['id'])}}, 400
        elif isinstance(db_result, dict) and 'error' in db_result:
            if isinstance(db_result['error'], dict) and 'message' in db_result['error']:
                return {'error': {'message': db_result['error']['message']}}, 400
            else:
                return {'error': {'message': db_result['error']}}, 400

        if not (isinstance(db_result, dict) or isinstance(db_result, ormin.Model)):
            print('ERROR: getting %s. db_result:' % self.resource, db_result)
            return {'error': {'message': 'Error getting %s.' % self.resource}}, 400

        if self.uses_blob:
            if isinstance(db_result, dict):
                json_result = db_result
            elif isinstance(db_result, ormin.Model):
                json_result = db_result.json()

            if not 'blob' in json_result:
                print('ERROR: No blob result db for %s. db_result:' % self.resource, db_result)
                return {'error': {'message': 'No blob result db for %s.' % self.resource}}, 400
            response = json.loads(json_result['blob'])
        else:
            if isinstance(db_result, dict):
                response = db_result
            elif isinstance(db_result, ormin.Model):
                response = db_result.json()

        if 'error' in response:
            return {'error': response['error']}, 400
        if 'errors' in response:
            return {'error': response['errors']}, 400
        return response, 200


class AddressResource(ChainResource):

    def search_by_address(self, height, addresses):

        block = GetBlockByHeight(self.rpccaller, height)
        if isinstance(block, dict) and 'error' in block:
            return block

        receipts = []
        expenditures = []
        tx_ids = json.loads(block.tx)
        for txid in tx_ids:
            orm_tx = models.transaction.Tx.get(txid)
            if isinstance(orm_tx, dict) and 'error' in orm_tx:
                return orm_tx
            elif not isinstance(orm_tx, models.transaction.Tx):
                print('Error in AddressResource.search_by_address: wrong type for tx', txid, orm_tx)
                return {'error': {'message': 'Error getting tx %s (address)' % txid}}
            tx = json.loads(orm_tx.blob)

            for output in tx['vout']:
                for address in addresses:
                    if 'addresses' in output['scriptPubKey'] and address in output['scriptPubKey']['addresses']:
                        receipts.append({'output': output, 'txid': txid, 'height': block.height})

            for tx_input in tx['vin']:
                if 'txid' in tx_input and 'vout' in tx_input:
                    orm_tx_in = models.transaction.Tx.get(tx_input['txid'])
                    if isinstance(orm_tx_in, dict) and 'error' in orm_tx_in:
                        return orm_tx_in
                    elif not isinstance(orm_tx_in, models.transaction.Tx):
                        print('Error in AddressResource.search_by_address_ascendant: wrong type for tx', tx_input['txid'], orm_tx_in)
                        return {'error': {'message': 'Error getting tx %s (address)' % tx_input['txid']}}
                    tx_in = json.loads(orm_tx_in.blob)
                    print('tx_in', tx_in, "tx_input['vout']", tx_input['vout'])
                    output = tx_in['vout'][ tx_input['vout'] ]
                    for address in addresses:
                        if 'addresses' in output['scriptPubKey'] and address in output['scriptPubKey']['addresses']:
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


def get_available_chains(**kwargs):
    available_chains = {}
    for k, v in AVAILABLE_CHAINS.iteritems():
        available_chains[k] = v['properties']
    return available_chains, 200

class ExplorerApiDomain(restmin.Domain):

    def __init__(self, domain, db_client, *args, **kwargs):

        ormin.Model.set_db( db_client )

        super(ExplorerApiDomain, self).__init__(domain, *args, **kwargs)

API_DOMAIN = ExplorerApiDomain({
    'available_chains': restmin.resources.FunctionResource(get_available_chains),
    # never cached, always hits the node
    'getmempoolentry': RpcCallerResource('getmempoolentry'),
    'getrawmempool': RpcCallerResource('getrawmempool', limit_array_result=4),
    # Data from db, independent from reorgs
    'mempoolstats': MempoolStatsResource(),
    # currently goes throught the whole block
    'address': AddressResource(),
    # cached in server and gui
    'block': GetByIdResource('block', model.Block),
    'blockheight': BlockheightResource(),
    'tx': GetByIdResource('tx', models.transaction.Tx, uses_blob=True),
    'blockstats': GetByIdResource('blockstats', models.stats.Blockstats, ['stats_support']),
    # TODO handle reorgs from gui (ie use websockets)
    'chaininfo': GetByIdResource('chaininfo', models.Chaininfo),
}, DB_CLIENT)
