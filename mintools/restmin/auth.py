# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from .resources import HttpResource

# TODO capture this ormin independent (also move)
class LoginError(BaseException):
    pass

class AuthorizationError(BaseException):
    pass

class AuthResource(HttpResource):

    def __init__(self, 
                 methods=None,
                 auth_func=None, 
                 auth_methods=None,
                 **kwargs):

        self.auth_func = auth_func
        self.auth_methods = auth_methods

        super(AuthResource, self).__init__(methods=methods, **kwargs)

    def resolve_request(self, request):
        try:
            if 'method' not in request:
                return {'errors': {'Error:': 'restmin.ClassResource: Missing parameter "method".'} }
            method = request['method']
            if self.auth_func and method in self.auth_methods:
                if not 'auth_form' in request:
                    return {'errors': {'Error:': 'Missing parameter "auth_form".'} }, 401
                user = self.auth_func(request['auth_form'])
                request['user'] = user
            if 'auth_form' in request:
                del request['auth_form']

            return super(AuthResource, self).resolve_request(request)
        except LoginError as e:
            return {'errors': {'Error:': 'Incorrect username or password.'} }, 401
        except AuthorizationError as e:
            return {'errors': {'Error:': 'Unauthorized access.'} }, 401
