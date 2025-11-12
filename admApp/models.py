from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Usuario(AbstractUser):
    
    class TipoRol(models.TextChoices):
        ADMINISTRADOR = 'ADMIN', 'Administrador'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor de Obra'
        BODEGUERO = 'BODEGUERO', 'Bodeguero'
        OBRERO = 'OBRERO', 'Obrero'
    
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=TipoRol.choices, default=TipoRol.OBRERO, verbose_name="Rol")
    fecha_ingreso = models.DateField(default=timezone.now)
    activo = models.BooleanField(default=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )
    
    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"
    
    def es_administrador(self):
        return self.rol == self.TipoRol.ADMINISTRADOR
    
    def es_supervisor(self):
        return self.rol == self.TipoRol.SUPERVISOR
    
    def es_bodeguero(self):
        return self.rol == self.TipoRol.BODEGUERO



class Obra(models.Model):
    
    class EstadoObra(models.TextChoices):
        PLANIFICACION = 'PLANIFICACION', 'Planificación'
        EN_CURSO = 'EN_CURSO', 'En Curso'
        PAUSADA = 'PAUSADA', 'Pausada'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre de la Obra")
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    supervisor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': Usuario.TipoRol.SUPERVISOR}, related_name='obras_supervisadas')
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    fecha_fin_real = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoObra.choices, default=EstadoObra.PLANIFICACION)
    presupuesto_estimado = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'obra'
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"
    
    def dias_transcurridos(self):
        if self.fecha_inicio:
            return (timezone.now().date() - self.fecha_inicio).days
        return 0


class Obrero(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': Usuario.TipoRol.OBRERO})
    especialidad = models.CharField(max_length=100)
    obras_asignadas = models.ManyToManyField(Obra, through='ObraObrero', related_name='obreros')
    
    class Meta:
        db_table = 'obrero'
        verbose_name = 'Obrero'
        verbose_name_plural = 'Obreros'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.especialidad}"


class ObraObrero(models.Model):
    
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    obrero = models.ForeignKey(Obrero, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(default=timezone.now)
    fecha_fin_asignacion = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'obra_obrero'
        unique_together = [['obra', 'obrero']]
        verbose_name = 'Asignación Obra-Obrero'
        verbose_name_plural = 'Asignaciones Obra-Obrero'
    
    def __str__(self):
        return f"{self.obrero} en {self.obra}"


class Actividad(models.Model):
    
    class EstadoActividad(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROGRESO = 'EN_PROGRESO', 'En Progreso'
        COMPLETADA = 'COMPLETADA', 'Completada'
        CANCELADA = 'CANCELADA', 'Cancelada'
    
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='actividades')
    tipo_actividad = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    horas_estimadas = models.IntegerField(validators=[MinValueValidator(1)])
    horas_reales = models.IntegerField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoActividad.choices, default=EstadoActividad.PENDIENTE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'actividad'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['obra', 'fecha_inicio']
    
    def __str__(self):
        return f"{self.nombre} - {self.obra.nombre}"


class Material(models.Model):
    
    class UnidadMedida(models.TextChoices):
        UNIDAD = 'UND', 'Unidad'
        METRO = 'M', 'Metro'
        METRO_CUADRADO = 'M2', 'Metro Cuadrado'
        METRO_CUBICO = 'M3', 'Metro Cúbico'
        KILOGRAMO = 'KG', 'Kilogramo'
        LITRO = 'L', 'Litro'
        SACO = 'SACO', 'Saco'
    
    nombre = models.CharField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True)
    unidad_medida = models.CharField(max_length=10, choices=UnidadMedida.choices, default=UnidadMedida.UNIDAD)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock_minimo = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    proveedor = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'material'
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_unidad_medida_display()})"


class Herramienta(models.Model):
    
    class EstadoHerramienta(models.TextChoices):
        DISPONIBLE = 'DISPONIBLE', 'Disponible'
        EN_USO = 'EN_USO', 'En Uso'
        MANTENIMIENTO = 'MANTENIMIENTO', 'En Mantenimiento'
        DAÑADA = 'DAÑADA', 'Dañada'
        BAJA = 'BAJA', 'Dada de Baja'
    
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=EstadoHerramienta.choices, default=EstadoHerramienta.DISPONIBLE)
    fecha_adquisicion = models.DateField(blank=True, null=True)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'herramienta'
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'
        ordering = ['nombre', 'marca']
    
    def __str__(self):
        return f"{self.nombre} {self.marca} - {self.get_estado_display()}"


class Bodega(models.Model):
    
    class TipoBodega(models.TextChoices):
        CENTRAL = 'CENTRAL', 'Bodega Central'
        OBRA = 'OBRA', 'Bodega de Obra'
    
    nombre = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TipoBodega.choices, default=TipoBodega.OBRA)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, blank=True, null=True, related_name='bodegas', help_text="Solo para bodegas de obra")
    encargado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol': Usuario.TipoRol.BODEGUERO}, related_name='bodegas_a_cargo')
    capacidad_m3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Capacidad (m³)")
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'bodega'
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['tipo', 'nombre']
    
    def __str__(self):
        if self.obra:
            return f"{self.nombre} - {self.obra.nombre}"
        return f"{self.nombre} ({self.get_tipo_display()})"


class InventarioMaterial(models.Model):
    
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='inventario_materiales')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad_actual = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'inventario_material'
        unique_together = [['bodega', 'material']]
        verbose_name = 'Inventario de Material'
        verbose_name_plural = 'Inventarios de Materiales'
    
    def __str__(self):
        return f"{self.material.nombre} en {self.bodega.nombre}: {self.cantidad_actual}"
    
    def esta_bajo_minimo(self):
        return self.cantidad_actual < self.material.stock_minimo


class InventarioHerramienta(models.Model):
    
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='inventario_herramientas')
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'inventario_herramienta'
        unique_together = [['bodega', 'herramienta']]
        verbose_name = 'Inventario de Herramienta'
        verbose_name_plural = 'Inventarios de Herramientas'
    
    def __str__(self):
        return f"{self.herramienta} en {self.bodega.nombre}"


class MovimientoInventario(models.Model):
    
    class TipoMovimiento(models.TextChoices):
        ENTRADA = 'ENTRADA', 'Entrada'
        SALIDA = 'SALIDA', 'Salida'
        TRANSFERENCIA = 'TRANSFERENCIA', 'Transferencia'
        AJUSTE = 'AJUSTE', 'Ajuste de Inventario'
        DEVOLUCION = 'DEVOLUCION', 'Devolución'
    
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_salida', blank=True, null=True)
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_entrada', blank=True, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TipoMovimiento.choices)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    usuario_responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, blank=True, null=True, help_text="Obra a la que se destina el material")
    motivo = models.TextField(blank=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'movimiento_inventario'
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha_movimiento']
    
    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} - {self.material.nombre} ({self.cantidad})"


class Prestamo(models.Model):
    
    class EstadoPrestamo(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        DEVUELTO = 'DEVUELTO', 'Devuelto'
        EXTRAVIADO = 'EXTRAVIADO', 'Extraviado'
        DAÑADO = 'DAÑADO', 'Dañado'
    
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    obrero = models.ForeignKey(Obrero, on_delete=models.CASCADE, related_name='prestamos')
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_estimada = models.DateField()
    fecha_devolucion_real = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=EstadoPrestamo.choices, default=EstadoPrestamo.ACTIVO)
    observaciones_prestamo = models.TextField(blank=True)
    observaciones_devolucion = models.TextField(blank=True)
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'prestamo'
        verbose_name = 'Préstamo'
        verbose_name_plural = 'Préstamos'
        ordering = ['-fecha_prestamo']
    
    def __str__(self):
        return f"{self.herramienta} → {self.obrero} ({self.get_estado_display()})"
    
    def esta_atrasado(self):
        if self.estado == self.EstadoPrestamo.ACTIVO:
            return timezone.now().date() > self.fecha_devolucion_estimada
        return False
