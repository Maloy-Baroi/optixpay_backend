from django.db import models

from app_bank.models.bank import AgentBankModel
from core.models.BaseModel import BaseModel


class Wallet(BaseModel):
    bank = models.ForeignKey(AgentBankModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wallet'

