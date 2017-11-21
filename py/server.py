
from flask import Blueprint, request, jsonify
import json

from lib.explorer.explorer_server import BetterNameResource
from lib.explorer.env_config import CONFIG, DB_CLIENT, AVAILABLE_CHAINS

import crossdomain
from settings import WEB_ALLOWED_CALLS

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
        return jsonify( {'error': {'message': 'Resource "%s" not supported.' % resource}} ), 400

    request_data = json.loads(request.data)

    json_result = BetterNameResource(DB_CLIENT, AVAILABLE_CHAINS[chain]['rpc'], chain, resource).resolve_request(request_data)

    if not json_result:
        return jsonify({'error': {'message': 'No result for %s.' % resource}}), 400
    if 'error' in json_result and json_result['error']:
        return jsonify({'error': json_result['error']}), 400
    return jsonify(json_result), 200

@api_blueprint.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options(chain, resource):
    return jsonify({'Allow' : 'GET,POST,PUT' }), 200
