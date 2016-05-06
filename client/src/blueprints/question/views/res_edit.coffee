angular.module 'throwCat'

.controller "questionResEditCtrl", [
  '$scope'
  '$filter'
  'restMedia'
  'MediaService'
  'MIMETypes'
  'Config'
  'dialog'
  'flash'
  'image'
  'type'
  'resource'
  (
    $scope
    $filter
    restMedia
    MediaService
    MIMETypes
    Config
    dialog
    flash
    image
    type
    resource
  ) ->
    if typeof(angular.translate) is 'function'
      $scope._ = angular.translate

    $scope.image = image
    $scope.resource = resource
    $scope.resource_type = type
    $scope.selected_tab = 0
    $scope.curr_media = {}

    $scope.tab = (tab_order)->
      $scope.selected_tab = tab_order

    $scope.trash = (resource)->
      resource._deleted = true
      dialog.hide(resource)

    $scope.save = (resource)->
      dialog.hide(resource)

    $scope.close = ->
      dialog.cancel()

    $scope.select = (media)->
      $scope.curr_media = media
      $scope.tab(0)

    # more
    $scope.paged = 1
    $scope.has_more = (mediafiles, paged, prepage)->
      curr_list = $filter('paginator')(mediafiles, paged, prepage)
      return curr_list.length < mediafiles.length

    $scope.more = (mediafiles, paged, prepage)->
      if $scope.has_more(mediafiles, paged)
        $scope.paged += 1
      else
        return false

    # media
    $scope.mediafiles = restMedia.media.query (data)->
      data.unshift {_empty:true}
    $scope.upload_status = 0
    $scope.percent = 0

    # get supported mime types
    mimetypes = MIMETypes('image', Config.media_mimetypes)
    $scope.mimetypes_str = mimetypes.join(', ')

    # create now for prevent cached image
    refresh_now = ->
      $scope.now = Date.now()

    # upload media
    $scope.onFileSelect = ($files, mediafiles) ->
      # check upload files
      if not $files or $files.length <= 0 or $scope.upload_status == 1
        return

      # ready to upload
      $scope.upload_status = 1
      media = $files[0]
      if MediaService.checkfile(media)
        upload(media)
      else
        resizeBadFile(media)


    flashFileInvalid = (filename)->
      if filename.length > 20
        filename = filename.substring(0,16) + '...'

      if typeof(angular.translate) is 'function'
        flash_msg = angular.translate("%s is invalid.", filename)
      else
        flash_msg = filename+" is invalid."

      $scope.percent = 0
      $scope.upload_status = 2

      flash flash_msg, true


    # resize file one by one, otherwise will kill your CPU.
    resizeBadFile = (media) ->
      _media_id = media.id if media.id
      _media_filename = media.filename if media.filename
      MediaService.resize(media)
      .then (media)->
        media.id = _media_id if _media_id
        media.filename = _media_filename if _media_filename
        upload(media)
      .catch (media)->
        flashFileInvalid(media.name)


    count_uploads = 0
    upload_api_url = restMedia.media_upload_url
    upload = (media) ->
      if not media
        return
      restMedia.doMediaAuth
        filename: media.filename or media.name
        mimetype: media.type
        is_new: not media.filename
      .then (data)->
        opts =
          method: data.method
          headers: data.headers
          data:
            token: data.token
            key: data.cdn_key
            Authorization: data.token
            FileName: data.cdn_key
        media._name = data.name
        media_upload(data.api_url, media, opts)

      .catch ->
        $scope.upload_status = 2
        $scope.percent = 0


    media_upload = (url, media, opts)->
      console.log count_uploads, media.name, media.filename, media.size
      $scope.upload_status = 1
      $scope.percent = 0

      media_id = media.id
      media_name = media._name
      media_filename = media.filename

      MediaService.upload(url, media, opts)
      .progress (evt) ->
        $scope.percent = parseInt(100.0 * evt.loaded / evt.total)

      .success (data) ->
        data.mimetype = media.type
        data.id = media_id
        data.filename = media_filename
        data.name = media_name
        data.upload = true
        media = new restMedia.media(data)
        media.$save()
        .then ->
          $scope.mediafiles.splice(1, 0, media)
        .finally ->
          $scope.percent = 0
          $scope.upload_status = 0
          flash "Media files have been uploaded."

      .error (error)->
        $scope.percent = 0
        $scope.upload_status = 2
      .finally ->
        refresh_now()


]