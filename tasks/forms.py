from django.forms import ModelForm, TextInput, Textarea, CheckboxInput
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']  # Lista de campos que deseas incluir
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description',
                'rows': 4,
            }),
            'important': CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
