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
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/block/:block', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/chain/:chain/tx/:txid', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
