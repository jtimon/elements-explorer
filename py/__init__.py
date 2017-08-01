
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

frontend = Blueprint('frontend', __name__)

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "bitcoin": "bitcoin:8332",
    "elementsregtest": "elements:7041",
    "testnet3": "bitcoin:18332",
    "regtest": "bitcoin:18332",
    # "elements": "elements:9042",
}

@frontend.route('/rpcexplorerrest/available_chains', methods = ['GET'])
@crossdomain.crossdomain(origin='*')
def available_chains():
    return jsonify( {'available_chains': AVAILABLE_CHAINS.keys()} ), 200

def rpcCall(chain, requestData):
    requestData["jsonrpc"] = "1.0"
    requestData["id"] = "curltest"
    rpcAuth = ('user1', 'password1')
    rpcHeaders = {'content-type': 'application/json'}
    response = requests.request('post', 'http://' + AVAILABLE_CHAINS[chain], data=json.dumps(requestData), auth=rpcAuth, headers=rpcHeaders)
    # response.raise_for_status()
    return response.json()

@frontend.route('/rpcexplorerrest', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest():
    requestData = json.loads(request.data)

    if 'method' in requestData and (not requestData['method'] in ALLOWED_CALLS):
        return jsonify( {'error': {'message': 'Method "%s" not supported.' % requestData['method']}} ), 400

    if not 'chain' in requestData or not requestData['chain']:
        return jsonify({"error": {"message": "No chain specified."} }), 400
    chain = requestData["chain"]
    del requestData["chain"]
    if not chain in AVAILABLE_CHAINS:
        return jsonify( {'error': {'message': 'Chain "%s" not supported.' % chain}} ), 400

    json_result = rpcCall(chain, requestData)
    if 'error' in json_result and json_result['error']:
        return jsonify({'error': json_result['error']}), 400
    return jsonify(json_result), 200

@frontend.route('/rpcexplorerrest', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options():
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
    app.run(host='0.0.0.0')
