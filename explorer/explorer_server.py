
import json
import datetime

from mintools import minql
from mintools import restmin

from explorer import model
from explorer.env_config import DB_CLIENT, AVAILABLE_CHAINS, DEFAULT_CHAIN

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        return rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        return rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        return rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})
    elif resource == 'chaininfo':
        return rpccaller.RpcCall('getblockchaininfo', {})
    else:
        raise NotImplementedError

def CacheChainInfoResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['bestblockhash'] = json_result['bestblockhash']
    db_cache['blocks'] = json_result['blocks']
    db_cache['mediantime'] = json_result['mediantime']
    db_client.put(chain + "_" + resource, db_cache)

def CacheTxResult(db_client, chain, resource, json_result, req_id):
    if 'blockhash' in json_result and json_result['blockhash']:
        # Don't cache mempool txs
        db_cache = {}
        db_cache['id'] = req_id
        db_cache['blockhash'] = json_result['blockhash']
        db_cache['blob'] = json.dumps(json_result)
        db_client.put(chain + "_" + resource, db_cache)

def CacheBlockResult(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['height'] = json_result['height']
    db_cache['blob'] = json.dumps(json_result)
    db_client.put(chain + "_" + resource, db_cache)

def CacheResultAsBlob(db_client, chain, resource, json_result, req_id):
    db_cache = {}
    db_cache['id'] = req_id
    db_cache['blob'] = json.dumps(json_result)
    db_client.put(chain + "_" + resource, db_cache)

def TryRpcAndCacheFromId(db_client, rpccaller, chain, resource, req_id):
    json_result = RpcFromId(rpccaller, resource, req_id)
    if 'error' in json_result:
        return json_result

    if resource == 'chaininfo':
        CacheChainInfoResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'block':
        CacheBlockResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'blockstats':
        CacheBlockResult(db_client, chain, resource, json_result, req_id)
    elif resource == 'tx':
        CacheTxResult(db_client, chain, resource, json_result, req_id)
    else:
        CacheResultAsBlob(db_client, chain, resource, json_result, req_id)

    return json_result

def GetByIdBase(db_client, rpccaller, chain, resource, req_id):
    try:
        db_result = None
        if resource == 'chaininfo':
            return model.Chaininfo.get(req_id, namespace=chain, minql_client=db_client).json()
        elif resource == 'block':
            db_result = model.Block.get(req_id, namespace=chain, minql_client=db_client).json()
        elif resource == 'blockstats':
            db_result = model.Blockstats.get(req_id, namespace=chain, minql_client=db_client).json()
        elif resource == 'tx':
            db_result = model.Tx.get(req_id, namespace=chain, minql_client=db_client).json()

        if not db_result:
            return {'error': {'message': 'No result db for %s.' % resource}}
        if not 'blob' in db_result:
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = json.loads(db_result['blob'])
    except minql.NotFoundError:
        json_result = TryRpcAndCacheFromId(db_client, rpccaller, chain, resource, req_id)
    except:
        return {'error': {'message': 'Error getting %s from db by id %s.' % (resource, req_id)}}
    return json_result

def GetBlockByHeight(db_client, rpccaller, chain, height):
    criteria = {'height': height}
    try:
        block_by_height = model.Block.search(criteria, namespace=chain, minql_client=db_client)
    except minql.NotFoundError:
        block_by_height = []
    except:
        return {'error': {'message': 'Error getting block from db by height %s' % height}}
    if len(block_by_height) > 1:
        return {'error': {'message': 'More than one block cached for height %s' % height}}
    if len(block_by_height) == 1:
        return json.loads(block_by_height[0].blob)

    blockhash = rpccaller.RpcCall('getblockhash', {'height': height})
    if 'error' in blockhash:
        return blockhash
    return GetByIdBase(db_client, rpccaller, chain, 'block', blockhash)

def GetById(db_client, rpccaller, chain, resource, req_id):
    if resource == 'blockheight':
        return GetBlockByHeight(db_client, rpccaller, chain, req_id)

    return GetByIdBase(db_client, rpccaller, chain, resource, req_id)

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

        self.rpccaller = AVAILABLE_CHAINS[self.chain]['rpc']

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


class ChainCachedResource(ChainResource):
    def __init__(self, db_client):
        self.db_client = db_client


class MempoolStatsResource(ChainCachedResource):

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'hours_ago' in request:
            return {'error': {'message': 'No hours_ago specified to get %s in request %s' % ('mempoolstats', request)}}, 400

        json_result = {}
        try:
            seconds_ago = request['hours_ago'] * 60 * 60
            min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
            db_result = self.db_client.search(self.chain + "_" + 'mempoolstats', {'time': {'ge': min_epoch}})
            if not db_result:
                return {'error': {'message': 'No result db for %s.' % 'mempoolstats'}}, 400
            for db_elem in db_result:
                json_result[db_elem['id']] = json.loads(db_elem['blob'])
        except:
            return {'error': {'message': 'Error getting %s from db.' % ('mempoolstats')}}, 400

        return json_result, 200


class GetByIdResource(ChainCachedResource):

    def __init__(self, db_client, resource, chain_required_properties=[]):
        super(GetByIdResource, self).__init__(db_client)

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

        return GetById(self.db_client, self.rpccaller, self.chain, self.resource, request['id']), 200


class AddressResource(ChainCachedResource):

    def search_by_address(self, height, addresses):

        block = GetBlockByHeight(self.db_client, self.rpccaller, self.chain, height)
        if 'error' in block:
            return block

        receipts = []
        expenditures = []
        for txid in block['tx']:
            tx = GetById(self.db_client, self.rpccaller, self.chain, 'tx', txid)
            if 'error' in tx:
                print('ERROR: error getting tx %s (address)' % txid)
                return tx

            for output in tx['vout']:
                for address in addresses:
                    if 'addresses' in output['scriptPubKey'] and address in output['scriptPubKey']['addresses']:
                        receipts.append({'output': output, 'txid': txid, 'height': block['height']})

            for tx_input in tx['vin']:
                if 'txid' in tx_input and 'vout' in tx_input:
                    tx_in = GetById(self.db_client, self.rpccaller, self.chain, 'tx', tx_input['txid'])
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


API_DOMAIN = restmin.domain.Domain({
    'available_chains': restmin.resources.FunctionResource(get_available_chains),
    # never cached, always hits the node
    'getmempoolentry': RpcCallerResource('getmempoolentry'),
    'getrawmempool': RpcCallerResource('getrawmempool', limit_array_result=4),
    # Data from db, independent from reorgs
    'mempoolstats': MempoolStatsResource(DB_CLIENT),
    # currently goes throught the whole block
    'address': AddressResource(DB_CLIENT),
    # cached in server and gui
    'block': GetByIdResource(DB_CLIENT, 'block'),
    'blockheight': GetByIdResource(DB_CLIENT, 'blockheight'),
    'tx': GetByIdResource(DB_CLIENT, 'tx'),
    'blockstats': GetByIdResource(DB_CLIENT, 'blockstats', ['stats_support']),
    # TODO handle reorgs from gui
    'chaininfo': GetByIdResource(DB_CLIENT, 'chaininfo'),
})
