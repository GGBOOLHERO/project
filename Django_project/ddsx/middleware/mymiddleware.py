from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

# class MD1(MiddlewareMixin):
# 	white_list = [
# 		'/seller/login/',
# 		'/seller/register/',
# 		'/'
# 	]
# 	def process_request(self, request):
# 		path = request.path.info
# 		print(path)
# 		return HttpResponse('xxx')