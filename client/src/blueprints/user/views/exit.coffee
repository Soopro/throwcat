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
    console.log Config.route.auth
    $location.path Config.route.auth
]