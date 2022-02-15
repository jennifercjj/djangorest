import os
from pickle import TRUE
import environ

env = environ.Env()

# Leer el archivo .env
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

#

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST= 'smtp.gmail.com'
#EMAIL_PORT= 587
#EMAIL_HOST_USER = 'alfredoji300@gmail.com'
#EMAIL_HOST_PASSWORD = 'vhrosfovsbtllurp'
#EMAIL_USE_TLS = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'core',
    'cart',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #
]

DEFAULT_FROM_EMAIL=env('DEFAULT_FROM_EMAIL')
NOTIFY_EMAIL=env('NOTIFY_EMAIL')
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR),'templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,public'
        },
            'NAME': 'restaurante',
            'USER': 'admin1',
            'PASSWORD': 'Jenniferjaramillo123',
            'HOST': 'bdresraurante.postgres.database.azure.com',
            'PORT': '5432',

    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PRESERVE_USERNAME_CASING =True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
CRISPY_TEMPLATE_PACK='bootstrap4'
LOGIN_REDIRECT_URL='/'

LANGUAGE_CODE = 'es-ec'
TIME_ZONE = 'America/Guayaquil'
USE_I18N = True
USE_L10N = True

PAYPAL_CLIENT_ID=env('PAYPAL_SANDBOX_CLIENT_ID')
PAYPAL_SECRET_KET=env('PAYPAL_SANDBOX_SECRET_KEY')



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[os.path.join(BASE_DIR,"static")]
STATIC_ROOT = os.path.join(BASE_DIR,"static_root")
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

if DEBUG is False:
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    ALLOWED_HOSTS = ['www.vitacho.es']

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    ####
    EMAIL_HOST= 'smtp.gmail.com'
    EMAIL_PORT= 587
    EMAIL_HOST_USER = 'alfredoji300@gmail.com'
    EMAIL_HOST_PASSWORD = 'vhrosfovsbtllurp'
    EMAIL_USE_TLS = True
    ####
    DATABASES = {
        'default':{
            
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'restaurante',
            'USER': 'admin1',
            'PASSWORD': 'Jenniferjaramillo123',
            'HOST': 'bdresraurante.postgres.database.azure.com',
            'PORT': '5432',
        }

    }

    PAYPAL_CLIENT_ID=env('PAYPAL_LIVE_CLIENT_ID')
    PAYPAL_SECRET_KET=env('PAYPAL_LIVE_SECRET_KEY')
