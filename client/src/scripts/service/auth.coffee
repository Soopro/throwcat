angular.module 'throwCat'

.service 'Auth', [
  '$cookies'
  (
    $cookies
  ) ->
    opts =
      path: '/'

    @config = (new_opts)->
      for k, v of new_opts
        opts[k] = v

    @is_logged = ->
      !!$cookies.get 'auth'

    @token = ->
      $cookies.get 'auth'

    @login = (token) ->
      $cookies.put 'auth', token, opts

    @logout = ->
      $cookies.remove 'auth', opts

    return
]