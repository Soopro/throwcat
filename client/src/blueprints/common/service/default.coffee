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
        alias: "about"
        name: "About Us"
        ico: "ic_info_outline_24px"
        path: "/about"
        open: true
      }
      {
        alias: "help"
        name: "Help"
        ico: "ic_help_outline_24px"
        path: "/about"
        open: true
      }
      {
        alias: "exit"
        name: "Exit"
        ico: "ic_exit_24px"
        path: "/user/exit"
      }
    ]

    @load =  ->
      navs = angular.copy(default_navs)
      navService.load(navs)

    return @
]