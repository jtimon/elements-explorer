'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($http, SrvChain) {

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

        srv.GetAvailableChains = function(callback, errorCallback) {
            $http.get(BACKEND_URL + '/available_chains')
                .then(safeCallback(callback), safeCallback(errorCallback));
        }

        srv.rpcCall = function(rpcMethod, vRpcParams, callback, errorCallback) {
            $http.post(BACKEND_URL + '/chain/' + SrvChain.get() + '/' + rpcMethod, vRpcParams)
                .then(safeCallback(callback), safeCallback(errorCallback));
        };

        srv.get = function(resource, id, callback, errorCallback) {
            var chain = SrvChain.get();
            CreateCacheForChainAndRsrc(chain, resource);
            if (!cache[chain][resource][id]) {
                function cache_callback(data) {
                    cache[chain][resource][id] = data;
                    safeCallback(callback)(data);
                }
                srv.rpcCall(resource, {'id': id}, cache_callback, errorCallback);
            } else {
                safeCallback(callback)(cache[chain][resource][id]);
            }
        };

        return srv;
    })
