from django.forms import ModelForm  # Corrección aquí
from .models import Task  # Importa el modelo correspondiente

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important']  # O lista de campos específicos si no quieres incluir todos
