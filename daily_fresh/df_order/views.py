# coding=utf-8
from django.shortcuts import render, redirect
from models import *
from df_user.models import *
from df_goods.models import *
from df_cart.models import *
from django.db import transaction
from datetime import datetime
from django.core.paginator import Paginator

# Create your views here.


def orders(request):
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


# 1、判断库存
# 2、减少库存
# 3、创建订单对象
# 4、创建详单对象
# 5、删除购物车
# 对于以上操作，应该使用事务
# 问题是：在django的模型类中如何使用事务？

@transaction.atomic
def handle(request):
    # 获取post传递的值
    post = request.POST
    uaddr = post.get('user_addr')
    cart_id = post.getlist('cart_id')

    # 设置保存点
    sid = transaction.savepoint()

    # 判断异常，决定事物的提交或回滚
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = 0
        order.oaddress = uaddr
        order.save()
        # 计算总金额
        total = 0
        # 创建订单详细页
        for cid in cart_id:
            cart = CartInfo.objects.get(id=cid)
            if cart.count <= cart.goods.ginventory:
                cart.goods.ginventory -= cart.count
                cart.goods.save()
                detail = OrderDetailInfo()
                detail.goods = cart.goods
                detail.order = order
                detail.price = cart.goods.gprice
                detail.count = cart.count
                detail.save()
                total += cart.goods.gprice * cart.count
                cart.delete()
            else:
                # 表示库存不足
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
        # 保存总价
        order.ototal = total
        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/user/ucenter_order_1/')
    except:
        # 出现任何异常就回滚，之前所有对数据库的操作全部取消
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


#         order_list = OrderInfo.objects.all()
#         p = Paginator(order_list, 2)
#         pindex = 1
#         page = p.page(pindex)
#         context = {
#             'page': page,
#         }
#        return render(request, 'df_user/user_center_order.html', context)
