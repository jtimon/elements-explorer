'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($q, $http, SrvChain) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var cache = {};

        function safeCallback(callback) {
            return function(data) {
                if (callback){
                    callback(data);
                }
            };
        }

        function CreateCacheForChainAndRsrc(chain, resource) {
            if (!cache[chain]) {
                cache[chain] = {};
            }
            if (!cache[chain][resource]) {
                cache[chain][resource] = {};
            }
        }

        function cache_callback_params(chain, resource, id) {
            function cache_callback(response) {
                cache[chain][resource][id] = response.data['result'];
            }
            return cache_callback;
        }

        srv.RpcCall = function(rpcMethod, vRpcParams) {
            return $http.post(BACKEND_URL + '/chain/' + SrvChain.get() + '/' + rpcMethod, vRpcParams);
        };

        // Pre: CreateCacheForChainAndRsrc has been previously called
        function CacheSingleItem(chain, resource, id, callback, errorCallback)
        {
            function cache_callback(response) {
                var result = response.data['result'];
                safeCallback(callback)(result);
                cache[chain][resource][id] = result;
            }
            srv.RpcCall(resource, {'id': id})
                .then(cache_callback)
                .catch(errorCallback);
        }

        srv.get = function(resource, id, callback, errorCallback) {
            var chain = SrvChain.get();
            CreateCacheForChainAndRsrc(chain, resource);
            if (!cache[chain][resource][id]) {
                CacheSingleItem(chain, resource, id, callback, errorCallback);
            } else {
                safeCallback(callback)(cache[chain][resource][id]);
            }
        };

        var MAX_PARALLEL_IT = 3; // Number of parallel calls - 1

        srv.GetBlockStats = function(start, end) {
            var chain = SrvChain.get();
            var resource = 'blockstats';
            CreateCacheForChainAndRsrc(chain, resource);
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
                    promises[it_parallel] = promises[it_parallel].then(cache_callback_params(chain, resource, i));
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
                                formatted_data[key].push(result[key][0]);
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
