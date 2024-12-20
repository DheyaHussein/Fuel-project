# from django.contrib.auth.models import User
# from myapp.serializers import UserSerializer
from logging import raiseExceptions
from re import L
from pypdf import Transformation
from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action


from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, AllowAny

from rest_framework import viewsets
from yaml import serialize
from apps.models import (
    OutgoingReturns,
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
    Damaged,
    TransformationStoreHouse
    
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
    StoreMovementReportSerializer,
    IncomingReturnsSerializer,
    OutgoingReturnsSerializer,
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
    permission_classes = [IsAuthenticated]
    
    
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
    permission_classes = [IsAuthenticated]
    
    
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

class TransformationstorehouseViewList(viewsets.ModelViewSet):
    """_summary_

    Args:
        viewsets (_type_): _description_
    """
    queryset = TransformationStoreHouse.objects.all()
    serializer_class = TransformationstorehouseSerializer
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Save the serializer, which will handle creating the new record
            self.perform_create(serializer)
        except ValidationError as e:
            # Return a validation error if the quantity is invalid
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        def perform_create(self, serializer):
        # This will call `update_storehouse_quantities` within the serializer's custom save logic
         serializer.save()
    
    
    # pass

class DamagedViewList(viewsets.ModelViewSet):
    queryset = Damaged.objects.all()
    serializer_class = DamagedSerializer
    permission_classes = [IsAuthenticated]  # Adjust as necessary for your use case

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Save the new damaged record
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # pass
          
class StoreMovementReportViewSet(viewsets.ModelViewSet):
    queryset = StoreHouse.objects.all()
    serializer_class = StoreMovementReportSerializer
    permission_classes = [IsAuthenticated]
    
    lookup_field = 'pk'

    # Define a custom action for retrieving the report
    @action(detail=True, methods=['get'])
    def retrieve_report(self, request, pk=None):
        # pk here refers to the store ID
        data = {'store_id': pk}
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
       
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class IncomingReturnsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Incoming Returns.
    """
    queryset = IncomingReturns.objects.all()
    serializer_class = IncomingReturnsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overriding to add custom logic during creation if necessary.
        """
        serializer.save()
        
class OutgoingReturnsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Incoming Returns.
    """
    queryset = OutgoingReturns.objects.all()
    serializer_class = OutgoingReturnsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overriding to add custom logic during creation if necessary.
        """
        serializer.save()