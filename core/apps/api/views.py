# from django.contrib.auth.models import User
# from myapp.serializers import UserSerializer
from re import L
from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from apps.models import (
    StoreHouse,
    Station,
    User,
    Incoming,
    Outgoing,
    IncomingReturns,
    Image,
    StoreHouseCategroy,
    Supplier,
    Category,
    Beneficiary,
    
)
from .serializers import (
    StoreHouseSerializer,
    StationSerializer,
    StoreHouseCategroySerializer,
    SupplierSerializer,
    BeneficiarySerializer,
    UserSerializer,
    IncomingSerializer,
    OutgoingSerializer,
    DamagedSerializer,
    TransformationstorehouseSerializer,
)


class StoreHouseView(viewsets.ModelViewSet):
    queryset = StoreHouse.objects.all()
    serializer_class = StoreHouseSerializer
    search_fields = ['id', ]
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
# Todo should rename classes name to be end with ViewSets    
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  

class IcomingViewList(viewsets.ModelViewSet):
    queryset = Incoming.objects.all()
    serializer_class = IncomingSerializer 
    
class StoreHouseCategroyViewList(viewsets.ModelViewSet):
    queryset = StoreHouseCategroy.objects.all()
    serializer_class = StoreHouseCategroySerializer
    
class OutgoinViewList(viewsets.ModelViewSet):
    queryset = Outgoing.objects.all()
    serializer_class = OutgoingSerializer
    

class TransformationstorehouseViewList(ListAPIView):
    pass

class DamagedViewList(ListAPIView):
    pass
          