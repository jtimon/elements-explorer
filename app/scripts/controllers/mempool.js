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

        $scope.loading = true;
        if ($routeParams.chain) {
            SrvChain.set($routeParams.chain);
        }

        function mempoolinfoCallback(data) {
            $scope.mempoolinfo = SrvUtil.GetResult(data);
        };
        $scope.InitForSelectedChain = function() {
            SrvBackend.RpcCall("getmempoolinfo", {})
                .then(mempoolinfoCallback)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        function mempooltxsCallback(data) {
            $scope.mempooltxs = SrvUtil.GetResult(data);
        };
        $scope.LoadMempoolTxs = function() {
            $scope.loading = true;
            SrvBackend.RpcCall("getrawmempool", {})
                .then(mempooltxsCallback)
                .then(function() {
                    $scope.loading = false;
                })
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
            $scope.loading = true;
            $scope.goToEntry($scope.txid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.InitForSelectedChain();
        if ($routeParams.txid) {
            $scope.txid = $routeParams.txid;
            $scope.goToEntry($routeParams.txid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        } else {
            $scope.loading = false;
        }
    });
