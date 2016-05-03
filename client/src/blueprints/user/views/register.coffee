angular.module 'throwCat'

.controller "userRegisterCtrl", [
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
    navService.section('register')

    $scope.reg = {}
    $scope.checked = false
    $scope.submitted = false

    $scope.input_pattern = Config.input_pattern

    $scope.check = ->
      if not fsv($scope.check_form, ['login']) or $scope.submitted
        return

      $scope.submitted = true
      console.log $scope.reg
      restUser.doRegisterCaptcha($scope.reg)
      .then (data)->
        if Config.debug
          console.log data
        $scope.checked = true
      .finally ->
        $scope.submitted = false

    $scope.register = ->
      fields = ['captcha', 'key', 'passwd', 'passwd2']
      if not fsv($scope.reg_form, fields) or $scope.submitted
        return

      $scope.submitted = true
      restUser.doRegister($scope.reg)
      .then (data)->
        do_login()
      .finally ->
        $scope.submitted = false

    do_login = (token)->
      Auth.login token
      $location.path '/'

]