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

        function mempoolinfoCallback(data) {
            $scope.mempoolinfo = data["data"]["result"];
            $scope.loading_mempool = false;
        };
        $scope.InitForSelectedChain = function() {
            $scope.loading_mempool = true;
            SrvBackend.RpcCall("getmempoolinfo", {})
                .then(mempoolinfoCallback)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };
        $scope.InitForSelectedChain();

        function mempooltxsCallback(data) {
            $scope.mempooltxs = data["data"]["result"];
            $scope.loading_mempool_txs = false;
        };
        $scope.LoadMempoolTxs = function() {
            $scope.loading_mempool_txs = true;
            SrvBackend.RpcCall("getrawmempool", {})
                .then(mempooltxsCallback)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function mempoolEntryCallback(data) {
            $scope.mempoolentry = data["data"]["result"];
        };
        $scope.searchTx = function() {
            if ($scope.txid == "") {
                $scope.mempoolentry = null;
                return;
            }
            SrvBackend.RpcCall("getmempoolentry", {"txid": $scope.txid})
                .then(mempoolEntryCallback)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };
        $scope.goToTx = function(txhash) {
            $scope.txid = txhash;
            $scope.searchTx();
        };
        if ($routeParams.txid) {
            $scope.goToTx($routeParams.txid);
        }
    });
