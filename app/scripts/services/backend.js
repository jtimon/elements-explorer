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
            function cache_callback(data) {
                cache[chain][resource][id] = data.data['result'];
            }
            return cache_callback;
        }

        srv.rpcCallProm = function(rpcMethod, vRpcParams) {
            return $http.post(BACKEND_URL + '/chain/' + SrvChain.get() + '/' + rpcMethod, vRpcParams);
        };

        srv.rpcCall = function(rpcMethod, vRpcParams, callback, errorCallback) {
            srv.rpcCallProm(rpcMethod, vRpcParams)
                .then(safeCallback(callback))
                .catch(safeCallback(errorCallback));
        };

        // Pre: CreateCacheForChainAndRsrc has been previously called
        function CacheSingleItem(chain, resource, id, callback, errorCallback)
        {
            function cache_callback(data) {
                safeCallback(callback)(data);
                cache[chain][resource][id] = data;
            }
            srv.rpcCall(resource, {'id': id}, cache_callback, errorCallback);
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

        srv.GetBlockStats = function(start, end, callback, errorCallback) {
            var chain = SrvChain.get();
            var resource = 'getblockstats';
            CreateCacheForChainAndRsrc(chain, resource);
            var promises = [];

            for (var i = start; i <= end; i++) {
                if (!cache[chain][resource][i]) {
                    promises.push(srv.rpcCallProm(resource, {"start": i, "end": i}).then(cache_callback_params(chain, resource, i)));
                }
            }

            function AccumulateStats(data){
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
                callback(formatted_data);
            }
            $q.all(promises)
                .then(AccumulateStats)
                .catch(errorCallback);
        };

        return srv;
    })
