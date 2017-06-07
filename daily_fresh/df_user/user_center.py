# coding=utf-8
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
def login(func):
    def login_in(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            # 当request的请求方式为ajax时,返回json数据
            # 因为此处确定了没有用户登录，
            if request.is_ajax():
                return JsonResponse({'islogin': 0})
            else:
                return redirect('/user/login/')
    return login_in