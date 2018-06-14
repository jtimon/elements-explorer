
from . import FieldError

class Field(object):

    def __init__(self, field_type, required=True, index=False,
                 unique=False,
                 *args, **kwargs):

        self.field_type = field_type
        self.required = required
        self.index = index
        self.unique = unique

        super(Field, self).__init__(*args, **kwargs)

    def json_schema(self, name):
        return {
            name: {
                'type': self.field_type,
                'required': self.required,
                'index': self.index,
            }
        }

    def json(self, model, name, full=False):
        value = getattr(model, '_' + name)
        if value == None and not self.required:
            return {}
        return { name: value }

    def from_json(self, model, name, json):
        if name in json:
            setattr(model, '_' + name, json[ name ])

    def _clean_value(self, value):
        raise NotImplementedError

    def clean_value(self, name, value):
        if value is None:
            if self.required:
                raise FieldError('"%s" is required' % name)
            else:
                return None
        try:
            value = self._clean_value(value)
        except Exception:
            # pass
            raise FieldError('Field "%s" is of type %s but value %s is not' % 
                             (name, self.field_type, value))
        return value

    def validate(self, model, name):

        value = getattr(model, '_' + name)
        value = self.clean_value(name, value)
        setattr(model, '_' + name, value)

        if self.unique and value is not None:
            if model.search({name: value}):
                raise FieldError('"%s" already exists' % value)

        return value

    def add_property(self, model_class, name):

        _fget = lambda _model, _name: getattr(_model, '_' + _name)
        _fset = lambda _model, _name, value: setattr(_model, '_' + _name, value)
        
        # Use static name
        fget = lambda _model: _fget(_model, name)
        fset = lambda _model, value: _fset(_model, name, value)

        # add property to model
        setattr(model_class, name, property(fget, fset))
