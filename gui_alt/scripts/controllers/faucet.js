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
        $scope.address = '';

        $scope.Freecoins = function() {
            SrvBackend.RpcCall('freecoins', {'address': $scope.address})
            .then(function(data) {
                $scope.freecoins = data['data'];
            })
            .catch(SrvUtil.errorCallbackScoped($scope));
        };

        SrvChain.set()
            .then(function() {
                SrvBackend.RpcCall('faucetinfo', {})
                    .then(function(data) {
                        $scope.faucet_info = data['data'];
                    });
            })
            .catch(SrvUtil.errorCallbackScoped($scope));
    });
