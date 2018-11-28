import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse


# class AjaxTesterView(View):
#     def get(self, request):
#         return render(request, 'ajax_tester.html')
#
#
# class AddView(View):
#     def get(self, request):
#         a = request.GET['a']
#         b = request.GET['b']
#         a = int(a)
#         b = int(b)
#         return HttpResponse(str(a+b))
#
#
# class AjaxListView(View):
#     def get(self, request):
#         a = list(range(100))
#         return HttpResponse(json.dumps(a), content_type='application/json')
#
#
# class AjaxDictView(View):
#     def get(self, request):
#         from time import time
#         name_dict = {'msg': 'Love django', 'time': time()}
#         return HttpResponse(json.dumps(name_dict), content_type='application/json')
