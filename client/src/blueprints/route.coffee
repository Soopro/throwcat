angular.module 'throwCat'

.config [
  '$routeProvider'
  (
    $routeProvider
  ) ->

    $routeProvider
    .when '/404',
      templateUrl: 'blueprints/404.html'
      controller: 'errorPageCtrl'

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