'use strict';

/**
 * @ngdoc function
 * @name sealedGenApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the sealedGenApp
 */
angular.module('sealedGenApp')
  .controller('MainCtrl', function($scope, factions, cards) {
    $scope.factions = factions;
    $scope.cards = cards;
    $scope.faction = $scope.factions[0];

    $scope.buildPool = function() {
      $scope.buildingPool = true;

      // var content = 'file content';
      // var blob = new Blob([content], {
      //   type: 'text/plain'
      // });
      // $scope.url = (window.URL || window.webkitURL).createObjectURL(blob);

      $scope.buildingPool = false;
      $scope.poolUrl = 'stuff';
      $scope.poolName = 'stuff.txt';
    };
  });
