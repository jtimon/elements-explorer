'use strict';

angular.module('rpcExplorerApp')
    .controller('ChainCtrl', function ($scope, $location, SrvChain, SrvUtil, SrvBackend) {

        $scope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];

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
            SrvBackend.rpcCall("getblockchaininfo", {}, initChainCallback, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.ChangeChain();
    });
