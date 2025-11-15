"""
==============================================================================
CONFIGURACIÓN DEL PROYECTO DJANGO - ICONSTRUCTION
==============================================================================
Proyecto: prjIContruction
Descripción: Sistema de gestión de construcción con control de inventarios,
             herramientas, materiales, obras, usuarios y préstamos.
Versión Django: 4.2.23
==============================================================================
"""

from pathlib import Path
import os
from decouple import config, Csv
from django.core.management.utils import get_random_secret_key


# ==============================================================================
# CONFIGURACIÓN DE RUTAS DEL PROYECTO
# ==============================================================================
# Define la ruta base del proyecto para referenciar directorios y archivos
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ==============================================================================
# SECRET_KEY: Clave secreta para cifrado (¡NUNCA compartir en producción!)
SECRET_KEY = config('SECRET_KEY', default=get_random_secret_key())

# DEBUG: Modo de desarrollo (activar solo en desarrollo, NUNCA en producción)
DEBUG = True

# ALLOWED_HOSTS: Lista de hosts/dominios permitidos para acceder a la aplicación
# En producción debe contener el dominio real (ej: ['midominio.com', 'www.midominio.com'])
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# ==============================================================================
# APLICACIONES INSTALADAS
# ==============================================================================
# Aplicaciones de Django y de terceros utilizadas en el proyecto
INSTALLED_APPS = [
    # Apps nativas de Django
    'django.contrib.admin',           # Panel de administración
    'django.contrib.auth',            # Sistema de autenticación
    'django.contrib.contenttypes',    # Framework de tipos de contenido
    'django.contrib.sessions',        # Manejo de sesiones
    'django.contrib.messages',        # Framework de mensajes
    'django.contrib.staticfiles',     # Manejo de archivos estáticos
    
    # Apps del proyecto
    'admApp',        # App principal de administración
    'sesionApp',     # App de gestión de sesiones y login
    
    # Apps de terceros
    'rest_framework',  # Framework para crear APIs REST
]


# ==============================================================================
# MIDDLEWARE (Capas de procesamiento de peticiones)
# ==============================================================================
# Define el orden de ejecución de middleware para procesar requests y responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Seguridad HTTP
    'django.contrib.sessions.middleware.SessionMiddleware',   # Manejo de sesiones
    'django.middleware.common.CommonMiddleware',              # Procesamiento común
    'django.middleware.csrf.CsrfViewMiddleware',              # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticación
    'django.contrib.messages.middleware.MessageMiddleware',   # Mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protección clickjacking
]


# ==============================================================================
# CONFIGURACIÓN DE URLS
# ==============================================================================
# Define el archivo principal de URLs del proyecto
ROOT_URLCONF = 'prjIContruction.urls'


# ==============================================================================
# CONFIGURACIÓN DE TEMPLATES (Plantillas HTML)
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Directorio global de templates
        'APP_DIRS': True,  # Buscar templates dentro de cada app
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


# ==============================================================================
# CONFIGURACIÓN WSGI
# ==============================================================================
# Punto de entrada para servidores WSGI en producción
WSGI_APPLICATION = 'prjIContruction.wsgi.application'


# ==============================================================================
# CONFIGURACIÓN DE BASE DE DATOS
# ==============================================================================
# Conexión a MySQL para almacenar datos del sistema
DATABASES = {
    'default': {
        'ENGINE': config('ENGINE'),  # Motor de base de datos
        'NAME': config('DB_NAME'),               # Nombre de la base de datos
        'USER': config('DB_USER'),                        # Usuario de MySQL
        'PASSWORD': config('DB_PASSWORD'),                   # Contraseña (cambiar en producción)
    }
}


# ==============================================================================
# VALIDADORES DE CONTRASEÑAS
# ==============================================================================
# Reglas de validación para contraseñas de usuarios (seguridad)
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


# ==============================================================================
# CONFIGURACIÓN REGIONAL E INTERNACIONALIZACIÓN
# ==============================================================================
# Idioma: Español de Chile
LANGUAGE_CODE = 'es-cl'

# Zona horaria: Santiago de Chile
TIME_ZONE = 'America/Santiago'

# Habilitar internacionalización (traducciones)
USE_I18N = True

# Usar zona horaria en fechas y horas
USE_TZ = True


# ==============================================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ==============================================================================
# URL pública para acceder a archivos estáticos
STATIC_URL = 'static/'

# (Opcional) Directorio donde se recopilan todos los archivos estáticos en producción
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ==============================================================================
# CONFIGURACIÓN DE ARCHIVOS MEDIA (Uploads de usuarios)
# ==============================================================================
# URL pública para acceder a archivos subidos por usuarios
MEDIA_URL = '/media/'

# Directorio donde se almacenan archivos subidos
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ==============================================================================
# CONFIGURACIÓN DE SESIONES Y AUTENTICACIÓN
# ==============================================================================
# Motor de almacenamiento de sesiones (base de datos)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# URL de redirección cuando el usuario no está autenticado
LOGIN_URL = '/login/'

# URL de redirección después de cerrar sesión
LOGOUT_REDIRECT_URL = '/login/'

# Modelo de usuario personalizado del proyecto
AUTH_USER_MODEL = 'admApp.Usuario'


# ==============================================================================
# CONFIGURACIÓN ADICIONAL DE MODELOS
# ==============================================================================
# Tipo de clave primaria por defecto para modelos nuevos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
