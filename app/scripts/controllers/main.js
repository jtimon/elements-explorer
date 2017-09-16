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

        function cleanBlock() {
            $scope.blockid = "";
            $scope.blockheight = null;
            $scope.block = null;
            $scope.blockjson = null;
        }

        $scope.searchBlock = function() {
            
            function statsCallbackBlock(data) {
                $scope.blockstats = data;
            };

            function successCallbackBlock(data) {
                $scope.block = data;
                $scope.blockheight = $scope.block["height"];
                SrvBackend.get("blockstats", $scope.block["height"], statsCallbackBlock, SrvUtil.errorCallbackScoped($scope));
                $scope.blockjson = JSON.stringify($scope.block, null, 4);
            };
            SrvBackend.get("block", $scope.blockid, successCallbackBlock, SrvUtil.errorCallbackScoped($scope));

        };

        $scope.searchBlockByHeight = function() {
            function successCallbackBlockHeight(data) {
                $scope.blockid = data["data"]["result"];
                $scope.searchBlock();
            };
            cleanTx();
            var params = {"height": $scope.blockheight};
            SrvBackend.RpcCall("getblockhash", params)
                .then(successCallbackBlockHeight)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchTx = function() {
            if ($scope.txid == "") {
                $scope.transaction = null;
                return;
            }
            function successCallbackTx(data) {
                $scope.showtxlist = false;
                $scope.transaction = data;
                $scope.blockid = $scope.transaction["blockhash"];
                if ($scope.blockid) {
                    $scope.searchBlock();
                }
                $scope.txjson = JSON.stringify($scope.transaction, null, 4);
            };
            cleanBlock();
            SrvBackend.get("tx", $scope.txid, successCallbackTx, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.goToBlock = function(blockhash) {
            $scope.blockid = blockhash;
            $scope.searchBlock();
            cleanTx();
        };

        $scope.goToTx = function(txhash) {
            $scope.txid = txhash;
            $scope.searchTx();
        };

        $scope.IsCTOut = function(output) {
            return !output["value"] && output["value"] != 0;
        };

        // Cleanup before going to block or tx
        cleanTx();
        cleanBlock();

        if ($routeParams.block) {
            $scope.goToBlock($routeParams.block);
        } else if ($routeParams.txid) {
            $scope.goToTx($routeParams.txid);
        }
    });
