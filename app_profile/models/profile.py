import hashlib
import uuid

from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel


def upload_to(instance, filename):
    return f'profiles/{instance.full_name}/{filename}'

def generate_short_uuid():
    """Generates a 10-character unique key using a UUID and hashing."""
    uuid_str = str(uuid.uuid4())
    hash_object = hashlib.sha256(uuid_str.encode())
    hex_digest = hash_object.hexdigest()
    return hex_digest[:10]

class Profile(BaseModel):
    # Choices for document type
    DOCUMENT_TYPE_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('NID', 'NID'),
        ('DRIVING_LICENSE', 'Driver License'),
    ]

    # Choices for countries (can also use a library like pycountry for dynamic country data)
    COUNTRY_CHOICES = [
        ('BD', 'Bangladesh'),
        ('US', 'United States'),
        ('IN', 'India'),
        ('UK', 'United Kingdom'),
        ('CA', 'Canada'),
        # Add more as needed
    ]

    PROFILE_CHOICES = [
        ('Admin', 'Admin'),
        ('Merchant', 'Merchant'),
        ('Agent', 'Agent'),
        ('Staff', 'Staff'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Active', 'Active'),
        ('Rejected', 'Rejected'),
        ('Hold', 'Hold'),
    ]

    # Fields
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=100, unique=True, default=f"agent_{generate_short_uuid()}")
    profile_type = models.CharField(max_length=20, choices=PROFILE_CHOICES, verbose_name="Profile_type",default='Agent')
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    country = models.CharField(max_length=25, choices=COUNTRY_CHOICES, verbose_name="Country")
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^(\+88)?01[3-9]\d{8}$',
                "Phone number must be a valid Bangladeshi number. Examples: '+8801855555555' or '01855555555'."
            )
        ],
        verbose_name="Phone Number"
    )

    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram Handle")
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Document Type"
    )
    front_side = models.FileField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name="Front Side"
    )
    back_side = models.FileField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name="Back Side",
        blank=True,
        null=True
    )
    selfie_with_id = models.FileField(
        upload_to=upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name="Selfie with ID/Passport"
    )

    status = models.CharField(max_length=20, verbose_name="Status", choices=STATUS_CHOICES, default='Pending')

    # Methods for file names and other utilities
    def get_full_document_path(self):
        """Returns all file paths."""
        return {
            "front_side": self.front_side.url if self.front_side else None,
            "back_side": self.back_side.url if self.back_side else None,
            "selfie_with_id": self.selfie_with_id.url if self.selfie_with_id else None,
        }

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        Overridden save method to generate unique_id based on profile_type.
        """
        if not self.id:  # Check if it's a new instance (not an update)
            # Generate a random unique ID based on profile_type
            random_unique_id = generate_short_uuid()
            self.unique_id = f"{self.get_profile_type_prefix()}_{random_unique_id}"

        super().save(*args, **kwargs)  # Call the original save method

    def get_profile_type_prefix(self):
        """
        Helper function to get the prefix for unique_id based on profile_type.
        """
        if self.profile_type == 'Agent':
            return "agent"
        elif self.profile_type == 'Merchant':
            return "merchant"
        elif self.profile_type == 'Admin':
            return "admin"
        elif self.profile_type == 'Staff':
            return "staff"
        else:
            return ""  # Handle unexpected profile_type
