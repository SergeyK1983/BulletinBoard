from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u18!^&+u#sa^@t@-*o#_=-=m%2eg7@o0g1vl=b3%(zav%a@8l*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "cabinet.User"

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',  # Для простых страничек
    'django.contrib.flatpages',  # Для простых страничек

    'announcement.apps.AnnouncementConfig',
    'cabinet.apps.CabinetConfig',
    'coment.apps.ComentConfig',

    'corsheaders',
    'rest_framework',
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],

    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",  # формат вывода времени в ответах
}

CORS_ORIGIN_ALLOW_ALL = True  # added to solve CORS
CORS_ALLOW_HEADERS = ('content-disposition', 'accept-encoding',
                      'content-type', 'accept', 'origin', 'Authorization',
                      'access-control-allow-methods', 'access-control-allow-origin',
                      'access-control-allow-credentials', 'attribution-reporting',
                      )

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',
# ]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # added to solve CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'Adboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Adboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME', 'pgdb'),
        'USER': os.getenv('USER', 'root'),
        'PASSWORD': os.getenv('PASSWORD', 'root'),
        'HOST': os.getenv('HOST', 'localhost'),
        'PORT': os.getenv('PORT', '5437')
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'  # 'en-us'

TIME_ZONE = 'Europe/Moscow'  # 'UTC'

USE_I18N = True

USE_TZ = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# две переменные, чтобы не путаться; SERG - потому что мои переменные, а не django, чтобы не забыть.
SERG_USER_CONFIRMATION_KEY = "user_confirmation_{token}"  # шаблон для ключа
SERG_USER_CONFIRMATION_TIMEOUT = 60  # время в секундах

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # путь к общей папке static, используемой реальным веб-сервером
STATICFILES_DIRS = []  # [BASE_DIR / 'static']  # список путей для нестандартных папок static

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # формат для Django 3+

# LOGIN_REDIRECT_URL = 'home'  # перенаправлять пользователя после успешной авторизации
LOGIN_URL = 'login'  # перенаправить неавторизованного пользователя при попытке посетить закрытую страницу сайта
# LOGOUT_REDIRECT_URL = 'home'  # перенаправляется пользователь после выхода

# DEFAULT_USER_IMAGE = MEDIA_URL + 'cabinet/default.png'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', )  # здесь указываем уже свою ПОЛНУЮ почту, с которой будут отправляться письма
SERVER_EMAIL = os.getenv('SERVER_EMAIL', )

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', )  # ваше имя пользователя
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', )  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl
