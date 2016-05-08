angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  '$location'
  'restCat'
  'navService'
  'image'
  (
    $scope
    $location
    restCat
    navService
    image
  ) ->
    navService.section('dashboard')

    $scope.questions = restCat.question.query()
    $scope.image = image

    $scope.create = ->
      $scope.enter('new')

    $scope.enter = (entry_id)->
      $location.path '/question/'+entry_id
]