angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    dir = 'blueprints/user/views'
    bp = 'user'

    resolve =
      global: gResolveProvider.resolve


    # outter
    $routeProvider
    .when '/login',
      templateUrl: dir+'/login.html'
      controller: 'userLoginCtrl'

    .when '/register',
      templateUrl: dir+'/register.html'
      controller: 'userRegisterCtrl'

    .when '/recovery',
      templateUrl: dir+'/recovery.html'
      controller: 'userRecoveryCtrl'

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