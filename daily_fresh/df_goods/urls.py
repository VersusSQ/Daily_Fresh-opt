from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index),
    url('^glist(\d+)_(\d+)_?(\d*?)/$', views.glist),
    url('^detail(\d+)/$', views.detail),
    url('^search/$', views.MySearchView()),
]