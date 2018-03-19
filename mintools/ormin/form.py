
from field import Field, FieldError

class ValidatorError(BaseException):
    def __init__(self, msg={}, *args, **kwargs):
        self.msg = msg
        super(ValidatorError, self).__init__(*args, **kwargs)

class Form(object):

    def __init__(self, json=None, *args, **kwargs):

        self.errors = {}

        self.__class__._init_fields()

        for attr_name, attr in self.__class__._fields.iteritems():
            setattr(self, attr_name, None)

        if json:
            for attr_name, attr in self.__class__._fields.iteritems():
                attr.from_json(self, attr_name, json)

        super(Form, self).__init__(*args, **kwargs)

    @classmethod
    def _init_fields(cls):
        if not hasattr(cls, '_fields'):

            cls._fields = {}
            attrs_dir = filter(lambda o:o not in dir(Form), dir(cls))
            for attr_name in attrs_dir:
                attr = getattr(cls, attr_name)
                if isinstance(attr, Field):
                    cls._fields[attr_name] = attr
                    attr.add_property(cls, attr_name)

    @classmethod
    def set_namespace(cls, value):
        cls._namespace = value

    @classmethod
    def get_name(cls):
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        if hasattr(cls, '_namespace') and cls._namespace:
            return cls._namespace + '_' + s2
        else:
            return s2

    @classmethod
    def json_schema(cls):
        cls._init_fields()
        json = {}
        for k, f in cls._fields.iteritems():
            json.update( f.json_schema(k) )
        return {cls.get_name(): json}

    def json(self, full=True):
        json = {}
        for k, f in self.__class__._fields.iteritems():
            json.update( f.json(self, k, full) )

        if hasattr(self, 'id') and self.id:
            json['id'] = self.id 
        if self.errors:
            json['errors'] = self.errors
        return json

    def validate(self):
        self.errors = {}
        for k, f in self.__class__._fields.iteritems():
            try:
                f.validate(self, k)
            except FieldError as e:
                self.errors[ k ] = e.msg

        return self.errors

    @classmethod
    def parse_json_list(cls, json_list):
        model_list = []
        for json in json_list:
            model_list.append(cls(json))
        return model_list

    @classmethod
    def list_to_json(cls, model_list):
        json_list = []
        for m in model_list:
            json_list.append(m.json(False))
        return json_list

    def __str__(self):
        return str(self.json(True))
