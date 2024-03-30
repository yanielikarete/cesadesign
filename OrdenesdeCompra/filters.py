# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
from proveedores.models import *
#from login.middlewares import ThreadLocal


class OrdenCompraFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenCompra
        fields = ['nro_compra']

class OrdenCompraAprobadaFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenCompra
        fields = ['nro_compra']

class ComprasLocalesFilter(django_filters.FilterSet):
       
    class Meta:
        model = ComprasLocales
        fields = ['orden_compra']