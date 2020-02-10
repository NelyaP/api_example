from django.shortcuts import render
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
