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
    bp = "info"
    dir = "blueprints/info/views"

    resolve =
      global: gResolveProvider.resolve

    outer_resolve =
      outer: outerResolveProvider.resolve

    $routeProvider
    .when '/'+bp+'-open/about',
      templateUrl: dir+'/about.html'
      controller: 'infoAboutCtrl'
      resolve: outer_resolve

    $routeProvider
    .when '/'+bp+'/about',
      templateUrl: dir+'/about.html'
      controller: 'infoAboutCtrl'
      resolve: resolve

]