from django.urls import path, include
# from django.conf.urls import url
from .views import *


urlpatterns = [
    path(r"stores/", StoreHouseView.as_view({'get': 'list'})),
    path(r"stores/create/", StoreHouseView.as_view({'post': 'create'})),
    path(r"stores/<int:pk>/deleate/", StoreHouseView.as_view({'delete': 'destroy'})),
    path(r"stores/<int:pk>/", StoreHouseView.as_view({'get': 'retrieve'})),
    
    
    
    path('users/', UserView.as_view({'get': 'list'})),
    path('users/create/', UserView.as_view({'post': 'create'})),
    
    path('incomes/', IcomingViewList.as_view({'get': 'list'})),
    path('incomes/create/', IcomingViewList.as_view({'post': 'create'})),
    
    path('outgoing/', OutgoinViewList.as_view({'get': 'list'})),
    path('outgoing/create/', OutgoinViewList.as_view({'post': 'create'})),
    
    # path('incoming returen/', StoreHouseCategroyViewList.as_view(), name='list'),
    # path('outgoing returen/', StoreHouseCategroyViewList.as_view(), name='list'),

    
    
]
