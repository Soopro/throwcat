angular.module 'throwCat'

.controller "userLoginCtrl", [
  '$scope'
  '$location'
  'restAgent'
  'Auth'
  'flash'
  'Config'
  'fsv'
  (
    $scope
    $location
    restAgent
    Auth
    flash
    Config
    fsv
  ) ->
    $scope.auth = {}
    $scope.submitted = false

    $scope.submit = ->
      if not fsv($scope.auth_form, ['pin']) or $scope.submitted
        return

      $scope.submitted = true
      do_auth = new restAgent.auth($scope.auth)
      do_auth.$post()
      .then (data)->
        Auth.login data.token
        $location.path '/'
      .finally ->
        $scope.submitted = false

]