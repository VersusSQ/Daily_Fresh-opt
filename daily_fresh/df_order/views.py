# coding=utf-8
from django.shortcuts import render
from models import *
from df_user.models import *
from df_goods.models import *
from df_cart.models import *

# Create your views here.


def order(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    clist = request.GET.getlist('cart_id')
    cart = CartInfo.objects.filter(id__in=clist)
    context = {
        'title': '订单页',
        'user': user,
        'cart_list': cart,
        'page_name': 1,
    }

    return render(request, 'df_order/place_order.html', context)

