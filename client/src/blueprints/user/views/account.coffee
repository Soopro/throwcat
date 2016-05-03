angular.module 'throwCat'

.controller "userAccountCtrl", [
  '$scope'
  '$location'
  'restUser'
  'navService'
  'flash'
  'fsv'
  (
    $scope
    $location
    restUser
    navService
    flash
    fsv
  ) ->
    navService.section('account/profile')

    $scope.submitted = false

    $scope.save = ->
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