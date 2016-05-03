angular.module 'throwCat'

# Media upload base on FileService
# service with request must capitalized.
.service 'MediaService', [
  '$q'
  '$timeout'
  'FileService'
  (
    $q
    $timeout
    FileService
  ) ->
    self = @
    max_image_size =
      width: 1650
      height: 1650

    encoder_options = 0.8

    getFileSizeOpt = (new_opt, old_opt)->
      if typeof(new_opt) is 'number'
        old_opt = new_opt
      return old_opt

    @config = (opts)->
      if typeof(opts.max_image_size) isnt 'object'
        throw new Error("Media Service config error.")
        return
      max_image_size.width = getFileSizeOpt(opts.max_image_size.width,
                                            max_image_size.width)
      max_image_size.height = getFileSizeOpt(opts.max_image_size.height,
                                             max_image_size.height)
      if opts.max_file_size
        FileService.config(opts)
      if opts.encoder_options
        encoder_options = opts.encoder_options

    @upload = FileService.upload
    @http = FileService.http

    @checkfile = FileService.checkfile


    @resize = (media)->
      console.log "Auto Resize: ", media.name
      deferred = $q.defer()

      if media.type.indexOf('image') < 0 or media.type.indexOf('svg') > -1
        timer = $timeout ->
          deferred.reject(media)
          $timeout.cancel(timer)
        , 0
        return deferred.promise

      img = new Image()
      reader = new FileReader()
      canvas = document.createElement("canvas")

      img.onerror = (e)->
        deferred.reject(media)

      reader.onerror =(e)->
        deferred.reject(media)

      reader.onload = (e)->
        try
          img.src = e.target.result
        catch e
          deferred.reject(media)

      img.onload = (e)->
        width = img.width
        height = img.height
        if width > height
          if width > max_image_size.width
            height *= max_image_size.width / width
            width = max_image_size.width
        else
          if height > max_image_size.height
            width *= max_image_size.height / height
            height = max_image_size.height

        canvas.width = width;
        canvas.height = height;
        try
          ctx = canvas.getContext("2d")
          ctx.drawImage(img, 0, 0, width, height)
          dataurl = canvas.toDataURL(media.type, encoder_options)
          new_media = angular.dataURLToBlob(dataurl)
          new_media.name = media.name
          new_media.lastModified = media.lastModified
          new_media.lastModifiedDate = new Date()
        catch err
          console.error(err)
          deferred.reject(media)
          throw err

        if self.checkfile new_media
          deferred.resolve(new_media)
        else
          deferred.reject(media)

      reader.readAsDataURL(media)

      return deferred.promise

    return @
]