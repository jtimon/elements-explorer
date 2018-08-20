# Copyright (c) 2012-2018 The Mintools developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import pprint

from .resources import Resource

class RepeteadResourceError(BaseException):
    pass

class ResourceNotFoundError(BaseException):
    pass

class Domain(Resource):

    def __init__(self, domain, *args, **kwargs):

        self.domain = {}
        for k, v in domain.iteritems():
            self.add(k, v)

        super(Domain, self).__init__(*args, **kwargs)

    def _init(self):
        pass

    def add(self, name, resource):

        if not isinstance(resource, Resource):
            raise TypeError('restmin.Domain only works with restmin.Resource')

        if name in self.domain:
            raise RepeteadResourceError
        self.domain.update({name: resource})

    def resolve_request(self, request):

        print('Request:')
        pprint.pprint(request)

        response = {}

        resource_name = request['resource']
        del request['resource']
        if resource_name in self.domain:
            resource = self.domain[ resource_name ]
            # response['json']  = resource.resolve_request(request)
            # print(response)
            response['json'], response['status'] = resource.resolve_request(request)
        else:
            response['errors'] = {'Error:':'Unkown resource %s.' % resource_name}
            response['status'] = 404

        if 'json' in response and 'errors' in response['json']:
            response['errors'] = response['json']['errors']
            del response['json']['errors']
        if 'status' not in response and 'errors' in response:
            response['status'] = 400
        print('Response:')
        pprint.pprint(response)
        return response
