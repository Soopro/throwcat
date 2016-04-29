# -------------------------------
# sup Localized
# -------------------------------
varsion = '1.1.3'

is_exports = typeof exports isnt "undefined" and exports isnt null
root = if is_exports then exports else this

unless root.sup
  root.sup = {}

# make it global, easy load localize by other js files.
sup.localizedDict = {}

localizedText = {}
locale = null
CASE_SENSITIVE = false


_all_basestring = ->
  for arg in arguments
    if typeof(arg) != 'string'
      return false
  return true

_trans_key = (str)->
  if not CASE_SENSITIVE
    return str.toLowerCase()
  return str


insert = (loc, text_list)->
  sup.localizedDict[loc] = text_list


load_dict = (loc_texts)->
  loc_text_dict = {}
  if Object.prototype.toString.call(loc_texts) == '[object Array]'
    for text in loc_texts
      if _all_basestring(text.msgid, text.msgid) and text.msgid
        loc_text_dict[_trans_key(text.msgid)] = text.msgstr
  else if loc_texts and typeof(loc_texts) == 'object'
    loc_text_dict = loc_texts

  return loc_text_dict


append = (new_text_list)->
  if Object.prototype.toString.call(new_text_list) isnt '[object Array]'
    return
  for text in new_text_list
    if _all_basestring(text.msgid, text.msgid) and text.msgid
       localizedText[_trans_key(text.msgid)] = text.msgstr
  return

restore = ->
  setLocale(locale)
  return

setLocale = (loc) ->
  if not loc
    loc = ''
  locale = null
  loc = loc.replace('-','_')

  for k,v of sup.localizedDict
    if k.toLowerCase() is loc.toLowerCase()
      locale = k
      break
  
  if locale and sup.localizedDict[locale]
    locale_dict = sup.localizedDict[locale]
  else
    locale_dict = null
    locale = loc

  localizedText = load_dict(locale_dict)

  return locale

    
translate = (text) ->
  if not text or typeof text isnt 'string'
    return text

  trans = localizedText[_trans_key(text)]
  if not trans
    trans = text
  
  args=[]
  for arg in arguments
    args.push arg

  for arg in args[1..]
    arg = '' if arg is undefined
    trans = trans.replace("%s", arg)

  return trans
 
self_translate = (text)->
  if not text or typeof text isnt 'object'
    return text
  if locale
    lang = locale.split('_')[0] or 'en'
    trans_text = text[locale] or text[lang]
  if not trans_text
    key = Object.keys(text)[0]
    trans_text = text[key]
  return trans_text
 

angular.module 'supLocales', ['ngCookies']

.run [
  'supLocales'
  (
    supLocales
  ) ->
    if not supLocales.inited
      supLocales.init()
]

.service "supLocales", [
  '$location'
  '$rootScope'
  '$cookies'
  (
    $location
    $rootScope
    $cookies
  ) ->
    default_locale = 'en_US'
    self = @
    
    @version = varsion
    @inited = false

    @init = (loc, case_sensitive)->
      @inited = true
      
      CASE_SENSITIVE = Boolean(case_sensitive)

      if loc
        default_locale = loc

      userLang = navigator.language or navigator.userLanguage
      userLocale = userLang.replace('-','_')

      try
        cookieLocale = $cookies.get('current_locale')
      catch e
        cookieLocale = null
      params = $location.search()
      if params.locale
        currLocale = params.locale
        $location.search("locale", null)
      else
        currLocale = if cookieLocale then cookieLocale else userLocale

      self.set(currLocale)
      $rootScope._ = angular.translate = translate
      $rootScope._t = angular.self_translate = self_translate
    
    @load = (loc, text_list)->
      insert(loc, text_list)
      setLocale(loc)
    
    @translate = (args)->
      return translate.apply(this, arguments)

    @set = (loc) ->
      locale = setLocale(loc) or default_locale
      $rootScope.locale = locale
      $rootScope.lang = locale.split('_')[0] or 'en'
      if $cookies.get('current_locale') != locale
        $cookies.put('current_locale', locale)
    
    @append = (translates)->
      append(translates)
    
    @restore = ->
      restore()
    
    @get = ->
      try
        cookieLocale = $cookies.get 'current_locale'
      catch e
        cookieLocale = null
      return cookieLocale

    @match = (lang1, lang2)->
      if typeof(lang1) isnt 'string' or typeof(lang2) isnt 'string'
        return false
      lang1 = lang1.replace('-','_')
      lang2 = lang2.replace('-','_')
      return lang1.toLowerCase() == lang2.toLowerCase()
        
    return  @
]