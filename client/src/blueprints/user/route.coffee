angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  'outerResolveProvider'
  (
    $routeProvider
    gResolveProvider
    outerResolveProvider
  ) ->
    dir = "blueprints/user/views"
    bp = "user"

    resolve =
      global: gResolveProvider.resolve

    outer_resolve =
      outer: outerResolveProvider.resolve

    $routeProvider
    .when '/'+bp+'/login',
      templateUrl: dir+'/login.html'
      controller: 'userLoginCtrl'
      resolve: outer_resolve

    $routeProvider
    .when '/'+bp+'/register',
      templateUrl: dir+'/register.html'
      controller: 'userRegisterCtrl'
      resolve: outer_resolve

    $routeProvider
    .when '/'+bp+'/recovery',
      templateUrl: dir+'/recovery.html'
      controller: 'userRecoveryCtrl'
      resolve: outer_resolve

    $routeProvider
    .when '/'+bp+'/exit',
      template: ''
      controller: 'userExitCtrl'

    return
]