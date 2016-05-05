angular.module 'throwCat'

.controller "questionCtrl", [
  '$scope'
  '$location'
  '$routeParams'
  'restCat'
  'navService'
  'Config'
  'ConfigQs'
  'fsv'
  'image'
  'dialog'
  'flash'
  (
    $scope
    $location
    $routeParams
    restCat
    navService
    Config
    ConfigQs
    fsv
    image
    dialog
    flash
  ) ->
    navService.section('question', '/')
    question_id = $routeParams.question_id

    $scope.submitted = false

    $scope.image = image

    if question_id == 'new'
      $scope.question = new restCat.question
        resources: []
    else
      $scope.question = restCat.question.get()
      $scope.question.$promise
      .catch (data)->
        $location.path Config.route.error

    $scope.question_types = ConfigQs.question_types

    $scope.save = ->
      fields = ['title', 'type', 'desc']
      if not fsv($scope.info_form, fields) or $scope.submitted
        return

      if $scope.question.resources.length <= 0
        flash 'Question need less one resource.', true
        return

      return
      $scope.submitted = true
      $.scope.question.$save()
      .then ->
        flash 'Question has been saved.'
        return
      .finally ->
        $scope.submitted = false


    $scope.trash = ->
      if $scope.submitted
        return
      $scope.submitted = true
      $.scope.question.$remove()
      .then ->
        flash 'Question has been deleted.'
        return
      .finally ->
        $scope.submitted = false

    # resources
    $scope.move_res_up = (entry, question)->
      return

    $scope.move_res_down = (entry, question)->
      return

    $scope.remove_res = (entry, question)->
      return

    $scope.edit_res =(entry, question)->
      dialog.show
        controller: 'questionEditCtrl'
        templateUrl: 'blueprints/question/views/edit.tmpl.html'
        locals:
          entry: entry
          question: question

      return

]