# coding: utf-8
import django_filters
from .models import *
#from login.middlewares import ThreadLocal


class AmbienteFilter(django_filters.FilterSet):
   
    class Meta:
        model = Ambiente
        fields = ['codigo','descripcion',]
