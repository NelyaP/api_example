from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import Group, Permission
from .models import Account, Order, OrderType, OrderStatus, \
    Age, Gender, Income, City, AccountFilter, OrderItem, \
    Calculator
from django.contrib.auth.models import Group, Permission
from .serializers import AccountSerializer, OrderSerializer, \
    GroupSerializer, PermissionSerializer, OrderDetailedSerializer, \
    OrderTypeSerializer, OrderStatusSerializer, AgeSerializer, \
    GenderSerializer, IncomeSerializer, CitySerializer, \
    AccountFilterSerializer, OrderItemSerializer, \
    CalculatorSerializer

from utils.pwd_generators import generate_20char_pwd
from django.contrib.auth import get_user_model
from utils.send_email import sp_send_simple_email

import random
import math
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

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


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionView(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class AgeView(viewsets.ModelViewSet):
    queryset = Age.objects.all()
    serializer_class = AgeSerializer


class GenderView(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class IncomeView(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

# User Filters #
class OrderTypeUserView(viewsets.ReadOnlyModelViewSet):
    queryset = OrderType.objects.all()
    serializer_class = OrderTypeSerializer

    def get_queryset(self):
        types_lst = ['population']
        done_status_obj = OrderStatus.objects.get(pk='done')
        orders = Order.objects.filter(created_by=self.request.user, o_status=done_status_obj)
        for order in orders:
            if order.o_type.code not in types_lst:
                types_lst.append(order.o_type.code)

        queryset = OrderType.objects.filter(pk__in=types_lst)
        return queryset


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_cities(request):
    if not 'o_type' in request.data \
        or not request.data['o_type']:
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    o_type = request.data['o_type']
    o_type_obj = OrderType.objects.get(pk=o_type)
    if not o_type_obj:
        return Response({"message": "Type is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    # Moscow and Voronezh by default
    if o_type == 'population':
        cities_lst = [1, 3]
    else:
        if o_type == 'dynamics':
            cities_lst = [1, 3]
        else:
            cities_lst = []
        
    done_status_obj = OrderStatus.objects.get(pk='done')
    orders = Order.objects.filter(created_by=request.user, o_status=done_status_obj, o_type=o_type_obj)
    for order in orders:
        items = OrderItem.objects.filter(order=order)
        for item in items:
            if item.city.id not in cities_lst:
                cities_lst.append(item.city.id)

    lst = []
    cities_objs = City.objects.filter(pk__in=cities_lst)
    for obj in cities_objs:
        lst.append({
            'id' : obj.id,
            'id_ref' : obj.id_ref,
            'name_ref' : obj.name_ref,
            'table_ref' : obj.table_ref,
            'grid' : obj.grid,
            'centroid_lat' : obj.centroid_lat,
            'centroid_lon' : obj.centroid_lon,
            'category' : obj.category,
            'is_active' : obj.is_active,
            'is_demo' : obj.is_demo
        })

    return Response(lst, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_slots(request):
    if not 'o_type' in request.data \
        or not request.data['o_type'] \
        or not 'city' in request.data \
        or not request.data['city']:
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    o_type_obj = OrderType.objects.get(pk=request.data['o_type'])
    if not o_type_obj:
        return Response({"message": "Type is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    city_obj = City.objects.get(pk=request.data['city'])
    if not city_obj:
        return Response({"message": "City is not defigned"}, status=status.HTTP_400_BAD_REQUEST)
    
    slots_lst = []
    start_date = date(2018, 1, 1)
    start_datetime = datetime(2018, 1, 1, 0, 0)
    # default 
    if o_type_obj.code == 'population':
        default = 32
        slot_date = start_date + relativedelta(months=+(default-1))
        slots_lst.append({
            'slot': default,
            'title': '{}-{}'.format(slot_date.month, slot_date.year)
        })
    
    done_status_obj = OrderStatus.objects.get(pk='done')
    orders = Order.objects.filter(
        created_by=request.user, 
        o_status=done_status_obj, 
        o_type=o_type_obj
    )
    for order in orders:
        items = OrderItem.objects.filter(
            order=order, 
            city=city_obj
        )
        for item in items:
            slots_txt = item.slots_lst
            for i in slots_txt.split(','):
                if i not in slots_lst:
                    if o_type_obj.code == 'population':
                        # ('1mth', '1 месяц')
                        slot_date = start_date + relativedelta(months=+(int(i)-1))
                        slots_lst.append({
                            'slot': int(i),
                            'title': '{}-{}'.format(slot_date.month, slot_date.year)
                        })
                    else: 
                        if o_type_obj.code == 'dynamics':
                            # ('30min', '30 минут')
                            slot_date = start_datetime + timedelta(minutes=(int(i)-1)*30)
                            slots_lst.append({
                                'slot': int(i),
                                'title': slot_date
                            })

    return Response(slots_lst, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_poi(request):
    if not 'o_type' in request.data \
        or not request.data['o_type'] \
        or not 'city' in request.data \
        or not request.data['city']:
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    o_type_obj = OrderType.objects.get(pk=request.data['o_type'])
    if not o_type_obj:
        return Response({"message": "Type is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    city_obj = City.objects.get(pk=request.data['city'])
    if not city_obj:
        return Response({"message": "City is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    # Get avaliable poi
    poi_lst = []
    done_status_obj = OrderStatus.objects.get(pk='done')
    orders = Order.objects.filter(
        created_by=request.user, 
        o_status=done_status_obj, 
        o_type=o_type_obj
    )
    for order in orders:
        items = OrderItem.objects.filter(
            order=order, 
            city=city_obj
        )
        for item in items:
            poi_txt = item.poi_lst
            if poi_txt:
                for i in poi_txt.split(','):
                    if i not in poi_lst:
                        poi_lst.append(i)
     #{ 'code': 'MiscCategories', 'name': 'Кладбища', 'disabled': True }
    f_poi_lst = [
        { 'code': 'AutoSvc', 'name': 'Автосервисы, АЗС, автомойки', 'disabled': True },
        { 'code': 'Business', 'name': 'Предприятия, бизнес-центры', 'disabled': True },
        { 'code': 'CommSvc', 'name': 'Государственные учреждения', 'disabled': True },
        { 'code': 'EduInsts', 'name': 'Образовательные учреждения', 'disabled': True },
        { 'code': 'Entertn', 'name': 'Театры, клубы, кинотеатры', 'disabled': True },
        { 'code': 'FinInsts', 'name': 'Банки', 'disabled': True },
        { 'code': 'Hospital', 'name': 'Медицинские учреждения', 'disabled': True },
        { 'code': 'Metro', 'name': 'Станции метро', 'disabled': True },
        { 'code': 'ParkRec', 'name': 'Парки, стадионы, фитнесс-центры', 'disabled': True },
        { 'code': 'Restrnts', 'name': 'Рестораны', 'disabled': True },
        { 'code': 'Shopping', 'name': 'Магазины', 'disabled': True },
        { 'code': 'TransHubs', 'name': 'Вокзалы, автовокзалы, метро и жд', 'disabled': True },
        { 'code': 'TravDest', 'name': 'Туристические места', 'disabled': True },
        { 'code': 'Airports', 'name': 'Аэропорты', 'disabled': True }
    ]
    for poi in f_poi_lst:
        if poi['code'] in poi_lst:
            poi['disabled'] = False
                    
    return Response(f_poi_lst, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_user_segment(request):
    if not 'o_type' in request.data \
        or not request.data['o_type'] \
        or not 'city' in request.data \
        or not request.data['city']:
        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    o_type_obj = OrderType.objects.get(pk=request.data['o_type'])
    if not o_type_obj:
        return Response({"message": "Type is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    city_obj = City.objects.get(pk=request.data['city'])
    if not city_obj:
        return Response({"message": "City is not defigned"}, status=status.HTTP_400_BAD_REQUEST)

    # Get avaliable segments
    filters_lst = []
    done_status_obj = OrderStatus.objects.get(pk='done')
    orders = Order.objects.filter(
        created_by=request.user, 
        o_status=done_status_obj, 
        o_type=o_type_obj
    )
    for order in orders:
        items = OrderItem.objects.filter(
            order=order, 
            city=city_obj
        )
        for item in items:
            filters_txt = item.filters_lst
            for i in filters_txt.split(','):
                if i not in filters_lst:
                    filters_lst.append(i)

    return Response(filters_lst, status=status.HTTP_200_OK)
    

@api_view(['POST'])    
@authentication_classes([])
@permission_classes([])
def register(request):
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
    if not 'variant' in request.data \
        or not request.data['variant'] \
        or not 'month_code' in request.data \
        or not request.data['month_code'] \
        or not 'cities' in request.data \
        or not request.data['cities'] \
        or not 'o_type' in request.data \
        or not request.data['o_type'] \
        or not 'segments' in request.data \
        or not 'poi' in request.data:

        return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    if request.data['month_code'] < 13 and request.data['month_code'] not in [1, 3, 6, 12]:
        return Response({"message": "Month code less than 13 must have value 1, 3, 6 or 12"}, status=status.HTTP_400_BAD_REQUEST)
        
    if len(request.data['cities']) == 0:
        return Response({"message": "Must be at least 1 picked city"}, status=status.HTTP_400_BAD_REQUEST)
    
    o_type_obj = OrderType.objects.get(pk=request.data['o_type'])
    if not o_type_obj:
        return Response({"message": "Type undefigned"}, status=status.HTTP_400_BAD_REQUEST)

    cities = request.data['cities']
    cities_n = len(request.data['cities'])
    amount = 0
    amount_13 = 0
    discount_lst = []
    discount_priority = [(3, 1), (2, 2), (1, 3), (98, 4), (99, 5)]
    # month
    month_n = request.data['month_code']
    month_main = month_n
    if month_n > 12:
        month_main = 12

    for city in cities:
        city_obj = City.objects.get(pk=city)
        if not city_obj:
            return Response({"message": "City undefigned"}, status=status.HTTP_400_BAD_REQUEST)

        category = getattr(city_obj, 'category', None)
        if not category:
            return Response({"message": "Category undefigned"}, status=status.HTTP_400_BAD_REQUEST)

        # add for discount
        discount_lst.append({
            'id': city_obj.id,
            'priority': [item for item in discount_priority if item[0] == category][0][1]
        })
        
        if month_n > 12:
            calc_13 = Calculator.objects.filter(
                o_type=o_type_obj,
                category=category,
                month_code=13
            )
            amount_13 += (month_n - 12) * calc_13[0].price

        calc_main = Calculator.objects.filter(
            o_type=o_type_obj,
            category=category,
            month_code=month_main
        )
        amount += calc_main[0].price

    ## Discount ##
    discount = 0
    discount_lst_sorted = sorted(
        discount_lst,
        key=lambda x: x['priority'], reverse=False
    )
    has_discount = []
    if cities_n > 5 and cities_n <= 20:
        has_discount = discount_lst_sorted[0:(cities_n - 5)]
        print('30% Off ', has_discount)
        for i in has_discount:
            category_i = [item for item in discount_priority if item[1] == i['priority']][0][0]
            calc_discount = Calculator.objects.filter(
                o_type=o_type_obj,
                category=category_i,
                month_code=month_main
            )
            discount += calc_discount[0].price*30/100 
    else:
        if cities_n > 20 and cities_n <= 50:
            has_discount = discount_lst_sorted[0:(cities_n - 20)]
            print('50% Off ', has_discount)
            for i in has_discount:
                category_i = [item for item in discount_priority if item[1] == i['priority']][0][0]
                calc_discount = Calculator.objects.filter(
                    o_type=o_type_obj,
                    category=category_i,
                    month_code=month_main
                )
                discount += calc_discount[0].price*50/100 
        else:
            if cities_n > 50:
                has_discount = discount_lst_sorted[0:(cities_n - 50)]
                print('70% Off ', has_discount)
                for i in has_discount:
                    category_i = [item for item in discount_priority if item[1] == i['priority']][0][0]
                    calc_discount = Calculator.objects.filter(
                        o_type=o_type_obj,
                        category=category_i,
                        month_code=month_main
                    )
                    discount += calc_discount[0].price*70/100 

    segment_idx = 1
    if request.data['segments'] != 0:
        segment_idx = 1.2**len(request.data['segments'])

    poi_amt = len(request.data['poi'])*2000

    price = {
        'amount': round((float(amount) + float(amount_13))*segment_idx + poi_amt, 2),
        'discount': round(discount, 2),
        'month': month_n
    }

    return Response(price, status=status.HTTP_200_OK)