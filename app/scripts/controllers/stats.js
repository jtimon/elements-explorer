'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        if ($routeParams.chain) {
            SrvChain.set($routeParams.chain);
        }
        $scope.loading_stats = false;
        $scope.verbose_stats = false;
        $scope.start_height = (SrvChain.getHeight() > 0) ? (SrvChain.getHeight() - 1) : 0;
        $scope.end_height = SrvChain.getHeight();

        $scope.xaxis_list = [
            "height",
            "time",
            "mediantime"
        ];
        $scope.xaxis = $scope.xaxis_list[0];

        $scope.valid_stats = [
            "txs",
            "swtxs",
            "ins",
            "outs",
            "subsidy",
            "totalfee",
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
        ];

        $scope.selected_stats = [
            "utxo_size_inc",
            "swtxs",
            "avgfeerate",
            "medianfeerate",
            "minfeerate",
        ];

        $scope.IsErrorString = function IsErrorString () {
            return $scope.error && $scope.error.message && typeof $scope.error.message === 'string';
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
            $scope.loading_stats = false;
        };

        $scope.doPlot = function() {
            $scope.loading_stats = true;
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
    });
