from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from optixpay_backend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/app-auth/', include('app_auth.urls')),
    path('api/v1/app-profile/', include('app_profile.urls')),
    path('api/v1/app-deposit/', include('app_deposit.urls')),
    path('api/v1/app-withdraw/', include('app_withdraw.urls')),
    path('api/v1/auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
