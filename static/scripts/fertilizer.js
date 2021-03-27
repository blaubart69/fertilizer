angular.module('fertilizer', ['ngWebsocket'])
.controller('FertilizerController', function($scope, $websocket) {	
	$scope.data = {
		fertilizerImpulsePerHa: 50,
		distanceImpulePer100M:  200
	};
	$scope.response = {
		distance: 0,
		amount: 0,
		impulsesOfDistance: 0,
		impulsesOfAmount: 0
	};
	
    this.stop = function() {
	};
    this.perform = function(direction) {
	};
    this.applyChanges = function() {
	};

    var ws = $websocket.$new({
        url: 'ws://localhost:12345',
        reconnect: true // it will reconnect after 2 seconds
    });

    ws.$on('$open', function () {
        console.log('Here we are and I\'m pretty sure to get back here for another time at least!');
    })
    .$on('$close', function () {
        console.log('Got close, damn you silly wifi!');
    });

    console.log("initialize controller");
});