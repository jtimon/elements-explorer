'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvBackend', function SrvBackend($http) {

        var BACKEND_URL = 'http://127.0.0.1:5000/rpcexplorerrest';
        var srv = {};

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
                "jsonrpc": "1.0",
                "id": "curltest",
            };
            $http.post(BACKEND_URL, requestData)
                .then(safeCallback(callback), safeCallback(errorCallback));
        };

        return srv;
    })
