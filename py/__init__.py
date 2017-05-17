
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

@frontend.route('/rpcexplorerrest', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest():
    rpcUrl = DEFAULT_DEAMONS_HOST + ':' + DEFAULT_DEAMONS_PORT
    rpcAuth = ('user1', 'password1')
    rpcHeaders = {'content-type': 'application/json'}
    requestData = json.loads(request.data)

    if 'method' in requestData and (not requestData['method'] in ALLOWED_CALLS):
        return jsonify( {'error': {'message': 'Method "%s" not supported.' % requestData['method']}} ), 200

    strRequestData = json.dumps(requestData)
    print(requestData, strRequestData)
    response = requests.request('post', rpcUrl, data=strRequestData, auth=rpcAuth, headers = rpcHeaders)
    # response.raise_for_status()
    return jsonify( response.json() ), 200

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
