from django.db import models

from app_deposit.models.deposit import Currency
from app_profile.models.profile import Profile
from core.models.BaseModel import BaseModel


class AgentWallet(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
    payment_method = models.CharField(max_length=20)


