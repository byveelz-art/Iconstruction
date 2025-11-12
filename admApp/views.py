from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Herramienta, Material, Obra, Actividad, Usuario, Obrero, Bodega, InventarioMaterial, Prestamo
from .forms import HerramientaForm, MaterialForm, ObraForm, ActividadForm, UsuarioForm, ObreroForm, BodegaForm, PrestamoForm
from .decorators import admin_required, admin_or_supervisor, admin_or_bodeguero, staff_only


# ============================================
# DASHBOARD
# ============================================
@login_required
def dashboard(request):
    """Dashboard principal - todos los usuarios autenticados"""
    context = {
        'total_obras': Obra.objects.count(),
        'total_herramientas': Herramienta.objects.filter(activo=True).count(),
        'total_materiales': Material.objects.filter(activo=True).count(),
        'total_obreros': Obrero.objects.count(),
    }
    return render(request, 'admApp/dashboard.html', context)


# ============================================
# CRUD HERRAMIENTAS (Admin o Bodeguero)
# ============================================
@login_required
@admin_or_bodeguero
def herramientas_list(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'admApp/herramientas_list.html', {'herramientas': herramientas})


@login_required
@admin_or_bodeguero
def herramienta_create(request):
    form = HerramientaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Herramienta creada correctamente')
        return redirect('herramientas_list')
    return render(request, 'admApp/herramienta_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    form = HerramientaForm(request.POST or None, instance=herramienta)
    if form.is_valid():
        form.save()
        messages.success(request, 'Herramienta actualizada correctamente')
        return redirect('herramientas_list')
    return render(request, 'admApp/herramienta_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    if request.method == 'POST':
        herramienta.delete()
        messages.success(request, 'Herramienta eliminada')
        return redirect('herramientas_list')
    return render(request, 'admApp/confirm_delete.html', {'object': herramienta})


# ============================================
# CRUD MATERIALES (Admin o Bodeguero)
# ============================================
@login_required
@admin_or_bodeguero
def materiales_list(request):
    materiales = Material.objects.all()
    return render(request, 'admApp/materiales_list.html', {'materiales': materiales})


@login_required
@admin_or_bodeguero
def material_create(request):
    form = MaterialForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Material creado correctamente')
        return redirect('materiales_list')
    return render(request, 'admApp/material_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(request.POST or None, instance=material)
    if form.is_valid():
        form.save()
        messages.success(request, 'Material actualizado correctamente')
        return redirect('materiales_list')
    return render(request, 'admApp/material_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material eliminado')
        return redirect('materiales_list')
    return render(request, 'admApp/confirm_delete.html', {'object': material})


# ============================================
# CRUD OBRAS (Admin o Supervisor)
# ============================================
@login_required
@admin_or_supervisor
def obras_list(request):
    obras = Obra.objects.all()
    return render(request, 'admApp/obras_list.html', {'obras': obras})


@login_required
@admin_or_supervisor
def obra_create(request):
    form = ObraForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obra creada correctamente')
        return redirect('obras_list')
    return render(request, 'admApp/obras_form.html', {'form': form})


@login_required
@admin_or_supervisor
def obra_update(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    form = ObraForm(request.POST or None, instance=obra)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obra actualizada correctamente')
        return redirect('obras_list')
    return render(request, 'admApp/obras_form.html', {'form': form})


@login_required
@admin_or_supervisor
def obra_delete(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == 'POST':
        obra.delete()
        messages.success(request, 'Obra eliminada')
        return redirect('obras_list')
    return render(request, 'admApp/confirm_delete.html', {'object': obra})


# ============================================
# CRUD ACTIVIDADES (Admin o Supervisor)
# ============================================
@login_required
@admin_or_supervisor
def actividades_list(request):
    actividades = Actividad.objects.all()
    return render(request, 'admApp/actividades_list.html', {'actividades': actividades})


@login_required
@admin_or_supervisor
def actividad_create(request):
    form = ActividadForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Actividad creada correctamente')
        return redirect('actividades_list')
    return render(request, 'admApp/actividad_form.html', {'form': form})


@login_required
@admin_or_supervisor
def actividad_update(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    form = ActividadForm(request.POST or None, instance=actividad)
    if form.is_valid():
        form.save()
        messages.success(request, 'Actividad actualizada')
        return redirect('actividades_list')
    return render(request, 'admApp/actividad_form.html', {'form': form})


@login_required
@admin_or_supervisor
def actividad_delete(request, pk):
    actividad = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        actividad.delete()
        messages.success(request, 'Actividad eliminada')
        return redirect('actividades_list')
    return render(request, 'admApp/confirm_delete.html', {'object': actividad})


# ============================================
# CRUD USUARIOS (Solo Admin)
# ============================================
@login_required
@admin_required
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admApp/usuarios_list.html', {'usuarios': usuarios})


@login_required
@admin_required
def usuario_create(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuarios_list')
    return render(request, 'admApp/usuario_form.html', {'form': form})


@login_required
@admin_required
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado')
        return redirect('usuarios_list')
    return render(request, 'admApp/usuario_form.html', {'form': form})


@login_required
@admin_required
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado')
        return redirect('usuarios_list')
    return render(request, 'admApp/confirm_delete.html', {'object': usuario})


# ============================================
# CRUD OBREROS (Solo Admin)
# ============================================
@login_required
@admin_required
def obreros_list(request):
    obreros = Obrero.objects.all()
    return render(request, 'admApp/obreros_list.html', {'obreros': obreros})


@login_required
@admin_required
def obrero_create(request):
    form = ObreroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obrero creado correctamente')
        return redirect('obreros_list')
    return render(request, 'admApp/obreros_form.html', {'form': form})


@login_required
@admin_required
def obrero_update(request, pk):
    obrero = get_object_or_404(Obrero, pk=pk)
    form = ObreroForm(request.POST or None, instance=obrero)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obrero actualizado')
        return redirect('obreros_list')
    return render(request, 'admApp/obreros_form.html', {'form': form})


@login_required
@admin_required
def obrero_delete(request, pk):
    obrero = get_object_or_404(Obrero, pk=pk)
    if request.method == 'POST':
        obrero.delete()
        messages.success(request, 'Obrero eliminado')
        return redirect('obreros_list')
    return render(request, 'admApp/confirm_delete.html', {'object': obrero})


# ============================================
# CRUD BODEGAS (Admin o Bodeguero)
# ============================================
@login_required
@admin_or_bodeguero
def bodegas_list(request):
    bodegas = Bodega.objects.select_related('encargado').all()
    return render(request, 'admApp/bodegas_list.html', {'bodegas': bodegas})


@login_required
@admin_or_bodeguero
def bodega_create(request):
    form = BodegaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bodega creada correctamente')
        return redirect('bodegas_list')
    return render(request, 'admApp/bodega_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def bodega_detail(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    inventarios = InventarioMaterial.objects.filter(bodega=bodega).select_related('material')
    return render(request, 'admApp/bodega_detail.html', {'bodega': bodega, 'inventarios': inventarios})


# ============================================
# INVENTARIO (Admin o Bodeguero)
# ============================================
@login_required
@admin_or_bodeguero
def inventario_list(request):
    inventarios = InventarioMaterial.objects.select_related('bodega', 'material').all()
    
    inventarios_con_alerta = []
    for inv in inventarios:
        inv.alerta = inv.cantidad_actual < inv.material.stock_minimo
        inventarios_con_alerta.append(inv)
    
    return render(request, 'admApp/inventario_list.html', {'inventarios': inventarios_con_alerta})


# ============================================
# PRÉSTAMOS (Admin o Bodeguero)
# ============================================
@login_required
@admin_or_bodeguero
def prestamos_list(request):
    prestamos = Prestamo.objects.select_related('herramienta', 'obrero__usuario', 'obra').all().order_by('-fecha_prestamo')
    return render(request, 'admApp/prestamos_list.html', {'prestamos': prestamos})


@login_required
@admin_or_bodeguero
def prestamo_create(request):
    from datetime import date
    
    form = PrestamoForm(request.POST or None)
    if form.is_valid():
        prestamo = form.save(commit=False)
        prestamo.estado = Prestamo.EstadoPrestamo.ACTIVO
        prestamo.usuario_registro = request.user
        prestamo.save()
        
        # Marcar herramienta como prestada
        herramienta = prestamo.herramienta
        herramienta.estado = 'EN_USO'
        herramienta.save()
        
        messages.success(request, f'Préstamo registrado: {herramienta.nombre} → {prestamo.obrero.usuario.get_full_name()}')
        return redirect('prestamos_list')
    return render(request, 'admApp/prestamo_form.html', {'form': form})


@login_required
@admin_or_bodeguero
def prestamo_devolver(request, pk):
    from datetime import datetime
    
    prestamo = get_object_or_404(Prestamo, pk=pk)
    
    if request.method == 'POST':
        prestamo.estado = Prestamo.EstadoPrestamo.DEVUELTO
        prestamo.fecha_devolucion_real = datetime.now()
        prestamo.save()
        
        # Marcar herramienta como disponible
        herramienta = prestamo.herramienta
        herramienta.estado = 'DISPONIBLE'
        herramienta.save()
        
        messages.success(request, f'Herramienta devuelta: {herramienta.nombre}')
        return redirect('prestamos_list')
    
    return render(request, 'admApp/prestamo_devolver.html', {'prestamo': prestamo})
