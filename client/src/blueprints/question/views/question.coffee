angular.module 'throwCat'

.controller "questionCtrl", [
  '$scope'
  '$location'
  '$routeParams'
  'restCat'
  'navService'
  'Config'
  'ConfigQs'
  'helpModal'
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
    helpModal
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
      $scope.is_new = true
      $scope.question = new restCat.question
        resources: []
        type: 0
        stauts: 0
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
      $scope.question.$remove()
      .then ->
        $location.path '/'
        flash 'Question has been deleted.'
        return
      .finally ->
        $scope.submitted = false

    $scope.help = (content)->
      console.log content
      helpModal(content)

    # resources

    # $scope.move_res_up = (question, entry)->
    #   return
    #
    # $scope.move_res_down = (question, entry)->
    #   return

    $scope.remove_res = (question, entry)->
      return

    $scope.edit_res =(question, entry)->
      question_type = prepare_res_type(question)
      if not question_type
        flash 'Question type invalid.', true
        return

      if entry
        resource = entry
      else
        resource =
          src: ''
          recipe: {}
          _new: true

      dialog.show
        controller: 'questionResEditCtrl'
        templateUrl: 'blueprints/question/views/res_edit.tmpl.html'
        fullscreen: true
        locals:
          type: question_type
          resource: resource
      .then (res) ->
        if res._deleted
          angular.removeFromList(question, res, 'deleted')
        else if res._new
          delete res._new
          question.resources.push(res)


    prepare_res_type = (question)->
      question_type = null
      for type in ConfigQs.question_types
        if type.key == question.type
          question_type =
            key: type.key
            name: type.name
          break
      return question_type

]