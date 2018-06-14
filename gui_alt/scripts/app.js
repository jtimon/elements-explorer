'use strict';

/**
 * @ngdoc overview
 * @name rpcExplorerApp
 * @description
 * # rpcExplorerApp
 *
 * Main module of the application.
 */
angular
  .module('rpcExplorerApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/chain/:chain/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/block/:block', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/block-height/:block_height', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/tx/:txid', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/stats', {
        templateUrl: 'views/stats.html',
        controller: 'StatsCtrl',
        controllerAs: 'stats',
        reloadOnSearch: false
      })
      .when('/chain/:chain/queue', {
        templateUrl: 'views/mempoolstats.html',
        controller: 'MempoolStatsCtrl',
      })
      .when('/chain/:chain/address', {
        templateUrl: 'views/address.html',
        controller: 'AddressCtrl',
      })
      .when('/chain/:chain/faucet', {
        templateUrl: 'views/faucet.html',
        controller: 'FaucetCtrl',
      })
      .when('/chain/:chain/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .otherwise({
        redirectTo: '/chain/bitcoin'
      });
  });
