# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import minql
from mintools import restmin

from .models import User

def orminAuth(auth):
    if 'user' not in auth or not auth['user']:
        raise restmin.AuthorizationError()

    # first try to authenticate by token
    if 'token' in auth:
        user = User.verify_token(auth['token'])
        if not user or user.id != auth['user']:
            raise restmin.AuthorizationError()
    # try to authenticate with username/password
    elif 'password' in auth:
        try:
            user = User.get(auth['user'])
        except minql.NotFoundError:
            raise restmin.AuthorizationError()
        if not user.verify_password(auth['password']):
            raise restmin.AuthorizationError()
    else:
        raise restmin.AuthorizationError()

    return user

def userAAA(auth):
    return User.get('aaa')
