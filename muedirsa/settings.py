"""
Django settings for muedirsa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=02c-1&!6idy$l44pz5_txkh#&=0g)w8jd2#451#*l5u6@ntc4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['localhost']

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'muedirsa.apps.configuraciones',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'inventario',
    'clientes',
    'proveedores',
    'config',
    'OrdenesdeCompra',
    'devolucionCliente',
    'devolucionProveedor',
    'empleados',
    'proforma',
    'pedido',
    'django_tables2',
    'django_filters',
    'bootstrap3',
    'django.contrib.humanize',
    'reunion',
    'vendedor',
    'ordenproduccion',
    'ambiente',
    'facturacion',
    'ordenServicio',
    'ordenEgreso',
    'subordenproduccion',
    'ordenIngreso',
    'reporte',
    'contabilidad',
    'transacciones',
    'retenciones',
    'liquidacion_comisiones',
    'recursos_humanos',
    'bancos',
    'mantenimiento',
    'ats',
    'ajustes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'muedirsa.configuracion_general.datos_globales',
)

ROOT_URLCONF = 'muedirsa.urls'

WSGI_APPLICATION = 'muedirsa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'CESA',
        'NAME': 'cesadesign',
        'USER': 'postgres',
        'PASSWORD': 'akedan2024',
        #'PASSWORD': '',
        #'HOST': 'localhost',
        'HOST': '127.0.0.1',
        'PORT': '',
    },
    
    
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-Es'

TIME_ZONE = 'America/Guayaquil'

USE_I18N = False

USE_L10N = False

USE_TZ = True

GRAPPELLI_ADMIN_TITLE = 'Administracion'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

LOGIN_URL = '/login/iniciar/'
DEFAULT_CHARSET = 'utf-8'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)