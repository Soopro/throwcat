angular.module 'throwCat'

.controller 'mainNavCtrl', [
  '$scope'
  '$location'
  '$mdSidenav'
  '$mdMedia'
  'Auth'
  'navService'
  (
    $scope
    $location
    $mdSidenav
    $mdMedia
    Auth
    navService
  ) ->
    $scope.navs = navs = navService
    singleMode = false

    $scope.is_locked_open = (hasNav)->
      return $mdMedia('gt-md')

    $scope.is_open = ->
      is_open = $mdSidenav('main_nav').isOpen()
      is_locked_open = $scope.isLockedOpen()
      if is_open and is_locked_open
        $mdSidenav('main_nav').close()
      return is_open

    $scope.toggle = (menu) ->
      if singleMode
        if navs.activatedMenus != menu
          navs.activatedMenus = menu
        else
          navs.activatedMenus = ''
      else
        angular.toggleList(navs.activatedMenus, menu)

    $scope.is_show = (menu) ->
      if singleMode
        return navs.activatedMenus == menu or $scope.is_current(menu)
      else
        activated = navs.activatedMenus.indexOf(menu) > -1
        return activated or $scope.is_current(menu)

    $scope.is_current = (menu) ->
      return navs.currSection is menu

    $scope.toggle_nav = (nav)->
      $mdSidenav(nav).toggle()

    $scope.go = (route)->
      if route
        $location.path route
        $mdSidenav('main_nav').close()
]