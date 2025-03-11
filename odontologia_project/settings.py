"""
Django settings for odontologia_project project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

ALLOWED_HOSTS = [*]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CSRF_TRUSTED_ORIGINS = [
    'https://odontologia-tarea.onrender.com',
    'http://localhost',
]



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+q3yd)ft+@^3l473b+0n!t%%m7fuqh&bn=s%9o%j-ual_pm#j0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'odontologia_app',
    'fontawesomefree'

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

ROOT_URLCONF = 'odontologia_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'odontologia_app/Templates')],  # Ruta a la carpeta global de templates
        'APP_DIRS': True,  # Busca templates en las carpetas de las apps
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
WSGI_APPLICATION = 'odontologia_project.wsgi.application'

AUTH_USER_MODEL = "odontologia_app.Usuario"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
LOGIN_REDIRECT_URL = '/principal'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": os.getenv("DB_NAME", "doctora"),
        "USER": os.getenv("DB_USER", "josmar"),
        "PASSWORD": os.getenv("DB_PASSWORD", "6NAOqaQkrkksENSefywtrvtbA5VzWOFr"),
        "HOST": os.getenv("DB_HOST", "dpg-cv6gv3l6l47c73d88br0-a"),
        "PORT": os.getenv("DB_PORT", "5432"),
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

TIME_ZONE = 'America/Caracas'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# settings.py

# Configuración para archivos estáticos
STATIC_URL = '/static/'

# Directorio donde se almacenan los archivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'odontologia_app/static'),  # Ruta a la carpeta static de tu app
]
# Directorio donde se recolectan los archivos estáticos en producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
