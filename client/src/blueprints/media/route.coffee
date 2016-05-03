angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    bp = "media"
    dir = "blueprints/media/views"

    resolve =
      global: gResolveProvider.resolve

    $routeProvider
    .when bp,
      templateUrl: dir+'/media.html'
      controller: 'mediaCtrl'
      resolve: resolve

]