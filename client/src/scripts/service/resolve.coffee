angular.module 'throwCat'

.provider 'gResolve', ->
  resolve: [
    'navDefault'
    'App'
    'g'
    (
      navDefault
      App
      g
    ) ->
      g.$clear()
      g.app = App
      navDefault.load()
  ]

  $get: ->