angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  'restCat'
  'navService'
  'image'
  (
    $scope
    restCat
    navService
    image
  ) ->
    navService.section('dashboard')

    $scope.questions = restCat.question.query()
    $scope.image = image
]