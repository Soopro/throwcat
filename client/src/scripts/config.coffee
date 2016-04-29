angular.module 'throwCat'

.constant 'Config',
  baseURL:
    'api': throwcat.server.api
    'self': throwcat.server.self

  cookie_domain: throwcat.cookie_domain

  debug: throwcat.debug

  route:
    portal: '/'
    auth: '/user/login'
    exit: '/user/exit'
    error: '/404'

  locales: [
    { code:'en_US', text:'English'}
    { code:'zh_CN', text:'简体中文'}
  ]

  default_locale: 'en_US'

  path:
    outer: [
      '/user/register'
      '/user/login'
      '/user/recovery'
    ]
    open: [
      '/404'
      '/403'
    ]