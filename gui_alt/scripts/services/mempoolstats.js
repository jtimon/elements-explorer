'use strict';
/*global $:false */

angular.module('rpcExplorerApp')
    .service('SrvMempoolstats', function SrvMempoolstats(SrvChain) {

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

        srv.DEFAULT_SELECTED_STATS = [
            '1',
            '10', '20', '30', '50', '70',
            '100', '120', '200', '300', '500', '700',
            'total'
        ];

        srv.DEFAULT_HOURS_AGO = 6;

        srv.CalculatePlotData = function(stats_type, valid_stats, data)
        {
            var plot_data = {};

            var xaxis_data = [];
            for (var key in data) {
                xaxis_data.push(new Date(parseInt(key) * 1000));
            }

            for (var i = 0; i < valid_stats.length; i++) {
                var val_stat = valid_stats[i];
                var yaxis_data = [];
                for (var key in data) {
                    yaxis_data.push(data[key][val_stat]);
                }
                plot_data[val_stat] = {'x': xaxis_data, 'y': yaxis_data};
            }

            return plot_data;
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
