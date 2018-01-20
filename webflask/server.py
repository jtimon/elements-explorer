
from flask import Blueprint, request, jsonify

from lib.explorer.explorer_server import explorer_request_processor

import crossdomain

api_blueprint = Blueprint('api_blueprint', __name__)
API_URL = '/api/v0'

@api_blueprint.route(API_URL + '/<string:resource>', methods = ['POST', 'GET'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest(resource):
    response = explorer_request_processor(request, resource)
    status = 400
    if 'status' in response:
        status = response['status']
        del response['status']
    return jsonify(response), status

@api_blueprint.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options(chain, resource):
    return jsonify({'Allow' : 'GET,POST,PUT' }), 200
