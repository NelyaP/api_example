from rest_framework import serializers
from .models import User, Report, Order, \
    OrderType, OrderStatus

from django.contrib.auth.models import Group, Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:        
        model = User        
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Report        
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Order        
        fields = '__all__'