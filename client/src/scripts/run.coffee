angular.module 'throwCat'

.run [
  '$rootScope'
  '$location'
  '$animate'
  'App'
  'Auth'
  'Config'
  'flashWatcher'
  'MediaService'
  (
    $rootScope
    $location
    $animate
    App
    Auth
    Config
    flashWatcher
    MediaService
  ) ->
    console.log "-----------------------------"
    console.log "ThrowCat:", App.version
    console.log "Developers:", App.artisan.join(', ')
    console.log "Github:", App.github
    console.log "-----------------------------"

    # MediaService
    MediaService.config
      max_file_size: Config.max_file_size
      max_image_size: Config.max_image_size
      encoder_options: Config.media_encoder_options

    # flash
    flashWatcher.init()

    isInPathList = (names)->
      for arg in arguments
        pathList = Config.path[arg] or []
        for pth in pathList
          url = $location.url()
          reg = new RegExp pth
          return true if reg.test url
      return false

    # location change lisenter
    $rootScope.$on '$locationChangeStart', ->
      # auth
      if Auth.is_logged()
        $location.path Config.route.portal if isInPathList('outer')
      else
        $location.path Config.route.auth if not isInPathList('outer')

]

