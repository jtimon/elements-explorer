'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, $routeParams, $location, SrvChain, SrvUtil) {

        $rootScope.selected_chain = SrvChain.get();
        $scope.available_chains = [$rootScope.selected_chain];

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
                $location.path($location.path().replace(/chain\/(.+?)\/(.*)/g,"chain/" + $scope.selected_chain + "/$2"));
            }
            SrvChain.GetInfo()
                .then(safeCallback(initChainCallback))
                .catch(safeCallback(SrvUtil.errorCallbackScoped($scope)));
        };

        $scope.$on('$routeChangeSuccess', function() {
            $scope.ChangeChain();
        });
    });
