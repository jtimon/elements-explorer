

class FieldError(BaseException):
    def __init__(self, msg={}, *args, **kwargs):
        self.msg = msg
        super(FieldError, self).__init__(*args, **kwargs)

from .base import Field
from .number import NumericField
from .string import StringField, TextField
from .float import FloatField
from .integer import IntField
