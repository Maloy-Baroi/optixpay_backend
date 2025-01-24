import secrets

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel
from django.db import models

from utils.generate_unique_id import generate_short_uuid


class MerchantProfile(BaseModel):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('hold', 'hold'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30, null=True, blank=False)
    unique_id = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='merchant_logos')
    payment_methods = models.ManyToManyField('app_bank.BankTypeModel', related_name='merchant_payment_method', blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    merchant_wallet = models.ManyToManyField('app_profile.MerchantWallet', related_name='merchant_profiles', blank=True)
    app_key = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)
    is_negative_transaction_allowed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.secret_key:  # Generate only if not already set
            self.secret_key = secrets.token_urlsafe(64)  # 64 bytes long secret
        if not self.app_key:  # Generate only if not already set
            self.app_key = secrets.token_urlsafe(32)  # 32 bytes long app key
        if not self.unique_id:
            self.unique_id = f"merchant_{generate_short_uuid()}"
        super(MerchantProfile, self).save(*args, **kwargs)


