'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MempoolCtrl
 * @description
 * # MempoolCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MempoolCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        if ($routeParams.chain) {
            SrvChain.set($routeParams.chain);
        }
        $scope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }
        SrvBackend.GetAvailableChains()
            .then(SrvUtil.safeCb(successAvailableChains))
            .catch(SrvUtil.errorCallbackScoped($scope));

        function mempoolinfoCallback(data) {
            $scope.mempoolinfo = data["data"]["result"];
        };
        function mempooltxsCallback(data) {
            $scope.mempooltxs = data["data"]["result"];
        };
        $scope.InitForSelectedChain = function() {
            SrvChain.set($scope.selected_chain);
            SrvBackend.rpcCall("getmempoolinfo", {}, mempoolinfoCallback, SrvUtil.errorCallbackScoped($scope));
            SrvBackend.rpcCall("getrawmempool", {}, mempooltxsCallback, SrvUtil.errorCallbackScoped($scope));
        };
        $scope.InitForSelectedChain();

        function mempoolEntryCallback(data) {
            $scope.mempoolentry = data["data"]["result"];
        };
        $scope.searchTx = function() {
            SrvBackend.rpcCall("getmempoolentry", {"txid": $scope.txid}, mempoolEntryCallback, SrvUtil.errorCallbackScoped($scope));
        };
        $scope.goToTx = function(txhash) {
            $scope.txid = txhash;
            $scope.searchTx();
        };
        if ($routeParams.txid) {
            $scope.goToTx($routeParams.txid);
        }
    });
