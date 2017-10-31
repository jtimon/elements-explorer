
from flask import Blueprint, request, jsonify
import json

from lib.explorer.explorer_server import GetById

import crossdomain
from settings import *

api_blueprint = Blueprint('api_blueprint', __name__)
API_URL = '/api/v0'

@api_blueprint.route(API_URL + '/available_chains', methods = ['GET'])
@crossdomain.crossdomain(origin='*')
def available_chains():
    return jsonify( {'available_chains': AVAILABLE_CHAINS.keys()} ), 200

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
