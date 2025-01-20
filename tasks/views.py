from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        # Pasamos un formulario vacío a la plantilla
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        # Proceso de creación de usuario y verificación de contraseña
        form = UserCreationForm(request.POST)  # Reconstruimos el formulario con los datos enviados
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                return HttpResponse('User created successfully')
            except:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'User already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Passwords do not match'
            })
