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