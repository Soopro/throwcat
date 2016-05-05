angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  '$location'
  'restCat'
  'navService'
  'dialog'
  'image'
  (
    $scope
    $location
    restCat
    navService
    dialog
    image
  ) ->
    navService.section('dashboard')

    $scope.questions = restCat.question.query()
    $scope.image = image

    $scope.go = (entry_id)->
      $location.path '/question/'+entry_id
]