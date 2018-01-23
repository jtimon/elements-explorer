
from .number import NumericField

class FloatField(NumericField):

    def __init__(self, **kwargs):
        super(FloatField, self).__init__(field_type='float', **kwargs)

    def _clean_value(self, value):
        return float(value)
