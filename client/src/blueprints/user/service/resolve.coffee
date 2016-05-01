angular.module 'throwCat'

.provider 'outerResolve', ->
  resolve: [
    'navOuter'
    'g'
    (
      navOuter
      g
    ) ->
      navOuter.load()

  ]

  $get: ->