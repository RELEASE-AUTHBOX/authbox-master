try:from django.utils.deprecation import MiddlewareMixin
except ImportError:MiddlewareMixin=object
class ForceDefaultLanguageMiddleware(MiddlewareMixin):
	def process_request(C,request):
		B='HTTP_ACCEPT_LANGUAGE';A=request
		if B in A.META:del A.META[B]