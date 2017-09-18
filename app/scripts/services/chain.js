'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($http, $rootScope) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var selected_chain = "bitcoin";

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
            return $http.post(BACKEND_URL + '/chain/' + srv.get() + '/' + "getblockchaininfo", {})
                .then(function (response) {
                    return response["data"]["result"];
                });
        }

        return srv;
    })
