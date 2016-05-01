angular.module 'throwCat'

.provider 'gResolve', ->
  resolve: [
    'navDefault'
    'g'
    (
      navDefault
      g
    ) ->
      navDefault.load()
  ]

  $get: ->
