angular.module 'throwCat'

.factory 'restMedia', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/media"

    media: do ->
      supResource "#{api}/:filename",
        filename: '@filename'

    doMediaAuth: (data) ->
      supResource "#{api}/auth/upload"
      .post data
      .$promise

    media_upload_url: ->
      return "#{api}"

]