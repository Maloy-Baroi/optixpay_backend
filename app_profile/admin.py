from django.contrib import admin

from app_profile.models.profile import Profile


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'country', 'phone_number', 'created_at')
    search_fields = ('full_name', 'country', 'phone_number')

admin.site.register(Profile, ProfileAdmin)
