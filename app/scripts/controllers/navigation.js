'use strict';

angular.module('rpcExplorerApp')
  .controller('NavigationCtrl', function ($scope, $location) {

    $scope.navClass = function (page) {
      var currentRoute = $location.path().substring(1) || 'chain';
      return page === currentRoute ? 'active' : '';
    };
  });
