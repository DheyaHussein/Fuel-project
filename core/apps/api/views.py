# from django.contrib.auth.models import User
# from myapp.serializers import UserSerializer
from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAdminUser
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
    IncomingSerializer
)


class StoreHouseView(ListAPIView):
    queryset = StoreHouse.objects.all()
    serializer_class = StoreHouseSerializer
    
    
class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer  

class IcomingViewList(ListAPIView):
    queryset = Incoming.objects.all()
    serializer_class = IncomingSerializer
    
class StoreHouseCategroyViewList(ListAPIView):
    queryset = StoreHouseCategroy.objects.all()
    serializer_class = StoreHouseCategroySerializer
          