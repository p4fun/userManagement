'use strict';
angular.module('UserManagementApp.controllers', []).
controller('loginController', function($scope,$location,$http) {
    $scope.loginSubmit = function(){ 
	var emailParam = $scope.userEmail;
        var passParam = $scope.userPass;
        var dataObj = {
	  email : emailParam,
	  pass : passParam
	};	
	var res = $http.post('/auth', dataObj);
	res.success(function(data, status, headers, config) {
	  $scope.message = data;
	  console.log(data.id);
          $location.url('/landing').search({param: data.id});
	});
	res.error(function(data, status, headers, config) {
	  alert( "failure message: " + JSON.stringify({data: data}));
	});		
   };
    $scope.userId=null;
    $scope.listOfUsers=null;
    $scope.createAccount = function(){$location.url('/register');};
    $scope.regSubmit = function(){ };
    $scope.regReset = function(){};
    $scope.initLanding = function(){
	 var url = $location.url();
	 var id = url.split('=')[1];
	 $scope.userId=id;
    };
    $scope.listOfUsers = function(){
	var res = $http.get('/usersHtml');
        res.success(function(data, status, headers, config) {
	  $scope.result = data;
	});
    }
    $scope.listOfMessages = function(){
        var dataObj = {
	  id : $scope.userId
	};	
	var res = $http.post('/messageHtml',dataObj);
        res.success(function(data, status, headers, config) {
	  $scope.result = data;
	});
    }
});
