'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $routeParams, $http, SrvUtil, SrvChain, SrvBackend) {

        $scope.CTverbose = false;
        $scope.verbose = false;
        $scope.rawhex_limit = 100;
        $scope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
            $scope.available_chains.push("forbiddenchain");
        }

        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
        };
        $scope.getBlockchainInfo = function() {
            SrvBackend.rpcCall("getblockchaininfo", {}, successCallbackInfo, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchBlock = function() {
            function successCallbackBlock(data) {
                $scope.block = data["data"]["result"];
                $scope.blockjson = JSON.stringify($scope.block, null, 4);
                $scope.blockheight = $scope.block["height"];
                $scope.getBlockchainInfo();
            };
            SrvBackend.get("block", $scope.blockid, successCallbackBlock, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchBlockByHeight = function() {
            function successCallbackBlockHeight(data) {
                $scope.blockid = data["data"]["result"];
                $scope.searchBlock();
            };
            $scope.txid = "";
            $scope.transaction = null;
            var params = {"height": $scope.blockheight};
            SrvBackend.rpcCall("getblockhash", params, successCallbackBlockHeight, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.searchTx = function() {
            function successCallbackTx(data) {
                $scope.showtxlist = false;
                $scope.transaction = data["data"]["result"];
                $scope.txjson = JSON.stringify($scope.transaction, null, 4);
                $scope.blockid = $scope.transaction["blockhash"];
                $scope.searchBlock();
            };
            SrvBackend.get("tx", $scope.txid, successCallbackTx, SrvUtil.errorCallbackScoped($scope));
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
            SrvChain.set($scope.selected_chain);
            SrvBackend.rpcCall("getblockchaininfo", {}, initCallback, SrvUtil.errorCallbackScoped($scope));
        };

        SrvBackend.GetAvailableChains(successAvailableChains, SrvUtil.errorCallbackScoped($scope));
        // Init from $routeParams
        if ($routeParams.chain) {
            $scope.selected_chain = $routeParams.chain;
            SrvChain.set($scope.selected_chain);
        }
        if ($routeParams.block) {
            $scope.goToBlock($routeParams.block);
        } else if ($routeParams.txid) {
            $scope.goToTx($routeParams.txid);
        } else {
            $scope.InitForSelectedChain();
        }
    });
