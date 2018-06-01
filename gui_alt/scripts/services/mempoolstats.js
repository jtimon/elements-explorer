'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvMempoolstats', function SrvMempoolstats(SrvChain, SrvUtil) {

        var srv = {};

        srv.STAT_TYPES = [
            'count',
            'fee',
            'vsize'
        ];

        srv.GetDefaultStatType = function()
        {
            return srv.STAT_TYPES[0];
        };

        srv.VALID_STATS = [
            '1', '2', '3', '4', '5',
            '10', '15', '20', '25', '30',
            '40', '50', '60', '70', '80', '90',
            '100', '120', '140', '160', '180',
            '200', '250', '300', '350', '400', '450',
            '500', '600', '700', '800', '900',
            '1000', '1500', '2000',
            'total'
        ];

        srv.selected_stats = [
            '1',
            '10', '50',
            '100', '120', '200',
            'total'
        ];

        srv.cached_hours_ago = 6;
        srv.plot_data = {};

        // TODO Use current time to avoid forcing user to reload or change hours_ago
        srv.IsCached = function(hours_ago, stat_type)
        {
            var chain = SrvChain.get();
            SrvUtil.PreCache(srv.plot_data, chain, stat_type);
            return (srv.plot_data[chain][stat_type] && !angular.equals(srv.plot_data[chain][stat_type], {}) && hours_ago == srv.cached_hours_ago);
        };

        srv.CalculatePlotData = function(stat_type, data)
        {
            var chain = SrvChain.get();
            SrvUtil.PreCache(srv.plot_data, chain, stat_type);

            var xaxis_data = [];
            for (var key in data) {
                xaxis_data.push(new Date(parseInt(key) * 1000));
            }

            for (var i = 0; i < srv.VALID_STATS.length; i++) {
                var val_stat = srv.VALID_STATS[i];
                var yaxis_data = [];
                for (var key in data) {
                    yaxis_data.push(data[key][val_stat]);
                }
                srv.plot_data[chain][stat_type][val_stat] = {'x': xaxis_data, 'y': yaxis_data};
            }
            return srv.plot_data[chain][stat_type];
        };

        // Functions for presentations to plotly.js
        function CreateTrace(key, xaxis_data, yaxis_data)
        {
            return {
                name: key,
                x: xaxis_data,
                y: yaxis_data,
                fill: 'tonexty',
                type: 'scatter'
            };
        };

        srv.StatsToGraph = function(selected_stats, plot_data)
        {
            var graph_list = [];

            for (var i = 0; i < selected_stats.length; i++) {
                var sel_stat = selected_stats[i];
                graph_list.push(CreateTrace(sel_stat, plot_data[sel_stat]['x'], plot_data[sel_stat]['y']));
            }
            return graph_list;
        };

        return srv;
    })
