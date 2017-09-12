'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($http, $rootScope, $location) {

        var BACKEND_URL = '/api/v0';
        var srv = {};
        var selected_chain = "bitcoin";
        var height = 0;

        srv.set = function(_selected_chain) {
            selected_chain = _selected_chain;
            $rootScope.selected_chain = selected_chain;
            $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + selected_chain + "/$2"));
        }

        srv.get = function() {
            return selected_chain;
        }

        srv.setHeight = function(_Height) {
            height = _Height;
        }

        srv.getHeight = function() {
            return height;
        }

        srv.GetAvailableChains = function() {
            return $http.get(BACKEND_URL + '/available_chains');
        }

        srv.GetInfo = function(chain) {
            return $http.post(BACKEND_URL + '/chain/' + chain + '/' + "getblockchaininfo", {});
        }

        return srv;
    })
