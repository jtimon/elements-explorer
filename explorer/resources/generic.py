
import json

from mintools import ormin
from explorer.env_config import AVAILABLE_CHAINS

from .chain import UnknownChainError, ChainResource

class GetByIdResource(ChainResource):

    def __init__(self, resource, model, chain_required_properties=[], uses_blob=False, *args, **kwargs):
        super(GetByIdResource, self).__init__(*args, **kwargs)

        self.resource = resource
        self.model = model
        self.chain_required_properties = chain_required_properties
        self.uses_blob = uses_blob

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        for required_property in self.chain_required_properties:
            if not AVAILABLE_CHAINS[self.chain]['properties'][required_property]:
                return {'error': {'message': 'API resource %s is not supported by chain %s' % (self.resource, self.chain)}}, 400

        request = req['json']
        if not 'id' in request:
            return {'error': {'message': 'No id specified to get %s by id.' % self.resource}}, 400

        try:
            db_result = self.model.get(request['id'])
        except Exception as e:
            print("Error in GetByIdResource.resolve_request (resource=%s):" % self.resource, type(e), e)
            return {'error': {'message': 'Error getting %s from db by id %s.' % (self.resource, request['id'])}}, 400

        if not db_result:
            return {'error': {'message': 'No result db for %s %s.' % (self.resource, request['id'])}}, 400
        elif isinstance(db_result, dict) and 'error' in db_result:
            if isinstance(db_result['error'], dict) and 'message' in db_result['error']:
                return {'error': {'message': db_result['error']['message']}}, 400
            else:
                return {'error': {'message': db_result['error']}}, 400

        if not (isinstance(db_result, dict) or isinstance(db_result, ormin.Model)):
            print('ERROR: getting %s. db_result:' % self.resource, db_result)
            return {'error': {'message': 'Error getting %s.' % self.resource}}, 400

        if self.uses_blob:
            if isinstance(db_result, dict):
                json_result = db_result
            elif isinstance(db_result, ormin.Model):
                json_result = db_result.json()

            if not 'blob' in json_result:
                print('ERROR: No blob result db for %s. db_result:' % self.resource, db_result)
                return {'error': {'message': 'No blob result db for %s.' % self.resource}}, 400
            response = json.loads(json_result['blob'])
        else:
            if isinstance(db_result, dict):
                response = db_result
            elif isinstance(db_result, ormin.Model):
                response = db_result.json()

        if 'error' in response:
            return {'error': response['error']}, 400
        if 'errors' in response:
            return {'error': response['errors']}, 400
        return response, 200
