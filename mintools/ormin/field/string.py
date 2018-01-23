
from .base import Field

class StringField(Field):

    def __init__(self, min_len=None, max_len=None,
                 min_len_msg=None, max_len_msg=None,
                 **kwargs):

        self.min_len, self.max_len = min_len, max_len
        self.min_len_msg, self.max_len_msg = min_len_msg, max_len_msg

        super(StringField, self).__init__(field_type='string', **kwargs)

    def _clean_value(self, value):
        return str(value)

    def validate(self, model, name):
        value = super(StringField, self).validate(model, name)
        if value is None:
            return None

        if self.min_len is not None and len(value) < self.min_len:
            raise FieldError(self.min_len_msg or '"%s" must be longer than %s' % (name, self.min_len))
        if self.max_len is not None and len(value) < self.max_len:
            raise FieldError(self.max_len_msg or '"%s" must be shorter than %s' % (name, self.max_len))

        return value
