from django.conf.urls import url
from django.urls import path,re_path
from . import views
urlpatterns=[
    path('',views.index),
    path('booklist/',views.booklist),
    path('booklist.html', views.booklist),
    #path('(\d+)'//'(\d+)',views.booklist),
    re_path(r'^(?P<num1>\d+)/(?P<num2>\d+)/$',views.test),
    re_path(r'^(\d+)/(\d+)/$',views.test2),
    re_path(r'^(\d+)/$', views.test3),
    re_path(r'^register/$', views.Register.as_view(), name='register'),
] #路由引导函数
