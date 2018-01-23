
from relation import Relation, FieldError

class ManyToManyField(Relation):

    def __init__(self, model, *args, **kwargs):

        self._model = model

        super(ManyToManyField, self).__init__(model=model, field_type='string', index=True, *args, **kwargs)

    def json_schema(self, name):
        return {}

    def json(self, model, name, full=False):
        pass

    def from_json(self, model, name, json):
        pass

    def validate(self, model, name):
        pass

    def save(self, model, name):
        pass

    def add_property(self, model_class, name):
        pass
