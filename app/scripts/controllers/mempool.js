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
            $scope.mempoolinfo = SrvUtil.GetResult(data);
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
            $scope.mempooltxs = SrvUtil.GetResult(data);
            $scope.loading_mempool_txs = false;
        };
        $scope.LoadMempoolTxs = function() {
            $scope.loading_mempool_txs = true;
            SrvBackend.RpcCall("getrawmempool", {})
                .then(mempooltxsCallback)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function mempoolEntryCallback(data) {
            $scope.mempoolentry = SrvUtil.GetResult(data);
        };
        $scope.goToEntry = function(txhash) {
            return SrvBackend.RpcCall("getmempoolentry", {"txid": $scope.txid})
                .then(mempoolEntryCallback);
        };
        $scope.searchTx = function() {
            if ($scope.txid == "") {
                $scope.mempoolentry = null;
                return;
            }
            $scope.goToEntry($scope.txid)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        if ($routeParams.txid) {
            $scope.txid = $routeParams.txid;
            $scope.goToEntry($routeParams.txid)
                .catch(SrvUtil.errorCallbackScoped($scope));
        }
    });
