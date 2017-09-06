'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, SrvUtil, SrvChain, SrvBackend) {

        $scope.start_height = 1;
        $scope.end_height = 1;
        $scope.verbose_stats = false;
        $scope.selected_chain = SrvChain.get();
        $scope.available_chains = [$scope.selected_chain];
        $scope.xaxis_list = [
            "height",
            "time",
            "mediantime"
        ];
        $scope.xaxis = "height";
        $scope.valid_stats = [
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
            "txs",
            "swtxs",
            "total_size",
            "total_weight",
            "swtotal_size",
            "swtotal_weight",
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

                var xaxis_data = [];
                if ($scope.xaxis == 'height') {
                    xaxis_data = data[$scope.xaxis];
                } else {
                    for (var i = 0; i <  data[$scope.xaxis].length; i++) {
                        xaxis_data.push(new Date(data[$scope.xaxis][i] * 1000));
                    }
                }
                
                var trace = {
                    name: key,
                    x: xaxis_data,
                    y: data[key],
                    type: 'scatter'
                };
                $scope.graphPlots.push(trace);
            }
        };

        $scope.changeXaxis = function(name) {
            if ($scope.xaxis_list.indexOf(name) > -1) {
                $scope.xaxis = name;
            }
            StatsToGraph($scope.plot_data);
        };

        function successCallbackPerBlockStats(data)
        {
            $scope.plot_data = data["data"]["result"];
            StatsToGraph($scope.plot_data);
        };

        $scope.doPlot = function() {
            SrvBackend.GetBlockStats($scope.start_height, $scope.end_height,
                                     successCallbackPerBlockStats, SrvUtil.errorCallbackScoped($scope));
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
        SrvBackend.GetAvailableChains()
            .then(SrvUtil.safeCb(successAvailableChains))
            .catch(SrvUtil.errorCallbackScoped($scope));
    });
