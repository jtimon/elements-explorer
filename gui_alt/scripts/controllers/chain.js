'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, $location, SrvChain, SrvUtil) {

        SrvChain.GetAvailableChains()
            .then(function (available_chains) {
                $scope.available_chains = SrvUtil.GetKeys(available_chains);
                $rootScope.chain_properties = available_chains;
            })
            .catch(SrvUtil.errorCallbackScoped($scope));

        $scope.ChangeChain = function () {
            $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + $scope.selected_chain + "/$2"));
        };
    });
