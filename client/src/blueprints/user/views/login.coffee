angular.module 'throwCat'

.controller "userLoginCtrl", [
  '$scope'
  '$location'
  'restUser'
  'navService'
  'Auth'
  'flash'
  'Config'
  'fsv'
  (
    $scope
    $location
    restUser
    navService
    Auth
    flash
    Config
    fsv
  ) ->
    navService


    $scope.auth = {}
    $scope.submitted = false

    $scope.login = ->
      if not fsv($scope.auth_form, ['log', 'pwd']) or $scope.submitted
        return

      # local develop only
      # remove it after backend is ready.
      do_login('xxx')
      return

      $scope.submitted = true
      do_auth = new restUser.auth($scope.auth)
      do_auth.$post()
      .then (data)->
        do_login()
      .finally ->
        $scope.submitted = false

    do_login = (token)->
      Auth.login token
      $location.path '/'

]