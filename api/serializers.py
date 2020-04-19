from rest_framework import serializers
from .models import Account, Order, \
    OrderType, OrderStatus

from django.contrib.auth.models import Group, Permission
#from django.contrib.auth.hashers import make_password

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:        
        model = Account        
        fields = (
            'username',
            'password',
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

    def create(self, validated_data):
        account = super().create(validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account

    def update(self, instance, validated_data):
        account = super().update(instance, validated_data)
        try:
            account.set_password(validated_data['password'])
            account.save()
        except KeyError:
            pass
        return account

class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:        
        model = OrderType        
        fields = (
            'code',
            'name'
        )       

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:        
        model = OrderStatus        
        fields = (
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
        read_only_fields = [ 'created_at' ]
        depth = 1