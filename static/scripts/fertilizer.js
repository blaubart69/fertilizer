angular.module('fertilizer', [])
    .controller('FertilizerController', function ($scope, $http, $interval) {
        // initialize the content type of post request with text/plaien
        // TO AVOID triggering the pre-flight OPTIONS request
        $http.defaults.headers.post["Content-Type"] = "text/plain";

        $scope.fertilizers = ['Kali', 'Phosphor', 'Harnstoff', 'KAS'];
        $scope.data = {
            amountPerArea: 50,
            fertilizer: 'Kali',
            gpioDistance: 12,
            gpioAmount: 13
        };
        $scope.response = {
            distance: 0,
            amount: 0,
            calculated: 0
        };

        this.stop = function () {
            $http.get('/stop').then(this.handleResponse);
        };
        this.reset = function () {
            $http.get('/reset').then(this.handleResponse);
        };
        this.calculate = function () {
            $http.get('/calculate').then(this.handleResponse);
        };
        this.applyChanges = function () {
            $http.post('/applyChanges', $scope.data).then(this.handleResponse);
        };

        this.handleResponse = function (response) {
            console.log(response);
            if (response.status == 200) {
                console.log('data', response.data);
                $scope.response = response.data;
            }
        };

        var stop;
        this.startCalculation = function() {
            // Don't start a new fight if we are already fighting
            if (angular.isDefined(stop)) return;
  
            stop = $interval(this.calculate, 60000);
        };
        this.stopCalculation = function() {
            if (angular.isDefined(stop)) {
              $interval.cancel(stop);
              stop = undefined;
            }
        };
        // Make sure that the interval is destroyed too
        $scope.$on('$destroy', this.stopCalculation);

        this.startCalculation();
        console.log("initialize controller");
    });