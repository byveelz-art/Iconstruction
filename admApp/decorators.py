from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def role_required(*roles):
    """
    Decorador personalizado para requerir ciertos roles.
    Uso: @role_required('ADMIN', 'BODEGUERO')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.rol not in roles:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Solo administradores"""
    return role_required('ADMIN')(view_func)


def admin_or_supervisor(view_func):
    """Administradores o supervisores"""
    return role_required('ADMIN', 'SUPERVISOR')(view_func)


def admin_or_bodeguero(view_func):
    """Administradores o bodegueros"""
    return role_required('ADMIN', 'BODEGUERO')(view_func)


def staff_only(view_func):
    """Administradores, supervisores o bodegueros (NO obreros)"""
    return role_required('ADMIN', 'SUPERVISOR', 'BODEGUERO')(view_func)
