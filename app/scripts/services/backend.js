'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($http, SrvChain) {

        var BACKEND_URL = 'http://127.0.0.1:5000/api/v0';
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

        srv.rpcCall = function(rpcMethod, vRpcParams, callback, errorCallback) {
            $http.post(BACKEND_URL + '/chain/' + SrvChain.get() + '/' + rpcMethod, vRpcParams)
                .then(safeCallback(callback), safeCallback(errorCallback));
        };

        srv.get = function(resource, id, callback, errorCallback) {
            var chain = SrvChain.get();
            if (!cache[chain] || !cache[chain][resource] || !cache[chain][resource][id]) {
                var params = {};
                if (resource == 'getblock') {
                    params = {"blockhash": id};
                } else if (resource == 'getrawtransaction') {
                    params = {
                        "txid": id,
                        "verbose": 1,
                    };
                } else {
                    var error_msg = 'Resource ' + resource + ' not supported for SrvBackend.get';
                    safeCallback(errorCallback)({'data': {'error': {'message': error_msg}}});
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
                srv.rpcCall(resource, params, cache_callback, errorCallback);
            } else {
                safeCallback(callback)(cache[chain][resource][id]);
            }
        };

        return srv;
    })
