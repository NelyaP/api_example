from django.db import models
from django.utils.translation import ugettext_lazy as _
from utils.pwd_generators import generate_20char_pwd
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class AccountManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('Введите username.'))
        if not password:
            raise ValueError(_('Введите пароль.'))
        account = self.model(username=username, **extra_fields)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_user(self, username, password, **extra_fields):
        if not password:
            password = generate_20char_pwd()
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(username, password, **extra_fields)


class Account(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Female'),
        ('F', 'Male'),
    )

    ROLES_CHOICES = (
        ('trial', 'Trial'),
        ('user', 'User'),
        ('master', 'Master'),
    )

    username = models.CharField(primary_key=True, max_length=100, unique=True)
    phone = models.CharField('Mob. phone', max_length=50, blank=True, null=True)
    email = models.EmailField('E-mail', max_length=500, unique=True, blank=True, null=True)
    company = models.CharField('Company', max_length=250, blank=True, null=True)
    inn = models.CharField('INN', max_length=100, blank=True, null=True)
    alias_name = models.CharField('Alias name', max_length=500, blank=True, null=True)
    first_name = models.CharField('First name', max_length=50, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Middle name', max_length=50, blank=True, null=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField('Date of birth', blank=True, null=True)
    is_allowed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    active_from = models.DateTimeField('Active: From', blank=True, null=True)
    active_to = models.DateTimeField('Active: To', blank=True, null=True)
    role = models.CharField('Role', max_length=20, choices=ROLES_CHOICES, blank=True, null=True)
    tuturial_passed = models.BooleanField(default=False) 
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Last update', auto_now=True, null=True)
    is_staff = models.BooleanField(default=False)                                   # for all stuff
    is_admin = models.BooleanField(default=False)                                   # admin
    is_superuser = models.BooleanField(default=False)  

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class City(models.Model):
    id_ref = models.IntegerField('ID Ref') 
    name_ref = models.CharField('Name Ref', max_length=250)
    table_ref = models.CharField('Table Ref', max_length=250)
    grid = models.CharField('Grid', max_length=250)
    centroid_lat = models.CharField('Latitude', max_length=20, blank=True, null=True)
    centroid_lon = models.CharField('Longitude', max_length=20, blank=True, null=True)
    category = models.SmallIntegerField('Category', blank=True, null=True)
    is_active = models.BooleanField(default=True)  
    is_demo = models.BooleanField(default=False)  

    def __str__(self):
        return self.name_ref


class AccountFilter(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    save_type = models.CharField('Save type', max_length=250) 
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    poi = models.CharField('Poi', max_length=250, blank=True, null=True)
    layer = models.CharField('Layer', max_length=250, blank=True, null=True)
    option = models.CharField('Option', max_length=250, blank=True, null=True)
    month = models.CharField('Month', max_length=250, blank=True, null=True)
    ts = models.CharField('Ts partitions', max_length=500, blank=True, null=True)
    gender = models.CharField('Gender range', max_length=250, blank=True, null=True)
    age = models.CharField('Age range', max_length=250, blank=True, null=True)
    income = models.CharField('Income range', max_length=250, blank=True, null=True)
    count = models.CharField('Count range', max_length=250, blank=True, null=True)

    def __str__(self):
        return self.account + '/' + str(id)


class OrderType(models.Model):
    PERIOD_CHOICES = (
        ('1mth', '1 месяц'),
        ('1d', '1 день'),
        ('30min', '30 минут')
    )
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)
    period = models.CharField('Period', max_length=20, choices=PERIOD_CHOICES)
    count_dt = models.DateTimeField('Count date and time')

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class OrderStatus(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class Order(models.Model):
    o_type = models.ForeignKey(OrderType, on_delete=models.CASCADE)
    o_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    amount = models.DecimalField('Amount', max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField('Discount Amount', max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField('Descr.', max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True) 

    def __str__(self):
        return 'Order #{}'.format(str(self.id))

    @property
    def items(self):
        return self.orderitem_set.all()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    slots_lst = models.CharField('Chosen time slots', max_length=500)
    filters_lst = models.CharField('Chosen filters', max_length=500, blank=True, null=True)
    poi_lst = models.CharField('Chosen POI', max_length=500, blank=True, null=True)

    def __str__(self):
        return 'Item #{}'.format(str(self.id))


# Filters #
class Age(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class Gender(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class Income(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class Calculator(models.Model):
    o_type = models.ForeignKey(OrderType, on_delete=models.CASCADE)
    category = models.SmallIntegerField('Category') 
    month_code = models.IntegerField('Month code') 
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)

    def __str__(self):
        return 'Rule #{}'.format(str(self.id))