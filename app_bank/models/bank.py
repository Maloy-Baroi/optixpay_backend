from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from app_profile.models.agent import AgentProfile
from core.models.BaseModel import BaseModel

import uuid

class BankTypeModel(BaseModel):
    name = models.CharField(max_length=50, help_text="Name of the bank type, e.g., Bkash, Rocket, Nagad")
    CATEGORY_CHOICES = [
        ('p2p', 'Peer-to-Peer'),
        ('p2c', 'Peer-to-Customer'),
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, help_text="Category of the bank type")
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, help_text="Currency of the bank type")
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.name}_{self.get_category_display()}"

    class Meta:
        db_table = "bank_type"
        verbose_name = "Bank Type"
        verbose_name_plural = "Bank Types"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_name_category'
            )
        ]


class AgentBankModel(BaseModel):
    # Username
    master_username = models.CharField(max_length=50, help_text="Master username", null=True, blank=True)
    master_password = models.CharField(max_length=50, help_text="Master password", null=True, blank=True)
    bank_unique_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the bank")
    # Business Name
    bank_name = models.CharField(max_length=100, help_text="Name of the bank")
    # currency = models.ForeignKey('app_deposit.Currency', on_delete=models.SET_NULL, null=True, blank=True)
    # Bank
    bank_type = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE, related_name="banks", help_text="Type of the bank")
    # Agent
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name="banks_agent", help_text="Agent linked to the bank")
    account_number = models.CharField(
        max_length=50,
    )
    minimum_amount = models.FloatField(
        validators=[MinValueValidator(1.00)],
        default=1.00,
        help_text="Minimum amount allowed"
    )
    maximum_amount = models.FloatField(
        validators=[MinValueValidator(1.00), MaxValueValidator(25000.00)],
        default=25000.00,
        help_text="Maximum amount allowed"
    )
    daily_limit = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Daily transaction limit"
    )
    daily_usage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Daily usage so far"
    )
    monthly_limit = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Monthly transaction limit"
    )
    monthly_usage = models.FloatField(
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Monthly usage so far"
    )

    withdraw_commission = models.FloatField(default=5.00)
    deposit_commission = models.FloatField(default=10.00)

    balance = models.FloatField(default=0.0, help_text="Balance")
    # App Key
    app_key = models.CharField(max_length=255, help_text="API key for the application")
    # Secret Key
    secret_key = models.CharField(max_length=255, help_text="Secret key for the application")

    def __str__(self):
        return self.bank_name

    class Meta:
        db_table = "agent_bank"
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    def check_transaction_limits(self, amount):
        """Check if a transaction is within the daily and monthly limits."""
        if amount + self.daily_usage > self.daily_limit:
            return False, "Daily limit exceeded."
        if amount + self.monthly_usage > self.monthly_limit:
            return False, "Monthly limit exceeded."
        return True, "Transaction within limits."

    def update_usage(self, amount):
        """Update the daily and monthly usage after a transaction."""
        self.daily_usage += amount
        self.monthly_usage += amount
        self.save()

    def save(self, *args, **kwargs):
        """Override save to automatically generate bank_unique_id before saving the instance."""
        if not self.bank_unique_id:
            self.bank_unique_id = str(uuid.uuid4())
        # Ensure that self.created_by_id and self.updated_by_id are managed if needed
        super(AgentBankModel, self).save(*args, **kwargs)
