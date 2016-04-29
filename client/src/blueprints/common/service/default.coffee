angular.module 'throwCat'

.factory 'navDefault', [
  'navService'
  (
    navService
  )->
    default_navs = [
      {
        alias: "dashboard"
        name: "Dashboard"
        path: "/"
        ico: "ic_dashboard_24px"
      }
      {
        alias: "promo"
        name: "Promotions"
        ico: "ic_local_play_24px"
        path: "/promo"
      }
      {
        alias: "events"
        name: "Events"
        ico: "ic_event_24px"
        path: "/event"
      }
      {
        alias: "member"
        name: "Membership"
        ico: "ic_people_24px"
        path: "/member"
      }
      {
        alias: "exit"
        name: "Exit"
        ico: "ic_exit_24px"
        path: "/exit"
      }
    ]

    @load =  ->
      navs = angular.copy(default_navs)
      navService.load(navs)

    return @
]