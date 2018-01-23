
from ..field import StringField, FieldError

class Relation(StringField):

    def __init__(self, model, cascade=False, *args, **kwargs):

        self._model = model
        self._cascade = cascade

        super(Relation, self).__init__(*args, **kwargs)

    def save(self, model, name):
        raise NotImplementedError
