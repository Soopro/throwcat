angular.module 'throwCat'

.config [
  '$routeProvider'
  (
    $routeProvider
  ) ->
    dir = "blueprints/user/views"
    bp = "user"

    $routeProvider
    .when '/'+bp+'/login',
      templateUrl: dir+'/login.html'
      controller: 'userLoginCtrl'

    $routeProvider
    .when '/'+bp+'/exit',
      template: ''
      controller: 'userExitCtrl'

    return
]