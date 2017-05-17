
from flask import Blueprint, request, jsonify
import requests
import json

import crossdomain

DEFAULT_DEAMONS_HOST = 'http://127.0.0.1'
DEFAULT_DEAMONS_PORT = '7041'

frontend = Blueprint('frontend', __name__)

@frontend.route('/rpcexplorerrest', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def rpcexplorerrest():
    response = requests.request('post',
                                DEFAULT_DEAMONS_HOST + ':' + DEFAULT_DEAMONS_PORT, 
                                data=request.data,
                                auth=('user1', 'password1'), 
                                headers = {'content-type': 'application/json'})
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
