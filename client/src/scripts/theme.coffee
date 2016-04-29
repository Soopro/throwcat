angular.module 'throwCat'

.config([
  '$mdThemingProvider'
  (
    $mdThemingProvider
  ) ->

    $mdThemingProvider.theme('default')
    .primaryPalette('indigo')
    .accentPalette('pink')
    return
])
.config [
  '$mdIconProvider'
  ($mdIconProvider) ->
    $mdIconProvider.defaultIconSet '/styles/svg-sprite-icons.svg', 24
    return
]
