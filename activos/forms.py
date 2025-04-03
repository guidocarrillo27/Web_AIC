from django import forms
from django.forms import ModelForm,SelectDateWidget
from .models import mantenimientos,SubArea,Maquina,Parte
from django.contrib.admin import widgets 


class CrearNuevaTarea(ModelForm):
    #codigo=forms.CharField(label='Código')  #es para crear input tipo texto
    #nombre=forms.CharField(label='Nombre subárea',widget=forms.Textarea)

    class Meta:
        model=SubArea 
        fields=['subarea','nombre','cod_subArea']
    
        widgets={
            'cod_subArea':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código area'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre area'})
        }

class CrearNuevaArea(forms.Form):
    nombre=forms.CharField(label='Nombre área',widget=forms.Textarea)
    codigo=forms.CharField(label='Código')  #es para crear input tipo texto    

class NuevaMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields=['area','codigo','nombre','descripción','disponibilidad','fecha_instalación','foto','link']

        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código máquina'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre máquina'}),
            'descripción':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de máquina'}),
            'fecha_instalación':forms.widgets.DateInput(attrs={'type':'date'})                                
        }

class NuevaParte(ModelForm):
    class Meta:
        model=Parte
        fields=['maquina','codigo_parte','nombre','descripción','mantenimiento','anexo1','anexo2']

        widgets={
            'codigo_parte':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código parte'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre parte'}),
            'descripción':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'}),
            'mantenimiento':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'})                              
        }

class CrearMantenimiento(ModelForm):
    #fecha_planificada=forms.DateField(widget = forms.SelectDateWidget())

    class Meta:
        model=mantenimientos
        fields=['tipo','nombre','descripcion','fecha_planificada','responsable']

        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre actividad'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7'}),
            'fecha_planificada':forms.widgets.DateInput(attrs={'type':'date'})
        }

class DetalleMantenimiento(ModelForm):
    class Meta:
        model=mantenimientos
        fields=['tipo','nombre','descripcion','fecha_planificada','responsable','evidencia']
        
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre actividad'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7'}),
            'fecha_planificada':forms.widgets.DateInput(attrs={'type':'date'})
        }
        
class VerMantenimiento(ModelForm):
    class Meta:
        model=mantenimientos
        fields="__all__"    #se usa para ver todos los campos

class VerMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields="__all__"    #se usa para ver todos los campos

        fields=['area','codigo','descripción',
                'disponibilidad','fecha_instalación','link']

        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'descripción':forms.Textarea(attrs={'class':'form-control',
                                                'rows':'5'})                                                
        }

class ActualizaMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields="__all__"    #se usa para ver todos los campos

        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'descripción':forms.Textarea(attrs={'class':'form-control',
                                                'rows':'5'})                                                
        }