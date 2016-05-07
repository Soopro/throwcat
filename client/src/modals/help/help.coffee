angular.module 'throwCat'

.controller 'helpModalCtrl', [
  '$scope'
  'dialog'
  'help'
  (
    $scope
    dialog
    help
  ) ->
    if typeof(angular.translate) is 'function'
      $scope._ = angular.translate

    if not angular.endswith(help, '.tmpl.html')
      $scope.content = $scope._(help)
      reg_html = /<\/[a-z][\s\S]*>/i
      if not reg_html.test(content)
        $scope.content = "<p>"+$scope.content+"</p>"
    else
      $scope.tmpl = help

    $scope.ok = ->
      dialog.hide()
]

.service 'helpModal', [
  'dialog'
  (
    dialog
  ) ->
    (content)->
      if not content
        return

      dialog.show
        controller: 'helpModalCtrl'
        templateUrl: 'modals/help/help.tmpl.html'
        locals:
          help: content
      , true
]