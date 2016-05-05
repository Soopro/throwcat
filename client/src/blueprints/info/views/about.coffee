angular.module 'throwCat'

.controller "infoAboutCtrl", [
  '$scope'
  '$location'
  'restUser'
  'navService'
  'App'
  'Auth'
  'Config'
  'flash'
  'fsv'
  (
    $scope
    $location
    restUser
    navService
    App
    Auth
    Config
    flash
    fsv
  ) ->
    navService.section('about')

    $scope.auth = {}
    $scope.submitted = false

    $scope.input_pattern = Config.input_pattern

    $scope.app =
      version: App.version
      artisan: App.artisan
      github: App.github
]