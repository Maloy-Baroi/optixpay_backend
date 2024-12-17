from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model to be inherited by all models.
    Provides common fields and functionality.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",  # Unique related name
        verbose_name="Created By"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",  # Unique related name
        verbose_name="Updated By"
    )
    is_active = models.BooleanField(default=False, verbose_name="Is Active")

    class Meta:
        abstract = True  # Marks this model as abstract (won't create a table)
        ordering = ["-created_at"]  # Default ordering by creation date
        get_latest_by = "created_at"  # Use created_at for latest queries

    def soft_delete(self):
        """Perform a soft delete by setting is_active to False."""
        self.is_active = False
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_active = True
        self.save()

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id})"

