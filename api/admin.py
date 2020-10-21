from django.contrib import admin
from .models import Account, Order, OrderItem, \
    OrderType, OrderStatus, Age, Gender, Income, \
    City, AccountFilter, SourceProp, Calculator

admin.site.register(Account)
admin.site.register(AccountFilter)
admin.site.register(City)
admin.site.register(OrderType)
admin.site.register(OrderStatus)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(SourceProp)
admin.site.register(Age)
admin.site.register(Gender)
admin.site.register(Income)
admin.site.register(Calculator)