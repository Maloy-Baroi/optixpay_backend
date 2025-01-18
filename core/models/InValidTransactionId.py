from core.models.BaseModel import BaseModel
from django.db import models


class InvalidTransactionId(BaseModel):
    txn_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.txn_id
