
from .number import NumericField

MAX_INT = 2147483647

class IntField(NumericField):

    def __init__(self, **kwargs):
        if not 'lt' in kwargs or kwargs['lt'] == None or kwargs['lt'] > MAX_INT:
            kwargs['lt'] = MAX_INT
        super(IntField, self).__init__(field_type='int', **kwargs)

    def _clean_value(self, value):
        return int(value)

class BigIntField(NumericField):

    def __init__(self, **kwargs):
        super(BigIntField, self).__init__(field_type='bigint', **kwargs)

    def _clean_value(self, value):
        return int(value)
