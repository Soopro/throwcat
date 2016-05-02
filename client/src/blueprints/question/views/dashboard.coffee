angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  'restCat'
  'image'
  (
    $scope
    restCat
    image
  ) ->
    $scope.questions = restCat.question.query()
    $scope.image = image
]