from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),

    # Herramientas
    path('herramientas/', views.herramientas_list, name='herramientas_list'),
    path('herramientas/nueva/', views.herramienta_create, name='herramienta_create'),
    path('herramientas/editar/<int:pk>/', views.herramienta_update, name='herramienta_update'),
    path('herramientas/eliminar/<int:pk>/', views.herramienta_delete, name='herramienta_delete'),

    # Materiales
    path('materiales/', views.materiales_list, name='materiales_list'),
    path('materiales/nuevo/', views.material_create, name='material_create'),
    path('materiales/editar/<int:pk>/', views.material_update, name='material_update'),
    path('materiales/eliminar/<int:pk>/', views.material_delete, name='material_delete'),

    # Obras y Actividades
    path('obras/', views.obras_list, name='obras_list'),
    path('obras/nueva/', views.obra_create, name='obra_create'),
    path('obras/editar/<int:pk>/', views.obra_update, name='obra_update'),
    path('obras/eliminar/<int:pk>/', views.obra_delete, name='obra_delete'),

    path('obras/<int:id_obra>/actividades/', views.actividades_list, name='actividades_list'),
    path('obras/<int:id_obra>/actividades/nueva/', views.actividad_create, name='actividad_create'),

    # Usuarios
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_create'),
    path('usuarios/editar/<int:pk>/', views.usuario_update, name='usuario_update'),
    path('usuarios/eliminar/<int:pk>/', views.usuario_delete, name='usuario_delete'),

    # Obreros
    path('obreros/', views.obreros_list, name='obreros_list'),
    path('obreros/nuevo/', views.obrero_create, name='obrero_create'),
    path('obreros/editar/<int:pk>/', views.obrero_update, name='obrero_update'),
    path('obreros/eliminar/<int:pk>/', views.obrero_delete, name='obrero_delete'),

    # Bodegas
    path('bodegas/', views.bodegas_list, name='bodegas_list'),
    path('bodegas/nueva/', views.bodega_create, name='bodega_create'),
    path('bodegas/<int:pk>/', views.bodega_detail, name='bodega_detail'),

    # Inventario
    path('inventario/', views.inventario_list, name='inventario_list'),

    # Préstamos
    path('prestamos/', views.prestamos_list, name='prestamos_list'),
    path('prestamos/nuevo/', views.prestamo_create, name='prestamo_create'),
    path('prestamos/<int:pk>/devolver/', views.prestamo_devolver, name='prestamo_devolver'),


]
