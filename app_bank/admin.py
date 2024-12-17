from django.contrib import admin

from app_bank.models.bank import BankModel, BankTypeModel

# Register your models here.
admin.site.register(BankModel)
admin.site.register(BankTypeModel)
