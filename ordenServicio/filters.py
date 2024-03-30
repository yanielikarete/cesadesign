# coding: utf-8
import django_filters
from .models import *

class OrdenServicioFilter(django_filters.FilterSet):
    nro_orden = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = OrdenServicio
        fields = ['nro_orden',]