from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.orders),
    url('^handle/$', views.handle),
]