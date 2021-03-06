"""
Django settings for UFood project.

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
SECRET_KEY = 'w0$y1*d&h1p4cx6v*rm%#lyp%92stnk2u!w0mg1e#*_144_$@#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'paypalrestsdk',
    'south',
    'restaurante',
    'webapp',
    'pedidos',
    'clientes',
    'carton',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'UFood.urls'

WSGI_APPLICATION = 'UFood.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	os.path.join(BASE_DIR,'static'),
)


LOGIN_URL = '/ingresar/'
REDIRECT_FIELD_NAME = '/tralari/'


# Sesion para carton
CART_SESSION_KEY = 'carrito_plato'
CART_TEMPLATE_TAG_NAME = 'get_cart'
CART_PRODUCT_MODEL = 'restaurante.models.Plato'


# Paypal options cris_gi_06@hotmail.com
PAYPAL_MODE = 'sandbox' # sandbox or live
PAYPAL_CLIENT_ID = 'AZyHuBCADbHGZ_ZKkB7gQvnaQx3L_O0IP7g5UC6UZskirh01huaj-DazzvHo'
PAYPAL_CLIENT_SECRET = 'EJslvBD7zxMBLZHwWwCtsJeEq3MzJGfQyiixS1EFbkXyxjpD0_8e79ikjXEv'