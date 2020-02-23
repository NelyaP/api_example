from rest_framework import serializers
from .models import User, Report, Order, \
    OrderType, OrderStatus

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