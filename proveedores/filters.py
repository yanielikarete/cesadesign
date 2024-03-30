# coding: utf-8
import django_filters
from .models import *



class ProveedorFilter(django_filters.FilterSet):
    nombre_proveedor= django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Proveedor
        fields = ['codigo_proveedor','nombre_proveedor',]
