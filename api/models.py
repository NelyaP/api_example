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

    username = models.CharField(primary_key=True, max_length=100, unique=True)
    phone = models.CharField('Mob. phone', max_length=50, blank=True, null=True)
    email = models.EmailField('E-mail', max_length=500, unique=True, blank=True, null=True)
    company = models.CharField('Company', max_length=250, blank=True, null=True)
    first_name = models.CharField('First name', max_length=50, blank=True, null=True)
    last_name = models.CharField('Last name', max_length=50, blank=True, null=True)
    middle_name = models.CharField('Middle name', max_length=50, blank=True, null=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthdate = models.DateField('Date of birth', blank=True, null=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Last update', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)                                   # for all users
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

class Source(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)


class OrderType(models.Model):
    code = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=250)

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
    period = models.PositiveSmallIntegerField('Period (month)', default=0)
    offer = models.CharField('Offer', max_length=250, blank=True, null=True)
    amount = models.DecimalField('Amount', max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField('Descr.', max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True) 