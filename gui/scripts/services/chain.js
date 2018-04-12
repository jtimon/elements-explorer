'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($q, $http, $rootScope, $routeParams, $route, SrvUtil) {

        var BACKEND_URL = '/api/v0';
        var srv = {};

        var cache = {};

        srv.GetAvailableChains = function() {
            if (cache['available_chains']) {
                return $q(function(resolve) {
                    resolve(cache['available_chains']);
                });
            } else {
                return $http.get(BACKEND_URL + '/available_chains')
                    .then(function (response) {
                        cache['available_chains'] = response["data"]["available_chains"];
                        return cache['available_chains'];
                    });
            }
        }

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
            return _selected_chain;
        }

        srv.set = function() {
            if ($routeParams.chain == $rootScope.selected_chain) {
                return $q(function(resolve) {
                    resolve($routeParams.chain);
                });
            }

            return srv.GetAvailableChains()
                .then(function(available_chains) {
                    $rootScope.selected_chain = SetSelectedChain($routeParams.chain);
                    return $rootScope.selected_chain;
                });
        }

        srv.get = function() {
            return $routeParams.chain;
        }

        srv.GetChainInfo = function() {
            SrvUtil.PreCache(cache, srv.get(), 'chaininfo');
            if (cache[srv.get()]['chaininfo'][srv.get()]) {
                return $q(function(resolve) {
                    resolve(cache[srv.get()]['chaininfo'][srv.get()]);
                });
            } else {
                return $http.post(BACKEND_URL + '/chaininfo', {'id': srv.get(), 'chain': srv.get()})
                    .then(function (response) {
                        var result = SrvUtil.GetResult(response);
                        return SrvUtil.CacheResult(cache, srv.get(), 'chaininfo', srv.get())(result);
                    });
            }
        }

        return srv;
    })
