from rest_framework import serializers
from apps.models import *


class StoreHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHouse
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'        