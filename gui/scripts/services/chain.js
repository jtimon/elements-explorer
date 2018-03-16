'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($q, $http, $rootScope, $route, SrvUtil) {

        var BACKEND_URL = '/api/v0';
        var srv = {};

        var selected_chain = "bitcoin";
        var cache = {};

        function SetSelectedChain(_selected_chain)
        {
            // If it's not an avilable chain, try to see if it's a
            // chain_id instead of a petname
            if (cache['available_chains'] && !cache['available_chains'][_selected_chain]) {
                for (var chain_petname in cache['available_chains']) {
                    // skip loop if the property is from prototype
                    if (!cache['available_chains'].hasOwnProperty(chain_petname)) {
                        continue;
                    }

                    if (cache['available_chains'][chain_petname] &&
                        cache['available_chains'][chain_petname]['chain_id'] &&
                        _selected_chain == cache['available_chains'][chain_petname]['chain_id']) {
                        $route.updateParams({chain: chain_petname})
                        _selected_chain = chain_petname;
                        break;
                    }
                }
            }
            selected_chain = _selected_chain;
            $rootScope.selected_chain = selected_chain;
            return selected_chain;
        }
        
        srv.set = function(_selected_chain) {

            if (cache['available_chains']) {
                return SetSelectedChain(_selected_chain);
            } else {
                return srv.GetAvailableChains()
                    .then(function() {
                        return SetSelectedChain(_selected_chain);
                    });
            }
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
                    .then(function (response) {
                        var result = SrvUtil.GetResult(response);
                        result['properties'] = cache['available_chains'][ selected_chain ];
                        return SrvUtil.CacheResult(cache, selected_chain, resource, selected_chain)(result);
                    });
            }
        }

        return srv;
    })
