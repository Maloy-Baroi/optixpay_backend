from django.contrib import admin

from app_auth.models import CustomUser, UserVerificationToken


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_filter = ('is_active', 'is_staff')  # Add filters on the right sidebar
    search_fields = ('username', 'email')  # Add search box for username and email
    ordering = ('username',)  # Default ordering by username


admin.site.register(CustomUser, CustomUserAdmin)

class UserVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'user')


admin.site.register(UserVerificationToken, UserVerificationTokenAdmin)
