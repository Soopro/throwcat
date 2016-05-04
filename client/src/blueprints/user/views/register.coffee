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
      $scope.captcha()

    $scope.captcha = ->
      $scope.submitted = true
      restUser.doRegisterCaptcha($scope.reg)
      .then (data)->
        if Config.debug
          console.log data
        $scope.checked = true
      .finally ->
        $scope.submitted = false

    $scope.register = ->
      fields = ['captcha', 'slug', 'passwd', 'passwd2']
      if not fsv($scope.reg_form, fields) or $scope.submitted
        return

      $scope.submitted = true
      restUser.doRegister($scope.reg)
      .then (data)->
        $location.path Config.route.auth
      .finally ->
        $scope.submitted = false



]