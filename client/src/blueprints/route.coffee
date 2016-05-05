angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    resolve =
      global: gResolveProvider.resolve

    $routeProvider
    .when '/404',
      templateUrl: 'blueprints/404.html'
      controller: 'errorPageCtrl'
      resolve: resolve


    .otherwise redirectTo: '/404'

    return
]

.controller "errorPageCtrl", [
  'navService'
  'Config'
  (
    navService
    Config
  ) ->
    navService.section('404', Config.route.portal)
]