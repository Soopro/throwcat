angular.module 'throwCat'

.factory 'restUser', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/crm/agent"

    auth: do ->
      supResource "#{api}/check_in"

]
