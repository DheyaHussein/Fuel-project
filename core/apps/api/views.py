# from django.contrib.auth.models import User
# from myapp.serializers import UserSerializer
from logging import raiseExceptions
from re import L
from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny

from rest_framework import viewsets
from yaml import serialize
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
    IncomeCreateSerializer,
    OutgoingCreateSerializer,
)


class StoreHouseView(viewsets.ModelViewSet):
    # queryset = StoreHouse.objects.all()
    serializer_class = StoreHouseSerializer
    
    search_fields = ['id', ]
    # lookup_field = ['name', ] 
    def get_queryset(self):
        if self.action == 'list':
            print('hi')
            authentication_classes = [AllowAny]
            queryset = StoreHouse.objects.all()
            
            return queryset
        # elif self.action == 'create':
            
        
    
    def create(self, request, *args, **kwargs):
        # print(self.serializer_class.data)    
        return super().create(request, *args, **kwargs)
    
# Todo should rename classes name to be end with ViewSets    
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer 
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
     

class IcomingViewList(viewsets.ModelViewSet):
    queryset = Incoming.objects.all()
    # serializer_class = IncomingSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return IncomeCreateSerializer
        return IncomingSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate the incoming data
        incoming = serializer.save()
        return  Response({
            "message": _("Incoming record created successfully."),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
     
class StoreHouseCategroyViewList(viewsets.ModelViewSet):
    queryset = StoreHouseCategroy.objects.all()
    serializer_class = StoreHouseCategroySerializer
    
class OutgoinViewList(viewsets.ModelViewSet):
    queryset = Outgoing.objects.all()
    # serializer_class = OutgoingSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OutgoingCreateSerializer
        return OutgoingSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        outgoing = serializer.save() 
        return Response({
            "message": _("Incoming record created successfully."),
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

class TransformationstorehouseViewList(ListAPIView):
    pass

class DamagedViewList(ListAPIView):
    pass
          