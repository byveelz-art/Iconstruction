from django.db import models


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_obra = models.ForeignKey('Obra', models.DO_NOTHING, db_column='id_obra', blank=True, null=True)
    tipo_actividad = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    horas_estimadas = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividad'
    
    def __str__(self):
        return self.nombre or f"Actividad {self.id_actividad}"


class Herramienta(models.Model):
    id_herramienta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    bateria = models.CharField(max_length=50, blank=True, null=True)
    alimentacion = models.CharField(max_length=50, blank=True, null=True)
    dimension = models.CharField(max_length=50, blank=True, null=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    volts = models.IntegerField(blank=True, null=True)
    amperes = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'herramienta'


class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='id_solicitud', blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario'


class InventarioHerramienta(models.Model):
    id_inventario = models.OneToOneField(Inventario, models.DO_NOTHING, db_column='id_inventario', primary_key=True)  # The composite primary key (id_inventario, id_herramienta) found, that is not supported. The first column is selected.
    id_herramienta = models.ForeignKey(Herramienta, models.DO_NOTHING, db_column='id_herramienta')
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_herramienta'
        unique_together = (('id_inventario', 'id_herramienta'),)


class InventarioMaterial(models.Model):
    id_inventario = models.OneToOneField(Inventario, models.DO_NOTHING, db_column='id_inventario', primary_key=True)  # The composite primary key (id_inventario, id_material) found, that is not supported. The first column is selected.
    id_material = models.ForeignKey('Material', models.DO_NOTHING, db_column='id_material')
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventario_material'
        unique_together = (('id_inventario', 'id_material'),)


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    dimension = models.CharField(max_length=100, blank=True, null=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ancho = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    largo = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    alto = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material'


class Obra(models.Model):
    id_obra = models.AutoField(primary_key=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obra'

    def __str__(self):
        return self.direccion or f"Obra {self.id_obra}"

class ObraObrero(models.Model):
    id_obra = models.OneToOneField(Obra, models.DO_NOTHING, db_column='id_obra', primary_key=True)  # The composite primary key (id_obra, id_obrero) found, that is not supported. The first column is selected.
    id_obrero = models.ForeignKey('Obrero', models.DO_NOTHING, db_column='id_obrero')

    class Meta:
        managed = False
        db_table = 'obra_obrero'
        unique_together = (('id_obra', 'id_obrero'),)
    
    def __str__(self):
        return f"Obra {self.id_obra_id} - Obrero {self.id_obrero_id}"
    


class Obrero(models.Model):
    id_obrero = models.AutoField(primary_key=True)
    nombre_completo = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'obrero'
    
    def __str__(self):
        return self.nombre_completo or f"Obrero {self.id_obrero}"


class Prestamo(models.Model):
    id_prestamo = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey('Solicitud', models.DO_NOTHING, db_column='id_solicitud', blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    fecha_devolucion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestamo'


class Reclamo(models.Model):
    id_reclamo = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    tipo_reclamo = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reclamo'


class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitud'


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    nombre_completo = models.CharField(max_length=200, blank=True, null=True)
    correo_electronico = models.CharField(unique=True, max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    perfil = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
