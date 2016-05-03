angular.module 'throwCat'

.factory 'navOuter', [
  'navService'
  (
    navService
  )->
    outer_navs = [
      {
        alias: "login"
        name: "Login"
        path: "/login"
        ico: "ic_account_circle_24px"
      }
      {
        alias: "register"
        name: "Register"
        path: "/register"
        ico: "ic_person_add_24px"
      }
      {
        alias: "about"
        name: "About"
        ico: "ic_info_outline_24px"
        path: "/about"
      }
    ]

    @load =  ->
      navs = angular.copy(outer_navs)
      navService.load(navs)

    return @
]