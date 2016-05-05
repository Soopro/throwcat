angular.module 'throwCat'

.controller "questionCtrl", [
  '$scope'
  '$location'
  '$routeParams'
  'restCat'
  'navService'
  'ConfigQs'
  'dialog'
  'image'
  (
    $scope
    $location
    $routeParams
    restCat
    navService
    ConfigQs
    dialog
    image
  ) ->
    navService.section('question', '/')
    question_id = $routeParams.question_id

    $scope.image = image

    if question_id == 'new'
      $scope.question = new restCat.question()
    else
      $scope.question = restCat.question.get()

    $scope.question_types = ConfigQs.question_types

]