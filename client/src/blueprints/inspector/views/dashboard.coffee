angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  'restCat'
  (
    $scope
    restCat
  ) ->
    $scope.inspector = restCat.inspector.query()
]