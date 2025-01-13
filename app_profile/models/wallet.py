from django.db import models

from app_bank.models.bank import BankTypeModel
from core.models.BaseModel import BaseModel


class CurrencyConvertion(BaseModel):
    base_currency = models.ForeignKey('app_deposit.Currency', on_delete=models.CASCADE, related_name='base_conversions')
    to_currency = models.ForeignKey('app_deposit.Currency', on_delete=models.CASCADE, related_name='to_conversions')
    base_currency_amount = models.FloatField(default=0)
    to_currency_amount = models.FloatField(default=0)

    class Meta:
        db_table = 'currency_conversion'


class MerchantWallet(BaseModel):
    bank = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    currency_conversion = models.ManyToManyField(CurrencyConvertion, related_name='merchant_wallet', blank=True)


    class Meta:
        db_table = 'merchant_wallet'

