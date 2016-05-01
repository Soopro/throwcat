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
    .when '/'+bp+'/register',
      templateUrl: dir+'/register.html'
      controller: 'userRegisterCtrl'

    $routeProvider
    .when '/'+bp+'/recovery',
      templateUrl: dir+'/recovery.html'
      controller: 'userRecoveryCtrl'

    $routeProvider
    .when '/'+bp+'/exit',
      template: ''
      controller: 'userExitCtrl'

    return
]