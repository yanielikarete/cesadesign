# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
#from login.middlewares import ThreadLocal
# coding: utf-8
import django_filters
from .models import *
from muedirsa.models import *
from proveedores.models import *
#from login.middlewares import ThreadLocal


class OrdenIngresoFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenIngreso
        fields = ['codigo']

class OrdenIngresoAprobadaFilter(django_filters.FilterSet):
       
    class Meta:
        model = OrdenIngreso
        fields = ['codigo']

class INgresoOrdenIngresoFilter(django_filters.FilterSet):
       
    class Meta:
        model = IngresoOrdenIngreso
        fields = ['orden_ingreso']
