from rest_framework import serializers
from .models import Account, Order, \
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

class AccountSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Account        
        fields = (
            'username',
            'phone',
            'email',
            'company',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'birthdate',
            'is_active',
            'is_staff',
            'is_admin',
            'is_superuser',
            'created_at',
            'updated_at'
        )
        read_only_fields = [ 'created_at', 'updated_at' ]


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:        
        model = OrderType        
        fields = (
            'id',
            'code',
            'name'
        )       

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:        
        model = OrderStatus        
        fields = (
            'id',
            'code',
            'name'
        )         

class OrderSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Order        
        fields = (
            'id',
            'description',
            'o_type',
            'o_status',
            'created_by',
            'created_at'
        )
        read_only_fields = [ 'created_at' ]

class OrderDetailedSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Order        
        fields = (
            'id',
            'description',
            'o_type',
            'o_status',
            'created_by',
            'created_at'
        )
        
        depth = 1