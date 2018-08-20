# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from ..field import StringField, FieldError

class Relation(StringField):

    def __init__(self, model, cascade=False, *args, **kwargs):

        self._model = model
        self._cascade = cascade

        super(Relation, self).__init__(*args, **kwargs)

    def save(self, model, name):
        raise NotImplementedError
