import os


#####~~~~~ RELATED CONSTRAINTS ~~~~~#####
# 6. Uploaded (attached/embedded) content of a Post must not exceed a certain size limit (limit is TBD).

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')a1yx87-7lwrn!o9sj^g$bse2)*5k956j=-5_6w3@g-iyn6f63'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.sites',
    # imported apps
    'django.contrib.humanize',
    'crispy_forms',
    'mptt',
    'trix',
    'django_summernote',
    # my apps
    'users.apps.UsersConfig',
    'common.apps.CommonConfig',
    'community.apps.CommunityConfig',
    'posts.apps.PostsConfig',
    # apps for debugging
    'django_extensions',
]

MIDDLEWARE = [
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
      'ENGINE': 'django.db.backends.mysql',
      'NAME': os.environ.get('WROOVIE_DB_NAME'),
      'USER': os.environ.get('WROOVIE_DB_USER'),
      'PASSWORD': os.environ.get('WROOVIE_DB_PASS'),
      'HOST': 'localhost',
      'PORT': '3306',
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('WROOVIE_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('WROOVIE_EMAIL_PASS')

# summernote settings
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'

SUMMERNOTE_CONFIG = {
    #####~~~~~ CONSTRAINT (6) ~~~~~#####
    # file-size limit on uploaded images for an article
    'attachment_filesize_limit': 1024 * 1024 * 3,       # specify the file size

    'width': '100%', 
    'height': '450px',

    # You can add custom css/js for SummernoteWidget.
    'css': ('/static/posts/css/summernote.css',),
}







# summernote config
    # useful to skip CDN, use local server copies
    # 'inplacewidget_external_css': (
    #     '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
    #     '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    # ),
    # 'inplacewidget_external_js': (
    #     '//code.jquery.com/jquery-1.9.1.min.js',
    #     '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    # ),
