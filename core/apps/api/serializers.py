# from curses import meta
# from dataclasses import fields
from os import name
from pyexpat import model
import re
from tkinter import NO
from typing import Required
from attr import fields
import attr
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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
    Damaged
    
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


class IncomeCreateSerializer(serializers.ModelSerializer):
    store = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.all())
    attach_file = Image_Serializers(many=True, required=False) 
    
    def get_store(self, obj):
        return obj.store.name

    def get_supplier(self, obj):
        return obj.supplier.name
    
    def get_station(self, obj):
        return obj.station.station_name    

    def create(self, validated_data):
        attach_file = validated_data.pop('attach_file', None)
        # store = validated_data.pop('store')
        
        
        incoming = Incoming.objects.create(**validated_data)
        if attach_file:
            incoming.attach_file.set(attach_file)
            
       # Update the corresponding StoreHouseCategroy's current amount
       
        # store_cat = StoreHouseCategroy.objects.filter(catergory__name=incoming.cat, storehouse=incoming.store).filter()
        # print(store_cat)
        # print(incoming.cat)
        # if store_cat:
            
        #     for store_cat_sq in store_cat:
        #         store_cat_sq.current_amount += float(incoming.imported_quantites) 
        #         print(f"Updating {store_cat} current amount from {store_cat_sq.current_amount - float(incoming.imported_quantites)} to {store_cat_sq.current_amount}")
    
        #         store_cat_sq.save()
        # else:
        #     # Log a warning if the store category was not found
        #     print(f"Warning: StoreHouseCategory not found for store {incoming.store} and category {incoming.cat}")
      
        # log_event(in)
        

        
        
        return incoming
    class Meta:
        model = Incoming
        fields = '__all__'
    # pass
    
        
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

class OutgoingCreateSerializer(serializers.ModelSerializer):
    store_house = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    beneficiary = serializers.PrimaryKeyRelatedField(queryset=Beneficiary.objects.all())
    attach_file = Image_Serializers(many=True, read_only=False, required=False)
    
    def validate(self, data):
        outgoing_quantites = data.get('outgoing_quantites')
        print(outgoing_quantites)
        store_house = data.get('store_house')
        cat = data.get('cat')
        store_categroy_qs = StoreHouseCategroy.objects.filter(storehouse=store_house, catergory__name=cat)
        print(store_categroy_qs)
        for stor in store_categroy_qs:
            if stor.current_amount < float(outgoing_quantites):
                raise ValidationError(_("Not enough stock in the storehouse for this category.")) 
        return data
    
    def create(self, validated_data):
        attach_file = validated_data.pop('attach_file', None)
        
        outgoing = Outgoing.objects.create(**validated_data)
        
        if attach_file:
            outgoing.attach_file.set(attach_file)
        return outgoing
    
    class Meta:
        model = Outgoing
        fields = '__all__'
    
    # pass
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
    store = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    
    def validate(self, data):
        # Retrieve related fields from data
        store = data.get('store')
        cat = data.get('cat')
        damaged_quantites = data.get('damaged_quantites')
        
        # Check available stock for the specific category in the store
        store_category_qs = StoreHouseCategroy.objects.filter(storehouse=store, catergory__name=cat)
        if not store_category_qs.exists():
            raise ValidationError("The specified category does not exist in this store.")

        # Ensure there's enough stock to mark as damaged
        for store_category in store_category_qs:
            if store_category.current_amount < damaged_quantites:
                raise ValidationError("Damaged quantity exceeds the available stock in the store.")

        return data

    class Meta:
        model = Damaged
        fields = '__all__'
    # pass


class StoreMovementReportSerializer(serializers.Serializer):
    # store = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    incoming = serializers.SerializerMethodField()
    outgoing = serializers.SerializerMethodField()
    damaged = serializers.SerializerMethodField()

    def get_incoming(self, obj):
        # Retrieve Incoming entries related to the store
        incoming_data = Incoming.objects.filter(store=obj.id)
        return IncomingSerializer(incoming_data, many=True).data

    def get_outgoing(self, obj):
        # Retrieve Outgoing entries related to the store
        outgoing_data = Outgoing.objects.filter(store_house=obj.id)
        return OutgoingSerializer(outgoing_data, many=True).data

    def get_damaged(self, obj):
        # Retrieve Damaged entries related to the store
        damaged_data = Damaged.objects.filter(store=obj.id)
        return DamagedSerializer(damaged_data, many=True).data

    def to_representation(self, instance):
        # Custom serialization logic to include the store and its movement data
        report_data = {
            "store": instance.id,
            "incoming": self.get_incoming(instance) or None,
            "outgoing": self.get_outgoing(instance) or None,
            "damaged": self.get_damaged(instance) or None,
        }
        return report_data

    class Meta:
        fields = ['incoming', 'outgoing', 'damaged']
