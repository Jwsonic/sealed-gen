'use strict';

/**
 * @ngdoc function
 * @name sealedGenApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the sealedGenApp
 */
angular.module('sealedGenApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
