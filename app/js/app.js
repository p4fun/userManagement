'use strict';

angular.module('UserManagementApp', [
  'UserManagementApp.controllers','ngRoute'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
	when("/login", {templateUrl: "partials/login.html", controller: "driversController"}).
	when("/register", {templateUrl: "partials/reg.html", controller: "driversController"}).
	otherwise({redirectTo: '/login'});
}]);
