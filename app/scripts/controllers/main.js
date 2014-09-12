'use strict';

/**
 * @ngdoc function
 * @name sealedGenApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sealedGenApp
 */
angular.module('sealedGenApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
