angular.module 'throwCat'

.service 'dialog', [
  '$mdDialog'
  '$mdMedia'
  (
    $mdDialog
    $mdMedia
  ) ->
    self = @

    parse_options = (options) ->
      if options.clickOutsideToClose is undefined
        options.clickOutsideToClose = true
      if options.hasBackdrop is undefined
        options.hasBackdrop = true
      if options.fullscreen is undefined
        options.fullscreen = Boolean($mdMedia('sm') or $mdMedia('xs'))
      options.focusOnOpen = Boolean(options.focusOnOpen)
      return options

    @alert = ->
      $mdDialog.alert()

    @confirm = ->
      $mdDialog.confirm()

    @show = (options, force) ->
      return $mdDialog.show(parse_options(options))


    @hide = (data) ->
      $mdDialog.hide(data)

    @cancel = (data) ->
      $mdDialog.cancel(data)

    return @
]