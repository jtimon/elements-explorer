
from flask import Blueprint, request, jsonify, send_from_directory
import requests
import json
import os

import crossdomain

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

ALLOWED_CALLS = [
    "getblockchaininfo",
    "getblock",
    "getblockhash",
    "getrawtransaction",
    "getblockstats",
]

RESOURCES_FOR_GET_BY_ID = [
    'block',
    'tx',
]

frontend = Blueprint('frontend', __name__)

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "bitcoin": "bitcoin:8332",
    "testnet3": "bitcoin:18332",
    "elementsregtest": "elements:7041",
    # "elements": "elements:9042",
}

API_URL = '/api/v0'

@frontend.route(API_URL + '/available_chains', methods = ['GET'])
@crossdomain.crossdomain(origin='*')
def available_chains():
    return jsonify( {'available_chains': AVAILABLE_CHAINS.keys()} ), 200

def rpcCall(chain, method, params):
    if not method in ALLOWED_CALLS:
        return jsonify( {'error': {'message': 'Method "%s" not supported.' % method}} ), 400

    requestData = {
        'method': method,
        'params': params,
        'jsonrpc': '2.0',
        'id': chain + '_' + method,
    }
    rpcAuth = ('user1', 'password1')
    rpcHeaders = {'content-type': 'application/json'}
    response = requests.request('post', 'http://' + AVAILABLE_CHAINS[chain], data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
    # response.raise_for_status()
    json_result = response.json()
    if 'error' in json_result and json_result['error']:
        return jsonify({'error': json_result['error']}), 400
    return jsonify(json_result), 200

@frontend.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest(chain, resource):
    if not chain in AVAILABLE_CHAINS:
        return jsonify( {'error': {'message': 'Chain "%s" not supported.' % chain}} ), 400

    request_data = json.loads(request.data)
    if not 'id' in request_data and resource in RESOURCES_FOR_GET_BY_ID:
        return jsonify({'error': {'message': 'No id specified to get %s by id.' % resource}}), 400

    rpc_request_data = {}
    if resource == 'block':
        method = 'getblock'
        rpc_request_data['blockhash'] = request_data['id']
    elif resource == 'tx':
        method = 'getrawtransaction'
        rpc_request_data['txid'] = request_data['id']
        rpc_request_data['verbose'] = 1
    else:
        method = resource
        rpc_request_data.update(request_data)
    return rpcCall(chain, method, rpc_request_data)

@frontend.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options(chain, resource):
    return jsonify({'Allow' : 'GET,POST,PUT' }), 200

from flask import Flask
app = Flask(__name__)

app.register_blueprint(frontend)

app.static_url_path = ''
app.static_folder   = CLIENT_DIRECTORY
app.add_url_rule('/<path:filename>',
    endpoint  = 'static',
    view_func = app.send_static_file)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(CLIENT_DIRECTORY, filename)

if __name__ == '__main__':
    app.debug = True
    app.run()
