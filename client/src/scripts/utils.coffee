# -------------------------------
# Helpers
# -------------------------------

# ---- make pop ----
angular.popObj = (obj, key)->
  value = obj[key]
  delete obj[key]
  return value

# ---- make set ----
angular.set = (list)->
  try
    newlist = []
    for i in list
      newlist.push(i) if i not in newlist
    return newlist
  catch
    return null

# ---- get extension ----
angular.get_file_ext = (str)->
  try
    str = str.split('?')[0].split('#')[0]
    if str.substr(-1) is '/'
      str = str.substr(0, str.length - 1)
    pair = str.split('.')
    if pair.length > 1
      ext = pair.pop()
      return ext.toLowerCase()
    return ''
  catch e
    return ''


# ---- process slug ----
angular.pre_process_slug = (value) ->
  try
    slug = value.toLowerCase()
    if not slug.match(/^[a-z0-9_\-]+$/g)
      return null
  catch
    slug = null
  return slug

# ---- startswith ----
angular.startswith = (str, text) ->
  if typeof(str) isnt 'string' or typeof(text) isnt 'string'
    return null
  return str.indexOf(text) is 0

# ---- endswith ----
angular.endswith = (str, text) ->
  if typeof(str) isnt 'string' or typeof(text) isnt 'string'
    return null
  return str.indexOf(text) is (str.length - text.length)

# ---- Date to String ----
angular.date2str = (date, format) ->
  if not angular.isDate(date)
    return false
  if not format
    format = 'YYYY-MM-DD'
  dd = date.getDate()
  mm = date.getMonth()+1
  yyyy = date.getFullYear()
  hour = date.getHours()
  mins = date.getMinutes()
  secs = date.getSeconds()

  if dd<10
    dd = '0'+dd
  if mm<10
    mm = '0'+mm
  if hour<10
    hour = '0'+hour
  if mins<10
    mins = '0'+mins
  if secs<10
    secs = '0'+secs

  date_str = format
  .replace('YYYY', yyyy)
  .replace('MM', mm)
  .replace('DD', dd)
  .replace('hh', hour)
  .replace('mm', mins)
  .replace('ss', secs)

  return date_str

# ---- String to Date ----
angular.str2date = (date_str) ->
  if typeof(date_str) isnt 'string'
    return false
  try
    date = new Date(date_str)
  catch e
    return false

  return date


# ---- Sortby ----
angular.sortby = (list, keys, reverse) ->

  # keys ['update','-date','priority']
  # 'reverse' is not required
  # keys can also be a string or a list of string.

  if typeof(keys) is 'string'
    keys = [keys]
  if not angular.isArray(keys)
    return list

  compare = (a, b) ->
    for key in keys
      k_rev = 1
      if key.charAt(0) is '-'
        key = key.substr(1)
        k_rev = -1
      else if key.charAt(0) is '+'
        key = key.substr(1)

      if a[key] < b[key]
        return -1 * k_rev
      if a[key] > b[key]
        return 1 * k_rev
    return 0

  new_list = list.sort(compare)

  if reverse
    new_list = new_list.reverse()

  return new_list

# ---- Capitalize ----
angular.capitalize = (str) ->
  return str.charAt(0).toUpperCase() + str.slice(1)

# ---- String to list ----
angular.str2list = (str, is_set, separator, whitespace) ->
  if angular.isArray(str)
    return str
  else if typeof(str) isnt 'string'
    return []
  unless separator
    separator = ','
    str = str.replace(/[，]/g,',')

  try
    orglist = str.split(',')
  catch e
    orglist = []

  newlist = []
  for s in orglist
    if s
      unless whitespace
        s = s.trim()
      if is_set and s in newlist
        continue
      newlist.push(s)

  return newlist

# ---- List to string ----
angular.list2str = (list, separator) ->
  if typeof(list) == 'string'
    return list
  else if not angular.isArray(list)
    return ''
  if not separator
    separator = ', '
  try
    str = list.join(separator)
  catch e
    str = ''
  return str

# ---- Toggle item in list ----
angular.toggleList = (list, item) ->
  idx = list.indexOf(item)
  if idx > -1
    list.splice idx, 1
  else
    list.unshift item
  return list

# ---- Test in list ----
angular.inList = (list, item, attr) ->
  equals = (obj1, obj2, attr)->
    if attr
      return angular.equals(obj1[attr], obj2[attr])
    else
      return angular.equals(obj1, obj2)

  for obj, idx in list
    if equals(obj, item, attr)
      return true

  return false

# ---- Shift in List ----
angular.shiftFromList = (list, current, next) ->
  temp = list[next]
  list[next] = list[current]
  list[current] = temp
  return list

# ---- Pop item From List ----
angular.popFromList = (list, item, attr) ->
  equals = (obj1, obj2, attr)->
    if attr
      return angular.equals(obj1[attr], obj2[attr])
    else
      return angular.equals(obj1, obj2)
  pop_obj = null
  for obj, idx in list
    if equals(obj, item, attr)
      pop_obj = obj
      list.splice idx, 1
      break

  return pop_obj

# ---- Remove From List ----
angular.removeFromList = (list, item, attr) ->
  equals = (obj1, obj2, attr)->
    if attr
      return angular.equals(obj1[attr], obj2[attr])
    else
      return angular.equals(obj1, obj2)

  compare = (a, b)->
    return b-a

  indexbook = []
  for obj, idx in list
    if equals(obj, item, attr)
      indexbook.push idx

  indexbook.sort(compare)
  for i in indexbook
    list.splice i, 1

  return list

# ---- Object to Json string ----
angular.obj2jsonstr = (obj, ugly) ->
  jsonstr = null
  if not obj
    return ''
  if typeof(obj) is "string"
    return obj
  else if typeof(obj) isnt "object"
    return null

  i=0
  for prop of obj
    i++ if obj.hasOwnProperty(prop)
  if i is 0
    jsonstr = ''
  else
    try
      if not ugly
        jsonstr = JSON.stringify obj, null, 2
      else
        jsonstr = JSON.stringify obj
    catch e
      jsonstr = false

  return jsonstr

# ---- Json string to Object ----
angular.jsonstr2obj = (str) ->
  if not str
    return {}
  obj = null
  try
    obj = JSON.parse(str)
  catch e
    obj = false

  return obj


# ---- HTML Tags free ----
angular.cleanTags = (str) ->
  if not angular.isString(str)
    str = ''
  return str.replace(/<[^>]+>/gm, '')

# ---- Space free ----
angular.cleanSpace = (content, force) ->
  if not force
    return content.replace(/\s{2,}/g, " ").trim()
  else
    return content.replace(" ", "").trim()

# ---- ng attribute free ----
angular.cleanNgAttr = (content) ->
  return content.replace(/ng-[a-zA-Z0-9_\-]+=["\'].*?["\']/ig, '')

angular.isUrl = (url, regex) ->
  if typeof(url) isnt 'string'
    return false
  if url.match(/^[\w]+:/)
    if regex
       return url.match(regex)
    else
      return true
  else
    return false

# ---- Add Params to a URL String ----
angular.addURLParams = (url, params) ->
  if typeof params isnt 'object'
    return url
  _add = (url, key, value)->
    joint = if url.indexOf('?') > -1 then '&' else '?'
    key = encodeURIComponent(key)
    value = encodeURIComponent(value)
    url = url+joint+key+'='+value
    return url

  for k, v of params
    if angular.isArray(v)
      for item in v
        url = _add(url, k, item)
    else
      url = _add(url, k, v)

  return url



angular.dataURLToBlob = (dataURL) ->
  BASE64_MARKER = ';base64,'
  if dataURL.indexOf(BASE64_MARKER) == -1
    parts = dataURL.split(',')
    contentType = parts[0].split(':')[1]
    raw = parts[1]
    return new Blob([ raw ], type: contentType)
  parts = dataURL.split(BASE64_MARKER)
  contentType = parts[0].split(':')[1]
  raw = window.atob(parts[1])
  rawLength = raw.length
  uInt8Array = new Uint8Array(rawLength)
  i = 0
  while i < rawLength
    uInt8Array[i] = raw.charCodeAt(i)
    ++i
  new Blob([ uInt8Array ], type: contentType)


# -------------------------------
# Consoles
# -------------------------------
console.apiError = (error, error_stack) ->
  console.log '---------------API Error--------------'
  for k,v of error
    if v
      console.error k,':',v
  if error_stack
    console.log error_stack
  console.log '--------------------------------------'
  return
