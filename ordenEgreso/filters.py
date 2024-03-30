# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
from proveedores.models import *
#from login.middlewares import ThreadLocal


class OrdenEgresoFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenEgreso
        fields = ['codigo']

class OrdenEgresoAprobadaFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenEgreso
        fields = ['codigo']

class EgresoOrdenEgresoFilter(django_filters.FilterSet):
       
    class Meta:
        model = EgresoOrdenEgreso
        fields = ['orden_egreso']