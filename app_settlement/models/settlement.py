from django.db import models
from app_deposit.models.deposit import Currency
from core.models.BaseModel import BaseModel


class Settlement(BaseModel):
    STATUS_CHOICES = [
        ('completed', 'completed'),
        ('pending', 'pending'),
        ('failed', 'failed'),
    ]

    settlement_id = models.CharField(max_length=20, unique=True)
    merchant_id = models.ForeignKey('app_profile.MerchantProfile', on_delete=models.CASCADE, null=True)
    wallet = models.ForeignKey('app_profile.MerchantWallet', on_delete=models.DO_NOTHING, blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    commission_percentage = models.FloatField(default=0) # fees
    # Newly added fields
    commission_amount = models.FloatField(default=0)
    exchange_rate = models.FloatField(default=0)

    amount_after_commission = models.FloatField(default=0)
    amount_in_usd = models.FloatField(default=0)
    txn_id = models.CharField(max_length=20, unique=True)
    usdt_address = models.CharField(max_length=34)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.settlement_id} - {self.merchant_id.name}"
