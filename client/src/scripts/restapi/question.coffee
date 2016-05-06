angular.module 'throwCat'

.factory 'restCat', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/crm/agent"

    question: do ->
      supResource "#{api}/question"

]
