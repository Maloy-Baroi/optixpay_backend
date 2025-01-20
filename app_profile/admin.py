from django.contrib import admin
from app_profile.models.wallet import CurrencyConversion, MerchantWallet
from app_profile.models.agent import AgentProfile
from app_profile.models.merchant import MerchantProfile

admin.site.register(CurrencyConversion)
admin.site.register(MerchantWallet)
admin.site.register(AgentProfile)
admin.site.register(MerchantProfile)