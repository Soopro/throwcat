angular.module 'throwCat'

.filter "paginator", ->
  (list, page, perpage) ->
    if not list or not list.length or list.length <= 0
      return []
    if not page
      page = 1
    if angular.isArray(list)
      if not perpage
        perpage = 'short'
      switch perpage
        when 'short'
          perpage = 12
        when 'full'
          perpage = 48
        when 'medium'
          perpage = 24

      idx = page * perpage
      if idx > list.length
        idx = list.length
      return list[0...idx]
    else
      return []


.filter "dateformat", [
  '$filter'
  (
    $filter
  ) ->
    (date, format)->
      if not format
        format = 'mediumDate'
      if typeof(angular.translate) is 'function'
        format = angular.translate(format)
      digit = 0
      if typeof(date) is 'number'
        digit = date.toString().length
      if digit is 10
        date = date * 1000

      return $filter('date')(date, format)
]

.filter "abbrnum", ->
  (number, arg2, arg3) ->

      if typeof(arg2) == 'boolean'
        upper = Boolean(arg2)
      else
        upper = Boolean(arg3)

      if typeof(arg2) == 'number'
        dec_places = arg2
      else
        dec_places = 0

      dec_places = 10 ** dec_places

      # Enumerate number abbreviations
      abbrev = [
        'k'
        'm'
        'b'
        't'
        'q'
      ]
      # Go through the array backwards, so we do the largest first
      i = abbrev.length - 1
      while i >= 0
        # Convert array index to "1000", "1000000", etc
        size = 10 ** ((i + 1) * 3)
        # If the number is bigger or equal do the abbreviation
        if size <= number
          # Here, we multiply by dec_places, round, and then divide by dec_places.
          # This gives us nice rounding to a particular decimal place.
          number = Math.round(number * dec_places / size) / dec_places
          # Handle special case where we round up to the next abbreviation
          if number == 1000 and i < abbrev.length - 1
            number = 1
            i++
          # Add the letter for the abbreviation
          abbrev_str = abbrev[i]
          abbrev_str.toUpperCase() if upper
          number += abbrev_str
          # We are done... stop
          break
        i--
      number
