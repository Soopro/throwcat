angular.module 'throwCat'

.factory 'restUser', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/user"

    doRegisterCaptcha: (data)->
      supResource "#{api}/register/captcha"
      .post null, data
      .$promise

    doRegister: (data)->
      supResource "#{api}/register"
      .create null, data
      .$promise

    doRecoveryCaptcha: (data)->
      supResource "#{api}/recovery/captcha"
      .post null, data
      .$promise

    doRecovery: (data)->
      supResource "#{api}/recovery"
      .post null, data
      .$promise

    doLogin: (data)->
      supResource "#{api}/login"
      .post null, data
      .$promise

    password: do ->
      supResource "#{api}/security/password"
      ,
       change:
         method: "PUT"

    secret: do ->
      supResource "#{api}/security/secret"
      ,
       reset:
         method: "PUT"

]
