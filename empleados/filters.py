# coding: utf-8
import django_filters
from .models import *

class EmpleadoFilter(django_filters.FilterSet):
    nombre_empleado = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Empleado
        fields = ['codigo_empleado','nombre_empleado','cedula_empleado',]

class  TipoEmpleadoFilter(django_filters.FilterSet):
    cargo = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = TipoEmpleado
        fields = ['cargo_empleado',]

class VendedorFilter(django_filters.FilterSet):
    codigo_vendedor = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Vendedor
        fields = ['codigo_vendedor',]

class ChoferFilter(django_filters.FilterSet):
    codigo_chofer = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Chofer
        fields = ['codigo_chofer',]


class VehiculoFilter(django_filters.FilterSet):
    placa = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Vehiculo
        fields = ['placa',]

class DepartamentoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Departamento
        fields = ['codigo','nombre',]
