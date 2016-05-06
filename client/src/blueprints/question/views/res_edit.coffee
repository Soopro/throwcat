angular.module 'throwCat'

.controller "questionResEditCtrl", [
  '$scope'
  'dialog'
  'type'
  'resource'
  (
    $scope
    dialog
    type
    resource
  ) ->
    if typeof(angular.translate) is 'function'
      $scope._ = angular.translate

    $scope.resource = resource
    $scope.resource_type = type

    $scope.trash = (resource)->
      resource._deleted = true
      dialog.hide(resource)

    $scope.save = (resource)->
      dialog.hide(resource)

    $scope.close = ->
      dialog.cancel()

]