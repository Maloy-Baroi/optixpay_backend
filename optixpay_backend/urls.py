from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from app_auth.views.auto_user_create import AutoCreateUserView
from optixpay_backend import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    path('admin/', admin.site.urls),
    path('api/v1/app-auth/', include('app_auth.urls')),
    path('api/v1/app-profile/', include('app_profile.urls')),
    path('api/v1/app-deposit/', include('app_deposit.urls')),
    path('api/v1/app-withdraw/', include('app_withdraw.urls')),
    path('api/v1/app-bank/', include('app_bank.urls')),
    path('api/v1/app-mobile/', include('app_mobile.urls')),
    path('api/v1/app-prepayment/', include('app_prepayment.urls')),


    path('api/v1/auth/', include('rest_framework.urls')),
    path('auto-user-create/', AutoCreateUserView.as_view(), name='auto-user-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

