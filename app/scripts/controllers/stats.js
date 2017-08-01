'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, $http, SrvUtil, SrvBackend) {

        $scope.start_height = 1;
        $scope.end_height = 1;
        $scope.verbose_stats = false;
        $scope.selected_chain = "bitcoin";
        $scope.available_chains = ["bitcoin"];

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }

        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
            // TODO write test for start_height=0 in the gui 
            $scope.start_height = $scope.chaininfo.blocks - 1;
            $scope.end_height = $scope.chaininfo.blocks;

        };
        $scope.getBlockchainInfo = function() {
            SrvBackend.rpcCall($scope.selected_chain, "getblockchaininfo", [], successCallbackInfo, SrvUtil.errorCallbackScoped($scope));
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
            SrvBackend.rpcCall($scope.selected_chain, "getblockstats",
                               [parseInt($scope.start_height), parseInt($scope.end_height)],
                               successCallbackPerBlockStats,
                               SrvUtil.errorCallbackScoped($scope));
        };

        SrvBackend.GetAvailableChains(successAvailableChains, SrvUtil.errorCallbackScoped($scope));
        $scope.getBlockchainInfo();
    });
