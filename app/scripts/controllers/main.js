'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $routeParams, $http, SrvBackend) {

        $scope.CTverbose = false;
        $scope.verbose = false;
        $scope.selected_chain = "bitcoin";
        $scope.available_chains = ["bitcoin"];

        function safeCallback(callback) {
            return function(data) {
                if (data["data"]["error"]) {
                    $scope.error = data["data"]["error"];
                }
                else if (callback){
                    $scope.error = null;
                    callback(data);
                }
            };
        };

        function errorCallback(data) {
            $scope.error = JSON.stringify(data, null, 4);
        };

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }

        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
        };
        $scope.getBlockchainInfo = function() {
            SrvBackend.rpcCall($scope.selected_chain, "getblockchaininfo", [], safeCallback(successCallbackInfo), errorCallback);
        };

        $scope.searchBlock = function() {
            function successCallbackBlock(data) {
                $scope.block = data["data"]["result"];
                $scope.blockjson = JSON.stringify($scope.block, null, 4);
                $scope.blockheight = $scope.block["height"];
                $scope.getBlockchainInfo();
            };
            SrvBackend.rpcCall($scope.selected_chain, "getblock", [$scope.blockid], safeCallback(successCallbackBlock), errorCallback);
        };

        $scope.searchBlockByHeight = function() {
            function successCallbackBlockHeight(data) {
                $scope.blockid = data["data"]["result"];
                $scope.searchBlock();
            };
            $scope.txid = "";
            $scope.transaction = null;
            var height = parseInt($scope.blockheight);
            SrvBackend.rpcCall($scope.selected_chain, "getblockhash", [height], safeCallback(successCallbackBlockHeight), errorCallback);
        };

        $scope.searchTx = function() {
            function successCallbackTx(data) {
                $scope.transaction = data["data"]["result"];
                $scope.txjson = JSON.stringify($scope.transaction, null, 4);
                $scope.blockid = $scope.transaction["blockhash"];
                $scope.searchBlock();
            };
            SrvBackend.rpcCall($scope.selected_chain, "getrawtransaction", [$scope.txid, 1], safeCallback(successCallbackTx), errorCallback);
        };

        $scope.goToBlock = function(blockhash) {
            $scope.blockid = blockhash;
            $scope.searchBlock();
            $scope.txid = "";
            $scope.transaction = null;
        };

        $scope.goToTx = function(txhash) {
            $scope.txid = txhash;
            $scope.searchTx();
        };

        $scope.IsCTOut = function(output) {
            return !output["value"] && output["value"] != 0;
        };

        function initCallback(data) {
            successCallbackInfo(data);
            $scope.blockheight = $scope.chaininfo["blocks"];
            $scope.blockid = $scope.chaininfo["bestblockhash"];
            $scope.searchBlock();
        };
        $scope.InitForSelectedChain = function() {
            SrvBackend.rpcCall($scope.selected_chain, "getblockchaininfo", [], safeCallback(initCallback), errorCallback);
        };

        SrvBackend.GetAvailableChains(safeCallback(successAvailableChains), errorCallback);
        // Init from $routeParams
        if ($routeParams.chain) {
            $scope.selected_chain = $routeParams.chain;
        }
        if ($routeParams.block) {
            $scope.goToBlock($routeParams.block);
        } else if ($routeParams.txid) {
            $scope.goToTx($routeParams.txid);
        } else {
            $scope.InitForSelectedChain();
        }
    });
