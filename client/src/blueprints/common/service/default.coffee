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
        alias: "media"
        name: "Media Library"
        ico: "ic_collections_24px"
        path: "/media"
      }
      {
        alias: "account"
        name: "Account"
        ico: "ic_account_box_24px"
        path: "/account"
      }
      {
        alias: "about"
        name: "About"
        ico: "ic_info_outline_24px"
        path: "/info/about"
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