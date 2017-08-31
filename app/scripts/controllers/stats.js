'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, $http, SrvUtil, SrvChain, SrvBackend) {

        $scope.start_height = 1;
        $scope.end_height = 1;
        $scope.verbose_stats = false;
        $scope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];
        $scope.valid_stats = [
            // "height",
            // "time",
            "mediantime",
            "txs",
            "swtxs",
            "ins",
            "outs",
            "subsidy",
            "totalfee",
            "reward",
            "utxo_increase",
            "utxo_size_inc",
            "total_size",
            "total_weight",
            "swtotal_size",
            "swtotal_weight",
            "total_out",
            "minfee",
            "maxfee",
            "medianfee",
            "avgfee",
            "minfeerate",
            "maxfeerate",
            "medianfeerate",
            "avgfeerate",
            "minfeerate_old",
            "maxfeerate_old",
            "medianfeerate_old",
            "avgfeerate_old"
        ];
        $scope.selected_stats = [
            "total_size",
            "minfeerate",
            "medianfeerate",
            "totalfee",
            "utxo_size_inc",
        ];

        function successCallbackInfo(data) {
            $scope.chaininfo = data["data"]["result"];
            // TODO write test for start_height=0 in the gui
            $scope.start_height = $scope.chaininfo.blocks - 1;
            $scope.end_height = $scope.chaininfo.blocks;

        };
        $scope.getBlockchainInfo = function() {
            SrvChain.set($scope.selected_chain);
            SrvBackend.rpcCall("getblockchaininfo", {}, successCallbackInfo, SrvUtil.errorCallbackScoped($scope));
        };

        function StatsToGraph(data)
        {
            $scope.graphPlots = [];

            for (var key in data) {
                // skip loop if the property is from prototype
                if (!data.hasOwnProperty(key) || $scope.selected_stats.indexOf(key) < 0 ||
                    key == 'time' || key == 'height' || key == 'mediantime') {
                    continue;
                }

                var trace = {
                    name: key,
                    x: data["height"],
                    y: data[key],
                    type: 'scatter'
                };
                $scope.graphPlots.push(trace);
            }
        };

        function successCallbackPerBlockStats(data)
        {
            $scope.plot_data = data["data"]["result"];
            StatsToGraph($scope.plot_data);
        };

        $scope.doPlot = function() {
            var params = {
                "start": $scope.start_height,
                "end": $scope.end_height,
            };
            SrvBackend.rpcCall("getblockstats", params, successCallbackPerBlockStats, SrvUtil.errorCallbackScoped($scope));
        };

        $scope.toggleStat = function(name) {
            var idx = $scope.selected_stats.indexOf(name);

            if (idx > -1) {
                // Is currently selected
                $scope.selected_stats.splice(idx, 1);
            } else {
                // Is newly selected
                $scope.selected_stats.push(name);
            }

            if ($scope.plot_data) {
                StatsToGraph($scope.plot_data);
            }
        };

        $scope.getBlockchainInfo();

        function successAvailableChains(data) {
            $scope.available_chains = data["data"]["available_chains"];
        }
        SrvBackend.GetAvailableChains(successAvailableChains, SrvUtil.errorCallbackScoped($scope));
    });
