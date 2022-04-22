from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('booklist/',views.booklist),
] #路由引导函数
