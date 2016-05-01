angular.module 'throwCat'


# passwordVerify
.directive "passwordVerify", ->
  require: "ngModel"
  scope:
    passwordVerify: "="

  link: (scope, element, attrs, ctrl) ->
    scope.$watch (->
      combined = undefined
      if scope.passwordVerify or ctrl.$viewValue
        combined = scope.passwordVerify + "_" + ctrl.$viewValue
      combined
    ), (value) ->
      if value
        ctrl.$parsers.unshift (viewValue) ->
          origin = scope.passwordVerify
          if origin isnt viewValue
            ctrl.$setValidity "passwordVerify", false
            return undefined
          else
            ctrl.$setValidity "passwordVerify", true
            return viewValue
