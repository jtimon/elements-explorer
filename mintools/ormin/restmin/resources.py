
from mintools import minql
from mintools import restmin

class ValidationError(Exception):
    def __init__(self, errors={}, *args, **kwargs):
        self.errors = errors
        super(ValidationError, self).__init__(*args, **kwargs)

class ModelResource(restmin.AuthResource):

    def __init__(self, model,
                 methods=['GET', 'POST', 'PUT'],
                 auth_func = None,
                 auth_methods=['POST', 'PUT'],
                 **kwargs):

        self.model = model

        super(ModelResource, self).__init__(methods=methods,
                                            auth_func=auth_func,
                                            auth_methods=auth_methods,
                                            **kwargs)

    def resolve_request(self, request):
        try:
            return super(ModelResource, self).resolve_request(request)
        except ValidationError as e:
            return {'errors': e.errors }, 400
        except minql.NotFoundError as e:
            return {'errors': e.errors }, 404
        except minql.AlreadyExistsError as e:
            return {'errors': e.errors }, 400

    def GET(self, json, params):
        if 'id' in params:
            return self.model.get(params['id']).json(True), 200

        models = self.model.search( params )
        return self.model.list_to_json(models), 200

    def POST(self, json, params):
        m = self.model(json)

        m.validate()
        if m.errors:
            raise ValidationError(m.errors)

        return m.insert().json(True), 201

    def PUT(self, json, params):
        m = self.model(json)

        m.validate()
        if m.errors:
            raise ValidationError(m.errors)

        m.id = params['id']
        return m.update().json(True), 200
