angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    bp = "inspector"
    dir = "blueprints/inspector/views"

    resolve =
      global: gResolveProvider.resolve

    $routeProvider
    .when '/',
      templateUrl: dir+'/dashboard.html'
      controller: 'dashboardCtrl'
      resolve: resolve

]