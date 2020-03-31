import os

from django.contrib.messages import constants as messages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'REPLACE-ME'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: use your actual domain name in production!
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userena',
    'guardian',
    'easy_thumbnails',
    #'taggit',
    'bookstore',
    'compressor',
    'django_images',
    'pinry.core',
    'pinry.users',
    #'vote',
    #'like',
    #'django_mobile',
    #'tbk_picker',
    # 'django_user_agents',
    # 'is_weixin',
    
     'django.contrib.sites',
     #'allauth',
     #'allauth.account',
     #'allauth.socialaccount',
     
     'accounts',
     
     'rest_framework',
    #  'bookstore',
]





ROOT_URLCONF = 'pinry.urls'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pinry.users.middleware.Public',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    # 'django_user_agents.middleware.UserAgentMiddleware',

]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pinry/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pinry.core.context_processors.template_settings',
                'django_mobile.context_processors.flavour',
                # "is_weixin.context_processors.is_weixin",
                # Already defined Django-related contexts here

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],

        },
    },
]

TEMPLATE_LOADERS = (
    ('django_mobile.loader.Loader',
     'django.template.loaders.app_directories.Loader',
     ),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'pinry/static'),os.path.join(BASE_DIR, 'pinry/static/jui'),]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

WSGI_APPLICATION = 'pinry.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/static/media/'

# Set to False to disable people from creating new accounts.
ALLOW_NEW_REGISTRATIONS = True

# Set to False to force users to login before seeing any pins.
PUBLIC = True

AUTHENTICATION_BACKENDS = [
    # 'pinry.users.auth.backends.CombinedAuthBackend',
    # 'django.contrib.auth.backends.ModelBackend',
    #     # Needed to login by username in Django admin, regardless of `allauth`

    # # `allauth` specific authentication methods, such as login by e-mail
    # 'allauth.account.auth_backends.AuthenticationBackend',
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/accounts/signin'

LOGIN_REDIRECT_URL = '/'

MESSAGE_TAGS = {
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}

API_LIMIT_PER_PAGE = 50

IMAGE_PATH = 'pinry.core.utils.upload_path'

IMAGE_SIZES = {
    'thumbnail': {'size': [240, 0]},
    'standard': {'size': [600, 0]},
    'square': {'crop': True, 'size': [125, 125]},
}

# django-user-agent
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
USER_AGENTS_CACHE = 'default'
# end of django-user-agent

#userena
SITE_ID=1

ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.MyProfile'

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'applogfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'APPNAME.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        },    
    },


    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,

        },
        'APPNAME': {
            'handlers': ['applogfile',],
            'level': 'INFO',
        },

    }
}

USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True
# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 10
# }