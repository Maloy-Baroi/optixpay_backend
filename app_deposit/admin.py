from django.contrib import admin

from app_deposit.models.deposit import Deposit, Currency

# Register your models here.
admin.site.register(Currency)
admin.site.register(Deposit)
