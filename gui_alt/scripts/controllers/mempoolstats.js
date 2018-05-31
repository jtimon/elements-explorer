'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MempoolStatsCtrl
 * @description
 * # MempoolStatsCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MempoolStatsCtrl', function ($scope, $location, SrvUtil, SrvChain, SrvBackend, SrvMempoolstats) {

        $scope.curious = $location.search().curious == 'true';
        $scope.hours_ago = $location.search().hours_ago ? SrvUtil.ParseNatural($location.search().hours_ago) : SrvMempoolstats.cached_hours_ago;
        $scope.sel_stats_type = $location.search().stats_type ? $location.search().stats_type : SrvMempoolstats.GetDefaultStatType();

        $scope.loading_stats = false;
        $scope.stats_types = SrvMempoolstats.STAT_TYPES;
        $scope.valid_stats = SrvMempoolstats.VALID_STATS;
        $scope.selected_stats = SrvMempoolstats.selected_stats;

        $scope.cached_mempoolstats = {};

        function CachePlotData(data)
        {
            // Clean up cache when hours change
            if ($scope.hours_ago != SrvMempoolstats.cached_hours_ago) {
                SrvMempoolstats.plot_data = {};
                SrvMempoolstats.cached_hours_ago = $scope.hours_ago;
            }
            SrvMempoolstats.CalculatePlotData($scope.sel_stats_type, data['data']);
        }

        function PlotCachedData()
        {
            $scope.cached_mempoolstats[$scope.sel_stats_type] = SrvMempoolstats.StatsToGraph($scope.selected_stats, SrvMempoolstats.plot_data[SrvChain.get()][$scope.sel_stats_type]);
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
            else if (SrvMempoolstats.IsCached($scope.hours_ago, $scope.sel_stats_type)) {
                PlotCachedData();
            } else {
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
            SrvMempoolstats.selected_stats = aux_sel_stats;
            $scope.selected_stats = SrvMempoolstats.selected_stats;
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
