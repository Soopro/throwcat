angular.module 'throwCat'

.controller "userLoginCtrl", [
  '$scope'
  '$location'
  'restUser'
  'navService'
  'Auth'
  'Config'
  'flash'
  'fsv'
  (
    $scope
    $location
    restUser
    navService
    Auth
    Config
    flash
    fsv
  ) ->
    navService.section('login')

    $scope.auth = {}
    $scope.submitted = false

    $scope.input_pattern = Config.input_pattern

    $scope.login = ->
      if not fsv($scope.auth_form, ['login', 'passwd']) or $scope.submitted
        return

      $scope.submitted = true
      restUser.doLogin($scope.auth)
      .then (data)->
        Auth.login data.token
        $location.path '/'
      .finally ->
        $scope.submitted = false

]