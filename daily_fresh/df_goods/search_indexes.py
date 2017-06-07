# coding=utf-8
from haystack import indexes
from models import GoodsInfo
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class GoodsInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
