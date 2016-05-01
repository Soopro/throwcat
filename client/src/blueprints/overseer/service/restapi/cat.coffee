angular.module 'throwCat'

.factory 'restCat', [
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
