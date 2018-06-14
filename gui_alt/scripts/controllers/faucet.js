'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:FaucetCtrl
 * @description
 * # FaucetCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('FaucetCtrl', function ($scope, $location, SrvUtil, SrvChain, SrvBackend) {

        $scope.loading = false;
        $scope.curious = $location.search().curious == 'true';
    });
