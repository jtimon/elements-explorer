
from .model import Model 

class RepeteadModelError(BaseException):
    pass

class ModelNotFoundError(BaseException):
    pass

class Domain(object):

    def __init__(self, domain, *args, **kwargs):

        self.domain = {}
        for model in domain:
            self.add(model)

        super(Domain, self).__init__(*args, **kwargs)

    def add(self, model):
        print('add.model', model)
        assert issubclass(model, Model), 'ormin.Domain only works with ormin.Model'

        if model.get_name() in self.domain:
            raise RepeteadModelError
        self.domain.update({model.get_name(): model})

    def get(self, name):
        if name in self.domain:
            return self.domain[ name ]
        raise ModelNotFoundError

    def json_schema(self):
        schema = {}
        for model in self.domain.values():
            schema.update(model.json_schema())
        return schema
