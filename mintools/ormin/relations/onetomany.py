
from relation import Relation, FieldError
from manytoone import ManyToOneField

class OneToManyField(Relation):

    def __init__(self, model, index_field, cascade=True, *args, **kwargs):

        self._index_field = index_field

        super(OneToManyField, self).__init__(model=model, cascade=cascade, *args, **kwargs)

    def json_schema(self, name):
        return {}

    def json(self, model, name, full=False):
        if full:
            json = []
            models = getattr(model, '_' + name)
            if models:
                for m in models:
                    json.append(m.json(full and self._cascade))
            return { name: json }
        else:
            return {}

    def from_json(self, model, name, json):
        if name in json:
            values = json[ name ]
            if isinstance(values, list):
                models = []
                for value in values:
                    if isinstance(value, dict):
                        models.append(self._model(value))
                    else:
                        raise ValueError
                setattr(model, name, models)
            else:
                raise ValueError

    def validate(self, model, name):
        models = getattr(model, '_' + name)
        if models and self._cascade:
            for m in models:
                # If the parent doesn't have id, set a dummy key temporarily to avoid the error
                if model.id:
                    setattr(m, model.get_name() + '_id', model.id)
                else:
                    setattr(m, model.get_name() + '_id', 'dummy')
                m.validate()
                if not model.id:
                    setattr(m, model.get_name() + '_id', None)
                if m.errors:
                    raise FieldError(m.errors)

    def save(self, model, name):
        if not self._cascade:
            return

        models = getattr(model, '_' + name)
        if models:
            for m in models:
                setattr(m, model.get_name() + '_id', model.id)
                m.save()

    def add_property(self, model_class, name):

        def _fget(_model, _name, related_model, index_field):
            model_attr = getattr(_model, '_' + _name)
            if not model_attr:
                model_attr = []
                if _model.id:
                    model_attr = related_model.search({index_field: _model.id})
                setattr(_model, '_' + _name, model_attr)
            return model_attr

        def _fset(_model, _name, values, related_model, index_field):
            if values:
                assert isinstance(values, list), 'Expected a list of %s models.' % related_model.get_name()
                for value in values:
                    assert isinstance(value, related_model), (
                        'Expected a list of %s models.' % related_model.get_name())
                    setattr(value, index_field, _model.id)
                setattr(_model, '_' + _name, values)
            else:
                setattr(_model, '_' + _name, None)

        # Use static params
        fget = lambda _model: _fget(_model, name, self._model, self._index_field)
        fset = lambda _model, value: _fset(_model, name, value, self._model, self._index_field)

        # add property to model
        setattr(model_class, name, property(fget, fset))

        # Add ManyToOneField in the related Model
        if not hasattr(self._model, '_relations'):
            self._model._init_relations()

        related_name = model_class.get_name()
        related_field = ManyToOneField(model_class, required=False)
        self._model._fields[ related_name ] = related_field
        self._model._relations[ related_name ] = related_field
        related_field.add_property(self._model, related_name)
        setattr(self._model, '_' + related_name, None)
        setattr(self._model, '_' + related_name + '_id', None)
