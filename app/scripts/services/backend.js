'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($q, $http, SrvChain, SrvUtil) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var cache = {};

        srv.RpcCall = function(rpcMethod, vRpcParams) {
            return $http.post(BACKEND_URL + '/chain/' + SrvChain.get() + '/' + rpcMethod, vRpcParams);
        };

        srv.get = function(resource, id) {
            var chain = SrvChain.get();
            SrvUtil.PreCache(cache, chain, resource);

            var retPromise;
            if (cache[chain][resource][id]) {
                retPromise = $q(function(resolve) {
                    resolve(cache[chain][resource][id]);
                });
            } else {
                retPromise = srv.RpcCall(resource, {'id': id})
                    .then(SrvUtil.CacheElem(cache, chain, resource, id))
            }
            return retPromise;
        };

        var MAX_PARALLEL_IT = 7; // (8) Number of parallel calls - 1 

        srv.GetBlockStats = function(start, end) {
            var chain = SrvChain.get();
            var resource = 'blockstats';
            SrvUtil.PreCache(cache, chain, resource);

            var promises = [];
            var it_parallel = 0;

            for (var i = start; i <= end; i++) {
                if (!cache[chain][resource][i]) {
                    function task(index) {
                        return function task_func() {
                            return srv.RpcCall(resource, {"id": index});
                        }
                    }
                    if (!promises[it_parallel]) {
                        promises[it_parallel] = task(i)();
                    } else {
                        promises[it_parallel] = promises[it_parallel].then(task(i));
                    }
                    promises[it_parallel] = promises[it_parallel].then(SrvUtil.CacheElem(cache, chain, resource, i));
                    if (it_parallel == MAX_PARALLEL_IT) {
                        it_parallel = 0;
                    } else {
                        ++it_parallel;
                    }
                }
            }

            function AccumulateStats(){
                var formatted_data = {};
                for (var it_height = start; it_height <= end; it_height++) {
                    var result = cache[chain][resource][it_height];
                    if (result) {
                        for (var key in result) {
                            if (result.hasOwnProperty(key)) {
                                if (!formatted_data[key]) {
                                    formatted_data[key] = [];
                                }
                                formatted_data[key].push(result[key]);
                            }
                        }
                    }
                }
                return formatted_data;
            }

            var retPromise;
            if (promises.length > 0) {
                retPromise = $q.all(promises).then(AccumulateStats);
            } else {
                retPromise = $q(function(resolve) {
                    resolve(AccumulateStats());
                });
            }
            return retPromise;
        };

        return srv;
    })
