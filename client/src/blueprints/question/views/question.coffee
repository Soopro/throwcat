angular.module 'throwCat'

.controller "questionCtrl", [
  '$scope'
  '$location'
  '$routeParams'
  'restCat'
  'navService'
  'dialog'
  'image'
  (
    $scope
    $location
    $routeParams
    restCat
    navService
    dialog
    image
  ) ->
    navService.section('dashboard')
    question_id = $routeParams.question_id

    $scope.image = image

    if question_id == 'new'
      $scope.question = new restCat.question()
    else
      $scope.question = restCat.question.get()


]