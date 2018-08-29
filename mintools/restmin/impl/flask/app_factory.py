# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

from flask import Blueprint, current_app
from flask import Flask
from flask import make_response, jsonify, abort, request, Response

from .crossdomain import crossdomain

def api_generic(request, request_processor, app, resource, auth_required=False):
    req = {}
    req['method'] = request.method
    req['resource'] = resource
    req['json'] = request.json
    if request.environ.get('HTTP_X_REAL_IP'):
        req['ip'] = request.environ.get('HTTP_X_REAL_IP')
    else:
        req['ip'] = request.remote_addr
    req['params'] = {}

    params = {}
    for k, v in request.args.iteritems():
        try:
            in_json = json.loads(v)
            if type(in_json) is dict:
                params[k] = in_json
            else:
                params[k] = str(in_json)
        except:
            params[k] = v
    req['params'] = params

    if auth_required:
        auth_form = {}
        if request.authorization:
            auth_form['user'] = request.authorization.username
            auth_form['password'] = request.authorization.password
        else:
            if 'X-User' in request.headers:
                auth_form['user'] = request.headers['X-User']
            if 'X-Token' in request.headers:
                auth_form['token'] = request.headers['X-Token']
        req['auth_form'] = auth_form

    response = request_processor(app, req)
    if 'errors' in response:
        return jsonify({'errors': response['errors']}), 400
    if 'error' in response:
        return jsonify({'error': response['error']}), 400
    elif request.method == 'GET':
        return jsonify({resource: response['json']}), response['status']
    return jsonify(response['json']), response['status']

def create_restmin_app(app_name, config_path, base_url, request_processor, auth_required=False):
    app = Flask(app_name)
    if config_path:
        app.config.from_object(config_path)

    @app.route(base_url + '<string:resource>', methods = ['GET', 'POST', 'PUT'])
    @crossdomain(origin='*')
    def _api_generic(resource):
        return api_generic(request, request_processor, current_app, resource, auth_required)

    @app.route(base_url + '<string:resource>', methods = ['OPTIONS'])
    @crossdomain(origin='*', headers='Content-Type, X-User, X-Token')
    def _options(self):
        return jsonify({'Allow' : 'GET,POST,PUT' }), 200

    return app
