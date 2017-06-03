#coding=utf-8
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from django.core.paginator import Paginator

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
        'title': '首页', 'guest_cart': 1,
        'type_list': type_list,
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
        p = Paginator(goods_list, 10)
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
        'new_list': new_list,
        'page': page,
        'tid': pid,
        'pageid': op,

    }
    return render(request, 'df_goods/list.html', context)

def detail(request, pid):
    good = GoodsInfo.objects.get(id=pid)
    newlist = GoodsInfo.objects.filter(gtype_id=good.gtype_id).order_by('-id')[0:2]
    context = {
        'title': '详细信息',
        'goods': good,
        'type': TypeInfo.objects.get(id=good.gtype_id),
        'newlist': newlist,
    }
    return render(request, 'df_goods/detail.html', context)