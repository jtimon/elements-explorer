'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $rootScope, SrvChain, SrvUtil, SrvBackend) {

        $rootScope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }
        SrvBackend.GetAvailableChains()
            .then(SrvUtil.safeCb(successAvailableChains))
            .catch(SrvUtil.errorCallbackScoped($scope));

        function initChainCallback(data) {
            $scope.chaininfo = data["data"]["result"];
            SrvChain.setHeight($scope.chaininfo.blocks);
        };
        $scope.ChangeChain = function () {
            if ($rootScope.selected_chain) {
                SrvChain.set($scope.selected_chain);
            }
            SrvBackend.rpcCall("getblockchaininfo", {}, initChainCallback, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.ChangeChain();
    });
