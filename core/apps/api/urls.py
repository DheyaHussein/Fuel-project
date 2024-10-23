from django.urls import path, include
# from django.conf.urls import url
from .views import *


urlpatterns = [
    path(r"store/", StoreHouseView.as_view(), name='list'),
    path('user/', UserView.as_view(), name='list'),
    path('income/', IcomingViewList.as_view(), name='list'),
    path('storecat/', StoreHouseCategroyViewList.as_view(), name='list'),
    
]
