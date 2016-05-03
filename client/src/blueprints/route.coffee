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
      resolve: resolve


    .otherwise redirectTo: '/404'

    return
]