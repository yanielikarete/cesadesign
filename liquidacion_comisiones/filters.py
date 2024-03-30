# coding: utf-8
import django_filters
from .models import *
#from login.middlewares import ThreadLocal


class LiquidacionComisionesAmbienteFilter(django_filters.FilterSet):
   
    class Meta:
        model = LiquidacionComisiones
        fields = ['codigo',]
