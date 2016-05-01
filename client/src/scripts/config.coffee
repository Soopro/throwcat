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
    error: [
      '/404'
      '/403'
    ]

  input_pattern:
    slug: /^[a-zA-Z0-9_-]{3,50}$/
    pwd: /^[\~!@#$%^&*()-_=+|{}\[\],.?\/:;\'\'\d\w]{3,50}$/