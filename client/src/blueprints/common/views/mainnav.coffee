angular.module 'throwCat'

.controller 'mainNavCtrl', [
  '$scope'
  '$location'
  '$mdSidenav'
  '$mdMedia'
  'Auth'
  'navService'
  'navDefault'
  (
    $scope
    $location
    $mdSidenav
    $mdMedia
    Auth
    navService
    navDefault
  ) ->
    $scope.navs = navs = navService
    singleMode = false
    navDefault.load()

    $scope.isLockedOpen = (hasNav)->
      return $mdMedia('gt-md')

    $scope.isOpen = ->
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

    $scope.isShow = (menu) ->
      if singleMode
        return navs.activatedMenus == menu or $scope.isCurrent(menu)
      else
        return navs.activatedMenus.indexOf(menu) > -1 or $scope.isCurrent(menu)

    $scope.isCurrent = (menu) ->
      return navs.currSection is menu

    $scope.toggleNav = (nav)->
      $mdSidenav(nav).toggle()

    $scope.go = (route)->
      if route
        $location.path route
        $mdSidenav('main_nav').close()
]