from django.urls import path, include
# from django.conf.urls import url
from .views import *


urlpatterns = [
    path(r"store/", StoreHouseView.as_view({'get': 'list'})),
    path(r"store/create/", StoreHouseView.as_view({'post': 'create'})),
    path(r"store/<int:pk>/deleate/", StoreHouseView.as_view({'delete': 'destroy'})),
    path(r"store/<int:pk>/", StoreHouseView.as_view({'get': 'retrieve'})),
    
    
    
    path('user/', UserView.as_view({'get': 'list'})),
    path('income/', IcomingViewList.as_view({'get': 'list'})),
    path('outgoing/', OutgoinViewList.as_view({'get': 'list'})),
    # path('incoming returen/', StoreHouseCategroyViewList.as_view(), name='list'),
    # path('outgoing returen/', StoreHouseCategroyViewList.as_view(), name='list'),

    
    
]
