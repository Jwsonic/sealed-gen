'use strict';

function httpGet($http, url) {
  return $http.get(url).then(function(response) {
    return response.data;
  });
}

/**
 * @ngdoc overview
 * @name sealedGenApp
 * @description
 * # sealedGenApp
 *
 * Main module of the application.
 */
var app = angular.module('sealedGenApp', [
  'ngAnimate',
  'ngCookies',
  'ngResource',
  'ngRoute',
  'ngSanitize',
  'ngTouch'
]).config(function($routeProvider) {
  console.log('hello');
  $routeProvider
    .when('/', {
      templateUrl: 'views/main.html',
      controller: 'MainCtrl',
      resolve: {
        factions: ['$http',
          function($http) {
            return httpGet($http, 'factions.json');
          }
        ],
        cards: ['$http',
          function($http) {
            return httpGet($http, 'cards.json');
          }
        ]
      }
    })
    .otherwise({
      redirectTo: '/'
    });
}).config([
  '$compileProvider',
  function($compileProvider) {
    console.log('hello');
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|blob|chrome-extension):/);
    // Angular before v1.2 uses $compileProvider.urlSanitizationWhitelist(...)
  }
]);