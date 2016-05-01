angular.module 'throwCat'

.config [
  '$routeProvider'
  (
    $routeProvider
  ) ->
    bp = "overseer"
    dir = "blueprints/overseer/views"

    $routeProvider
    .when '/',
      templateUrl: dir+'/dashboard.html'
      controller: 'dashboardCtrl'

]