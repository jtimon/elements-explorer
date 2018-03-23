'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, $location, SrvChain, SrvUtil) {

        function successAvailableChains(data) {
            $scope.available_chains = data;
        }
        SrvChain.GetAvailableChains()
            .then(successAvailableChains)
            .catch(SrvUtil.errorCallbackScoped($scope));

        function initChainCallback(data) {
            $rootScope.chaininfo = data;
        };

        $scope.ChangeChain = function () {
            if ($scope.selected_chain) {
                SrvChain.set($scope.selected_chain, $scope);
                $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + $scope.selected_chain + "/$2"));
            }
        };

        $scope.ChangeChainRoute = function () {
            if ($scope.selected_chain) {
                SrvChain.GetChainInfo()
                    .then(initChainCallback)
                    .catch(SrvUtil.errorCallbackScoped($scope));
            }
        };

        $scope.$on('$routeChangeSuccess', function() {
            $scope.ChangeChainRoute();
        });
    });
