# coding=utf-8
from django.shortcuts import render, redirect
from df_user.user_center import *
from django.http import JsonResponse
from models import *
from df_user.models import *


# Create your views here.
@login
def cart(request):
    cart_list = CartInfo.objects.filter(user_id=request.session['user_id'])
    context = {
        'title': '购物车',
        'page_name': 1,
        'cart_list': cart_list,
    }
    return render(request, 'df_cart/cart.html', context)


def add(request, gid, count):
    carts = CartInfo.objects.filter(goods_id=gid).filter(user_id=request.session['user_id'])
    if len(carts):
        cart = carts[0]
        cart.count += int(count)
        cart.save()
    else:
        cart = CartInfo()
        cart.count = int(count)
        cart.user_id = request.session['user_id']
        cart.goods_id = int(gid)
        cart.save()

    if request.is_ajax():
        return JsonResponse({'count': CartInfo.objects.filter(user_id=request.session['user_id']).count()})
    else:
        return redirect('/cart/')


def delete(request):
    id = request.GET.get('id')
    cart = CartInfo.objects.get(id=int(id))
    cart.delete()
    return JsonResponse({'result': 'ok'})


def change(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    cart = CartInfo.objects.get(id=int(id))
    cart.count = int(count)
    print count
    cart.save()
    return JsonResponse({'count', cart.count})





