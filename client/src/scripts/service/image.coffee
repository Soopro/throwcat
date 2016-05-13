angular.module 'throwCat'

.service 'image', ->
  @trans = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'

  @trans_cover = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAABkCAMAAAA2aMu9AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAACZJREFUaN7twTEBAAAAwqD1T20LL6AAAAAAAAAAAAAAAAAAAADgYz7kAAGPQQV3AAAAAElFTkSuQmCC'

  @trans_banner = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAA8CAMAAACac46aAAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAB5JREFUWMPtwYEAAAAAw6D5Ux/hAlUBAAAAAAAAfAMcXAABK1y9+AAAAABJRU5ErkJggg=='

  @default = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNjAgMTYwIj48dGl0bGU+ZGVmYXVsdF9waG90bzwvdGl0bGU+PHBhdGggZD0iTTkxLDg2Vjc0YTEuOTk5NCwxLjk5OTQsMCwwLDAtMS45OTg4LTJINzFhMS45OTk0LDEuOTk5NCwwLDAsMC0yLDEuOTk4OFY4NmExLjk5OTQsMS45OTk0LDAsMCwwLDEuOTk4OCwySDg5YTEuOTk5NCwxLjk5OTQsMCwwLDAsMi0xLjk5ODhWODZaTTc2LjUsODAuNUw3OSw4My41MDUsODIuNSw3OSw4Nyw4NUg3M1oiIGZpbGw9IiNjY2MiLz48L3N2Zz4='

  @avatar = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+PHRpdGxlPmRlZmF1bHRfYXZhdGFyPC90aXRsZT48cGF0aCBkPSJNMjQsMjRhOCw4LDAsMSwwLTgtOEE4LjAyMzUsOC4wMjM1LDAsMCwwLDI0LDI0Wm0wLDRjLTUuMywwLTE2LDIuNy0xNiw4djRINDBWMzZDNDAsMzAuNywyOS4zLDI4LDI0LDI4WiIgZmlsbD0iI2NjYyIvPjxwYXRoIGQ9Ik0wLDBINDhWNDhIMFYwWiIgZmlsbD0ibm9uZSIvPjwvc3ZnPg=='

  return @