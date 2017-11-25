'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MempoolStatsCtrl
 * @description
 * # MempoolStatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MempoolStatsCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        SrvChain.set($routeParams.chain);

        $scope.loading_stats = false;
        $scope.verbose_stats = false;

        $scope.stats_types = ['count', 'fee', 'vsize'];
        $scope.sel_stats_type = $scope.stats_types[0];

        $scope.valid_stats = ['1', '2', '3', '4', '5', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', 'total'];

        $scope.selected_stats = ['1', '2', '3', '4', '5', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', 'total'];

        function CreateTrace(key, xaxis_data, yaxis_data)
        {
            return {
                name: key,
                x: xaxis_data,
                y: yaxis_data,
                fill: 'tonexty',
                type: 'scatter'
            };
        }

        function StatsToGraph(stats_type, selected_stats, data)
        {
            var graph_list = [];
            for (var i = 0; i < selected_stats.length; i++) {

                var sel_stat = selected_stats[i];
                var xaxis_data = [];
                var yaxis_data = [];
                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        xaxis_data.push(new Date(parseInt(key) * 1000));
                        yaxis_data.push(data[key][stats_type][sel_stat]);
                    }
                }
                graph_list.push(CreateTrace(sel_stat, xaxis_data, yaxis_data));
            }

            return graph_list;
        };

        var successDoPlot = function(data) {

            $scope.graph_mp = {};
            for (var i = 0; i < $scope.stats_types.length; i++) {
                $scope.graph_mp[$scope.stats_types[i]] = StatsToGraph($scope.stats_types[i], $scope.selected_stats, data['data']);
            }

            $scope.graphPlots = $scope.graph_mp[$scope.sel_stats_type];

            $scope.loading_stats = false;
        };
        
        $scope.doPlot = function() {
            $scope.loading_stats = true;

            SrvBackend.RpcCall('mempoolstats', {})
                .then(successDoPlot)
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.doPlot();

        $scope.toggleStat = function(name) {
            var idx = $scope.selected_stats.indexOf(name);

            if (idx > -1) {
                // Is currently selected
                $scope.selected_stats.splice(idx, 1);
            } else {
                // Is newly selected
                $scope.selected_stats.push(name);
            }

            // if ($scope.plot_data) {
            //     StatsToGraph($scope.plot_data);
            // }
            $scope.doPlot();
            $scope.graphPlots = $scope.graph_mp[$scope.sel_stats_type];
        };

        $scope.changeStatType = function(name) {
            if ($scope.stats_types.indexOf(name) > -1) {
                $scope.sel_stats_type = name;
            }
            $scope.graphPlots = $scope.graph_mp[$scope.sel_stats_type];
        };

    });
