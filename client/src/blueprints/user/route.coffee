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
    dir = 'blueprints/user/views'
    bp = ''

    resolve =
      global: gResolveProvider.resolve

    outer_resolve =
      outer: outerResolveProvider.resolve


    # outter
    $routeProvider
    .when '/login',
      templateUrl: dir+'/login.html'
      controller: 'userLoginCtrl'
      resolve: outer_resolve

    .when '/register',
      templateUrl: dir+'/register.html'
      controller: 'userRegisterCtrl'
      resolve: outer_resolve

    .when '/recovery',
      templateUrl: dir+'/recovery.html'
      controller: 'userRecoveryCtrl'
      resolve: outer_resolve

    .when '/exit',
      template: ''
      controller: 'userExitCtrl'

    # logged
    .when '/account',
      templateUrl: dir+'/account.html'
      controller: 'userAccountCtrl'
      resolve: resolve

    return
]