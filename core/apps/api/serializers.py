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
    
 
 
class IncomingReturnsSerializer(serializers.ModelSerializer):
     # Read-only fields derived from the related Incoming instance
    incoming_date = serializers.DateTimeField(read_only=True)
    store_house = serializers.PrimaryKeyRelatedField(read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)
    station = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IncomingReturns
        fields = [
            "incoming",
            "incoming_date",
            "store_house",
            "supplier",
            "station",
            "paper_number",
            "recipient_name",
            "deliverer_name",
            "recipient_miltry_number",
            "deliverer_miltry_number",
            "return_date",
            "cat",
            "returned_quantites",
            "reason_for_return",
            "note",
        ]

    def validate(self, data):
        """Custom validation logic for returned quantities and categories."""
        incoming = data.get("incoming")
        returned_quantities = data.get("returned_quantites")
        category = data.get("cat")

        # Ensure returned quantities are numeric
        try:
            returned_qty = float(returned_quantities)
        except ValueError:
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities must be a valid number."}
            )

        # Ensure the returned category matches the incoming category
        if category != incoming.cat:
            raise serializers.ValidationError(
                {"cat": "The return category must match the incoming category."}
            )

        # Validate returned quantities do not exceed imported quantities
        if returned_qty > float(incoming.imported_quantites):
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities cannot exceed imported quantities."}
            )

        return data

    def create(self, validated_data):
        """Handle creation and update store quantities."""
        incoming = validated_data.get("incoming")
        returned_quantities = float(validated_data.get("returned_quantites"))

        # Fetch related StoreHouseCategory
        store_category_qs = StoreHouseCategroy.objects.filter(
            storehouse=incoming.store, catergory__name=incoming.cat
        ).first()

        if not store_category_qs:
            raise serializers.ValidationError(
                {"store_house": "No matching storehouse category found."}
            )

        # Update the current amount in the storehouse category
        store_category_qs.current_amount -= returned_quantities
        if store_category_qs.current_amount < 0:
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities result in negative stock."}
            )

        store_category_qs.save()

        # Proceed with creating the IncomingReturns record
        return super().create(validated_data)
    # pass
 
 
class OutgoingReturnsSerializer(serializers.ModelSerializer):
     # Read-only fields derived from the related Incoming instance
    outgoing_date = serializers.DateTimeField(read_only=True)
    store_house = serializers.PrimaryKeyRelatedField(read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(read_only=True)
    station = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = IncomingReturns
        fields = [
            "outgoing",
            "outgoing_date",
            "store_house",
            "supplier",
            "station",
            "paper_number",
            "recipient_name",
            "deliverer_name",
            "recipient_miltry_number",
            "deliverer_miltry_number",
            "return_date",
            "cat",
            "returned_quantites",
            "reason_for_return",
            "note",
        ]

    def validate(self, data):
        """Custom validation logic for returned quantities and categories."""
        outgoing = data.get("outgoing")
        returned_quantities = data.get("returned_quantites")
        category = data.get("cat")

        # Ensure returned quantities are numeric
        try:
            returned_qty = float(returned_quantities)
        except ValueError:
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities must be a valid number."}
            )

        # Ensure the returned category matches the incoming category
        if category != outgoing.cat:
            raise serializers.ValidationError(
                {"cat": "The return category must match the outgoing category."}
            )

        # Validate returned quantities do not exceed imported quantities
        if returned_qty > float(outgoing.outgoing_quantites):
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities cannot exceed imported quantities."}
            )

        return data

    def create(self, validated_data):
        """Handle creation and update store quantities."""
        outgoing = validated_data.get("outgoing")
        returned_quantities = float(validated_data.get("returned_quantites"))

        # Fetch related StoreHouseCategory
        store_category_qs = StoreHouseCategroy.objects.filter(
            storehouse=outgoing.store, catergory__name=outgoing.cat
        ).first()

        if not store_category_qs:
            raise serializers.ValidationError(
                {"store_house": "No matching storehouse category found."}
            )

        # Update the current amount in the storehouse category
        store_category_qs.current_amount += returned_quantities
        if store_category_qs.current_amount < 0:
            raise serializers.ValidationError(
                {"returned_quantites": "Returned quantities result in negative stock."}
            )

        store_category_qs.save()

        # Proceed with creating the IncomingReturns record
        return super().create(validated_data)
 
        
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
    from_storehouse = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    to_storehouse = serializers.PrimaryKeyRelatedField(queryset=StoreHouse.objects.all())
    
    
    def validate(self, data):
        from_storehouse = data.get("from_storehouse")
        to_storehouse = data.get("to_storehouse")
        transform_quantites = data.get("transform_quantites")
        cat = data.get("cat")
        
        # Check if from_storehouse and to_storehouse are different
        if from_storehouse == to_storehouse:
            raise serializers.ValidationError("The 'from' and 'to' storehouses must be different.")
        
        # Retrieve store categories for the from_storehouse and to_storehouse
        store_category_from = StoreHouseCategroy.objects.filter(storehouse=from_storehouse, catergory__name=cat).first()
        store_category_to = StoreHouseCategroy.objects.filter(storehouse=to_storehouse, catergory__name=cat).first()
        
         # Validate existence of categories
        if not store_category_from or not store_category_to:
            raise serializers.ValidationError("Either the 'from' or 'to' storehouse category does not exist.")
                
        # Validate available quantity
        if transform_quantites > store_category_from.current_amount:
            raise serializers.ValidationError("The transform quantities exceed the available quantity in the 'from' storehouse.")
        return data


    def create(self, validated_data):
        transformation = TransformationStoreHouse.objects.create(**validated_data)
        transformation.update_storehouse_quantities()
        
        return transformation
        
         
    class Meta:
        model = TransformationStoreHouse
        fields = '__all__'
           

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
    income_return = serializers.SerializerMethodField()
    outgoing_return = serializers.SerializerMethodField()

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
    def get_income_return(self, obj):
        return_data = IncomingReturns.objects.filter(store_house=obj.id)
        return IncomingReturnsSerializer(return_data, many=True).data
    def get_outgoing_return(self, obj):
        return_data = OutgoingReturns.objects.filter(store_house=obj.id)
        return OutgoingSerializer(return_data, many=True).data
        

    def to_representation(self, instance):
        # Custom serialization logic to include the store and its movement data
        report_data = {
            "store": instance.id,
            "incoming": self.get_incoming(instance) or None,
            "outgoing": self.get_outgoing(instance) or None,
            "damaged": self.get_damaged(instance) or None,
            "income return": self.get_income_return(instance) or None,
            "outgoing return": self.get_outgoing_return(instance) or None,
        }
        return report_data

    class Meta:
        fields = ['incoming', 'outgoing', 'damaged']
        

class StoreSatatSerializer(serializers.ModelSerializer):
   pass 
