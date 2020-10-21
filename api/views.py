from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import Group, Permission
from .models import Account, Order, OrderType, OrderStatus, \
    Age, Gender, Income, City, AccountFilter, SourceProp, OrderItem, \
    Calculator
from django.contrib.auth.models import Group, Permission
from .serializers import AccountSerializer, OrderSerializer, \
    GroupSerializer, PermissionSerializer, OrderDetailedSerializer, \
    OrderTypeSerializer, OrderStatusSerializer, AgeSerializer, \
    GenderSerializer, IncomeSerializer, CitySerializer, \
    AccountFilterSerializer, SourcePropSerializer, OrderItemSerializer, \
    CalculatorSerializer

from utils.pwd_generators import generate_20char_pwd
from django.contrib.auth import get_user_model
from utils.send_email import sp_send_simple_email

import random
import math

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class AccountView(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = Account.objects.filter(username=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(username=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class AccountFilterView(viewsets.ModelViewSet):
    queryset = AccountFilter.objects.all()
    serializer_class = AccountFilterSerializer

class AgeView(viewsets.ModelViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer

class GenderView(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class OrderTypeView(viewsets.ModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer

class OrderStatusView(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(created_by=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class OrderItemView(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderDetailedView(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderDetailedSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(created_by=self.request.user)
        return queryset

class SourcePropView(viewsets.ModelViewSet):
    queryset = SourceProp.objects.all()
    serializer_class = SourcePropSerializer

class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def register(request):
    if not request.method == 'POST':
        return Response({"message": "Only POST method is available"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not 'phone' in request.data \
        or not request.data['phone'] \
        or not 'email' in request.data \
        or not request.data['email'] \
        or not 'alias_name' in request.data \
        or not request.data['alias_name'] \
        or not 'is_allowed' in request.data \
        or not request.data['is_allowed'] \
        or not 'company' in request.data \
        or not request.data['company']:
        
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    phone = request.data['phone']
    email = request.data['email']
    alias_name = request.data['alias_name']
    first_name = None
    if 'first_name' in request.data and request.data['first_name']:
        first_name = request.data['first_name']
    last_name = None
    if 'last_name' in request.data and request.data['last_name']:
        last_name = request.data['last_name']
    is_allowed = request.data['is_allowed']
    company = request.data['company']
    
    User = get_user_model()
    if User.objects.filter(phone=phone).exists():
        return Response({"message": "This phone number is already in use"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"message": "This email is already in use"}, status=status.HTTP_400_BAD_REQUEST)

    found = False
    for _ in range(10):
        # Generate username
        print('tick')
        username_int = f"{random.randint(1, 9999999):07d}"
        username = 'U{}'.format(username_int)
        if not User.objects.filter(username=username).exists():
            found = True
            print('found-', username)
            break

    if not found:
        return Response({"message": "Generation of new login has been failed"}, status=status.HTTP_400_BAD_REQUEST)

    password = generate_20char_pwd()
    User.objects.create_user(
        username=username, 
        password=password, 
        phone=phone, 
        alias_name=alias_name, 
        first_name=first_name, 
        last_name=last_name, 
        email=email, 
        is_allowed=is_allowed,
        company=company)
    # send email
    subject = 'Регистрация в приложении Геоаналитика'
    html = '<p>Уважаемый, ' + alias_name + '! Ваш логин: ' + username + ', пароль: ' + password + '.</p>'
    text = 'Уважаемый, ' + alias_name + '! Ваш логин: ' + username + ', пароль: ' + password + '. '
    sp_send_simple_email(subject, html, text, alias_name, email)

    return Response({"message": "User registared successfully"},status=status.HTTP_201_CREATED)


@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def calculate(request):
    if not request.method == 'POST':
        return Response({"message": "Only POST method is available"}, status=status.HTTP_400_BAD_REQUEST)

    if not 'variant' in request.data \
        or not request.data['variant'] \
        or not 'month_code' in request.data \
        or not request.data['month_code'] \
        or not 'cities' in request.data \
        or not request.data['cities'] \
        or not 'o_type' in request.data \
        or not request.data['o_type'] \
        or not 'segments' in request.data \
        or not request.data['segments'] \
        or not 'poi' in request.data \
        or not request.data['poi']:

        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    if len(request.data['cities']) == 0:
        return Response({"message": "Must be at least 1 picked city"}, status=status.HTTP_400_BAD_REQUEST)
    
    cities = request.data['cities']
    cities_n = len(request.data['cities'])
    amount = 0
    amount_13 = 0
    for city in cities:
        o_type_obj = OrderType.objects.get(pk=request.data['o_type'])
        if not o_type_obj:
            return Response({"message": "Type undefigned"}, status=status.HTTP_400_BAD_REQUEST)

        city_obj = City.objects.get(pk=city)
        if not city_obj:
            return Response({"message": "City undefigned"}, status=status.HTTP_400_BAD_REQUEST)

        category = getattr(city_obj, 'category', None)
        if not category:
            return Response({"message": "Category undefigned"}, status=status.HTTP_400_BAD_REQUEST)

        if cities_n > 12:
            calc = Calculator.objects.filter(
                o_type=o_type_obj,
                category=13,
                month_code=request.data['month_code']
            )
            amount_13 += calc[0].price

        calc = Calculator.objects.filter(
            o_type=o_type_obj,
            category=category,
            month_code=request.data['month_code']
        )

        amount += calc[0].price

    ## Discount ##
    discount = 0
    if cities_n > 5 and cities_n <= 20:
        if request.data['o_type'] == 'population':
            # (!) 30000 is not correct
            discount += (cities_n - 5)*30000*30/100
        else:
            if request.data['o_type'] == 'dynamics':
                # (!) 60000 is not correct
                discount += (cities_n - 5)*60000*30/100
    else:
        if cities_n > 20 and cities_n <= 50:
            if request.data['o_type'] == 'population':
                discount += (city_n - 20)*30000*50/100
            else:
                if request.data['o_type'] == 'dynamics':
                    discount += (city_n - 20)*60000*50/100
        else:
            if cities_n > 50:
                if request.data['o_type'] == 'population':
                    discount += (city_n - 50)*30000*70/100
                else:
                    if request.data['o_type'] == 'dynamics':
                        discount += (city_n - 50)*60000*70/100

    segment_idx = 1.2**len(request.data['segments'])
    poi_amt = len(request.data['poi'])*2000

    price = {
        'amount': round((float(amount) + float(amount_13))*segment_idx + poi_amt, 2),
        'discount': round(discount, 2)
    }

    return Response(price, status=status.HTTP_200_OK)