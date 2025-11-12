from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils import timezone
from django.db import connection

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirección según el rol
            if user.is_superuser:
                return redirect('/administracion/dashboard')
            else:
                return redirect('#') # Redirigir a una página para usuarios normales

        else:
            messages.error(request, 'Credenciales incorrectas.')

    return render(request, 'sesionApp/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')