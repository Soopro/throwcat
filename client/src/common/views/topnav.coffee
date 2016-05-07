angular.module 'throwCat'

.controller 'topNavCtrl', [
  '$scope'
  '$route'
  '$location'
  '$mdSidenav'
  '$mdMedia'
  'navService'
  'Config'
  'Auth'
  'supLocales'
  (
    $scope
    $route
    $location
    $mdSidenav
    $mdMedia
    navService
    Config
    Auth
    supLocales
  ) ->
    $scope.navs = navService
    $scope.locales = Config.locales

    $scope.toggle_nav = (nav) ->
      $mdSidenav(nav).toggle()

    $scope.is_current_lang = (locale) ->
      current = supLocales.get()
      return supLocales.match(locale.code, current)

    $scope.use_lang = (locale) ->
      supLocales.set(locale.code)
      $route.reload()

    $scope.is_logged = ->
      return Auth.is_logged()

    $scope.exit = ->
      $location.path Config.route.exit

    $scope.go = (route)->
      if route
        $location.path route

    $scope.reload = ->
      location.reload(true)
]
