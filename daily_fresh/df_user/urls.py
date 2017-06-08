from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.index),
    url('^register/$', views.register),
    url('^register_handle/$', views.register_handle),
    url('^register_exist/$', views.register_exist),
    url('^login/$', views.login),
    url('^login_handle/$', views.login_handle),
    url('^logout/$', views.logout),
    url('^ucenter_info/$', views.ucenter_info),
    url('^ucenter_site/$', views.ucenter_site),
    url('^ucenter_order_(\d+)/$', views.ucenter_order),
    url('^pay/$', views.pay),
]