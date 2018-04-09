'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, $location, SrvChain, SrvUtil) {

        SrvChain.GetAvailableChains()
            .then(function (available_chains) {
                $scope.available_chains = available_chains;
            })
            .catch(SrvUtil.errorCallbackScoped($scope));

        $scope.ChangeChain = function () {
            $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + $scope.selected_chain + "/$2"));
        };

        $scope.$on('$routeChangeSuccess', function() {
            SrvChain.GetChainInfo()
                .then(function (chaininfo) {
                    $rootScope.chaininfo = chaininfo;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        });
    });
