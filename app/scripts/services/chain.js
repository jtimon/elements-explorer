'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain($rootScope) {

        var srv = {};
        var selected_chain = "bitcoin";
        var height = 0;

        srv.set = function(_selected_chain) {
            selected_chain = _selected_chain;
            $rootScope.selected_chain = selected_chain;
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
        
        return srv;
    })
