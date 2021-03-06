from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    isdelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=100)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isdelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=10)
    gclick = models.IntegerField(default=0)
    gabstract = models.CharField(max_length=100)
    ginventory = models.IntegerField(default=100)
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle.encode('utf-8')

