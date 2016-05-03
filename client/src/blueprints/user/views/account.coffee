angular.module 'throwCat'

.controller "userAccountCtrl", [
  '$scope'
  '$location'
  'supChain'
  'restUser'
  'navService'
  'Auth'
  'flash'
  'fsv'
  (
    $scope
    $location
    supChain
    restUser
    navService
    Auth
    flash
    fsv
  ) ->
    navService.section('account/profile')

    $scope.submitted = false
    $scope.show_secret = false

    $scope.user = new restUser.profile()
    $scope.secret = new restUser.secret()
    $scope.pwd = new restUser.password()

    supChain()
    .then ->
      $scope.user.$get()
    .then ->
      $scope.secret.$get()


    $scope.toggle_secret = ->
      $scope.show_secret = not $scope.show_secret

    $scope.save_pwd = ->
      fields = ['passwd', 'new_passwd', 'new_passwd2']
      if not fsv($scope.security_form, fields) or $scope.submitted
        return

      $scope.submitted = true
      $scope.pwd.$change()
      .then (data)->
        Auth.login data.token
        $scope.security_form.$setPristine()
        $scope.security_form.$setUntouched()
        flash 'Password has been changed.'
        return
      .finally ->
        $scope.submitted = false


    $scope.reset_secret = ->
      $scope.submitted = true
      $scope.secret.$reset()
      .then (data)->
        flash 'AppSecret has been reseted.'
        return
      .finally ->
        $scope.submitted = false

]