'use strict';

angular.module('rpcExplorerApp')
    .controller('NavigationCtrl', function ($scope, $location) {

        $scope.navClass = function (page) {

            var path = $location.path();
            if (page === 'chain') {
                if (path.search('block') >= 0 ||
                    path.search('tx') >= 0 ||
                    $location.path().replace(/chain\/(.+)?\/(.*)/g, "$2") === '/') {
                    return 'active';
                }
            } else {
                return path.search(page) >= 0 ? 'active' : '';
            }
            return '';
        };
    });
