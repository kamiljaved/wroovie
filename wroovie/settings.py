import os
from common.utils import createSecretsFile

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# import secrets
try:
    from common.secrets import (
        WRV_SCRT_SECRET_KEY, WRV_SCRT_DB_NAME, WRV_SCRT_DB_USER, WRV_SCRT_DB_PASS,
        WRV_SCRT_DB_HOST, WRV_SCRT_DB_PORT, 
        WRV_SCRT_EMAIL_USER, WRV_SCRT_EMAIL_PASS)
except (ModuleNotFoundError, ImportError, SyntaxError):
    # bad, incomplete or non-existent secrets file
    createSecretsFile(BASE_DIR)
    # notify to update example secrets file with correct information 
    import sys
    sys.exit("Error! Bad, incomplete or non-existent secrets file.\n\
        An example secrets file has been added as 'common/secrets.py'.\n\
        Please update it with the correct information, and re-run this app.\n")


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = WRV_SCRT_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['192.168.10.52', '127.0.0.1', 'localhost', ]
SESSION_COOKIE_NAME = 'wroovie'
#SESSION_COOKIE_DOMAIN = '192.168.10.52'
#PARENT_SITE_URL = 'http://192.168.10.52:8000'
#MOBILE_SITE_URL = 'http://192.168.10.52:8001'


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # imported apps
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.humanize',
    'crispy_forms',
    'mptt',
    'trix',
    'django_summernote',
    # 'django_user_agents',
    # apps for debugging
    'django_extensions',
    # my apps
    'users.apps.UsersConfig',
    'common.apps.CommonConfig',
    'community.apps.CommunityConfig',
    'posts.apps.PostsConfig',
]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'main_site_cache',
#     }
# }

# Name of cache backend to cache user agents. If it not specified default cache alias will be used. Set to `None` to disable caching.
# USER_AGENTS_CACHE = 'default'

MIDDLEWARE = [
    # imported middleware
    # 'django_user_agents.middleware.UserAgentMiddleware',
    # my middleware
    # 'wroovie.middleware.SiteFlavorMiddleware',
    # django middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wroovie.urls'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [            
            os.path.join('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "common.context_processors.current_site.current_site",
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wroovie.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
  'default': {
      'ENGINE':     'django.db.backends.mysql',
      'NAME':       WRV_SCRT_DB_NAME,
      'USER':       WRV_SCRT_DB_USER,
      'PASSWORD':   WRV_SCRT_DB_PASS,
      'HOST':       WRV_SCRT_DB_HOST,
      'PORT':       WRV_SCRT_DB_PORT
    }
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = ( os.path.join('static'), )

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'wroovie-media'))
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'uni_form'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND =         'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST =            'smtp.gmail.com'
EMAIL_PORT =            587
EMAIL_USE_TLS =         True
EMAIL_HOST_USER =       WRV_SCRT_EMAIL_USER
EMAIL_HOST_PASSWORD =   WRV_SCRT_EMAIL_PASS


##################### SUMMERNOTE SETTINGS ########################

X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'attachment_absolute_uri': True,
    # file-size limit on uploaded images for an article
    'attachment_filesize_limit': 1024 * 1024 * 3,       # specify the file size (bytes)
    # rich text editor size  
    'width': '100%', 
    'height': '450px',
    # add custom css/js for SummernoteWidget
    'css': ('/static/posts/css/summernote.css',),
    # additional options
    # useful to skip CDN, use local server copies
    # 'inplacewidget_external_css': (
    #     '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
    #     '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    # ),
    # 'inplacewidget_external_js': (
    #     '//code.jquery.com/jquery-1.9.1.min.js',
    #     '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    # ),
}

