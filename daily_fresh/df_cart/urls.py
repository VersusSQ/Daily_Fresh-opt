from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.cart),
    url('^add(\d+)_(\d+)/$', views.add),
    url('^count_change/$', views.change),
    url('^delete/$', views.delete),
]