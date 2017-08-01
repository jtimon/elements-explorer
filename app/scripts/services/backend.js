'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($http) {

        var BACKEND_URL = 'http://127.0.0.1:5000/rpcexplorerrest';
        var srv = {};
        var cache = {};

        function safeCallback(callback) {
            return function(data) {
                if (callback){
                    callback(data);
                }
            };
        }

        srv.GetAvailableChains = function(callback, errorCallback) {
            $http.get(BACKEND_URL + '/available_chains')
                .then(safeCallback(callback), safeCallback(errorCallback));
        }

        srv.rpcCall = function(chain, rpcMethod, vRpcParams, callback, errorCallback) {
            var requestData = {
                "chain": chain,
                "method": rpcMethod,
                "params": vRpcParams,
            };
            $http.post(BACKEND_URL, requestData)
                .then(safeCallback(callback), safeCallback(errorCallback));
        };

        srv.get = function(chain, resource, id, callback, errorCallback) {
            if (!cache[chain] || !cache[chain][resource] || !cache[chain][resource][id]) {
                var params = [id];
                if (resource == 'getrawtransaction') {
                    params = [id, 1]; // verbose for tx
                }
                function cache_callback(data) {
                    if (!cache[chain]) {
                        cache[chain] = {};
                    }
                    if (!cache[chain][resource]) {
                        cache[chain][resource] = {};
                    }
                    cache[chain][resource][id] = data;
                    safeCallback(callback)(data);
                }
                srv.rpcCall(chain, resource, params, cache_callback, errorCallback);
            } else {
                safeCallback(callback)(cache[chain][resource][id]);
            }
        };

        return srv;
    })
