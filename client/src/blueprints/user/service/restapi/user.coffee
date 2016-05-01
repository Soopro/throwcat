angular.module 'throwCat'

.factory 'restUser', [
  'supResource'
  'Config'
  (
    supResource
    Config
  ) ->
    api = "#{Config.baseURL.api}/crm/agent"

    # -- Auth --
    auth: do ->
      supResource "#{api}/check_in"

    # -- Status --
    status: do ->
      supResource "#{api}/status"

    # -- Member --
    member: do ->
      supResource "#{api}/member/:member_id",
        'member_log': '@login'
        'member_id': '@id'

    member_apply: do ->
      supResource "#{api}/member/:member_id/applyment/:apply_id",
        'member_id': '@member_id'
        'apply_id': '@id'
      ,
        done: method: "POST"

    # -- Events --
    activity: do ->
      supResource "#{api}/activity/:act_id",
        'act_id': '@id'

    applyment: do ->
      supResource "#{api}/activity/:act_id/applyment/:apply_id",
        'act_id': '@activity_id'
        'apply_id': '@id'
      ,
        done: method: "POST"

    # -- Promo --
    promo: do ->
      supResource "#{api}/promo/:promo_id",
        'promo_id': '@id'

    promocode: do ->
      supResource "#{api}/promo/:promo_id/code/:code",
        'promo_id': '@id'
        'code':'@code'
      ,
        use: method: "POST"

]
