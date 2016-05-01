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
        alias: "account"
        name: "Account"
        ico: "ic_account_box_24px"
        nodes:[
          {
            alias: "create"
            name: "Create New"
            path: "/create_app"
            class: "md-primary"
          }
        ]
      }
      {
        alias: "about"
        name: "About"
        ico: "ic_info_outline_24px"
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