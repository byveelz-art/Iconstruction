from django.contrib import admin
from .models import (
    Usuario, Obra, Obrero, ObraObrero, Actividad,
    Material, Herramienta, Bodega, InventarioMaterial,
    InventarioHerramienta, MovimientoInventario, Prestamo
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'rol', 'rut', 'activo']
    list_filter = ['rol', 'activo']
    search_fields = ['username', 'first_name', 'last_name', 'rut']

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'region', 'estado', 'fecha_inicio', 'supervisor']
    list_filter = ['estado', 'region', 'ciudad']
    search_fields = ['nombre', 'ciudad']
    date_hierarchy = 'fecha_inicio'

@admin.register(Obrero)
class ObreroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidad']

@admin.register(ObraObrero)
class ObraObreroAdmin(admin.ModelAdmin):
    list_display = ['obra', 'obrero', 'fecha_asignacion', 'activo']
    list_filter = ['activo', 'fecha_asignacion']

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'obra', 'tipo_actividad', 'estado', 'fecha_inicio']
    list_filter = ['estado', 'tipo_actividad']
    search_fields = ['nombre', 'obra__nombre']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'unidad_medida', 'precio_unitario', 'stock_minimo', 'activo']
    list_filter = ['unidad_medida', 'activo']
    search_fields = ['nombre', 'proveedor']

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'marca', 'modelo', 'tipo', 'estado', 'activo']
    list_filter = ['estado', 'tipo', 'activo']
    search_fields = ['nombre', 'marca', 'numero_serie']

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'ciudad', 'region', 'obra', 'encargado', 'activa']
    list_filter = ['tipo', 'region', 'activa']
    search_fields = ['nombre', 'ciudad']

@admin.register(InventarioMaterial)
class InventarioMaterialAdmin(admin.ModelAdmin):
    list_display = ['bodega', 'material', 'cantidad_actual', 'fecha_ultima_actualizacion']
    search_fields = ['bodega__nombre', 'material__nombre']

@admin.register(InventarioHerramienta)
class InventarioHerramientaAdmin(admin.ModelAdmin):
    list_display = ['bodega', 'herramienta', 'fecha_ingreso']
    search_fields = ['bodega__nombre', 'herramienta__nombre']

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['material', 'tipo_movimiento', 'cantidad', 'bodega_origen', 'bodega_destino', 'fecha_movimiento']
    list_filter = ['tipo_movimiento', 'fecha_movimiento']
    search_fields = ['material__nombre']
    date_hierarchy = 'fecha_movimiento'

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['herramienta', 'obrero', 'obra', 'fecha_prestamo', 'fecha_devolucion_estimada', 'estado']
    list_filter = ['estado', 'fecha_prestamo']
    search_fields = ['herramienta__nombre', 'obrero__usuario__first_name']
    date_hierarchy = 'fecha_prestamo'
