'use strict';

angular.module('UserManagementApp', [
  'UserManagementApp.controllers','ngRoute','ngSanitize'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.
	when("/login", {templateUrl: "partials/login.html", controller: "loginController"}).
	when("/register", {templateUrl: "partials/reg.html", controller: "loginController"}).
        when("/landing", {templateUrl: "partials/landing.html", controller: "loginController"}).
	otherwise({redirectTo: '/login'});
}]);
