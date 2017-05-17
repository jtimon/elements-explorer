
from flask import Blueprint, request, jsonify
import requests
import json

import crossdomain

DEFAULT_DEAMONS_HOST = 'http://127.0.0.1'
DEFAULT_DEAMONS_PORT = '7041'

ALLOWED_CALLS = [
    "getblockchaininfo",
    "getblock",
    "getblockhash",
    "getrawtransaction",
]

frontend = Blueprint('frontend', __name__)

# TODO duplicated default ports, adapt to elements (with CA),
# uncomment, clean up
AVAILABLE_CHAINS = {
    "main": "8332",
    # "testnet3": "18332",
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

if __name__ == '__main__':
    app.debug = True
    app.run()
