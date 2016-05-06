angular.module 'throwCat'

# formSubmitValidation
.service 'fsv', ->
  (form, fields)->
    if not form
      console.error form, "Form is not exist"
      return false
    if not form.$valid
      for arg in fields
        if form[arg]
          form[arg].$touched = true
          form[arg].$dirty = true
        else
          console.warn "Form Submit Validation Service Error: "+
                        "'"+arg+"' is undefined"
      return false
    else
      return true

# pormot
.service 'prompt', ->
  (prompt_msg, prompt_content)->
    if typeof(angular.translate) is 'function'
      prompt_msg = angular.translate(prompt_msg)
    window.prompt(prompt_msg, prompt_content)

# confirm
.service 'confirm', ->
  (confirm_msg)->
    if typeof(angular.translate) is 'function'
      confirm_msg = angular.translate(confirm_msg)
    window.confirm(confirm_msg)

# MIME types
.service 'MIMETypes', ->
  (types, allowed_mimetypes)->

    if typeof(types) is 'string'
      types = [types]
    if not angular.isArray(types) or types.length is 0
      return []

    mimetypes = []

    for k,v of allowed_mimetypes
      for type in types
        if k == type
          mimetypes = mimetypes.concat(v)

        # support use mimetypes directly.
        else if type in v
         mimetypes.push(type)

    return mimetypes

