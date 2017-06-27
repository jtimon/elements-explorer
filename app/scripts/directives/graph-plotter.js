angular.module('rpcExplorerApp')
  .directive('linePlot', [function () {
    function linkFunc(scope, element, attrs) {
        scope.$watch('graphPlots', function (plots) {
            Plotly.newPlot(element[0], plots);
        });
    }

    return {
        link: linkFunc
    };
}]);
