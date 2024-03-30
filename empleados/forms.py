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

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        exclude = ("empleado_id","created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields['acumular_decimo_tercero'].label ="pagar decimo tercero"
        self.fields['acumular_fondo_reserva'].label = "pagar fondo reserva"
        self.fields['acumular_decimo_cuarto'].label= "pagar decimo cuarto"
        self.fields['acumular_iess_asumido'].label= "pagar iess asumido"
        self.fields['asumir_impuesto_renta'].label= "Asumir impuesto a la renta"

class TipoEmpleadoForm(ModelForm):
    class Meta:
        model = TipoEmpleado
        exclude = ("tipo_empleado_id","created_at","updated_at","created_by","updated_by")

class VendedorForm(ModelForm):
    class Meta:
        model = Vendedor
        exclude = ("vendedor_id","created_at","updated_at","created_by","updated_by")

class ChoferForm(ModelForm):
    class Meta:
        model = Chofer
        exclude = ("chofer_id","created_at","updated_at","created_by","updated_by")

class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ("vehiculo_id","created_at","updated_at","created_by","updated_by")

class DepartamentoForm(ModelForm):
    class Meta:
        model = Departamento
        exclude = ("created_at","updated_at","created_by","updated_by")



class TipoContratoForm(ModelForm):
    class Meta:
        model = TipoContrato
        exclude = ("created_at","updated_at","created_by","updated_by")



class GrupoPagoForm(ModelForm):
    class Meta:
        model = GrupoPago
        exclude = ("created_at","updated_at","created_by","updated_by")
