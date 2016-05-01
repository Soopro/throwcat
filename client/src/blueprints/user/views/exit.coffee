angular.module 'throwCat'

.controller "userExitCtrl", [
  '$scope'
  '$location'
  'Auth'
  'Config'
  'g'
  (
    $scope
    $location
    Auth
    Config
    g
  ) ->
    g.$clear()
    Auth.logout()
    $location.path Config.route.auth
]