'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        $scope.loading = true;
        if ($routeParams.chain) {
            SrvChain.set($routeParams.chain);
        }
        $scope.CTverbose = false;
        $scope.verbose = false;
        $scope.rawhex_limit = 100;

        function cleanTx() {
            $scope.txid = "";
            $scope.transaction = null;
            $scope.txjson = null;
        }

        function cleanBlockBase() {
            $scope.block = null;
            $scope.blockstats = null;
            $scope.blockjson = null;
        }

        function cleanBlock() {
            cleanBlockBase();
            $scope.blockid = "";
            $scope.blockheight = null;
        }

        cleanTx();
        cleanBlock();

        function successCallbackBlock(data) {
            $scope.block = data;
            $scope.blockheight = $scope.block["height"];
            $scope.blockjson = JSON.stringify($scope.block, null, 4);

            return $scope.block["height"];
        };

        function statsCallbackBlock(data) {
            $scope.blockstats = data;
        };

        function PromBlockstats(height) {
            return SrvBackend.get("blockstats", height)
                .then(statsCallbackBlock);
        };

        function successCallbackBlockHeight(data) {
            $scope.blockid = SrvUtil.GetResult(data);
            return $scope.blockid;
        };

        function successCallbackTx(data) {
            $scope.showtxlist = false;
            $scope.transaction = data;
            $scope.txjson = JSON.stringify($scope.transaction, null, 4);
            if ($scope.transaction["blockhash"]) {
                $scope.blockid = $scope.transaction["blockhash"];
                return goToBlock($scope.blockid)
                    .then(PromBlockstats);
            } else {
                cleanBlock();
            }
        };

        var goToBlock = function(blockhash) {
            return SrvBackend.get("block", blockhash)
                .then(successCallbackBlock);
        };

        var goToHeight = function(height) {
            return SrvBackend.RpcCall("getblockhash", {"height": height})
                .then(successCallbackBlockHeight)
                .then(goToBlock)
                .then(PromBlockstats);
        };

        var goToTx = function(txhash) {
            return SrvBackend.get("tx", txhash)
                .then(successCallbackTx);
        };

        $scope.IsCTOut = function(output) {
            return !output["value"] && output["value"] != 0;
        };

        $scope.searchBlock = function() {
            cleanBlockBase();
            $scope.blockheight = null;
            if ($scope.blockid == "") {
                cleanBlock();
                return;
            }
            $scope.loading = true;
            cleanTx();
            goToBlock($scope.blockid)
                .then(PromBlockstats)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchBlockByHeight = function() {
            $scope.loading = true;
            cleanBlockBase();
            $scope.blockid = "";
            cleanTx();
            goToHeight($scope.blockheight)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchTx = function() {
            if ($scope.txid == "") {
                cleanTx();
                return;
            }
            $scope.loading = true;
            cleanBlock();
            goToTx($scope.txid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        if ($routeParams.block) {
            $scope.blockid = $routeParams.block;
            goToBlock($routeParams.block)
                .then(PromBlockstats)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        } else if ($routeParams.txid) {
            $scope.txid = $routeParams.txid;
            goToTx($routeParams.txid)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        } else {
            $scope.loading = false;
        }
    });
