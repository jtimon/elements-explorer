# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import minql
from mintools import restmin

from ..resources import ModelResource, ValidationError
from .models import User, Register
from .forms import LoginForm
from .auth import orminAuth

class RegisterResource(restmin.AuthResource):

    def __init__(self, methods=['POST'], **kwargs):
        super(RegisterResource, self).__init__(methods=methods, **kwargs)

    def POST(self, json, params):
        m = Register(json)

        m.validate()
        if m.errors:
            raise ValidationError(m.errors)

        return m.insert().json(False), 201

class LoginResource(restmin.AuthResource):

    def __init__(self,
                 methods=['POST', 'GET'],
                 auth_func = orminAuth,
                 auth_methods=['GET'],
                 **kwargs):

        super(LoginResource, self).__init__(
                                            methods=methods,
                                            auth_func=auth_func,
                                            auth_methods=auth_methods,
                                            **kwargs)

    def POST(self, json, params):
        m = LoginForm(json)

        m.validate()
        if m.errors:
            raise ValidationError(m.errors)

        try:
            user = User.get(m.username)
        except minql.NotFoundError:
            raise restmin.LoginError()
        if not user.verify_password(m.password):
            raise restmin.LoginError()

        return user.json(full=True), 200

    def GET(self, json, params, user):
        # This will generate a new token
        return user.json(full=True), 200
