angular.module 'throwCat'

.service 'QRScanner', [
  '$q'
  (
    $q
  ) ->
    # window.$$__QRScannerJS__ =
    #   scan: (func)->
    #     eval(func)(null)

    scanner = window.$$__QRScannerJS__ or null
    scanning = false

    @scan = ->
      console.log 'scanning...'
      error_data = {}
      deferred = $q.defer()

      if not scanner
        error_data.msg = 'QRScanner not found.'
        deferred.reject(error_data)
        return deferred.promise

      if scanning
        error_data.msg = 'QRScanner is already started.'
        deferred.reject(error_data)
        return deferred.promise

      scanner.result = (result)->
        deferred.resolve({result: result})
        scanning = false

      try
        scanning = true
        scanner.scan('$$__QRScannerJS__.result')
      catch
        error_data.msg = 'QRScanner crashed.'
        deferred.reject(error_data)
        scanning = false

      return deferred.promise

    @check = ->
      return Boolean(scanner)

    return @
]