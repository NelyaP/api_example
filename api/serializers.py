from rest_framework import serializers
from .models import Account, Order, OrderItem, \
    OrderType, OrderStatus, Age, Gender, Income, \
    City, AccountFilter, Calculator

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


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'id',
            'id_ref',
            'name_ref',
            'table_ref',
            'grid',
            'centroid_lat',
            'centroid_lon',
            'category',
            'is_active',
            'is_demo'
        )


class AccountSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(
    #    write_only=True,
    #    required=True,
    #    help_text='Leave empty if no change needed',
    #    style={'input_type': 'password', 'placeholder': 'Password'}
    #)

    class Meta:        
        model = Account        
        fields = (
            'username',
            'phone',
            'email',
            'company',
            'inn',
            'alias_name',
            'first_name',
            'last_name',
            'middle_name',
            'gender',
            'birthdate',
            'is_allowed',
            'is_active',
            'active_from',
            'active_to',
            'role',
            'tuturial_passed',
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
            'name',
            'period',
            'count_dt'
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
            'o_type',
            'o_status',
            'amount',
            'discount_amount',
            'description',
            'created_by',
            'created_at'
        )
        read_only_fields = [ 'created_at' ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order',
            'city',
            'slots_lst',
            'filters_lst',
            'poi_lst'
        )

class OrderDetailedSerializer(serializers.ModelSerializer):
    o_type = OrderTypeSerializer(many=False, read_only=True)
    o_status = OrderStatusSerializer(many=False, read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    created_by = AccountSerializer(many=False, read_only=True)
    
    class Meta:        
        model = Order        
        fields = (
            'id',
            'o_type',
            'o_status',
            'amount',
            'discount_amount',
            'description',
            'items',
            'created_by',
            'created_at'
        )
        read_only_fields = [ 'created_at' ]

class AccountFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountFilter
        fields = (
            'account',
            'save_type', 
            'city',
            'poi', 
            'layer', 
            'option', 
            'month',
            'ts',
            'gender', 
            'age',
            'income',
            'count'
        )


class AgeSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Age        
        fields = (
            'code',
            'name'
        )   


class GenderSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Gender        
        fields = (
            'code',
            'name'
        )   


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Income        
        fields = (
            'code',
            'name'
        )   



class CalculatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculator
        fields = (
            'id',
            'o_type',
            'category',
            'month_code',
            'price'
        )