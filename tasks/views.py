from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login ,logout, authenticate
from django.db import IntegrityError

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
                login(request,user)
                return redirect('tasks')
                # return HttpResponse('User created successfully')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': form,
                    'error': 'User already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': form,
                'error': 'Passwords do not match'
            })
            

def tasks(request):
    return render(request, 'tasks.html')
 
 
#do not call logout it nakes issues 
def singout(request):
    logout(request)
    return redirect('home')
# redirect(): Se utiliza cuando necesitas cambiar de página. Genera una respuesta de redirección (código de estado HTTP 302) al navegador, lo que hace que cargue una nueva URL.
# path('logout/', views.singout, name='logout'),


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks')

           
        #   return render(request, 'signin.html', {
        # 'form' : AuthenticationForm,
        #  })
       
            
        # print(request.POST)
        
     
#render(): Cuando quieras mostrar una plantilla con datos a la página actual (por ejemplo, al mostrar un formulario de inicio de sesión o una página de detalles de un objeto).