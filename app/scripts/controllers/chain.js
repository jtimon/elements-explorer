'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, SrvChain, SrvUtil) {

        function successAvailableChains(data) {
            $scope.available_chains = data;
        }
        SrvChain.GetAvailableChains()
            .then(successAvailableChains)
            .catch(SrvUtil.errorCallbackScoped($scope));

        function initChainCallback(data) {
            $scope.chaininfo = data["data"]["result"];
        };

        $scope.ChangeChain = function () {
            if ($scope.selected_chain) {
                SrvChain.set($scope.selected_chain)
                    .then(initChainCallback)
                    .catch(SrvUtil.errorCallbackScoped($scope));
            }
        };

        $scope.$on('$routeChangeSuccess', function() {
            $scope.ChangeChain();
        });
    });
