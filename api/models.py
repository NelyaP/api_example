from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Female'),
        ('F', 'Male'),
    )

    phone = models.CharField('Mob. phone', max_length=50, blank=True, null=True)
    company = models.CharField('Company', max_length=250, blank=True, null=True)
    middle_name = models.CharField('Middle name', max_length=50, blank=True, null=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

class OrderType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)

class OrderStatus(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=250)

    def __str__(self):
        return '{} / {}'.format(self.code, self.name)

class Order(models.Model):
    number = models.CharField('Number', max_length=250)
    description = models.TextField('Descr.', max_length=500, blank=True)
    o_type = models.ForeignKey(OrderType, on_delete=models.CASCADE)
    o_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True) 