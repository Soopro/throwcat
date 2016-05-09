angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    bp = "info"
    dir = "blueprints/info/views"

    resolve =
      global: gResolveProvider.resolve

    $routeProvider
    .when '/'+bp+'/about',
      templateUrl: dir+'/about.html'
      controller: 'infoAboutCtrl'
      resolve: resolve

]