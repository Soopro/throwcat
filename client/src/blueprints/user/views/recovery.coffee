angular.module 'throwCat'

.controller "userRecoveryCtrl", [
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
    navService.section('recovery')

    $scope.rec = {}
    $scope.checked = false
    $scope.submitted = false

    $scope.input_pattern = Config.input_pattern

    $scope.check = ->
      if not fsv($scope.check_form, ['login']) or $scope.submitted
        return

      $scope.submitted = true
      restUser.doRecoveryCaptcha($scope.rec)
      .then (data)->
        if Config.debug
          console.log data
        $scope.checked = true
      .finally ->
        $scope.submitted = false

    $scope.recovery = ->
      fields = ['captcha', 'passwd', 'passwd2']
      if not fsv($scope.rec_form, fields) or $scope.submitted
        return

      $scope.submitted = true
      restUser.doRecovery($scope.rec)
      .then (data)->
        $location.path Config.route.auth
      .finally ->
        $scope.submitted = false

]