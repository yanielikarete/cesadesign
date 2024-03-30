# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from login.middlewares import ThreadLocal
from .models import *
from os import path
from django.views.generic import TemplateView
from django.shortcuts import render_to_response

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .models import *



class RolPagoCuentaContableForm(ModelForm):

    class Meta:
        model = RolPagoCuentaContable
        exclude = ("created_at","updated_at","created_by","updated_by")
class PrestamoForm(ModelForm):

    class Meta:
        model = Prestamo
        exclude = ("created_at","updated_at","created_by","updated_by")

class AnalisisPrestamoForm(ModelForm):

    class Meta:
        model = AnalisisPrestamo
        exclude = ("created_at","updated_at","created_by","updated_by")

class PlantillaRrhhForm(ModelForm):

    class Meta:
        model = PlantillaRrhh
        exclude = ("created_at","updated_at","created_by","updated_by")

class TipoSolicitudForm(ModelForm):

    class Meta:
        model = TipoSolicitud
        exclude = ("created_at","updated_at","created_by","updated_by")
        widgets = {
            'codigo': forms.TextInput(
                attrs={'id': 'codigo', 'required': True, 'placeholder': 'Código'}
            ),
            'descripcion': forms.TextInput(
                attrs={'id': 'descripcion', 'required': True, 'placeholder': 'Ingrese una descripción'}
            ),
        }

class PermisoForm(ModelForm):

    class Meta:
        model = Permiso
        exclude = ("created_at","updated_at","created_by","updated_by")



class DiasFeriadosForm(ModelForm):

    class Meta:
        model = DiasFeriados
        exclude = ("created_at","updated_at","created_by","updated_by")


class TipoIngresoEgresoForm(ModelForm):

    class Meta:
        model = TipoIngresoEgresoEmpleado
        exclude = ("created_at","updated_at","created_by","updated_by")

class LiquidacionLaboralForm(ModelForm):

    class Meta:
        model = LiquidacionLaboral
        exclude = ("created_at","updated_at","created_by","updated_by")

class LiquidacionVacacionesForm(ModelForm):

    class Meta:
        model = LiquidacionVacaciones
        exclude = ("created_at","updated_at","created_by","updated_by")

class VacacionesForm(ModelForm):

    class Meta:
        model = Vacaciones
        exclude = ("created_at","updated_at","created_by","updated_by")


class RolCuentacontableTipoingresoegresoForm(ModelForm):

    class Meta:
        model = RolCuentacontableTipoingresoegreso
        exclude = ("created_at","updated_at","created_by","updated_by")

class RolCuentacontableItemsForm(ModelForm):

    class Meta:
        model = RolCuentacontableItems
        exclude = ("created_at","updated_at","created_by","updated_by")
        
        
class DeudasEmpleadoForm(ModelForm):

    class Meta:
        model = DeudasEmpleado
        exclude = ("created_at","updated_at","created_by","updated_by")
        
class SueldosUnificadosForm(ModelForm):

    class Meta:
        model = SueldosUnificados
        exclude = ("created_at","updated_at","created_by","updated_by")
