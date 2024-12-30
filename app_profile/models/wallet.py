from django.db import models

from app_bank.models.bank import BankTypeModel
from app_deposit.models.deposit import Currency
from core.models.BaseModel import BaseModel


# class CurrencyConvertion(BaseModel):
#     base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
#     base_currency_amount = models.DecimalField(max_digits=8, decimal_places=2)
#     to_currency_amount = models.DecimalField(max_digits=8, decimal_places=2)
#
#     class Meta:
#         db_table = 'currency'


class MerchantWallet(BaseModel):
    bank = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    # currency_conversion = models.ManyToManyField(CurrencyConvertion, related_name='merchant_wallet', blank=True)


    class Meta:
        db_table = 'merchant_wallet'

