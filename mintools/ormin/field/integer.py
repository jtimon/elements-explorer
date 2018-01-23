
from .number import NumericField

class IntField(NumericField):

    def __init__(self, **kwargs):
        super(IntField, self).__init__(field_type='int', **kwargs)

    def _clean_value(self, value):
        return int(value)
