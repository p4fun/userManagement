'use strict';
angular.module('UserManagementApp.controllers', []).
controller('driversController', function($scope,$location) {
    $scope.loginSubmit = function(){ alert("submit clicked");};
    $scope.createAccount = function(){ alert("createAccount clicked");$location.url('/register');};
    $scope.regSubmit = function(){ alert("regSubmit clicked");};
    $scope.regReset = function(){ alert("regreset clicked");};
});
