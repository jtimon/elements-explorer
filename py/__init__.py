
from flask import Blueprint, request, jsonify
import requests
import json

import crossdomain

frontend = Blueprint('frontend', __name__)

@frontend.route('/bitcoind', methods = ['POST'])
@crossdomain.crossdomain(origin='*')
def bitcoind():
    response = requests.request('post', 'http://127.0.0.1:7041', 
                                data=request.data,
                                auth=('user1', 'password1'), 
                                headers = {'content-type': 'application/json'})
    # response.raise_for_status()
    return jsonify( response.json() ), 200
    
@frontend.route('/bitcoind', methods = ['OPTIONS'])
@crossdomain.crossdomain(origin='*', headers='Content-Type')
def options():
    return jsonify({'Allow' : 'GET,POST,PUT' }), 200

from flask import Flask
app = Flask(__name__)

app.register_blueprint(frontend)

if __name__ == '__main__':
    app.debug = True
    app.run()
