from django.db import models
from app_bank.models.bank import BankTypeModel
from app_profile.models.merchant import MerchantProfile
from core.models.BaseModel import BaseModel


class MerchantWallet(BaseModel):
    bank = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    wallet_base_currency = models.ForeignKey('app_deposit.Currency', on_delete=models.CASCADE,
                                             related_name='wallet_base_conversions', null=True)

    withdraw_commission = models.FloatField(default=10.00)
    deposit_commission = models.FloatField(default=5.00)
    settlement_commission = models.FloatField(default=2.5)

    class Meta:
        db_table = 'merchant_wallet'


class CurrencyConversion(models.Model):
    base_currency = models.ForeignKey('app_deposit.Currency', on_delete=models.CASCADE, related_name='base_conversions',
                                      null=True)
    to_currency = models.ForeignKey('app_deposit.Currency', on_delete=models.CASCADE, related_name='to_conversions',
                                    null=True)
    conversion_rate = models.FloatField(default=0.00)
    merchant_wallet = models.ForeignKey('MerchantWallet', on_delete=models.CASCADE, related_name='currency_conversions')

    class Meta:
        db_table = 'currency_conversion_based_on_wallet'
        unique_together = ('base_currency', 'to_currency', 'merchant_wallet')  # Ensuring unique rates per wallet

    def save(self, *args, **kwargs):
        if not self.base_currency and self.merchant_wallet:
            self.base_currency = self.merchant_wallet.wallet_base_currency
        super().save(*args, **kwargs)
