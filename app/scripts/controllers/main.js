'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MainCtrl', function ($scope, $http) {

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
        
        function rpcCall(rpcMethod, vRpcParams, successCallback) {
            var backendUrl = 'http://127.0.0.1:5000/bitcoind';
            var requestData = {"method": rpcMethod, "params": vRpcParams, "jsonrpc": "1.0", "id": "curltest"};
            $http.post(backendUrl, requestData).then(safeCallback(successCallback), errorCallback);
        };

        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
        };
        $scope.getBlockchainInfo = function() {
            rpcCall("getblockchaininfo", [], successCallbackInfo);
        };

        $scope.searchBlock = function() {
            function successCallbackBlock(data) {
                $scope.block = data["data"]["result"];
                $scope.blockheight = $scope.block["height"];
                $scope.getBlockchainInfo();
            };
            rpcCall("getblock", [$scope.blockid], successCallbackBlock);
        };

        $scope.searchBlockByHeight = function() {
            function successCallbackBlockHeight(data) {
                $scope.blockid = data["data"]["result"];
                $scope.searchBlock();
            };
            $scope.txid = "";
            $scope.transaction = null;
            var height = parseInt($scope.blockheight);
            rpcCall("getblockhash", [height], successCallbackBlockHeight);
        };

        $scope.searchTx = function() {
            function successCallbackTx(data) {
                $scope.transaction = data["data"]["result"];
                $scope.txjson = JSON.stringify($scope.transaction, null, 4);
                $scope.blockid = $scope.transaction["blockhash"];
                $scope.searchBlock();
            };
            rpcCall("getrawtransaction", [$scope.txid, 1], successCallbackTx);
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

        function initCallback(data) {
            successCallbackInfo(data);
            $scope.blockheight = $scope.chaininfo["blocks"];
            $scope.blockid = $scope.chaininfo["bestblockhash"];
            $scope.searchBlock();
        };
        rpcCall("getblockchaininfo", [], initCallback);
  });
