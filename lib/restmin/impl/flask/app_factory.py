# -*- coding: utf-8 -*-
# Copyright © 2012-2013, RokuSigma Inc. as an unpublished work.
# Proprietary property and company confidential: all rights reserved.
# See COPYRIGHT for details.

from flask import make_response, jsonify, abort, request, Response
from flask import Blueprint, current_app

import json

from .crossdomain import crossdomain

def api_generic(request, request_processor, app, resource):
    req = {}
    req['method'] = request.method
    req['resource'] = resource
    req['json'] = request.json
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
    elif request.method == 'GET':
        return jsonify({resource: response['json']}), response['status']
    return jsonify(response['json']), response['status']

def create_restmin_app(app_name, config_path, base_url, request_processor):
    from flask import Flask
    app = Flask(app_name)
    app.config.from_object(config_path)

    @app.route(base_url + '<string:resource>', methods = ['GET', 'POST', 'PUT'])
    @crossdomain(origin='*')
    def _api_generic(resource):
        return api_generic(request, request_processor, current_app, resource)

    @app.route(base_url + '<string:resource>', methods = ['OPTIONS'])
    @crossdomain(origin='*', headers='Content-Type, X-User, X-Token')
    def _options(self):
        return jsonify({'Allow' : 'GET,POST,PUT' }), 200

    return app
