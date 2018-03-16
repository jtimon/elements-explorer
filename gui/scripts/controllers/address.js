'use strict';

/**
 * @ngdoc function
 * @name rpcExplorerApp.controller:AddressCtrl
 * @description
 * # AddressCtrl
 * Controller of the rpcExplorerApp
 */
angular.module('rpcExplorerApp')
    .controller('AddressCtrl', function ($scope, $routeParams, $location, SrvUtil, SrvChain, SrvBackend) {

        SrvChain.set($routeParams.chain);
        $scope.loading = false;

        $scope.curious = $location.search().curious == 'true';
        $scope.address = $location.search().address;

        $scope.UpdateAddressArguments = function() {
            if ($scope.address) {
                $location.search('address', $scope.address);
            }
            $scope.start_height = $scope.start_height ? $scope.start_height : 1
            $scope.end_height = $scope.end_height ? $scope.end_height : 1
            if ($scope.start_height > $scope.end_height) {
                $scope.end_height = $scope.start_height;
            }
            $location.search('start_height', $scope.start_height);
            $location.search('end_height', $scope.end_height);
        };

        function SearchAddressCallback(data) {
            var result = SrvUtil.GetResult(data);
            $scope.address_data = JSON.stringify(result, null, 4)
            $scope.receipts = result['receipts'];
            $scope.expenditures = result['expenditures'];
            $scope.loading = false;
        };

        $scope.SearchAddress = function() {
            if ($scope.address && $scope.start_height && $scope.end_height) {
                $scope.loading = true;
                SrvBackend.RpcCall('address', {
                    'start_height': $scope.start_height,
                    'end_height': $scope.end_height,
                    'addresses': [$scope.address]
                })
                    .then(SearchAddressCallback)
                    .catch(SrvUtil.errorCallbackScoped($scope));
            }
        };

        SrvChain.GetChainInfo().then(function(chaininfo) {
            if ($location.search().end_height) {
                $scope.end_height = SrvUtil.ParseNatural($location.search().end_height);
            } else {
                $scope.end_height = chaininfo['blocks'];
            }
            if ($location.search().start_height) {
                $scope.start_height = SrvUtil.ParseNatural($location.search().start_height);
            } else {
                $scope.start_height = Math.max(1, $scope.end_height - 4);
            }
            if ($scope.start_height > $scope.end_height) {
                $scope.end_height = $scope.start_height;
            }
        }).then($scope.SearchAddress);

    });
