angular.module 'throwCat'

.service 'flash', [
  '$mdToast'
  'flashMsgGen'
  (
    $mdToast
    flashMsgGen
  )->
    (msg, warn, opts) ->
      if not opts
        opts = {}
      if not opts.pos
        opts.pos = "top right"
      if not opts.delay
        opts.delay = 3600
      if typeof(msg) is "string"
        msg = flashMsgGen(msg)

      preset =
        template: [
            '<md-toast md-theme="{{ opts.theme }}" '
            'class="text-nowrap"'
            'ng-class="{\'md-capsule\': opts.capsule, \'md-warn\': '
            'opts.warn}">'
            '<span flex>'
            '<md-icon ng-if="opts.warn" '
            'md-svg-icon="ic_warning_24px"></md-icon> '
            '{{ content }}'
            '</span>'
            '<md-button class="md-action" ng-if="opts.action" '
            'ng-click="resolve()" '
            'ng-class="{\'md-highlight\': opts.highlight}">'
            '{{ opts.action }}'
            '</md-button>'
            '</md-toast>'
          ].join('')
        locals:
          content: msg
          opts:
            warn: warn
            action: opts.action
            highlight: opts.highlight
            capsule: opts.capsule
        controller: 'flashToastCtrl'
        position: opts.pos
        hideDelay: opts.delay


      flash = $mdToast.build(preset)

      $mdToast.show(flash)
]

.service 'flashWatcher', [
  '$interval'
  'flashMsgStack'
  'flash'
  (
    $interval
    flashMsgStack
    flash
  ) ->
    @init = ->
      stack = flashMsgStack.get()
      interval = $interval ->
        if stack.length > 0
          for msg in stack
            if typeof(msg) is 'object'
              try
                flash msg.text, msg.warn
              catch e
                throw e.toString()
              stack = flashMsgStack.unset(msg)
            break
      , 500

    return @
]

.service 'flashMsgStack', ->
  stack = []
  @set = (msg)->
    stack.push(msg)
    return stack
  @unset = (msg) ->
    idx = stack.indexOf(msg)
    if idx > -1
      stack.splice(idx, 1)
    return stack
  @reset = ->
    stack = []
    return stack
  @get = ->
    return stack
  return @


.service 'flashMsgGen', [
  'error'
  (
    error
  )->
    (msg) ->
      if typeof(msg) in ['string', 'number']
        msg = error[msg.toString()] or msg
      # multi-language transalte
      if typeof(angular.translate) is "function"
        msg = angular.translate(msg)
      return msg
]

.controller 'flashToastCtrl', [
  '$scope'
  '$mdToast'
  'content'
  'opts'
  (
    $scope
    $mdToast
    content
    opts
  ) ->
    $scope.content = content
    $scope.opts = opts
    $scope.resolve = ->
      $mdToast.hide()
]
