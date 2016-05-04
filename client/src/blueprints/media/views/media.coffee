angular.module 'throwCat'

.controller 'mediaCtrl', [
  '$scope'
  '$window'
  '$filter'
  'restMedia'
  'MediaService'
  'navService'
  'dialog'
  'flash'
  'prompt'
  'MIMETypes'
  'Config'
  (
    $scope
    $window
    $filter
    restMedia
    MediaService
    navService
    dialog
    flash
    prompt
    MIMETypes
    Config
  ) ->
    navService.section('media')
    $scope.now = Date.now()

    $scope.mediafiles = restMedia.media.query()

    # upload media
    $scope.uploadedMediafiles = []
    $scope.upload_status = 0
    $scope.percent = 0
    $scope.paged = 1
    uploadStack = []
    resizeFileStack = []
    selectedMedia = []


    # get supported mime types
    mimetypes = MIMETypes('image', Config.media_mimetypes)
    $scope.mimetypes_str = mimetypes.join(', ')

    # create now for prevent cached image
    refresh_now = ->
      $scope.now = Date.now()

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
        uploadStack.push(media)
      .catch (media)->
        flashFileInvalid(media.name)
      .finally ->
        angular.removeFromList(resizeFileStack, media, 'name')
        startUpload()

    startUpload = ->
      if resizeFileStack.length > 0
        resizeBadFile(resizeFileStack[0])
      else if uploadStack.length > 0
        upload(uploadStack[0])
      else
        $scope.upload_status = 0

    $scope.select = (media) ->
      idx = selectedMedia.indexOf(media)
      if idx > -1
        selectedMedia.splice(idx, 1)
        media._seleted = false
      else
        selectedMedia.push(media)
        media._seleted = true

    $scope.has_selected = ->
      return selectedMedia.length > 0

    $scope.clean = (mediafiles)->
      console.log 'fuck'
      for media in mediafiles
        media._seleted = false
      selectedMedia.length = 0

    $scope.open = (media, e) ->
      e.preventDefault()
      e.stopPropagation()
      $window.open(media.src)
      return false

    $scope.trash = ->
      remain = selectedMedia.length
      angular.forEach selectedMedia, (entry) ->
        console.log entry.filename
        entry.$remove()
        .then (data)->
          angular.removeFromList($scope.mediafiles, data)
          if remain <= 1
            flash "Media files have been deleted."
        .finally ->
          remain -= 1
      selectedMedia.length = 0

    $scope.has_more = (mediafiles, paged, prepage)->
      curr_list = $filter('paginator')(mediafiles, paged, prepage)
      return curr_list.length < mediafiles.length


    $scope.onFileSelect = ($files, re_media) ->
      if not $files or $files.length <= 0
        return
      $scope.clean selectedMedia
      $scope.upload_status = 1
      uploadStack = []
      for media in $files
        if re_media
          media.id = re_media.id
          media.filename = re_media.filename
        unless MediaService.checkfile(media)
          if media.type.indexOf('image') > -1
            resizeFileStack.push(media)
          else
            flashFileInvalid(media.name)
          continue
        uploadStack.push(media)
      startUpload()


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
        $scope.upload_status = 0
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
        $scope.percent = parseInt(100.0 * evt.loaded / evt.total);
      .success (data) ->
        data.mimetype = media.type
        data.id = media_id
        data.filename = media_filename
        data.name = media_name
        data.upload = true
        media = new restMedia.media(data)
        media.$save()
        .then ->
          angular.removeFromList($scope.mediafiles, media, 'filename')
          $scope.mediafiles.unshift media
          $scope.uploadedMediafiles.unshift(data)
          media._reuploaded = Boolean(media_id)
        .finally ->
          $scope.percent = 0
          uploadStack.shift()
          if uploadStack.length <= 0
            $scope.upload_status = 0
            flash "Media files have been uploaded."
          else
            count_uploads++
            upload(uploadStack[0])

      .error (error)->
        $scope.percent = 0
        $scope.upload_status = 2
      .finally ->
        refresh_now()

]
