from django.contrib import admin
from .models import Task

# Definir el modelo de administración para Task
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)  # Asegúrate de que sea una tupla con la coma al final

# Registrar el modelo Task en el administrador de Django
admin.site.register(Task, TaskAdmin)


  
# admin.ModelAdmin: Es la clase base correcta para personalizar el comportamiento de un modelo en el administrador de Django.
# readonly_fields: Se utiliza para marcar campos como de solo lectura en el administrador. Asegúrate de que los nombres coincidan con los de tu modelo.
# Registrar el modelo: admin.site.register(Task, TaskAdmin) registra el modelo Task con las configuraciones personalizadas de TaskAdmin.