# coding=utf-8
from django.http import HttpResponse, HttpRequest
from django.middleware.csrf import CsrfViewMiddleware

# 设置中间件，用来获取请求页面的地址，存到cookie中
# 此中间件在所有响应返回浏览器前被调用，在每个请求上调用，返回HttpResponse对象
# 与装饰器－－－判断用户是否登录,结合使用的


class url():

    def process_response(self, request, response):
        url_list = [
            '/user/register/',
            '/user/register_handle/',
            '/user/register_exist/',
            '/user/login/',
            '/user/login_handle/',
            '/user/logout/'
        ]

        if not request.is_ajax() and request.path not in url_list:
            # 当不是ajax请求方式并且不在指定的路径列表中时(说明那些路径都是需要用户登录的)，
            # 此时需要设置当前发送请求的界面的地址，为了登录后可以直接跳转到之前发送请求的界面
            response.set_cookie('red_url', request.get_full_path())
        return response

