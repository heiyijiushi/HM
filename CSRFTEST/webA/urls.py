from django.urls import re_path
from .views import LoginView,TransferView

urlpatterns=[
    re_path(r'^$',LoginView.as_view()),
    re_path(r'^login/$',LoginView.as_view(),name='index'),
    re_path(r'^transfer/$',TransferView.as_view(),name='transfer'),

]