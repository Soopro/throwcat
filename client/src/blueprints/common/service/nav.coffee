angular.module 'throwCat'

.service 'navService', ->
  self = @
  @data = []
  @activatedMenus = []
  @currTitleLocked = null
  @currIcon = null
  @currTitle = ''
  @currSubTitle = ''
  @currSection = ''
  @currApp = null

  @load = (navs, title, icon, app) ->
    if not angular.equals(self.data, navs)
      self.data = navs
    self.currTitleLocked = if title then title else null
    self.currIcon = if icon then icon else null
    self.currApp = app

  @getElement = (alias) ->
    for element in self.data
      if element.alias == alias
        return element

  @section = (sec) ->
    idx = sec.indexOf('/')
    if idx > -1
      main_sec = sec[0...idx]
      sub_sec = sec[idx+1..]
    else
      main_sec = sec

    self.currSection = main_sec or ''
    self.activatedMenus = []

    for nav in self.data
      if nav.alias is main_sec
        if self.currTitleLocked
          self.title(self.currTitleLocked)
          self.subtitle(nav.name)
          break
        else
          self.title(nav.name)

        if nav.nodes and sub_sec
          _break = false
          for subnav in nav.nodes
            if subnav.alias is sub_sec
              self.subtitle(subnav.name)
              _break = true
              break
        else
          self.subtitle(false)

        if _break
          break

  @title = (title) ->
    self.currTitle = title or ''

  @subtitle = (title) ->
    self.currSubTitle = title or ''

  @clear = ->
    self.data = []
    self.activatedMenus = []
    self.currTitleLocked = null
    self.currIcon = null
    self.currTitle = ''
    self.currSubTitle = ''
    self.currSection = ''
    self.currApp = null

  return @