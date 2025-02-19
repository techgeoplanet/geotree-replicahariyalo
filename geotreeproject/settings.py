#VERSION = '1.5.0'
from pathlib import Path
from datetime import timedelta
import os
from decouple import AutoConfig
# Import required settings for Google Cloud Storage
#from google.oauth2 import service_account

# Automatically find the .env file and load the environment variables
config = AutoConfig()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['www.hariyalo.rajasthan.gov.in','hariyalo.rajasthan.gov.in','172.21.91.217','127.0.0.1']
CSRF_TRUSTED_ORIGINS = [
    'http://172.21.91.217/',  # Added scheme
    'https://www.hariyalo.rajasthan.gov.in',
    'https://hariyalo.rajasthan.gov.in'
]

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'rest_framework_simplejwt',
    'account',
    'api',
    'admindashboard',
    'subweb',
    'portaldash',
    'map',
    'rangefilter',
    'api_nursery',
    'update_app',
    'publicqrcode',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.RequestLimitMiddleware',
]

ROOT_URLCONF = 'geotreeproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "admindashboard/templates"],
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

WSGI_APPLICATION = 'geotreeproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": "mydatabase",
#     }
# }

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': config('DATABASE_NAME'),
       'USER': config('DATABASE_USER'),
       'PASSWORD': config('DATABASE_PASSWORD'),
       'HOST': config('DATABASE_HOST'),
       'PORT': config('DATABASE_PORT', default='5432'),
 }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'gpspl',
#         'USER': 'postgres',
#         'PASSWORD': 'Admin@123#',
#         'HOST': '172.21.83.82',
#         'PORT': '5432',
#     }
# }

# Uncomment if using PostgreSQL


# JWT Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# If you want to use separate backends for static and media files, uncomment and update the lines below
# STATICFILES_STORAGE = 'my_project.settings.StaticStorage'
# DEFAULT_FILE_STORAGE = 'my_project.settings.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'
AUTH_USERTEMP_MODEL = 'account.TempUser'

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
# sms otp send config

SMS_OTP_SENDER_ID = config('SMS_OTP_SENDER_ID')
SMS_OTP_ENTITY_ID = config('SMS_OTP_ENTITY_ID')
SMS_OTP_TEMPLATEID_ID = config('SMS_OTP_TEMPLATEID_ID')
SMS_OTP_API_KEY = config('SMS_OTP_API_KEY')
SMS_OTP_API_URL = config('SMS_OTP_API_URL')


# FOR GEOMAP CONFIG 

GEO_MAP_API_URL = config('GEO_MAP_API_URL')
GEO_MAP_API_X_AUTH_KEY = config('GEO_MAP_API_X_AUTH_KEY')
GEO_MAP_API_X_USERNAME = config('GEO_MAP_API_X_USERNAME')



# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

PASSWORD_RESET_TIMEOUT=900  # 900 Sec = 15 Min
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    # "http://192.168.1.59:8000",
]
CORS_ALLOW_ALL_ORIGINS = True



#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'
# MEDIA_ROOT = '/DATA/media/'
# MEDIA_URL = '/DATA/media/'



# Media settings for local filesystem
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTHENTICATION_BACKENDS = [
    'account.authentication.CustomUserBackend',
    'account.authentication.TempUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        }
    }
}

SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SECURE = True

ANONYMOUS_REQUEST_LIMIT = 300  # Number of allowed requests for an
AUTHENTICATED_REQUEST_LIMIT = 2000  # Number of allowed requests for authenticated users
REQUEST_TIMEOUT = 3600  # Timeout in seconds (e.g., 1 hour)
