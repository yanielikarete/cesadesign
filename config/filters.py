# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal


class AreasFilter(django_filters.FilterSet):
   
    class Meta:
        model = Areas
        fields = ['codigo','descripcion',]

class VehiculoFilter(django_filters.FilterSet):
   
    class Meta:
        model = Vehiculo
        fields = ['placa',]

class EstadosProFilter(django_filters.FilterSet):
   
    class Meta:
        model = EstadosPro
        fields = ['codigo','descripcion',]

class TipoMuebFilter(django_filters.FilterSet):
   
    class Meta:
        model = TipoMueb
        fields = ['codigo','descripcion',]

class MenuFilter(django_filters.FilterSet):
   
    class Meta:
        model = Menu
        fields = ['nom_option']


class SecuencialesFilter(django_filters.FilterSet):
   
    class Meta:
        model = Secuenciales
        fields = ['modulo']

class MenuGroupFilter(django_filters.FilterSet):
   
    class Meta:
        model = MenuGroup
        fields = ['group']

class TipoLugarFilter(django_filters.FilterSet):
   
    class Meta:
        model = TipoLugar
        fields = ['codigo','descripcion',]
class PuntosVentaFilter(django_filters.FilterSet):
   
    class Meta:
        model = PuntosVenta
        fields = ['codigo','nombre',]
