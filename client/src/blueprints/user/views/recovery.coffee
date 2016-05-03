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

      # local develop only
      # remove it after backend is ready.
      $scope.checked = true
      return

      $scope.submitted = true
      do_auth = new restUser.check($scope.rec)
      do_auth.$post()
      .then (data)->
        $scope.checked = true
      .finally ->
        $scope.submitted = false

    $scope.recovery = ->
      fields = ['captcha', 'passwd', 'passwd2']
      if not fsv($scope.rec_form, fields) or $scope.submitted
        return

      $scope.submitted = true
      do_auth = new restUser.recovery($scope.rec)
      do_auth.$post()
      .then (data)->
        $location.path Config.route.auth
      .finally ->
        $scope.submitted = false

]