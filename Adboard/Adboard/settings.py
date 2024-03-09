from pathlib import Path
import os
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', )

DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['158.160.46.141', '127.0.0.1']

AUTH_USER_MODEL = "cabinet.User"

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',  # Для простых страничек
    'django.contrib.flatpages',  # Для простых страничек

    'corsheaders',
    'django_filters',
    'rest_framework',
    'drf_spectacular',

    'announcement.apps.AnnouncementConfig',
    'cabinet.apps.CabinetConfig',
    'coment.apps.ComentConfig',

    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
]

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 12,

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DATETIME_FORMAT': "%d.%m.%Y %H:%M:%S",  # формат вывода времени в ответах
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Adboard',
    'DESCRIPTION': 'Description adboard',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ORIGIN_ALLOW_ALL = True  # added to solve CORS
CORS_ALLOW_HEADERS = ('content-disposition', 'accept-encoding',
                      'content-type', 'accept', 'origin', 'Authorization',
                      'access-control-allow-methods', 'access-control-allow-origin',
                      'access-control-allow-credentials', 'attribution-reporting',
                      )

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
    'allauth.account.middleware.AccountMiddleware',
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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 Mb limit

# две переменные, чтобы не путаться; SERG - потому что мои переменные, а не django, чтобы не забыть.
SERG_USER_CONFIRMATION_KEY = "user_confirmation_{token}"  # шаблон для ключа
SERG_USER_CONFIRMATION_TIMEOUT = 60  # время в секундах

# Celery
# команда при запуске с windows: celery -A Adboard worker -l INFO -P solo
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 5 * 60}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_CONNECTION_RETRY = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # путь к общей папке static, используемой реальным веб-сервером
STATICFILES_DIRS = []  # [BASE_DIR / 'static']  # список путей для нестандартных папок static

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # формат для Django 3+

LOGIN_REDIRECT_URL = 'board_list'  # перенаправлять пользователя после успешной авторизации
LOGIN_URL = 'login'  # перенаправить неавторизованного пользователя при попытке посетить закрытую страницу сайта
LOGOUT_REDIRECT_URL = 'board_list'  # перенаправляется пользователь после выхода

# DEFAULT_USER_IMAGE = MEDIA_URL + 'cabinet/default.png'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', )
SERVER_EMAIL = os.getenv('SERVER_EMAIL', )
EMAIL_ADMIN = os.getenv('EMAIL_ADMIN', )

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True  # Яндекс использует ssl
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', )
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', )

# dj-rest-auth
REST_AUTH = {
   "REGISTER_SERIALIZER": "cabinet.serializer.UserRegisterSerializer",
   'LOGIN_SERIALIZER': 'dj_rest_auth.serializers.LoginSerializer',
   'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
   'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',

   'TOKEN_MODEL': 'rest_framework.authtoken.models.Token',
   'TOKEN_CREATOR': 'dj_rest_auth.utils.default_create_token',

   'SESSION_LOGIN': True,
}

# Логирование
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'general_log_info': {
#             'format': '{asctime} - {levelname} - {module} - {message}',
#             'style': '{',
#         },
#         'error_log': {
#             'format': '{asctime} - {levelname} - {pathname} - {exc_info} - {message}',
#             'style': '{',
#         },
#         'security_log': {
#             'format': '{asctime} - {levelname} - {module} - {message}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',  # фильтр, который пропускает записи только в случае, когда DEBUG = True
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',  # фильтр, который пропускает записи только в случае, когда DEBUG = False
#         },
#     },
#     # Обработчики
#     'handlers': {
#         'file_general.log': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'general.log',
#             'formatter': 'general_log_info',
#         },
#         'file_errors.log': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'errors.log',
#             'formatter': 'error_log',
#         },
#         'file_security.log': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'security.log',
#             'formatter': 'security_log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file_general.log'],
#             # 'level': 'INFO',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file_errors.log'],
#             'level': "ERROR",
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['file_errors.log'],
#             'propagate': True,
#         },
#         'django.template': {
#             'handlers': ['file_errors.log'],
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['file_errors.log'],
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['file_security.log'],
#             'propagate': False,
#         },
#     },
# }
