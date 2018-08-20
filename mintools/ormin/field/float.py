# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from .number import NumericField

class FloatField(NumericField):

    def __init__(self, **kwargs):
        super(FloatField, self).__init__(field_type='float', **kwargs)

    def _clean_value(self, value):
        return float(value)
