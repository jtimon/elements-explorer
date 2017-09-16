'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($http, $rootScope, $location) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var selected_chain = "bitcoin";

        srv.GetInfo = function() {
            return $http.post(BACKEND_URL + '/chain/' + srv.get() + '/' + "getblockchaininfo", {});
        }

        srv.set = function(_selected_chain) {
            selected_chain = _selected_chain;
            $rootScope.selected_chain = selected_chain;
            $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + selected_chain + "/$2"));
        }

        srv.get = function() {
            return selected_chain;
        }

        srv.GetAvailableChains = function() {
            return $http.get(BACKEND_URL + '/available_chains');
        }

        return srv;
    })
