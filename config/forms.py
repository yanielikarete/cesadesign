# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from .models import *
from models import *
from os import path
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import *
from django.forms.models import model_to_dict, fields_for_model



class AreasForm(ModelForm):

    class Meta:
        model = Areas
        exclude = ("created_at","updated_at","created_by","updated_by")

class VehiculoForm(ModelForm):

    class Meta:
        model = Vehiculo
        exclude = ("created_at","updated_at","created_by","updated_by")

class EstadosProForm(ModelForm):

    class Meta:
        model = EstadosPro
        exclude = ("created_at","updated_at","created_by","updated_by")

class TipoMuebForm(ModelForm):

    class Meta:
        model = TipoMueb
        exclude = ("created_at","updated_at","created_by","updated_by")

class SecuencialesForm(ModelForm):

    class Meta:
        model = Secuenciales
        exclude = ("created_at","updated_at","created_by","updated_by")

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        exclude = ("created_at","updated_at","created_by","updated_by")

class MenuGroupForm(ModelForm):
    class Meta:
        model = MenuGroup
        exclude = ("created_at","updated_at","created_by","updated_by")

class TipoLugarForm(ModelForm):

    class Meta:
        model = TipoLugar
        exclude = ("created_at","updated_at","created_by","updated_by")

class PuntosVentaForm(ModelForm):

    class Meta:
        model = PuntosVenta
        exclude = ("created_at","updated_at","created_by","updated_by")
        
class ParametrosForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = Parametros
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("clave","valor","descripcion")

    def __init__(self, *args, **kwargs):
        super(ParametrosForm, self).__init__(*args, **kwargs)

class CiudadForm(ModelForm):

    class Meta:
        model = Ciudad
        exclude = ("created_at","updated_at","created_by","updated_by")

class EstadoCivilForm(ModelForm):

    class Meta:
        model = EstadoCivil
        exclude = ("created_at","updated_at","created_by","updated_by")

class PaisForm(ModelForm):

    class Meta:
        model = Pais
        exclude = ("created_at","updated_at","created_by","updated_by")

class ProvinciaForm(ModelForm):

    class Meta:
        model = Provincia
        exclude = ("created_at","updated_at","created_by","updated_by")

class RelacionLaboralForm(ModelForm):

    class Meta:
        model = RelacionLaboral
        exclude = ("created_at","updated_at","created_by","updated_by")

class TipoRemuneracionForm(ModelForm):

    class Meta:
        model = TipoRemuneracion
        exclude = ("created_at","updated_at","created_by","updated_by")


class FormaPagoEmpleadoForm(ModelForm):

    class Meta:
        model = FormaPagoEmpleado
        exclude = ("created_at","updated_at","created_by","updated_by")


class AnioForm(ModelForm):

    class Meta:
        model = Anio
        exclude = ("created_at","updated_at","created_by","updated_by")
        


class BloqueoPeriodoForm(ModelForm):

    class Meta:
        model = BloqueoPeriodo
        exclude = ("created_at","updated_at","created_by","updated_by")