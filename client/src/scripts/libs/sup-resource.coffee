###
 supResource

 Author : Redy Ru
 Email : redy.ru@gmail.com
 License : 2014 MIT
 Version 1.0.0

 ---- Usage ----
 A warp of ng-resource, add 'update' 'save' and 'create'
 and provider service warp $q.defer().promise, for chain request only
###
angular.module 'supResource', [
  'ngResource'
]

.factory "supResource", [
  '$resource'
  ($resource) ->
    (url, paramDefaults, actions) ->
      _actions =
        update:
          method: "PUT"
          isArray: false
        trigger:
          method: "POST"
        create:
          method: "POST"
        post:
          method: "POST"

      actions = angular.extend({}, _actions, actions)
      restapi = $resource url, paramDefaults, actions
      restapi::$save = (params, success, error)->
        unless @id
          @$create(params, success, error)
        else
          @$update(params, success, error)

      return restapi
]

.factory "supChain", [
  '$q'
  ($q) ->
    (object) ->
      if not object
        deferred = $q.defer()
        deferred.resolve()
        return deferred.promise

      else if typeof object.then is "function"
        return object
        
      else if object.$promise
        return object.$promise
        
      else
        throw "Error: Invalid parameter in 'supChain'. - Object must have" + 
              " Promise or $promise. [SupResource]"
]

.factory "supParallel", [
  '$q'
  ($q) ->
    (list) ->
      deferred = $q.defer()
      if angular.isArray(list)
        results = []
        count = 1
        limit = list.length
        
        start_then = (pms,index) ->
          pms.then (data) ->
            results[index]=data
            if count < limit
              count++
            else
              success(results)
          .catch (error) ->
            failure error
        
        for index, obj of list
          if typeof obj.then is "function"
            pms = obj
          else if obj.$promise
            pms = obj.$promise
          
          start_then pms, index
        
        success = (results) ->
          deferred.resolve(results)

        failure = (error) ->
          deferred.reject(error)

        return deferred.promise
      else
        throw "Error: Invalid parameter in 'supParallel'. - " +
              "Objst must be Array, each item must be a promise " + 
              "[SupResource]"
]