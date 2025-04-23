"""
Django settings for cupquality project.
"""

from pathlib import Path
import os
import sys
import environ

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment
root = environ.Path(start=__file__) - 2
env = environ.Env()
env.read_env(env_file=os.path.join(BASE_DIR, '.env'))




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0-kxmv*tk2at8sb4u_7!y#t+d4i^oy+6c$k*nl(o@_2g5y5yle'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autenticacion.apps.AutenticacionConfig',
    'registros.apps.RegistrosConfig',
    'analisis.apps.AnalisisConfig',
    'dataUtils.apps.DatautilsConfig',
    'ajaxdata.apps.AjaxdataConfig',
    'multiselectfield',
    'laboratorios.apps.LaboratoriosConfig',
    'jsignature',
    'home.apps.HomeConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'cupquality.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'static'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'get_tamizado': 'analisis.templatetags.get_tamizado',
                'get_defectos': 'analisis.templatetags.get_defectos',
                'get_sabores_aromas': 'analisis.templatetags.get_sabores_aromas',
                'utilidades': 'cupquality.templatetags.utilidades',
                'get_tamizadoLab': 'laboratorios.templatetags.get_tamizadoLab',
                'get_defectosLab': 'laboratorios.templatetags.get_defectosLab',
                'get_sabores_aromasLab': 'laboratorios.templatetags.get_sabores_aromasLab',
            }
        },
    },
]

WSGI_APPLICATION = 'cupquality.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cupquality_db',
        'USER': 'mvalladares',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-EN'
TIME_ZONE = 'America/Tegucigalpa'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Login
LOGIN_REDIRECT_URL = '/auth/login'

# Static files
STATICFILES_DIRS = (root('static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'assets-root', 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'

# Default PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 60

try:
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env.int('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
except Exception as e:
    print("⚠️ No se cargaron las variables de correo:", e)


# Admins
ADMINS = [
    'mcvm2101@gmail.com',

]

# Otros ajustes
JSIGNATURE_JQUERY = 'admin'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
