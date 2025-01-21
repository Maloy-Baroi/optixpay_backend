from django.db import models

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel
from utils.generate_unique_id import generate_short_uuid


class StaffProfile(BaseModel):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('hold', 'hold'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        self.unique_id = f"staff_{generate_short_uuid()}"
        super(StaffProfile, self).save(*args, **kwargs)
