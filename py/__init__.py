
from flask import Blueprint, request, jsonify, send_from_directory
import requests
import json
import os

import crossdomain

CLIENT_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'app')

DEFAULT_DEAMONS_HOST = 'http://127.0.0.1'
DEFAULT_DEAMONS_PORT = '7041'

ALLOWED_CALLS = [
    "getblockchaininfo",
    "getblock",
    "getblockhash",
    "getrawtransaction",
    "getperblockstats",
]

frontend = Blueprint('frontend', __name__)

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "main": "8332",
    "testnet3": "18332",
    # "regtest": "18332",
    # "elements": "9042",
    # "elementsregtest": "7041",
    "betatestnet3": "9041",
    "betaregtest": "7041",
    "liquid": "10098",
}

def urlForChain(chain):
    return DEFAULT_DEAMONS_HOST + ":" + AVAILABLE_CHAINS[chain]

def rpcCall(rpcUrl, requestData, rpcAuth, rpcHeaders):
    print(rpcUrl, requestData, rpcAuth, rpcHeaders) # TODO move to logs
    response = requests.request('post', rpcUrl, data=requestData, auth=rpcAuth, headers=rpcHeaders)
    # response.raise_for_status()
    return jsonify( response.json() ), 200

@frontend.route('/rpcexplorerrest', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest():
    rpcAuth = ('user1', 'password1')
    rpcHeaders = {'content-type': 'application/json'}
    requestData = json.loads(request.data)

    if 'method' in requestData and (not requestData['method'] in ALLOWED_CALLS):
        return jsonify( {'error': {'message': 'Method "%s" not supported.' % requestData['method']}} ), 200

    if not "chain" in requestData:
        return jsonify({"error": {"message": "No chain specified."} }), 200
    chain = requestData["chain"]
    del requestData["chain"]
    if not chain in AVAILABLE_CHAINS:
        return jsonify( {'error': {'message': 'Chain "%s" not supported.' % chain}} ), 200

    strRequestData = json.dumps(requestData)
    return rpcCall(urlForChain(chain), strRequestData, rpcAuth, rpcHeaders)

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
    app.run()
