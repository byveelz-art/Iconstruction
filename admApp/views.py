from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Herramienta, Material, Obra, Actividad, Usuario, Obrero, ObraObrero
from .forms import HerramientaForm, MaterialForm, ObraForm, ActividadForm, UsuarioForm, ObreroForm

# --- DASHBOARD ---
def dashboard(request):
    return render(request, 'admApp/dashboard.html')


# --- CRUD Herramientas ---
def herramientas_list(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'admApp/herramientas_list.html', {'herramientas': herramientas})

def herramienta_create(request):
    form = HerramientaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Herramienta registrada correctamente')
        return redirect('herramientas_list')
    return render(request, 'admApp/herramienta_form.html', {'form': form})

def herramienta_update(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    form = HerramientaForm(request.POST or None, instance=herramienta)
    if form.is_valid():
        form.save()
        messages.success(request, 'Herramienta actualizada correctamente')
        return redirect('herramientas_list')
    return render(request, 'admApp/herramienta_form.html', {'form': form})

def herramienta_delete(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    herramienta.delete()
    messages.success(request, 'Herramienta eliminada')
    return redirect('herramientas_list')


# --- CRUD Materiales ---
def materiales_list(request):
    materiales = Material.objects.all()
    return render(request, 'admApp/materiales_list.html', {'materiales': materiales})

def material_create(request):
    form = MaterialForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Material registrado correctamente')
        return redirect('materiales_list')
    return render(request, 'admApp/material_form.html', {'form': form})

def material_update(request, pk):
    material = get_object_or_404(Material, pk=pk)
    form = MaterialForm(request.POST or None, instance=material)
    if form.is_valid():
        form.save()
        messages.success(request, 'Material actualizado correctamente')
        return redirect('materiales_list')
    return render(request, 'admApp/material_form.html', {'form': form})

def material_delete(request, pk):
    material = get_object_or_404(Material, pk=pk)
    material.delete()
    messages.success(request, 'Material eliminado')
    return redirect('materiales_list')


# --- CRUD Obras y Actividades ---
def obras_list(request):
    obras = Obra.objects.all()
    return render(request, 'admApp/obras_list.html', {'obras': obras})

def obra_create(request):
    form = ObraForm(request.POST or None)
    if form.is_valid():
        obra = form.save(commit=False)
        obra.estado = "Abierto"
        obra.save()

        # Crear la relación ObraObrero
        obrero = form.cleaned_data['obrero']
        from .models import ObraObrero
        ObraObrero.objects.create(id_obra=obra, id_obrero=obrero)

        messages.success(request, f'Obra creada con estado "Abierto" y obrero asignado: {obrero.nombre_completo}.')
        return redirect('obras_list')

    return render(request, 'admApp/obras_form.html', {'form': form})

def obra_update(request, pk):
    obra = get_object_or_404(Obra, pk=pk)

    # Intentamos obtener el obrero actual si existe
    try:
        obra_obrero = ObraObrero.objects.get(id_obra=obra)
        initial_data = {'obrero': obra_obrero.id_obrero}
    except ObraObrero.DoesNotExist:
        initial_data = {}

    form = ObraForm(request.POST or None, instance=obra, initial=initial_data)
    if form.is_valid():
        obra = form.save(commit=False)
        # mantenemos el estado existente
        obra.save()

        obrero = form.cleaned_data['obrero']
        ObraObrero.objects.update_or_create(id_obra=obra, defaults={'id_obrero': obrero})

        messages.success(request, 'Obra actualizada correctamente.')
        return redirect('obras_list')

    return render(request, 'admApp/obras_form.html', {'form': form})

def obra_delete(request, pk):
    obra = get_object_or_404(Obra, pk=pk)
    obra.delete()
    messages.success(request, 'Obra eliminada')
    return redirect('obras_list')


# CRUD Actividades asociadas a una obra
def actividades_list(request, id_obra):
    actividades = Actividad.objects.filter(id_obra=id_obra)
    return render(request, 'admApp/actividades_list.html', {'actividades': actividades, 'id_obra': id_obra})

def actividad_create(request, id_obra):
    form = ActividadForm(request.POST or None)
    if form.is_valid():
        actividad = form.save(commit=False)
        actividad.id_obra_id = id_obra
        actividad.save()
        messages.success(request, 'Actividad agregada')
        return redirect('actividades_list', id_obra=id_obra)
    return render(request, 'admApp/actividad_form.html', {'form': form, 'id_obra': id_obra})


# --- CRUD Usuarios ---
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admApp/usuarios_list.html', {'usuarios': usuarios})

def usuario_create(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado correctamente')
        return redirect('usuarios_list')
    return render(request, 'admApp/usuario_form.html', {'form': form})

def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado')
        return redirect('usuarios_list')
    return render(request, 'admApp/usuario_form.html', {'form': form})

def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.delete()
    messages.success(request, 'Usuario eliminado')
    return redirect('usuarios_list')

# --- CRUD Obreros ---
def obreros_list(request):
    obreros = Obrero.objects.all()
    return render(request, 'admApp/obreros_list.html', {'obreros': obreros})


def obrero_create(request):
    form = ObreroForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obrero registrado correctamente.')
        return redirect('obreros_list')
    return render(request, 'admApp/obreros_form.html', {'form': form})


def obrero_update(request, pk):
    obrero = get_object_or_404(Obrero, pk=pk)
    form = ObreroForm(request.POST or None, instance=obrero)
    if form.is_valid():
        form.save()
        messages.success(request, 'Obrero actualizado correctamente.')
        return redirect('obreros_list')
    return render(request, 'admApp/obreros_form.html', {'form': form})


def obrero_delete(request, pk):
    obrero = get_object_or_404(Obrero, pk=pk)
    obrero.delete()
    messages.success(request, 'Obrero eliminado correctamente.')
    return redirect('obreros_list')