angular.module 'throwCat'

.provider 'gResolve', ->
  resolve: [
    'resolveProxy'
    (
      resolveProxy
    ) ->
      resolveProxy.run()
  ]

  $get: ->

.service 'resolveProxy', ->
  proxy_func = null

  self = @

  self.set = (fn)->
    proxy_func = fn

  self.run = ->
    if typeof proxy_func is 'function'
      return proxy_func()

  return self
