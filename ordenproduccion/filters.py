# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal


class OrdenProduccionFilter(django_filters.FilterSet):
   
    class Meta:
        model = OrdenProduccion
        fields = ['codigo','descripcion',]

class RopFilter(django_filters.FilterSet):
   
    class Meta:
        model = Rop
        fields = ['codigo','descripcion',]
