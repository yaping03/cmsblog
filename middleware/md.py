from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import re
class M1(MiddlewareMixin):

    def process_request(self,request,*args,**kwargs):
        pass
        # valid = ['/auth-login.html','/index.html']
        # if request.path_info not in valid:
        #     action = request.GET.get('md') # GET
        #     user_permission_dict = request.session.get('user_permission_dict')
        #     if not user_permission_dict:
        #         return HttpResponse('无权限')
        #
        #     # action_list = user_permission_dict.get(request.path_info)
        #     flag = False
        #     for k,v in user_permission_dict.items():
        #         if re.match(k,request.path_info):
        #             if action in v:
        #                 flag = True
        #                 break
        #     if not flag:
        #         return HttpResponse('无权限')
