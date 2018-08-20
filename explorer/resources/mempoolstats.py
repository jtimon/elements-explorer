# Copyright (c) 2017-2018 The Elements Explorer developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import datetime

from mintools.minql import NotFoundError

from explorer.models.stats import Mempoolstats

from .chain import UnknownChainError, ChainResource

class MempoolStatsResource(ChainResource):
    ALLOWED_MEMPOOL_STATS_TYPES = ['count', 'fee', 'vsize']

    def resolve_request(self, req):
        try:
            req['json'] = self.update_chain(req['json'])
        except UnknownChainError:
            return {'error': {'message': 'Chain "%s" not supported.' % self.chain}}, 400

        request = req['json']
        if not 'hours_ago' in request:
            return {'error': {'message': 'No hours_ago specified to get %s in request %s' % ('mempoolstats', request)}}, 400
        if not 'stat_type' in request:
            return {'error': {'message': 'No stat_type specified to get %s in request %s' % ('mempoolstats', request)}}, 400
        if request['stat_type'] not in self.ALLOWED_MEMPOOL_STATS_TYPES:
            return {'error': {'message':
                              'No stat_type=%s not allowed in request %s, allowed values %s' % (
                                  'mempoolstats', request, self.ALLOWED_MEMPOOL_STATS_TYPES)}}, 400

        seconds_ago = request['hours_ago'] * 60 * 60
        min_epoch = int((datetime.datetime.now() - datetime.timedelta(seconds=seconds_ago)).strftime('%s'))
        try:
            db_result = {}
            db_result = Mempoolstats.search({'stat_type': request['stat_type'], 'time': {'ge': min_epoch}})
        except NotFoundError:
            return {'error': {'message': 'No mempoolstats in the last %s hours.' % hours_ago}}, 400
        except Exception as e:
            print("Error in MempoolStatsResource.resolve_request:", type(e), e)
            return {'error': {'message': 'Error getting %s from db.' % ('mempoolstats')}}, 400

        if not db_result:
            return {'error': {'message': 'No result db for %s type %s' % ('mempoolstats', request['stat_type'])}}, 400

        json_result = {}
        for mempoolstats in db_result:
            json_result[mempoolstats.time] = mempoolstats.json(full=True)['blob']

        return json_result, 200
