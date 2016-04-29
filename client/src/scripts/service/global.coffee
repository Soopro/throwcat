angular.module 'throwCat'

.service 'g', ->
  self = @
  self.$clear = ->
    for k, v of self
      if k.indexOf('$') != 0
        delete self[k]

  self.$clear()

  return self
