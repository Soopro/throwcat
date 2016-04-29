angular.module 'throwCat'

.controller "dashboardCtrl", [
  '$scope'
  'restAgent'
  (
    $scope
    restAgent
  ) ->
    $scope.status = restAgent.status.get()
]