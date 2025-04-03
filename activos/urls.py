from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),                            #cuando visita la ruta principal, voy a ejecutar la función hello
    path('about/',views.about,name="about"),   
    path('login/',views.logearse,name="logearse"),    
    path('logout/',views.salir,name="logout"),      
    path('signin/',views.entrar,name="signin"),         
    path('areas/',views.areas,name="areas"),
    path('areas/<int:id>',views.detalle_areas,name="detalle_areas"),
    path('subareas/',views.subAreas,name="subareas"),
    path('subareas/<int:id>',views.detalle_subareas,name="detalle_subareas"),
    path('subareas/crea/<int:id>',views.nueva_maquina,name="nueva_maquina"),
    path('maquinas/',views.Maquinas,name="maquinas"),
    path('maquinas/<int:id>',views.detalle_maquina,name="detalle_maquina"),
    path('maquinas/<int:id>/actualiza',views.actualiza_maquina,name="actualiza_maquina"),
    path('crear_subarea/',views.crear_subarea,name="crear_subarea"),
    path('crear_area/',views.crear_area,name="crear_area"),
    path('parte/crea/<int:id>',views.nueva_parte,name="nueva_parte"),
    path('mantenimiento/<int:id>/crea',views.crear_mantenimiento,name="crear_mantenimiento"),
    path('mantenimiento/<int:id>/ver',views.ver_mantenimiento,name="ver_mantenimiento"),
    path('mantenimiento/<int:id>/detalle',views.detalle_mantenimiento,name="detalle_mantenimiento"),
    path('mantenimiento/<int:id>/completa',views.completa_mantenimiento,name="completa_mantenimiento"),
    path('mantenimiento/<int:id>/borra',views.borra_mantenimiento,name="borra_mantenimiento"),
    path('mantenimientos_pendiente/<int:id>',views.MantenimientoMaquinas_pendiente,name="mantenimiento_maquina_pendiente"),
    path('mantenimientos_completo/<int:id>',views.MantenimientoMaquinas_completo,name="mantenimiento_maquina_completo"),
]