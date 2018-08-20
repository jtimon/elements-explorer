# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from mintools import minql

from relation import Relation, FieldError

class ManyToOneField(Relation):

    def __init__(self, model, *args, **kwargs):
        super(ManyToOneField, self).__init__(model=model, index=True, *args, **kwargs)

    def json_schema(self, name):
        return {
            name + '_id': {
                'type': self.field_type,
                'required': self.required,
                'index': self.index,
            }
        }

    def json(self, model, name, full=False):
        if full and self._cascade:
            model_attr = getattr(model, '_' + name)
            if model_attr:
                return { name: model_attr.json(full) }
        return { name + '_id': getattr(model, name + '_id') }

    def from_json(self, model, name, json):
        if name in json:
            value = json[ name ]
            if isinstance(value, dict):
                new = self._model(value)
                setattr(model, name, new)
            else:
                raise ValueError
        elif name + '_id' in json:
            setattr(model, name + '_id', json[ name + '_id' ])
        else:
            setattr(model, name + '_id', None)

    def validate(self, model, name):
        model_attr = getattr(model, '_' + name)

        if model_attr:

            if model_attr.id:
                setattr(model, '_' + name + '_id', model_attr.id)
            if self._cascade:
                model_attr.validate()
            setattr(model, '_' + name, model_attr)

        elif self.required and not self._cascade:
            super(ManyToOneField, self).validate(model, name + '_id')

        return model_attr

    def save(self, model, name):
        if not self._cascade:
            return

        model_attr = getattr(model, '_' + name)
        if model_attr:
            model_attr.save()
            setattr(model, '_' + name + '_id', model_attr.id)

    def add_property(self, model_class, name):

        def _fk_fget(_model, _name):
            return getattr(_model, '_' + _name + '_id')

        def _fk_fset(_model, _name, value):
            setattr(_model, '_' + _name + '_id', value)
            id_attr = getattr(_model, '_' + _name + '_id')
            model_attr = getattr(_model, '_' + _name)
            if model_attr and model_attr.id != id_attr:
                setattr(_model, '_' + _name, None)

        def _fget(_model, _name, related_model):
            id_attr = getattr(_model, '_' + _name + '_id')
            model_attr = getattr(_model, '_' + _name)
            if not model_attr and id_attr:
                model_attr = related_model.get(id_attr)
                setattr(_model, '_' + _name, model_attr)

            return model_attr

        def _fset(_model, _name, value, related_model):
            if value:
                assert isinstance(value, related_model), 'Expected a %s model.' % related_model.get_name()

                if value.id:
                    setattr(_model, '_' + _name + '_id', value.id)
                else:
                    setattr(_model, '_' + _name + '_id', None)
            else:
                setattr(_model, '_' + _name + '_id', None)
            setattr(_model, '_' + _name, value)

        # Use static params
        fget = lambda _model: _fget(_model, name, self._model)
        fset = lambda _model, value: _fset(_model, name, value, self._model)

        fk_fget = lambda _model: _fk_fget(_model, name)
        fk_fset = lambda _model, value: _fk_fset(_model, name, value)

        # add properties to model
        setattr(model_class, name, property(fget, fset))
        setattr(model_class, name + '_id', property(fk_fget, fk_fset))
