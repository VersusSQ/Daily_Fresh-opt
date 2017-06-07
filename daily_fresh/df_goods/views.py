# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import *
from django.core.paginator import Paginator
from df_cart.models import *

# Create your views here.

def index(request):
    type_name = TypeInfo.objects.all()
    type_list = []
    for types in type_name:
        type_list.append({
            'type': types,
            'clist': types.goodsinfo_set.order_by('-gclick')[0:3],
            'nlist': types.goodsinfo_set.order_by('-id')[0:4],
        })
    context = {
        'title': '首页',
        'guest_cart': 1,
        'type_list': type_list,
        'cart_count': cart_count(request),
    }
    return render(request, 'df_goods/index.html', context)


def glist(request, pid, pindex, op):
    x = int(pid)
    new_list = GoodsInfo.objects.filter(gtype_id=x).order_by('-id')[0:2]
    order_price = GoodsInfo.objects.filter(gtype_id=x).order_by('-gprice')
    order_click = GoodsInfo.objects.filter(gtype_id=x).order_by('-gclick')
    goods_list = GoodsInfo.objects.filter(gtype_id=x)
    type_name = TypeInfo.objects.get(id=pid)
    page = ''
    if op == '1':
        # 返回的是分页对象,把指定的列表按照要求,每页n条分页
        p = Paginator(goods_list, 10)
        # 返回page对象,表示第几页数据
        page = p.page(int(pindex))
    elif op == '2':
        p = Paginator(order_price, 10)
        page = p.page(int(pindex))
    elif op == '3':
        p = Paginator(order_click, 10)
        page = p.page(int(pindex))

    context = {
        'title': '列表页',
        'type_name': type_name,
        'newlist': new_list,
        'page': page,
        'tid': pid,
        'pageid': op,
        'cart_count': cart_count(request),

    }
    return render(request, 'df_goods/list.html', context)


def detail(request, pid):
    good = GoodsInfo.objects.get(id=pid)
    good.gclick = good.gclick + 1
    good.save()

    newlist = GoodsInfo.objects.filter(gtype_id=good.gtype_id).order_by('-id')[0:2]
    context = {
        'title': '详细信息',
        'goods': good,
        'type': TypeInfo.objects.get(id=good.gtype_id),
        'newlist': newlist,
        'cart_count': cart_count(request),
    }
    response = render(request, 'df_goods/detail.html', context)

    # 设置cookie,用于调取浏览记录
    r_str = request.COOKIES.get('record', '')
    if r_str != '':
        r_list = r_str.split(',')
        if pid in r_list:
            r_list.remove(pid)
        r_list.insert(0, pid)
        if len(r_list) > 5:
            r_list.pop()
        record = ','.join(r_list)
        response.set_cookie('record', record)
    else:
        response.set_cookie('record', pid)

    return response


from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        extra = super(MySearchView, self).extra_context()
        extra['title'] = self.request.GET.get('q')
        return extra


def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0