from django.db import models

from app_bank.models.bank import BankTypeModel
from core.models.BaseModel import BaseModel


class SMSManager(BaseModel):
    amount = models.FloatField(default=0)
    sender = models.CharField(max_length=50)
    balance = models.FloatField(default=0)
    trxId = models.CharField(max_length=255)
    bank = models.CharField(max_length=50)
