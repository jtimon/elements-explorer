'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:MempoolCtrl
 * @description
 * # MempoolCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('MempoolCtrl', function ($scope, $routeParams, SrvUtil, SrvChain, SrvBackend) {

        SrvChain.set($routeParams.chain);

        $scope.loading = true;

        function mempooltxsCallback(data) {
            $scope.mempooltxs = SrvUtil.GetResult(data);
        };
        $scope.LoadMempoolTxs = function() {
            $scope.loading = true;
            SrvBackend.RpcCall("getrawmempool", {})
                .then(mempooltxsCallback)
                .then(function() {
                    $scope.loading = false;
                })
                .catch(SrvUtil.errorCallbackScoped($scope));
        };

        $scope.LoadMempoolTxs();
        $scope.loading = false;
    });
