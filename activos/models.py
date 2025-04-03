from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from uuid import uuid4

class Area(models.Model):
    cod_area=models.IntegerField()
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return str(self.cod_area) + ' - ' + self.nombre 

class SubArea(models.Model):
    subarea=models.ForeignKey(Area,on_delete=models.CASCADE)
    cod_subArea=models.CharField(max_length=15)
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Maquina(models.Model):

    def wrapper(instance, filename):
        ext = filename.split(".")[-1].lower()
        # se obtiene el nombre del archivo

        if ext not in ["jpg", "png", "gif", "jpeg"]:
            raise ValidationError(f"invalid image extension: {filename}")

        if instance.pk:
            filename = '{}.{}'.format(instance.nombre, ext)
        else:
            filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join("images_maquinas", filename)
       
    def inner(instance,filename):
        ext = filename.split('.')[-1].lower()
        
        if instance.pk:
            filename = '{}.{}'.format(instance.nombre, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join("archivos_maquinas", filename)
             
    #creo una lista de tuplas con el estado operativo que tendrá la máquina
    estado_operativo = [
        ("ON","EN OPERACIÓN"),
        ("BK","EN RESERVA/MANTENIMIENTO"),
        ("OFF","FUERA DE OPERACIÓN PERMANENTE")
    ]

    area=models.ForeignKey(SubArea,on_delete=models.CASCADE)                   #relación muchos a uno
    codigo=models.CharField(max_length=15)                                  #campo que guarda el código de la máquina
    nombre=models.CharField(max_length=100)                                 #campo guarda nombre máquina
    descripción=models.TextField()                                          #campo para escribir texto             
    disponibilidad=models.CharField(max_length=3,choices=estado_operativo)  #se escoge una opción de la lista de choices
    fecha_instalación = models.DateField()                                  #campo que guarda fecha de instalación máquina
    fecha_updated=models.DateField(auto_now=True)                           #campo para guardar la fecha en cada modificación
    foto=models.ImageField(upload_to=wrapper,null=True,blank=True)     #null=True indica que admite valores nulos
    link=models.FileField(upload_to=inner,null=True,blank=True) 

    def __str__(self):
        return self.nombre

class Parte(models.Model):

    def inner(instance,filename):
        ext = filename.split('.')[-1].lower()
        
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join("archivos_partes", filename)

    maquina=models.ForeignKey(Maquina,on_delete=models.CASCADE)
    codigo_parte=models.CharField(max_length=100)
    nombre=models.CharField(max_length=130) 
    descripción=models.TextField() 
    mantenimiento=models.TextField(null=True,blank=True)  
    anexo1=models.FileField(upload_to=inner,null=True,blank=True)    
    anexo2=models.FileField(upload_to=inner,null=True,blank=True) 

    def __str__(self):
        return self.nombre

class mantenimientos(models.Model):

    def inner(instance,filename):
        ext = filename.split('.')[-1].lower()
        
        if instance.pk:
            filename = '{}.{}'.format(instance.nombre, ext)
        else:
            # set filename as random string
            filename = ''.join(['content', instance.user.username, filename])
        # return the whole path to the file
        return os.path.join("mantenimientos_maquinas", filename)  
    
    tipo_servicio = [
        ("PRE","PREVENTIVO"),
        ("CORR","CORRECTIVO"),
        ("DIC","PREDICTIVO")
    ]

    maquina=models.ForeignKey(Maquina,on_delete=models.CASCADE)
    tipo=models.CharField(max_length=5,choices=tipo_servicio)
    nombre=models.CharField(max_length=200)  
    descripcion=models.TextField()
    fecha_planificada=models.DateField()
    fecha_ejecutada=models.DateField(null=True,blank=True)
    responsable=models.ForeignKey(User,on_delete=models.CASCADE)
    evidencia=models.FileField(upload_to=inner,null=True,blank=True)

    def __str__(self):
        return str(self.maquina.nombre) +' - '+self.nombre






