angular.module 'throwCat'

.config [
  '$routeProvider'
  (
    $routeProvider
  ) ->
    $routeProvider
    .when '/404',
      templateUrl: 'blueprints/404.html'

    .otherwise redirectTo: '/404'

    return
]