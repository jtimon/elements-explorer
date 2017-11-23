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
      .when('/chain/:chain/mempoolstats', {
        templateUrl: 'views/mempoolstats.html',
        controller: 'MempoolStatsCtrl',
      })
      .when('/chain/:chain/mempool', {
        templateUrl: 'views/mempool.html',
        controller: 'MempoolCtrl',
      })
      .when('/chain/:chain/mempool/entry/:txid', {
        templateUrl: 'views/mempool.html',
        controller: 'MempoolCtrl',
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
