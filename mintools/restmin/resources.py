
class Resource(object):

    def resolve_request(self, request):
        raise NotImplementedError

class FunctionResource(Resource):

    def __init__(self, function=None, 
                 **kwargs):

        self.function = function

        super(FunctionResource, self).__init__(**kwargs)

    def resolve_request(self, request):

        # if 'auth_form' in request:
        #     del request['auth_form']

        return self.function(**request)

class ClassResource(Resource):

    def __init__(self, instance=None, methods=None,
                 **kwargs):

        if instance:
            self.instance = instance
        else:
            self.instance = self
        if methods:
            self.methods = methods
        else:
            self.methods = []

        super(ClassResource, self).__init__(**kwargs)

    def resolve_request(self, request):

        if 'method' not in request:
            return {'errors': {'Error:': 'restmin.ClassResource: Missing parameter "method".'} }
        method = request['method']
        del request['method']
        if method not in self.methods:
            return {'errors': {'Error:': 'restmin.ClassResource: Unkown method "%s".' % method} }

        # self.function = getattr(self.instance, method)
        # return super(ClassResource, self).resolve_request(request)
        return getattr(self.instance, method)(**request)

class HttpResource(ClassResource):

    def resolve_request(self, request):

        if request['method'] not in self.methods:
            return {'errors': {'Error:': 'Unkown method "%s".' % method} }, 404

        return super(HttpResource, self).resolve_request(request)
