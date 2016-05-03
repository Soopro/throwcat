angular.module 'throwCat'

# File upload
# service with request must capitalized.
.service 'FileService', [
  'Upload'
  (
    Upload
  ) ->
    max_file_size =
      image: 600*1024
      video: 18*1024*1024
      audio: 8*1024*1024
      zip: 18*1024*1024
      docs: 2*1024*1024

    getFileSizeOpt = (new_opt, old_opt)->
      if typeof(new_opt) is 'number'
        old_opt = new_opt
      return old_opt


    kind_of = (file, type, exts)->
      if exts
        if typeof(exts) is 'string'
          exts = [exts]
        else if not angular.isArray(exts)
          exts = null
      if file.name
        ext = angular.get_file_ext(file.name)
        match_ext = if exts then exts.indexOf(ext) > -1 else true
      else
        match_ext = false

      return file.type.indexOf(type) > -1 and match_ext


    @config = (opts)->
      if typeof(opts.max_file_size) isnt 'object'
        throw new Error("File Service config error.")
        return

      max_file_size.image = getFileSizeOpt(opts.max_file_size.image,
                                           max_file_size.image)

      max_file_size.video = getFileSizeOpt(opts.max_file_size.video,
                                           max_file_size.video)

      max_file_size.audio = getFileSizeOpt(opts.max_file_size.audio,
                                           max_file_size.audio)

      max_file_size.zip = getFileSizeOpt(opts.max_file_size.zip,
                                         max_file_size.zip)

      max_file_size.docs = getFileSizeOpt(opts.max_file_size.docs,
                                          max_file_size.docs)

    @upload = (url, file, opts) ->
      opts = {} if not opts
      config =
        url: url
        method: opts.method or 'POST'
        file: file
        data: opts.data
        headers: opts.headers

      Upload.upload config
      .progress (evt) ->
        console.log "Uploading: #{parseInt(100.0 * evt.loaded / evt.total)} %"

    @http = (url, file, opts) ->
      opts = {} if not opts
      opts.headers['Authorization'] = opts.data.token or opts.token
      opts.headers['Content-Type'] = file.mimetype
      config =
        url: url
        method: opts.method or 'POST'
        data: file
        headers: opts.headers

      Upload.http config
      .progress (evt) ->
        console.log "Uploading: #{parseInt(100.0 * evt.loaded / evt.total)} %"


    @checkfile = (file) ->
      if not file or not file.size
        return false

      kind = ''
      if kind_of(file, 'image', ['png', 'jpg', 'jpeg', 'svg'])
        kind = 'image'
      else if kind_of(file, 'image', ['gif'])
        kind = "video"
      else if kind_of(file, 'video', ['mp4', 'mov'])
        kind = "video"
      else if kind_of(file, 'audio', ['mp3'])
        kind = "audio"
      else if kind_of(file, 'zip', ['zip'])
        kind = "zip"
      else if kind_of(file, 'pdf', ['pdf'])
        kind = "docs"
      else
        return false

      if max_file_size[kind] > file.size
        return true
      else
        return false

    return @
]