'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvChain', function SrvChain() {

        var srv = {};
        var selected_chain = "bitcoin";

        srv.set = function(_selected_chain) {
            selected_chain = _selected_chain;
        }

        srv.get = function() {
            return selected_chain;
        }

        return srv;
    })
