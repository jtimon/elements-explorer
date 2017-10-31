
from flask import Blueprint, request, jsonify
import json

import crossdomain
from settings import *

api_blueprint = Blueprint('api_blueprint', __name__)
API_URL = '/api/v0'

@api_blueprint.route(API_URL + '/available_chains', methods = ['GET'])
@crossdomain.crossdomain(origin='*')
def available_chains():
    return jsonify( {'available_chains': AVAILABLE_CHAINS.keys()} ), 200

def RpcFromId(rpccaller, resource, req_id):
    if resource == 'blockstats':
        rpc_result = rpccaller.RpcCall('getblockstats', {'height': req_id})
    elif resource == 'block':
        rpc_result = rpccaller.RpcCall('getblock', {'blockhash': req_id})
    elif resource == 'tx':
        rpc_result = rpccaller.RpcCall('getrawtransaction', {'txid': req_id, 'verbose': 1})

    return rpc_result

def GetById(db_client, rpccaller, chain, resource, req_id):
    try:
        db_result = db_client.get(chain + "_" + resource, req_id)
        if not db_result:
            return {'error': {'message': 'No result db for %s.' % resource}}
        if not 'blob' in db_result:
            return {'error': {'message': 'No blob result db for %s.' % resource}}
        json_result = json.loads(db_result['blob'])
    except:
        json_result = RpcFromId(rpccaller, resource, req_id)
        if not json_result:
            return {'error': {'message': 'No rpc result for %s.' % resource}}
        db_cache = {}
        db_cache['id'] = req_id
        db_cache['blob'] = json.dumps(json_result)
        db_client.put(chain + "_" + resource, db_cache)

    return json_result

@api_blueprint.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest(chain, resource):
    if not chain in AVAILABLE_CHAINS:
        return jsonify( {'error': {'message': 'Chain "%s" not supported.' % chain}} ), 400

    if not resource in WEB_ALLOWED_CALLS:
        return jsonify( {'error': {'message': 'Resource "%s" not supported.' % method}} ), 400

    request_data = json.loads(request.data)
    rpccaller = AVAILABLE_CHAINS[chain]
    if resource in RESOURCES_FOR_GET_BY_ID:
        if not 'id' in request_data:
            return jsonify({'error': {'message': 'No id specified to get %s by id.' % resource}}), 400

        json_result = GetById(DB_CLIENT, rpccaller, chain, resource, request_data['id'])
    else:
        json_result = rpccaller.RpcCall(resource, request_data)

    if not json_result:
        return jsonify({'error': {'message': 'No result for %s.' % resource}}), 400
    if 'error' in json_result and json_result['error']:
        return jsonify({'error': json_result['error']}), 400
    return jsonify(json_result), 200

@api_blueprint.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options(chain, resource):
    return jsonify({'Allow' : 'GET,POST,PUT' }), 200
