# coding=utf-8
from django.db import models
from df_goods.models import *
from df_user.models import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Create your models here.


class CartInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    user = models.ForeignKey(UserInfo)

