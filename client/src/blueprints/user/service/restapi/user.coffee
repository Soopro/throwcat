angular.module 'throwCat'

.factory 'restUser', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/user"

    doCheck: ->
      supResource "#{api}/check"
      .post null, data
      .$promise

    doRegister: ->
      supResource "#{api}/register"
      .create null, data
      .$promise


]
