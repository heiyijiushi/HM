from  django.urls import path
from . import views
urlpatterns=[
    path('index/',views.TransferView.as_view(),name='index'),
]
