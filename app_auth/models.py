from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission, GroupManager
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomPermission(models.Model):
    PERMISSION_TYPE = [
        ('Create', 'Create'),
        ('Read', 'Read'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
    ]

    permission_name = models.CharField(max_length=255)
    inclusive_models = models.ManyToManyField(
        ContentType,
        verbose_name=_("content type"),
        blank=True  # Ensures that it's okay for no ContentType to be associated initially
    )
    permission_type = models.CharField(max_length=255, choices=PERMISSION_TYPE, default='Read')

    class Meta:
        unique_together = ('permission_name', 'permission_type')

    def __str__(self):
        # This will output just the permission name and type
        return f"{self.permission_name} | {self.permission_type}"


class CustomGroup(Group):
    all_permissions = models.ManyToManyField(
        CustomPermission,
        verbose_name=_("all_permissions"),
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _("custom_group")
        verbose_name_plural = _("custom_groups")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


# app_auth/models.py
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("The email field must be set!")
        if not username:
            raise ValueError("The username field must be set!")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Check for the 'is_staff' and 'is_superuser' properties
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create and return the superuser
        return self._create_user(email, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    referral = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    write_date = models.DateTimeField(auto_now=True)
    create_uid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='created_users')
    write_uid = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name='written_users')
    is_staff = models.BooleanField(default=False)  # Add this field
    is_active = models.BooleanField(default=True)  # This field is also often required
    new_user = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    groups = models.ManyToManyField(
        CustomGroup,
        related_name='custom_user_set',  # Custom related name to avoid clash
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    def save(self, *args, **kwargs):
        # Check if the password needs to be hashed
        if self._password_is_plain(self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def _password_is_plain(self, password):
        """
        Helper method to check if a password is already hashed.
        Django hashed passwords start with a hash identifier.
        """
        return not password.startswith("pbkdf2_") and not password.startswith("argon2$")

    def set_password(self, raw_password):
        """
        Sets the user’s password to the given raw string, taking care of the hashing.
        """
        super().set_password(raw_password)


class UserVerificationToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification_token')
    token = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
