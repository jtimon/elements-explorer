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
            if (cache['available_chains']) {
                return SrvUtil.GetKeys(cache['available_chains']);
            } else {
                return $http.get(BACKEND_URL + '/available_chains')
                    .then(function (response) {
                        cache['available_chains'] = response["data"]["available_chains"];
                        return SrvUtil.GetKeys(cache['available_chains']);
                    });
            }
        }

        srv.GetProperties = function() {
            return cache[selected_chain]['chaininfo'][selected_chain]['properties'];
        }
        
        srv.GetChainInfo = function() {
            var resource = 'chaininfo';
            SrvUtil.PreCache(cache, selected_chain, resource);
            if (cache[selected_chain][resource][selected_chain]) {
                return $q(function(resolve) {
                    resolve(cache[selected_chain][resource][selected_chain]);
                });
            } else {
                return $http.post(BACKEND_URL + '/' + resource, {'id': selected_chain, 'chain': selected_chain})
                    .then(SrvUtil.CacheElem(cache, selected_chain, resource, selected_chain));
            }
        }

        return srv;
    })
