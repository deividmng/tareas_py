from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        # Renderizamos el formulario vacío
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        # Reconstruimos el formulario con los datos enviados
        form = UserCreationForm(request.POST)
        if form.is_valid():  # Validamos el formulario
            try:
                # Creamos el usuario de manera manual (ya que queremos capturar IntegrityError)
                user = User.objects.create_user(
                    username=request.POST['username'],  # Obtenemos el nombre del usuario
                    password=request.POST['password1']  # Obtenemos la contraseña
                )
                user.save()  # Intentamos guardar el usuario en la base de datos
                login(request, user)  # Inicia sesión automáticamente
                return redirect('tasks')  # Redirigimos a la vista "tasks"
            except IntegrityError:
                # Mostramos un mensaje si el usuario ya existe
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'A user with that username already exists.'
                })
        else:
            # Si el formulario es inválido, mostramos los errores
            return render(request, 'signup.html', {'form': form})
def tasks(request):
    return render(request, 'tasks.html')
 