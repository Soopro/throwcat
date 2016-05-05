angular.module 'throwCat'

.config [
  '$routeProvider'
  'gResolveProvider'
  (
    $routeProvider
    gResolveProvider
  ) ->
    bp = "question"
    dir = "blueprints/question/views"

    resolve =
      global: gResolveProvider.resolve

    $routeProvider
    .when '/',
      templateUrl: dir+'/dashboard.html'
      controller: 'dashboardCtrl'
      resolve: resolve

    $routeProvider
    .when '/'+bp+'/:question_id',
      templateUrl: dir+'/question.html'
      controller: 'questionCtrl'
      resolve: resolve

]