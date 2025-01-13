from django.db import models

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel
from utils.generate_unique_id import generate_short_uuid


class AgentProfile(BaseModel):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Pending', 'Pending'),
        ('Hold', 'Hold'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, default="Unknown")
    phone_number = models.CharField(max_length=30, null=True, blank=False)
    prepayment_address = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):

        self.unique_id = f"agent_{generate_short_uuid()}"
        super(AgentProfile, self).save(*args, **kwargs)

