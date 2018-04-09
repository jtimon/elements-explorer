'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:StatsCtrl
 * @description
 * # StatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('StatsCtrl', function ($scope, $routeParams, $location, SrvUtil, SrvChain, SrvBackend) {

        SrvChain.set($routeParams.chain, $scope);

        $scope.curious = $location.search().curious == 'true';
        $scope.loading_stats = false;
        $scope.cached_plot_data = {};
        
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
            "mintxsize",
            "maxtxsize",
            "mediantxsize",
            "avgtxsize",
        ];

        $scope.selected_stats = [
            "swtxs",
            "total_size",
            "swtotal_size",
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
            StatsToGraph($scope.cached_plot_data);
        };

        function successCallbackPerBlockStats(data)
        {
            $scope.cached_plot_data = data;
            StatsToGraph($scope.cached_plot_data);
            $scope.loading_stats = false;
        };

        $scope.doInitialPlot = function() {
            $scope.loading_stats = true;
            return SrvBackend.GetBlockStats($scope.start_height, $scope.end_height)
                .then(successCallbackPerBlockStats)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.doPlot = function() {
            $scope.doInitialPlot()
                .then(function () {
                    $location.search('start_height', $scope.start_height);
                    $location.search('end_height', $scope.end_height);
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
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

            if ($scope.cached_plot_data) {
                StatsToGraph($scope.cached_plot_data);
            }
        };

        SrvChain.GetChainInfo().then(function(chaininfo) {
            if ($location.search().end_height) {
                $scope.end_height = SrvUtil.ParseIntToPositive($location.search().end_height);
            } else {
                $scope.end_height = chaininfo['blocks'];
            }
            if ($location.search().start_height) {
                $scope.start_height = SrvUtil.ParseIntToPositive($location.search().start_height);
            } else {
                $scope.start_height = Math.max(1, $scope.end_height - 99);
            }
            if ($scope.start_height > $scope.end_height) {
                $scope.end_height = $scope.start_height;
            }
        }).then($scope.doInitialPlot)
            .catch(SrvUtil.errorCallbackScoped($scope));
    });
