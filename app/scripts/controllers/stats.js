'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, $http) {

        var BACKEND_URL = 'http://127.0.0.1:5000/rpcexplorerrest';
        $scope.start_height = 1;
        $scope.end_height = 1;
        $scope.verbose_stats = false;
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

        function rpcCall(rpcMethod, vRpcParams, successCallback) {
            var requestData = {
                "chain": $scope.selected_chain,
                "method": rpcMethod,
                "params": vRpcParams,
                "jsonrpc": "1.0",
                "id": "curltest",
            };
            $http.post(BACKEND_URL, requestData).then(safeCallback(successCallback), errorCallback);
        };

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }
        function GetAvailableChains() {
            $http.get(BACKEND_URL + '/available_chains').then(safeCallback(successAvailableChains), errorCallback);
        }
        
        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
            $scope.end_height = $scope.chaininfo.blocks;

        };
        $scope.getBlockchainInfo = function() {
            rpcCall("getblockchaininfo", [], successCallbackInfo);
        };

        function successCallbackPerBlockStats(data) {

            $scope.plot_data = data["data"]["result"];
            $scope.graphPlots = [];

            for (var key in $scope.plot_data) {
                // skip loop if the property is from prototype
                if (!$scope.plot_data.hasOwnProperty(key) || key == 'time' || key == 'height' || key == 'mediantime') {
                    continue;
                }

                var trace = {
                    name: key,
                    x: $scope.plot_data["height"],
                    y: $scope.plot_data[key],
                    type: 'scatter'
                };
                $scope.graphPlots.push(trace);
            }
        };

        $scope.doPlot = function() {
            rpcCall("getblockstats",
                    [parseInt($scope.start_height), parseInt($scope.end_height)],
                    successCallbackPerBlockStats);
        };

        $scope.getBlockchainInfo();
    });
