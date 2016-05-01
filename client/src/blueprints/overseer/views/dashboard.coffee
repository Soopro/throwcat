angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  'restCat'
  (
    $scope
    restCat
  ) ->
    # $scope.status = restCat.status.get()
]