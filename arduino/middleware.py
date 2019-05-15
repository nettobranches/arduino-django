
print('set class middleware')

class StackOverflowMiddleware(object):
	def __init__(self, get_response):
		self.get_response = get_response
		print("init")
		# One-time configuration and initialization.

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		response = self.get_response(request)
		response.middle = 'mid'
		print("call response", response)
		# Code to be executed for each request/response after
		# the view is called.

		return response