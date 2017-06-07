from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uName = models.CharField(max_length=20)
    uPwd = models.CharField(max_length=40)
    uEmail = models.CharField(max_length=30)
    uAddr = models.CharField(max_length=50, default='')
    uShou = models.CharField(max_length=50, default='')
    uYoubian = models.CharField(max_length=6, default='')
    uTel = models.CharField(max_length=20, default='')
    isdelete = models.BooleanField(default=False)



