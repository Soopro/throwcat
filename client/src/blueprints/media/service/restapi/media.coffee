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
      supResource "#{api}/:app_alias/:filename",
        app_alias: '@app_alias'
        filename: '@filename'

    doMediaAuth: (alias, data) ->
      supResource "#{api}/:app_alias/auth/upload"
      .post app_alias: alias, data
      .$promise

    media_upload_url: (alias)->
      return "#{api}/#{alias}"

]