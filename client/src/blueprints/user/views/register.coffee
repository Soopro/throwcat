angular.module 'throwCat'

.controller "userRegisterCtrl", [
  '$scope'
  '$location'
  'restUser'
  'Auth'
  'flash'
  'Config'
  'fsv'
  (
    $scope
    $location
    restUser
    Auth
    flash
    Config
    fsv
  ) ->
    $scope.reg = {}
    $scope.checked = false
    $scope.submitted = false

    $scope.input_pattern = Config.input_pattern

    $scope.check = ->
      if not fsv($scope.check_form, ['log']) or $scope.submitted
        return

      # local develop only
      # remove it after backend is ready.
      $scope.checked = true
      return

      $scope.submitted = true
      do_auth = new restUser.check($scope.reg)
      do_auth.$post()
      .then (data)->
        $scope.checked = true
      .finally ->
        $scope.submitted = false

    $scope.register = ->
      if not fsv($scope.reg_form, ['log', 'code']) or $scope.submitted
        return

      # local develop only
      # remove it after backend is ready.
      $scope.register_able = true
      return

      $scope.submitted = true
      do_auth = new restUser.register($scope.reg)
      do_auth.$post()
      .then (data)->
        do_login()
      .finally ->
        $scope.submitted = false

    do_login = (token)->
      Auth.login token
      $location.path '/'

]