from django.db import models

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel
from utils.generate_passimpay_id import send_request_with_signature
from utils.generate_unique_id import generate_short_uuid


class AgentProfile(BaseModel):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('hold', 'hold'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default="Unknown")
    phone_number = models.CharField(max_length=30, null=True, blank=False)
    prepayment_address = models.CharField(max_length=255, null=True, blank=True)
    currency = models.ForeignKey('app_deposit.Currency', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='active')
    is_negative_transaction_allowed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Only generate a new unique_id if it doesn't already exist
        if not self.unique_id:
            record_unique_id = f"agent{generate_short_uuid()}"
            self.unique_id = record_unique_id

        if not self.prepayment_address:
            response_from_passimpay = send_request_with_signature(self.unique_id)
            prepayment_address = response_from_passimpay.get('address', None)
            if prepayment_address is not None:
                self.prepayment_address = prepayment_address
        super(AgentProfile, self).save(*args, **kwargs)

