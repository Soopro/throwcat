angular.module 'throwCat'

.constant 'Config',
  baseURL:
    'api': throwcat.server.api
    'self': throwcat.server.self

  cookie_domain: throwcat.cookie_domain

  debug: throwcat.debug

  route:
    portal: '/'
    auth: '/login'
    exit: '/exit'
    error: '/404'

  locales: [
    { code:'en_US', text:'English'}
    { code:'zh_CN', text:'简体中文'}
  ]

  default_locale: 'en_US'

  path:
    outer: [
      '/login'
      '/register'
      '/recovery'
      '/info-open/about'
    ]
    error: [
      '/404'
      '/403'
    ]

  input_pattern:
    slug: /^[a-zA-Z0-9_-]{3,50}$/
    passwd: /^[\~!@#$%^&*()-_=+|{}\[\],.?\/:;\'\'\d\w]{3,50}$/


  media_mimetypes:
    image: [
      'image/png', 'image/jpeg', 'image/svg+xml', 'image/gif', 'image/bmp'
    ]
    video: ['video/mp4', 'video/quicktime']
    audio: ['audio/mpeg', 'audio/mp3']
    application: ['application/zip', 'application/pdf']