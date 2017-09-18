'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($q, $http, $rootScope, SrvUtil) {

        var BACKEND_URL = '/api/v0';
        var srv = {};

        var selected_chain = "bitcoin";
        var cache = {};

        srv.set = function(_selected_chain) {
            selected_chain = _selected_chain;
            $rootScope.selected_chain = selected_chain;
        }

        srv.get = function() {
            return selected_chain;
        }

        srv.GetAvailableChains = function() {
            return $http.get(BACKEND_URL + '/available_chains')
                .then(function (response) {
                    return response["data"]["available_chains"]
                });
        }

        srv.GetChainInfo = function() {
            var resource = 'getblockchaininfo';
            SrvUtil.PreCache(cache, selected_chain, resource);
            if (cache[selected_chain][resource][selected_chain]) {
                return $q(function(resolve) {
                    resolve(cache[selected_chain][resource][selected_chain]);
                });
            } else {
                return $http.post(BACKEND_URL + '/chain/' + selected_chain + '/' + resource, {})
                    .then(SrvUtil.CacheElem(cache, selected_chain, resource, selected_chain));
            }
        }

        return srv;
    })
