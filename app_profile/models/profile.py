from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_auth.models import CustomUser
from core.models.BaseModel import BaseModel


def upload_to(instance, filename):
    return f'profiles/{instance.full_name}/{filename}'

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
        ('CS', 'Customer'),
        ('MC', 'Merchant'),
        ('AG', 'Agent'),
    ]

    # Fields
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=3, choices=PROFILE_CHOICES, verbose_name="Profile_type",default='CS')
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, verbose_name="Country")
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

# Signal for post-save actions
# @receiver(post_save, sender=Profile)
# def post_save_profile(sender, instance, created, **kwargs):
#     if created:
#         # Add custom logic here, like sending a notification
#         print(f"Profile created for {instance.full_name}.")