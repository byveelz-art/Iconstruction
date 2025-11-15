# Descripción

IConstruction es un sistema web desarrollado en Django que permite la gestión integral de proyectos de construcción. Ofrece control de inventarios, registro de préstamos de herramientas, administración de personal y seguimiento de obras, todo desde una plataforma centralizada y segura.

Tecnologías Utilizadas

Python 3.10+

Django 4.2

MySQL 8.0

Bootstrap 5

# Requisitos Previos

# Instalar las dependencias necesarias:

pip install django mysqlclient python-decouple djangorestframework

# Proceso de Instalación

# Clonar el repositorio

git clone https://github.com/tu-usuario/iconstruction.git
cd iconstruction


# Crear la base de datos en MySQL

CREATE DATABASE iconstruction;


# Configurar variables de entorno (.env)

SECRET_KEY=tu-clave-secreta
ALLOWED_HOSTS=localhost,127.0.0.1


# Aplicar migraciones

python manage.py migrate


# Crear un superusuario

python manage.py createsuperuser


# Ejecutar el servidor

python manage.py runserver

# Usuarios de Prueba
Usuario	   | Contraseña	 |   Rol
admin	     | admin123	   |   Administrador
supervisor1| super123	   |   Supervisor
bodeguero1 | bodega123	 |   Bodeguero


# estructura del Proyecto

iconstruction/
├── admApp/         # Aplicación principal
├── sesionApp/      # Módulo de autenticación
├── templates/      # Plantillas HTML
├── static/         # Archivos estáticos (CSS, JS, imágenes)
└── sql_scripts/    # Scripts SQL auxiliares


# Seguridad Implementada

Autenticación obligatoria (@login_required)
Control de acceso por roles (decoradores personalizados)
Protección contra ataques CSRF
Validación de permisos por vista
Encriptación de contraseñas con el sistema interno de Django

# Funcionalidades Principales
CRUD de Obras, Materiales, Herramientas y Usuarios
Gestión de inventario por bodega
Sistema de préstamos y devoluciones de herramientas

Panel de control con métricas

Control de acceso basado en roles de usuario
