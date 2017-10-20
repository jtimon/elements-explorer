
from flask import Blueprint, request, jsonify, send_from_directory
import requests
import json

import crossdomain
from settings import *

frontend = Blueprint('frontend', __name__)
API_URL = '/api/v0'

@frontend.route(API_URL + '/available_chains', methods = ['GET'])
@crossdomain.crossdomain(origin='*')
def available_chains():
    return jsonify( {'available_chains': AVAILABLE_CHAINS.keys()} ), 200

def RpcCall(chain, method, params):
    if not method in RPC_ALLOWED_CALLS:
        return {'error': {'message': 'Method "%s" not supported.' % method}}

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
    # TODO remove special case for getrawmempool and getblockhash
    if ('result' in json_result and method != 'getrawmempool' and method != 'getblockhash'):
        json_result = json_result['result']
    return json_result

def RpcFromId(chain, resource, req_id):
    if resource == 'blockstats':
        rpc_result = RpcCall(chain, 'getblockstats', {'start': req_id, 'end': req_id})
    elif resource == 'block':
        rpc_result = RpcCall(chain, 'getblock', {'blockhash': req_id})
    elif resource == 'tx':
        rpc_result = RpcCall(chain, 'getrawtransaction', {'txid': req_id, 'verbose': 1})

    return rpc_result

def GetBlobById(chain, resource, req_id):
    try:
        db_result = DB_CLIENT.get(chain + "_" + resource, req_id)
        json_result = json.loads(db_result['blob'])
    except:
        json_result = RpcFromId(chain, resource, req_id)
        db_cache = {}
        db_cache['id'] = req_id
        db_cache['blob'] = json.dumps(json_result)
        DB_CLIENT.put(chain + "_" + resource, db_cache)

    return json_result

def GetById(chain, resource, req_id):
    json_result = GetBlobById(chain, resource, req_id)
    return json_result

@frontend.route(API_URL + '/chain/<string:chain>/<string:resource>', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest(chain, resource):
    if not chain in AVAILABLE_CHAINS:
        return jsonify( {'error': {'message': 'Chain "%s" not supported.' % chain}} ), 400

    if not resource in WEB_ALLOWED_CALLS:
        return jsonify( {'error': {'message': 'Resource "%s" not supported.' % method}} ), 400

    request_data = json.loads(request.data)
    if resource in RESOURCES_FOR_GET_BY_ID:
        if not 'id' in request_data:
            return jsonify({'error': {'message': 'No id specified to get %s by id.' % resource}}), 400

        json_result = GetById(chain, resource, request_data['id'])
    else:
        json_result = RpcCall(chain, resource, request_data)

    if not json_result:
        return jsonify({'error': {'message': 'No result for %s.' % resource}}), 400
    if 'error' in json_result and json_result['error']:
        return jsonify({'error': json_result['error']}), 400
    return jsonify(json_result), 200

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

