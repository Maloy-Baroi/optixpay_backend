import ast
from datetime import timedelta
from pathlib import Path
import os

from decouple import config
from django.contrib import staticfiles

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', "p3o&w8*i$af4)nsb%65k=pyt@%9fkgo9=15^nxqz=o+z!w6i8")

# SECURITY WARNING: don't run with debug turned on in production!
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', 'True') == 'True'

if not DEBUG:
    ALLOWED_HOSTS = ['optixpay.com', 'www.optixpay.com', '46.202.159.210', 'localhost', '127.0.0.1']
else:
    ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # App
    'app_auth.apps.AppAuthConfig',
    'app_profile',
    'app_deposit',
    'app_withdraw',
    'app_bank',
    'app_mobile',
    'app_prepayment',
    'app_sms',
    'core',
    'app_settlement',

    # Additional Libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'simple_history',
    'django_extensions'
]

AUTH_USER_MODEL = 'app_auth.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'optixpay_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'optixpay_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', None),
            'USER': config('DB_USER', None),
            'PASSWORD': config('DB_PASSWORD', None),
            'HOST': config('DB_HOST', None),
            'PORT': config('DB_PORT', '5432'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    # Make sure this path is correct
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Bkash Credential
BKASH_APP_KEY = 'E8QGBD19aGNfjYVmKgqfo9f1tc'
BKASH_APP_SECRET = 'tXTvohbA80UW0qtQazY2xGrEMuxW9uBto7oiwpJQWptFGXOR4gyZ'
BKASH_USERNAME = '01945503874'
BKASH_PASSWORD = '4CSX@Wr[I7B'
BKASH_BASE_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/'
# BKASH_BASE_URL = 'https://tokenized.sandbox.bka.sh/v1.2.0-beta/'

# Path to the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAGAD_BASE_URL = 'https://sandbox-ssl.mynagad.com/api/dfs/'
NAGAD_MERCHANT_ID = '683002007104225'
NAGAD_MERCHANT_MOBILE_NUMBER = '01845651598'
NAGAD_MERCHANT_PUBLIC_KEY = os.path.join(BASE_DIR, 'keys', "Merchant_MC00VHB20088378_1729337532364_pub.pem")
NAGAD_MERCHANT_PRIVATE_KEY = os.path.join(BASE_DIR, 'keys', "Merchant_MC00VHB20088378_1729337532364_pri.pem")
NAGAD_CALLBACK_URL = 'http://optixpay.com/'
NAGAD_API_VERSION = 'v-0.2.0'  # as mentioned in the guide

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Ensure global permission is public unless overridden in views
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT authentication for APIs
    ),
}

CORS_ALLOW_ALL_ORIGINS = True

PASSIMPAY_PLATFORM_ID = config('PASSIMPAY_PLATFORM_ID', None)
PASSIMPAY_SECRET_KEY = config('PASSIMPAY_SECRET_KEY', None)

# SWAGGER_SETTINGS = {
#     'USE_SESSION_AUTH': False,  # Disable session-based authentication for Swagger
#     'SECURITY_DEFINITIONS': None,  # Ensure Swagger doesn't enforce token-based authentication
#     'DEFAULT_INFO': 'optixpay_backend.swagger_urls.schema_view',  # Ensure Swagger loads correctly
# }

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=180),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": os.environ.get('ALGORITHM', 'HS256'),
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@optixpay.com'
EMAIL_HOST_PASSWORD = 'u3P#xEfPD!8PPLX'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'no-reply@optixpay.com'

# EMAIL_HOST="smtp.gmail.com"
# EMAIL_PORT=587
# EMAIL_HOST_USER="supplychain.usbangla@gmail.com"
# EMAIL_HOST_PASSWORD="qtykuvezcccmibyt"
# EMAIL_USE_TLS=True
# DEFAULT_FROM_EMAIL="crm@gmail.com"

# MinIO server connection details
MINIO_STORAGE_ENDPOINT = '147.79.66.187:9000'  # IP address and port of the MinIO server
MINIO_STORAGE_ACCESS_KEY = "DlDYlIh7zzodF08GfMj4"
MINIO_STORAGE_SECRET_KEY = "rZ8kB1B010XJYtF5eTkgTp1Dplncw5tC0eBonQjP"
MINIO_STORAGE_BUCKET_NAME = 'optixpaybucket'  # The bucket name in MinIO

COMMISSION = float(config('COMMISSION', 0))
