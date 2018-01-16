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
        $scope.start_height = SrvUtil.ParseNatural($location.search().start_height);
        $scope.end_height = SrvUtil.ParseNatural($location.search().end_height);
        if ($scope.start_height > $scope.end_height) {
            $scope.end_height = $scope.start_height;
        }

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
            if ($scope.address) {
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

        $scope.SearchAddress();
    });
