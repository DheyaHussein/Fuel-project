# from curses import meta
# from dataclasses import fields
from os import name
from pyexpat import model
import re
from tkinter import NO
from attr import fields
from rest_framework import serializers
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
    TransformationStoreHouse,
    
)

class Image_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image", "id")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'     


class Image_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("image", "id")



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StoreHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHouse
        fields = '__all__'
    # def create(self, validated_data):
    #     return super().create(validated_data)    
    def validate(self, attrs):
        
        return super().validate(attrs)

 
class StoreHouseCategroySerializer(serializers.ModelSerializer):
#    catergory = CategorySerializer(many=False)
   catergory = serializers.SerializerMethodField()
   storehouse = serializers.SerializerMethodField()
   

   
   
#    storehouse = StoreHouseSerializer(many=False)
#    print (storehouse.fields.items())
   def get_catergory(self, obj):
       return obj.catergory.name
   
   def get_storehouse(self, obj):
       return obj.storehouse.name
       
       

   
   class Meta:
        model = StoreHouseCategroy
        fields = ['id', 
                  'catergory', 
                  'storehouse', 
                  'measurement_type', 
                  'opening_balance', 
                  'current_amount']
   
 
        
   
        

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'
        
        
class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = '__all__'
        
class SupplierSerializer(serializers.ModelSerializer):
    """

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = Supplier
        fields = '__all__'
        
        
class IncomingSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    station = serializers.SerializerMethodField()
    # attach_file = serializers.SerializerMethodField()# this line need to fix it not retuern the image path
    attach_file = Image_Serializers(many=True, read_only=True) 
    
    def get_store(self, obj):
        return obj.store.name
    def get_supplier(self, obj):
        return obj.supplier.name
    
    def get_station(self, obj):
        return obj.station.station_name
    # def get_attach_file(self, obj):
    #     try:
    #         attach_file = obj.attach_file.url
    #         print(attach_file + 'hi')
    #     except:
    #         attach_file = None
    #     return attach_file        
    class Meta:
        model = Incoming
        fields = '__all__'

        
class OutgoingSerializer(serializers.ModelSerializer):
    store_house = serializers.SerializerMethodField()
    beneficiary = serializers.SerializerMethodField()
    # station = serializers.SerializerMethodField()
    attach_file = Image_Serializers(many=True, read_only=True)

    
    def get_store_house(self, obj):
        return obj.store_house.name
    
    def get_beneficiary(self, obj):
        return obj.beneficiary.name
    
    class Meta:
        model = Outgoing
        fields = '__all__'


class TransformationstorehouseSerializer(serializers.ModelSerializer):
    from_storehouse = serializers.SerializerMethodField()
    to_storehouse = serializers.SerializerMethodField()
    
    
    
    def get_from_storehouse(self, obj):
        return obj.from_storehouse.name
    def get_to_storehouse(self, obj):
        return obj.to_storehouse.name
    class Meta:
        model = TransformationStoreHouse
        fields = '__all__'
    pass       

class DamagedSerializer(serializers.ModelSerializer):
    pass