#-*- coding: utf-8 -*-
# 한글 사용을 위한 comment

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import urllib
from django.views.generic import View

class root(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Futsal-Manager OpenCV Server is Running', 'isSuccess': True})

    def post(self, request, *args, **kwargs):
        jsonBody = json.loads(request.body)
        return JsonResponse({'message': 'This is POST Request', 'isSuccess': True})


    def file(selfself, request, *args, **kwargs):
        return JsonResponse({'message': 'This is File Request'})