from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login ,logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone

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
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {
            'form': TaskForm
        }) 
    else:
        try:
            form = TaskForm(request.POST)  # Para obtener el formulario
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'erro': 'Please provide valid data'  # Corregido: coma añadida
            })

from django.shortcuts import get_object_or_404

def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks') 
    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks') 

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