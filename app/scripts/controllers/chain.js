'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, SrvChain, SrvUtil) {

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }
        SrvChain.GetAvailableChains()
            .then(SrvUtil.safeCb(successAvailableChains))
            .catch(SrvUtil.errorCallbackScoped($scope));

        function initChainCallback(data) {
            $scope.chaininfo = data["data"]["result"];
            SrvChain.setHeight($scope.chaininfo.blocks);
        };

        $scope.ChangeChain = function () {
            if ($scope.selected_chain) {
                SrvChain.set($scope.selected_chain);
            }
            SrvChain.GetInfo()
                .then(safeCallback(initChainCallback))
                .catch(safeCallback(SrvUtil.errorCallbackScoped($scope)));
        };

        $scope.$on('$routeChangeSuccess', function() {
            $scope.ChangeChain();
        });
    });
