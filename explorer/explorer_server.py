
import json
import datetime

from mintools import minql, restmin, ormin

from explorer import model
from explorer.env_config import DB_CLIENT, AVAILABLE_CHAINS, DEFAULT_CHAIN

def CacheBlockStatsResult(rpccaller, req_id):
    json_result = rpccaller.RpcCall('getblockstats', {'height': req_id})
    if 'error' in json_result:
        return json_result

    blockstats = model.Blockstats()
    blockstats.height = json_result['height']
    blockstats.blob = json.dumps(json_result)
    blockstats.id = req_id
    blockstats.save()
    if blockstats.errors:
        return {'error': {'message': json.dumps(blockstats.errors)}}
    return json_result

def GetByIdBase(rpccaller, resource, req_id):
    try:
        db_result = None
        if resource == 'chaininfo':
            db_result = model.Chaininfo.get(req_id)
            if isinstance(db_result, dict):
                return db_result
            elif isinstance(db_result, ormin.Model):
                return db_result.json()
            else:
                print('ERROR: getting chaininfo. db_result:', db_result)
                return {'error': {'message': 'Error getting chaininfo.'}}

        elif resource == 'block':
            db_result = model.Block.get(req_id)
        elif resource == 'blockstats':
            db_result = model.Blockstats.get(req_id)
        elif resource == 'tx':
            db_result = model.Tx.get(req_id)
        else:
            raise NotImplementedError
    except minql.NotFoundError:
        if resource == 'blockstats':
            return CacheBlockStatsResult(rpccaller, req_id)
        else:
            return {'error': {'message': 'Error caching %s from db by id %s. (unkown resource)' % (resource, req_id)}}
    except Exception as e:
        print("Error in GetByIdBase:", type(e), e)
        return {'error': {'message': 'Error getting %s from db by id %s.' % (resource, req_id)}}

    if not db_result:
        return {'error': {'message': 'No result db for %s.' % resource}}

    if isinstance(db_result, dict):
        if 'error' in db_result:
            return db_result
        elif not 'blob' in db_result:
            print('ERROR: No blob result db for %s. db_result:' % resource, db_result)
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = db_result
    elif isinstance(db_result, ormin.Model):
        json_result = db_result.json()
    else:
        print('ERROR: getting %s. db_result:' % resource, db_result)
        return {'error': {'message': 'Error getting %s.' % resource}}

    return json.loads(json_result['blob'])

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
        return json.loads(block_by_height[0].blob)

    blockhash = rpccaller.RpcCall('getblockhash', {'height': height})
    if 'error' in blockhash:
        return blockhash
    return GetByIdBase(rpccaller, 'block', blockhash)

def GetById(rpccaller, resource, req_id):
    if resource == 'blockheight':
        return GetBlockByHeight(rpccaller, req_id)

    return GetByIdBase(rpccaller, resource, req_id)

class UnknownChainError(BaseException):
    pass

class ChainResource(restmin.resources.Resource):

    def update_chain(self, request_data):
        self.chain = None
        if 'chain' in request_data:
            self.chain = request_data['chain']
            del request_data['chain']
        else:
            self.chain = DEFAULT_CHAIN
        if not self.chain in AVAILABLE_CHAINS:
            raise UnknownChainError

        ormin.Form.set_namespace(self.chain)
        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']
        model.RpcCachedModel.set_rpccaller(self.rpccaller)

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

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'hours_ago' in request:
            return {'error': {'message': 'No hours_ago specified to get %s in request %s' % ('mempoolstats', request)}}, 400

        seconds_ago = request['hours_ago'] * 60 * 60
        min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
        try:
            db_result = model.Mempoolstats.search({'time': {'ge': min_epoch}})
        except minql.NotFoundError:
            return {'error': {'message': 'No mempoolstats in the last %s hours.' % hours_ago}}, 400
        except Exception as e:
            print("Error in MempoolStatsResource.resolve_request:", type(e), e)
            return {'error': {'message': 'Error getting %s from db.' % ('mempoolstats')}}, 400

        if not db_result:
            return {'error': {'message': 'No result db for %s.' % 'mempoolstats'}}, 400

        json_result = {}
        for db_elem in db_result:
            json_result[db_elem.id] = json.loads(db_elem.blob)

        return json_result, 200


class GetByIdResource(ChainResource):

    def __init__(self, resource, chain_required_properties=[], *args, **kwargs):
        super(GetByIdResource, self).__init__(*args, **kwargs)

        self.resource = resource
        self.chain_required_properties = chain_required_properties

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

        response = GetById(self.rpccaller, self.resource, request['id'])
        if 'error' in response:
            return {'error': response['error']}, 400
        return response, 200


class AddressResource(ChainResource):

    def search_by_address(self, height, addresses):

        block = GetBlockByHeight(self.rpccaller, height)
        if 'error' in block:
            return block

        receipts = []
        expenditures = []
        for txid in block['tx']:
            tx = GetById(self.rpccaller, 'tx', txid)
            if 'error' in tx:
                print('ERROR: error getting tx %s (address)' % txid)
                return tx

            for output in tx['vout']:
                for address in addresses:
                    if 'addresses' in output['scriptPubKey'] and address in output['scriptPubKey']['addresses']:
                        receipts.append({'output': output, 'txid': txid, 'height': block['height']})

            for tx_input in tx['vin']:
                if 'txid' in tx_input and 'vout' in tx_input:
                    tx_in = GetById(self.rpccaller, 'tx', tx_input['txid'])
                    if 'error' in tx_in:
                        print('ERROR: error getting tx %s (address)' % tx_input['txid'])
                        return tx_in
                    output = tx_in['vout'][ tx_input['vout'] ]
                    for address in addresses:
                        if 'addresses' in output['scriptPubKey'] and address in output['scriptPubKey']['addresses']:
                            expenditures.append({'input': tx_input, 'prev_output': output, 'txid': tx['txid'], 'height': block['height']})

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
    'block': GetByIdResource('block'),
    'blockheight': GetByIdResource('blockheight'),
    'tx': GetByIdResource('tx'),
    'blockstats': GetByIdResource('blockstats', ['stats_support']),
    # TODO handle reorgs from gui (ie use websockets)
    'chaininfo': GetByIdResource('chaininfo'),
}, DB_CLIENT)
