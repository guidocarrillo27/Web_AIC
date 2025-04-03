from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from activos.models import Area,SubArea,Maquina,mantenimientos,Parte
from .forms import CrearNuevaTarea, CrearNuevaArea, CrearMantenimiento,VerMantenimiento,VerMaquina,DetalleMantenimiento,NuevaMaquina,ActualizaMaquina,NuevaParte
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    title='Programa de Mantenimiento'
    return render(request,'index.html', {'titulo':title})

def about(request):
    username='guido'
    return render(request,'about.html',{
        'usuario':username
    })

def hello(request,username):
    print(username)
    i=1
    return HttpResponse("<h1>Hola %s tu codigo es %s</h1>"%username %i)

def areas(request):
    #areas=list(Area.objects.values())
    #return JsonResponse(areas,safe=False)
    areas=Area.objects.all()
    return render(request,'areas/areas.html',{
        'locaciones':areas
    })

def subAreas(request):
    #sa=SubArea.objects.get(id=id)
    #return HttpResponse('Subarea: %s'%sa.nombre)
    sa=SubArea.objects.all()
    return render(request,'subareas/subareas.html',{
        'subareas':sa
    })

@login_required
def Maquinas(request):
    #return HttpResponse('Máquinas')
    maquinas=Maquina.objects.all()
    return render(request,'maquinas/maquinas.html',{
        'maquinas':maquinas
    })

def detalle_maquina(request,id):
    maquina=get_object_or_404(Maquina,id=id)
    form=VerMaquina(instance=maquina)
    activa_guarda=False

    partes=Parte.objects.filter(maquina_id=id)
    return render(request,'maquinas/detalle_maquina.html',{
        'maquina':maquina,
        'activa_guarda':activa_guarda,
        'form':form,
        'partes':partes
    })

@login_required
def crear_subarea(request):
    #print(request.GET['codigo'])
    #print(request.GET['nombre'])

    if request.method == 'GET':
        #voy a mostrar la interface
        return render(request,'subareas/crear_subarea.html',{'form':CrearNuevaTarea()})
    else:
        #print(request.POST)
        SubArea.objects.create(subarea_id=request.POST['subarea'],
                               nombre=request.POST['nombre'],
                            cod_subArea=request.POST['cod_subArea'])
        return redirect('subareas')

def nueva_maquina(request,id):   
    if request.method=='GET':
        area=get_object_or_404(SubArea,pk=id)
        return render(request,'subareas/nueva_maquina.html',{
        'area':area,
        'form':NuevaMaquina()})
    else:
        area=get_object_or_404(SubArea,pk=id)
        form=NuevaMaquina(request.POST,request.FILES)
        if form.is_valid():
            nueva_maquina=form.save(commit=False)
            nueva_maquina.subarea_id=area.id
            nueva_maquina.save()
            return redirect('detalle_subareas',id=id)
        else:
            print(form.errors)
        
        return render(request,'subareas/nueva_maquina.html',{
        'form':NuevaMaquina()})

def nueva_parte(request,id):   
    if request.method=='GET':
        maquina=get_object_or_404(Maquina,pk=id)
        return render(request,'partes/nueva_parte.html',{
        'maquina':maquina,
        'form':NuevaParte()})
    else:
        maquina=get_object_or_404(Maquina,pk=id)
        form=NuevaParte(request.POST,request.FILES)
        if form.is_valid():
            nueva_parte=form.save(commit=False)
            nueva_parte.save()
            return redirect('detalle_maquina',id=id)
        else:
            print(form.errors)
        
        return render(request,'partes/nueva_parte.html',{
        'form':()})



@login_required    
def crear_area(request):
    if request.method=='GET':
        return render(request,'areas/crear_area.html',{'form':CrearNuevaArea()})
    else:
        Area.objects.create(cod_area=request.POST['codigo'],
            nombre=request.POST['nombre'])
        return redirect('areas')

def detalle_areas(request,id):
    area=get_object_or_404(Area,id=id)
    subareas=SubArea.objects.filter(subarea_id=id)
    return render(request,'areas/detalle_areas.html',{
        'area':area,
        'subareas':subareas
    })

def detalle_subareas(request,id):
    subarea=get_object_or_404(SubArea,id=id)
    maquinas=Maquina.objects.filter(area_id=id)
    return render(request,'subareas/detalle_subareas.html',{
        'subarea':subarea,
        'maquinas':maquinas
    })

def actualiza_maquina(request,id):
    if request.method=='GET':
        maquina=get_object_or_404(Maquina,id=id)
        form=ActualizaMaquina(instance=maquina)
        activa_guarda=True
        return render(request,'maquinas/detalle_maquina.html',{
        'maquina':maquina,
        'activa_guarda':activa_guarda,
        'form1':form})
    else:
        try:
            maquina=get_object_or_404(Maquina,pk=id)
            form=ActualizaMaquina(request.POST,request.FILES,instance=maquina)
            form.save()
            #return redirect('/subareas/1')
            return redirect('detalle_subareas',id=maquina.area_id)
        except ValueError:
            return render(request,'maquinas/detalle_maquina.html',{
                                'maquina':maquina,
                                'activa_guarda':activa_guarda,
                                'error':"Error actualizando la maquina",
                                'form1':form})

def logearse (request):
    if (request.method == 'GET'):
        return render(request,'logeo.html',{
            'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('index')              
            except IntegrityError: 
                return render(request,'logeo.html',{
                    'form':UserCreationForm,
                    'error':'Username already exist'
                    })  
           
        return render(request,'logeo.html',{
                    'form':UserCreationForm,
                    'error':'Contraseñas son incorrectas'
                    })  
           
def salir(request):
    logout(request)
    return redirect('index')

def entrar(request):
    if request.method=='GET':
        return  render(request,'signin.html',{
       'form':AuthenticationForm 
        })
    else:
        print(request.POST)
        user=authenticate(request,username=request.POST['username'],
                      password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form':AuthenticationForm, 
                'error':'Usuario o password incorrecto'
                })
        else:
            login(request,user)
            return redirect('areas')
        
def crear_mantenimiento(request,id):
    if request.method=='GET':
        maquina=get_object_or_404(Maquina,pk=id)
        return render(request,'mantenimientos/crear_mantenimiento.html',{
        'maquina':maquina,
        'form':CrearMantenimiento()})
    else:
        maquina=get_object_or_404(Maquina,pk=id)
        form=CrearMantenimiento(request.POST,request.FILES)
        if form.is_valid():
            nuevo_mantenimiento=form.save(commit=False)
            nuevo_mantenimiento.maquina_id=maquina.id
            nuevo_mantenimiento.user=request.user
            nuevo_mantenimiento.save()
            return redirect(f'/mantenimientos_pendiente/{id}')
        else:
            print(form.errors)
        
        return render(request,'mantenimientos/crear_mantenimiento.html',{
        'form':CrearMantenimiento()})

def detalle_mantenimiento(request,id):
        if request.method == 'GET':
            mantenimiento=get_object_or_404(mantenimientos,pk=id)
            form=DetalleMantenimiento(instance=mantenimiento)
            return render(request,'mantenimientos/detalle_mantenimiento.html',{
            'mantenimiento':mantenimiento,
            'form':form})
        else:
            try:
                mantenimiento=get_object_or_404(mantenimientos,pk=id)
                form=DetalleMantenimiento(request.POST,request.FILES,instance=mantenimiento)
                form.save()
                return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)
            except ValueError:
                return render(request,'mantenimientos/detalle_mantenimiento.html',{
                            'mantenimiento':mantenimiento,
                            'error':"Error actualizando la actividad de mantenimiento",
                            'form':form})

def completa_mantenimiento(request,id):
    mantenimiento=get_object_or_404(mantenimientos,pk=id)
    if request.method=='POST':
        mantenimiento.fecha_ejecutada=timezone.now()
        mantenimiento.save()
        return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)
    
def borra_mantenimiento(request,id):
    mantenimiento=get_object_or_404(mantenimientos,pk=id)
    if request.method=='POST':
        mantenimiento.delete()
        return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)

def ver_mantenimiento(request,id):
    if request.method == 'GET':
        #mantenimiento=mantenimientos.objects.get(pk=id)
        mantenimiento=get_object_or_404(mantenimientos,pk=id)
        form=VerMantenimiento(instance=mantenimiento)
        return render(request,'mantenimientos/ver_mantenimiento.html',{
            'mantenimiento':mantenimiento,
            'form':form})
   
def MantenimientoMaquinas_pendiente(request,id):
    #return HttpResponse('Máquinas')
    maquina=get_object_or_404(Maquina,id=id)
    detalle_mantenimiento=mantenimientos.objects.filter(maquina_id=id,fecha_ejecutada__isnull=True).order_by('-fecha_ejecutada')

    return render(request,'mantenimientos/mantenimiento_maquina.html',{
            'maquina':maquina,'mantenimientos':detalle_mantenimiento})

def MantenimientoMaquinas_completo(request,id):

    maquina=get_object_or_404(Maquina,id=id)
    detalle_mantenimiento=mantenimientos.objects.filter(maquina_id=id,fecha_ejecutada__isnull=False).order_by('-fecha_ejecutada')

    return render(request,'mantenimientos/mantenimiento_maquina.html',{
            'maquina':maquina,'mantenimientos':detalle_mantenimiento})