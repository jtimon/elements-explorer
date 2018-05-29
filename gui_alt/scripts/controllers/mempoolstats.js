'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MempoolStatsCtrl
 * @description
 * # MempoolStatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MempoolStatsCtrl', function ($scope, $location, SrvUtil, SrvChain, SrvBackend) {

        $scope.curious = $location.search().curious == 'true';
        $scope.stats_types = ['count', 'fee', 'vsize'];

        $scope.hours_ago = $location.search().hours_ago ? SrvUtil.ParseNatural($location.search().hours_ago) : 6;
        $scope.sel_stats_type = $location.search().stats_type ? $location.search().stats_type : $scope.stats_types[0];
        $scope.loading_stats = false;
        // TODO caching should be done on a service
        $scope.plot_data = {}
        $scope.cached_mempoolstats = {};

        $scope.valid_stats = [
            '1', '2', '3', '4', '5',
            '10', '15', '20', '25', '30',
            '40', '50', '60', '70', '80', '90',
            '100', '120', '140', '160', '180',
            '200', '250', '300', '350', '400', '450',
            '500', '600', '700', '800', '900',
            '1000', '1500', '2000',
            'total'
        ];

        $scope.selected_stats = [
            '1',
            '10', '20', '30', '50', '70',
            '100', '120', '200', '300', '500', '700',
            'total'];

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

        function CalculatePlotData(stats_type, valid_stats, data)
        {
            var plot_data = {};

            for (var i = 0; i < valid_stats.length; i++) {

                var val_stat = valid_stats[i];
                var xaxis_data = [];
                var yaxis_data = [];
                for (var key in data) {
                    xaxis_data.push(new Date(parseInt(key) * 1000));
                    yaxis_data.push(data[key][val_stat]);
                }
                plot_data[val_stat] = {'x': xaxis_data, 'y': yaxis_data};
            }
            return plot_data;
        }

        function StatsToGraph(selected_stats, plot_data)
        {
            var graph_list = [];

            for (var i = 0; i < selected_stats.length; i++) {
                var sel_stat = selected_stats[i];
                graph_list.push(CreateTrace(sel_stat, plot_data[sel_stat]['x'], plot_data[sel_stat]['y']));
            }
            return graph_list;
        };

        function CachePlotData(_data)
        {
            $scope.plot_data[$scope.sel_stats_type] = CalculatePlotData($scope.sel_stats_type, $scope.valid_stats, _data['data']);
        }

        function PlotCachedData()
        {
            $scope.cached_mempoolstats[$scope.sel_stats_type] = StatsToGraph($scope.selected_stats, $scope.plot_data[$scope.sel_stats_type]);
            $scope.graphPlots = $scope.cached_mempoolstats[$scope.sel_stats_type];
            $scope.loading_stats = false;
        };

        $scope.doPlot = function() {
            $scope.loading_stats = true;

            if ($scope.hours_ago != SrvUtil.ParseNatural($location.search().hours_ago)) {
                $location.search('hours_ago', $scope.hours_ago);
            }
            else if ($scope.sel_stats_type != $location.search().stats_type) {
                $location.search('stats_type', $scope.sel_stats_type);
            }
            else if ($scope.plot_data[$scope.sel_stats_type] && $scope.hours_ago == $scope.cached_hours_ago) {
                PlotCachedData();
            } else {
                $scope.cached_hours_ago = $scope.hours_ago;
                SrvBackend.RpcCall('mempoolstats', {'hours_ago': $scope.hours_ago, 'stat_type': $scope.sel_stats_type})
                    .then(CachePlotData)
                    .then(PlotCachedData)
                    .catch(SrvUtil.errorCallbackScoped($scope));
            }
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

            var aux_sel_stats = [];
            for (var i = 0; i < $scope.valid_stats.length; i++) {
                var val_stat = $scope.valid_stats[i];
                if ($scope.selected_stats.indexOf(val_stat) > -1) {
                    aux_sel_stats.push(val_stat);
                }
            }
            $scope.selected_stats = aux_sel_stats;

            $scope.doPlot();
        };

        $scope.changeStatType = function(name) {
            $scope.loading_stats = true;

            if ($scope.stats_types.indexOf(name) > -1) {
                $scope.sel_stats_type = name;
            }
            $scope.doPlot();
        };

        SrvChain.set()
            .then($scope.doPlot)
            .catch(SrvUtil.errorCallbackScoped($scope));
    });
