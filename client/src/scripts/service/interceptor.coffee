angular.module 'throwCat'

.factory 'requestInterceptor', [
  '$q'
  '$location'
  'flashMsgStack'
  'Auth'
  'Config'
  (
    $q
    $location
    flashMsgStack
    Auth
    Config
  ) ->
    request: (request) ->
      request.headers = request.headers or {}
      if Auth.token() and not request.headers.AgentToken
        request.headers.AgentToken = Auth.token()
      return request

    response: (response) ->
      return response or $q.when(response)

    responseError: (rejection) ->
      is_api_reject = angular.startswith(rejection.config.url,
                                         Config.baseURL.api)
      if not is_api_reject
        console.log ('Request is rejected by remote.')
      else
        if rejection.status is 0 and rejection.data is null
          $location.path("/404")
          msg = 'Error! No connection to server.'
          flashMsgStack.set
            text: msg
            warn: true
        if rejection.status is 401
          # handle the case where the user is not Authenticated
          Auth.logout()
        if rejection.data and rejection.data.errmsg \
        and rejection.status isnt 200
          flashMsgStack.set
            text: rejection.data.errmsg
            warn: true
          console.apiError rejection.data

      return $q.reject rejection
]

.config [
  '$httpProvider'
  (
    $httpProvider
  ) ->
    # add interceptors to request
    $httpProvider.interceptors.push 'requestInterceptor'
    # add X-Requested-With
    common = $httpProvider.defaults.headers.common
    common["X-Requested-With"] = 'XMLHttpRequest'
]