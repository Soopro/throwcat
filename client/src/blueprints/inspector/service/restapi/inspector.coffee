angular.module 'throwCat'

.factory 'restCat', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/crm/agent"

    inspector: do ->
      supResource "#{api}/inspector"

]
