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

        function mempoolinfoCallback(data) {
            $scope.mempoolinfo = data["data"]["result"];
        };
        function mempooltxsCallback(data) {
            $scope.mempooltxs = data["data"]["result"];
            $scope.loading_mempool = false;
        };
        $scope.InitForSelectedChain = function() {
            $scope.selected_chain = SrvChain.get();
            $scope.loading_mempool = true;
            SrvBackend.rpcCall("getmempoolinfo", {}, mempoolinfoCallback, SrvUtil.errorCallbackScoped($scope));
            SrvBackend.rpcCall("getrawmempool", {}, mempooltxsCallback, SrvUtil.errorCallbackScoped($scope));
        };
        $scope.InitForSelectedChain();

        function mempoolEntryCallback(data) {
            $scope.mempoolentry = data["data"]["result"];
        };
        $scope.searchTx = function() {
            if ($scope.txid == "") {
                $scope.mempoolentry = null;
                return;
            }
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
