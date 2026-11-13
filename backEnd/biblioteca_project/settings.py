
"""
Django settings for biblioteca_project project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# =====================================================
# CONFIGURACION PRINCIPAL
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables del archivo .env
load_dotenv(BASE_DIR / ".env")


# =====================================================
# SEGURIDAD
# =====================================================

SECRET_KEY = 'django-insecure-cambia-esta-clave-en-produccion'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]


# =====================================================
# APLICACIONES INSTALADAS
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django REST Framework
    'rest_framework',
    'rest_framework.authtoken',

    # CORS
    'corsheaders',

    # Aplicacion principal
    'biblioteca',
]


# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =====================================================
# CONFIGURACION DE URLS
# =====================================================

ROOT_URLCONF = 'biblioteca_project.urls'


# =====================================================
# PLANTILLAS
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'biblioteca_project.wsgi.application'


# =====================================================
# BASES DE DATOS
# SQLITE + ORACLE FREESQL
# =====================================================

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '1521')
DB_SERVICE = os.getenv('DB_SERVICE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Comprobar credenciales de Oracle
if not all([DB_HOST, DB_SERVICE, DB_USER, DB_PASSWORD]):
    raise ValueError(
        "Faltan credenciales de Oracle en el archivo .env"
    )

DATABASES = {

    # Base de datos local para Django
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },

    # Base de datos Oracle FreeSQL
    'negocio': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': f'{DB_HOST}:{DB_PORT}/{DB_SERVICE}',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '',
        'PORT': '',
    },
}


# =====================================================
# ROUTER DE BASES DE DATOS
# =====================================================

DATABASE_ROUTERS = [
    'biblioteca_project.routers.NegocioRouter'
]


# =====================================================
# VALIDACION DE CONTRASEÑAS
# =====================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =====================================================
# IDIOMA Y ZONA HORARIA
# =====================================================

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# =====================================================
# ARCHIVOS ESTATICOS
# =====================================================

STATIC_URL = 'static/'


# =====================================================
# CLAVE PRIMARIA
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================================================
# DJANGO REST FRAMEWORK
# =====================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'biblioteca_project.autenticacion.CookieTokenAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# =====================================================
# CORS - CONEXION CON REACT
# =====================================================

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:4200',
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Configuración de cookie HttpOnly
AUTH_COOKIE = {
    "NAME": "auth_token",
    "MAX_AGE": 60 * 60 * 8,
    "PATH": "/api/",
    "SAMESITE": "Lax",
    "SECURE": not DEBUG,
}