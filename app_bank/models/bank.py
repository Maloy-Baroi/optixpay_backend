from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from app_profile.models.profile import Profile
from core.models.BaseModel import BaseModel

import uuid

class BankTypeModel(BaseModel):
    name = models.CharField(max_length=50, unique=True, help_text="Name of the bank type, e.g., Bkash, Rocket, Nagad")
    CATEGORY_CHOICES = [
        ('p2p', 'Peer-to-Peer'),
        ('p2c', 'Peer-to-Customer'),
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, help_text="Category of the bank type")


    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    class Meta:
        db_table = "bank_type"
        verbose_name = "Bank Type"
        verbose_name_plural = "Bank Types"

    # agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name="banks", help_text="Agent linked to the bank")
    # pial

class BankModel(BaseModel):
    bank_unique_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier for the bank")
    bank_name = models.CharField(max_length=100, help_text="Name of the bank")
    bank_type = models.ForeignKey(BankTypeModel, on_delete=models.CASCADE, related_name="banks", help_text="Type of the bank")
    agent = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="banks_agent", help_text="Agent linked to the bank")
    account_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+880\d{9,10}$', message="Account number must start with +880 and contain 9-10 digits")],
        help_text="Account number in the format +880XXXXXXXXX"
    )
    minimum_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(1.00)],
        default=1.00,
        help_text="Minimum amount allowed"
    )
    maximum_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(1.00), MaxValueValidator(25000.00)],
        default=25000.00,
        help_text="Maximum amount allowed"
    )
    daily_limit = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Daily transaction limit"
    )
    daily_usage = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Daily usage so far"
    )
    monthly_limit = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Monthly transaction limit"
    )
    monthly_usage = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="Monthly usage so far"
    )
    app_key = models.CharField(max_length=255, help_text="API key for the application")
    secret_key = models.CharField(max_length=255, help_text="Secret key for the application")

    def __str__(self):
        return self.bank_name

    class Meta:
        db_table = "bank"
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
            self.bank_unique_id = str(uuid.uuid4())  # Generate a unique UUID as the bank_unique_id
            self.created_by_id = self.agent.id  # Generate a unique UUID as the bank_unique_id
            self.updated_by_id = self.agent.id  # Generate a unique UUID as the bank_unique_id
        super().save(*args, **kwargs)