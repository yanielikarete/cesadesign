# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal



class ReunionFilter(django_filters.FilterSet):
    descripcion_producto = django_filters.CharFilter(lookup_type='icontains')
   
    class Meta:
        model = Reunion
        fields = ['codigo','motivo',]
