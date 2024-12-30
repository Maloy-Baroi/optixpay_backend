from django.contrib import admin

from app_bank.models.bank import AgentBankModel, BankTypeModel

# Register your models here.
admin.site.register(AgentBankModel)
admin.site.register(BankTypeModel)
