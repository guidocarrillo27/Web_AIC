from django.contrib import admin
from .models import Area,SubArea,Maquina,mantenimientos,Parte

# Register your models here.
admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(Maquina)
admin.site.register(mantenimientos)
admin.site.register(Parte)
