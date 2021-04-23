angular.module('fertilizer', [])
    .controller('FertilizerController', function ($scope, $http, $interval) {
        // initialize the content type of post request with text/plaien
        // TO AVOID triggering the pre-flight OPTIONS request
        $http.defaults.headers.post["Content-Type"] = "text/plain";

        $scope.fertilizer = 'Kali';
        $scope.fertilizers = ['Kali', 'Phosphor', 'Harnstoff', 'KAS'];
        $scope.data = {
            amountPerArea: 50,
            fertilizer: 'Kali',
            gpioDistance: 12,
            gpioAmount: 13
        };
        $scope.response = {
            distance: 0,
            distancePerDay: 0,
            amount: 0,
            amountPerDay: 0,
            calculated: 0
        };

        const handleResponse = function (response) {
            console.log(response);
            if (response.status == 200) {
                console.log('data', response.data);
                $scope.response = response.data;
                $scope.data.fertilizer = response.data.fertilizer;
            }
        };
        this.stop = function () {
            $http.get('/stop').then(handleResponse);
        };
        this.reset = function () {
            $http.get('/reset').then(handleResponse);
        };
        this.calculate = function () {
            $http.get('/calculate').then(handleResponse);
        };
        this.applyChanges = function () {
            $scope.data.fertilizer = $scope.fertilizer;
            $http.post('/applyChanges', $scope.data).then(handleResponse);
        };

        var stop;
        this.startCalculation = function() {
            if (angular.isDefined(stop)) return;
  
            stop = $interval(this.calculate, 2500);
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