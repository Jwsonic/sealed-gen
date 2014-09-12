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

      var pool = [];

      for (var i = 0; i < 5; i++) {
        Array.prototype.push.apply(pool, makePack($scope.cards));
      }

      Array.prototype.push.apply(pool, makePromoPack($scope.faction.cards));

      // var content = 'file content';
      // var blob = new Blob([content], {
      //   type: 'text/plain'
      // });
      // $scope.url = (window.URL || window.webkitURL).createObjectURL(blob);

      var poolFile = makePoolFile(pool);

      $scope.buildingPool = false;
      $scope.poolUrl = (window.URL || window.webkitURL).createObjectURL(poolFile);

      console.log($scope.poolUrl);
      $scope.poolName = $scope.faction.name + '.cod';
    };

    function makePoolFile(cards) {
      var fileFmt = '<?xml version="1.0" encoding="UTF-8"?>\n<cockatrice_deck version="1">\n<deckname></deckname>\n<comments></comments>\n<zone name="main"></zone>\n<zone name="side">\n%s</zone>\n</cockatrice_deck>';

      var names = _.countBy(cards, function(card) {
        return card;
      });

      var cardStr = _.map(names, function(num, name) {
        return sprintf('<card number="%s" price="0" name="%s"/>\n', num, name);
      }).join('');

      return new Blob([sprintf(fileFmt, cardStr)], {
        type: 'text/xml'
      });
    }

    //Makes a normal pack
    function makePack(allcards) {
      var cards = [];

      if (getRandomInt(0, 8) == 0) {
        cards.push(randomElement(allcards.mythic));
      } else {
        cards.push(randomElement(allcards.rare));
      }

      for (var i = 0; i < 3; i++) {
        cards.push(randomElement(allcards.uncommon));
      }

      for (var i = 0; i < 10; i++) {
        cards.push(randomElement(allcards.common));
      }

      cards.push(randomElement(allcards.land));

      return cards;
    }

    function makePromoPack(factionCards) {
      var cards = [];

      cards.push(randomElement(factionCards.promo));

      for (var i = 0; i < 3; i++) {
        cards.push(randomElement(factionCards.uncommon));
      }

      for (var i = 0; i < 10; i++) {
        cards.push(randomElement(factionCards.common));
      }

      cards.push(randomElement(factionCards.land));

      return cards;
    }

    function getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min)) + min;
    }

    function randomElement(array) {
      return array[getRandomInt(0, array.length)];
    }
  });