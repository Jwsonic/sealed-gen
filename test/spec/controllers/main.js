'use strict';

describe('Controller: MainCtrl', function() {

  // load the controller's module
  beforeEach(module('sealedGenApp'));

  var MainCtrl,
    scope,
    cards;

  // Initialize the controller and a mock scope
  beforeEach(inject(function($controller, $rootScope, $http) {
    scope = $rootScope.$new();
    cards = $http.get('cards.json').then(function(response) {
      return response.data;
    });
    MainCtrl = $controller('MainCtrl', {
      $scope: scope,
      cards: cards
    });
  }));

  // it('should attach cards to the scope', function() {
  //   expect(scope.cards.length).toBe(0);
  // });
});
