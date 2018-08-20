# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import ormin

class LoginForm(ormin.Form):
    username = ormin.StringField()
    password = ormin.StringField()
