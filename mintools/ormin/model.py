
import json

from mintools import minql

from . import form
from . import field
from . import relations

class Model(form.Form):

    id = field.StringField(required=False)

    def __init__(self, *args, **kwargs):

        self.__class__._init_relations()

        super(Model, self).__init__(*args, **kwargs)

    @classmethod
    def _init_relations(cls):
        if not hasattr(cls, '_fields'):
            cls._init_fields()
        if not hasattr(cls, '_relations'):
            cls._relations = {}
            for k, f in cls._fields.iteritems():
                if isinstance(f, relations.Relation):
                    cls._relations[k] = f

    @classmethod
    def json_schema(cls):
        cls._init_relations()
        json_dict = {}
        for k, f in cls._fields.iteritems():
            if k != 'id':
                json_dict.update( f.json_schema(k) )
        return {cls.get_name(): json_dict}

    @classmethod
    def db(cls):
        return cls._minql_client

    @classmethod
    def set_db(cls, value):
        cls._minql_client = value

    # TODO replace with uuid
    def new_id(self):
        import random
        while True:
            id = str(random.randrange(1,10000))
            try:
                obj = self.get(id)
            except minql.NotFoundError:
                break
        self.id = id

    @classmethod
    def get(cls, id):
        obj = cls.db().get(cls.get_name(), id)
        return cls(obj)

    @classmethod
    def search(cls, criteria={}):
        for k, c in criteria.iteritems():
            if c is None:
                raise Exception(criteria)
        objs = cls.db().search(cls.get_name(), criteria)
        return cls.parse_json_list(objs)

    @classmethod
    def all(cls):
        return cls.search()

    @classmethod
    def delete(cls, criteria={}):
        for k, c in criteria.iteritems():
            if c is None:
                raise Exception(criteria)
        cls.db().delete(cls.get_name(), criteria)

    def save(self):
        self.validate()
        if self.errors:
            return self
        for k, r in self.__class__._relations.iteritems():
            if isinstance(r, relations.ManyToOneField):
                r.save(self, k)

        result = self.put()
        for k, r in self.__class__._relations.iteritems():
            if isinstance(r, relations.OneToManyField):
                r.save(self, k)
        return result

    def insert(self):
        if not hasattr(self, 'id'):
            self.new_id()
        obj = self.db().insert(self.get_name(), self.json(False))
        print('Inserted...', self.get_name(), self.id)
        return self.__class__(obj)

    def update(self):
        obj = self.db().update(self.get_name(), self.json(False))
        print('Updated...', self.get_name(), self.id)
        return self.__class__(obj)

    def put(self):
        if not hasattr(self, 'id'):
            self.new_id()
        obj = self.db().put(self.get_name(), self.json(False))
        print('Put...', self.get_name(), self.id)
        return self.__class__(obj)


class CachedModel(Model):

    @classmethod
    def truth_src_get(cls, req_id):
        raise NotImplementedError

    @classmethod
    def get(cls, id):
        try:
            return super(CachedModel, cls).get(id)
        except minql.NotFoundError:
            obj = cls.truth_src_get(id)
            if isinstance(obj, dict):
                if 'error' in obj:
                    return obj
                return cls(obj)
            elif isinstance(obj, form.Form):
                if obj.errors:
                    return {'error': {'message': json.dumps(obj.errors)}}
                return obj
