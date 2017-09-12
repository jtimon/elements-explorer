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
            if (end - start > 100) {
                errorCallback("SrvBackend.GetBlockStats scales poorly and thus only allows 100 blocks at a time.");
            }
            srv.rpcCall("getblockstats", {"start": start, "end": end}, callback, errorCallback);
        };

        return srv;
    })
