angular.module 'throwCat'

.controller "questionResEditCtrl", [
  '$scope'
  '$filter'
  'restMedia'
  'dialog'
  'image'
  'type'
  'resource'
  (
    $scope
    $filter
    restMedia
    dialog
    image
    type
    resource
  ) ->
    if typeof(angular.translate) is 'function'
      $scope._ = angular.translate

    $scope.image = image
    $scope.resource = resource
    $scope.resource_type = type

    $scope.trash = (resource)->
      resource._deleted = true
      dialog.hide(resource)

    $scope.save = (resource)->
      dialog.hide(resource)

    $scope.close = ->
      dialog.cancel()

    # media
    $scope.mediafiles = restMedia.media.query()

    # more
    $scope.paged = 1

    $scope.has_more = (mediafiles, paged, prepage)->
      curr_list = $filter('paginator')(mediafiles, paged, prepage)
      return curr_list.length < mediafiles.length

    $scope.more = (mediafiles, paged, prepage)->
      if $scope.has_more(mediafiles, paged)
        $scope.paged += 1
      else
        return false
]