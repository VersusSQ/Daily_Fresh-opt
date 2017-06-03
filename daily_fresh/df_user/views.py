#coding=utf-8
from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
import user_center
# Create your views here.

# 首页
def index(request):
    return render(request, 'df_goods/index.html', {'title': '首页'})

# 注册
def register(request):
    return render(request, 'user_info/register.html', {'title': '注册'})
def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # register.html中js设置的当鼠标离开输入框(失去焦点),就会会每个字段的值进行校验,
    # 只有所有的条件都满足时，才可以点击注册按钮,生成用户数据存到数据库

    # 当两次密码不相同时,重定向到register
    if upwd != upwd2:
        return redirect('/user/register/')

    # 当输入符合条件时，生成UserInfo对象,密码需要加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = User_Info()
    user.uName = uname
    user.uPwd = upwd3
    user.uEmail = uemail
    user.save()

    # 注册成功跳转到登录界面
    return redirect('/user/login/')
def register_exist(request):
    # 因为ajax发送的请求方式为get
    uname = request.GET.get('uname')
    count = User_Info.objects.filter(uName=uname).count()
    # 返回一个json形式的数据
    return JsonResponse({'count': count})


# 登录
def login(request):
    return render(request, 'user_info/login.html', {'title': '登录'})
def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 获取checkbox勾选情况,get()当为空时，默认为0
    remember = post.get('remember', 0)

    # 根据获取的用户姓名,在数据库中判断是否存在
    # 返回的是一个列表,列表中的元素都是符合条件的数据
    user = User_Info.objects.filter(uName=uname)
    if len(user) == 1:
        # 说明用户存在,此时判断密码,需加密
        s1 = sha1()
        s1.update(upwd)
        upwd2 = s1.hexdigest()
        if user[0].uPwd == upwd2:
            # 此时先获取cookie,目的：可以直接跳转到申请登录的界面,而不是每次都是主页
            # 设置cookie,在当需要在某一个界面获取登录用户信息时创建
            # 当不存在时，则默认跳转地址为首页的url/
            url = request.COOKIES.get('url', '/')
            # 生成一个HttpResponseRedirect对象,参数为跳转的地址
            red = HttpResponseRedirect(url)
            # 成功获取跳转地址后,防止以后直接登录造成影响
            # 设置为-1表示立刻删除
            red.set_cookie('url', '', max_age=-1)

            # 判断用户是否点击了'记住用户',点击就生成cookie
            if remember != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)

            # 为发送请求的对象生成session,为了之后界面信息可以显示出相应的用户信息
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            # 重定向
            return red

        else:
            # 用户信息错误或者密码错误都返回error信息给前端html的js用来现实提示信息
            context = {
                'title': '用户登录', 'error_info':1, 'uname': uname,'upwd':upwd
            }
            return render(request, 'user_info/login.html', context)


    else:
        # 用户信息错误或者密码错误都返回error信息给前端html的js用来现实提示信息
        context = {
            'title': '用户登录', 'error_info':1, 'uname': uname, 'upwd':upwd
        }
        return render(request, 'user_info/login.html', context)
def logout(request):
    # 退出登录时，需要删除创建好的session
    request.session.flush()
    return redirect('/')

# 用户中心
# 个人信息
@user_center.login
def ucenter_info(request):
    user = User_Info.objects.get(id=request.session.get('user_id'))
    context = {
        'title': '用户中心',
        'uname': request.session['user_name'],
        'uemail': user.uEmail,
        'page_name': 1,
    }
    return render(request, 'user_info/user_center_info.html', context)
# 收货地址
@user_center.login
def ucenter_site(request):
    user = User_Info.objects.get(id=request.session['user_id'])
    # 当请求方式为post时，才是需要更新用户的相关信息
    if request.method == 'POST':
        info = request.POST
        user.uShou = info.get('sname')
        user.uAddr = info.get('saddr')
        user.uTel = info.get('stel')
        user.uYoubian = info.get('syoubian')
        user.save()
    context = {
        'title': '用户中心',
        'user': user,
        'page_name': 1,
    }
    return render(request, 'user_info/user_center_site.html', context)

