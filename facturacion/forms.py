# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from login.middlewares import ThreadLocal
from .models import *
from os import path
from django.views.generic import TemplateView
from django.contrib.admin.widgets import AdminDateWidget 

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.admin import widgets
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import *
import datetime
import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm, Form

class GuiaRemisionForm(ModelForm):
	class Meta:
		model = GuiaRemision
		widgets = {
            'tipo_guia': forms.RadioSelect(),
        }
		exclude = ("guia_id", "created_at", "updated_at","created_by","updated_by")

	def __init__(self, *args, **kwargs):
		super(GuiaRemisionForm, self).__init__(*args, **kwargs)
		self.fields['tipo_guia'].empty_label = None

class GuiaDetalleForm(object):
	class Meta:
		model = GuiaDetalle
		exclude = ("detalle_id", "guia_id")


# class FacturaForm(ModelForm):
# 
# 	class Meta:
# 		model = Factura
# 		widgets = {
# 		'fecha': forms.DateInput(format='%d-%m-%Y'),
#         }
# 
# 		exclude = ("created_at", "updated_at","created_by","updated_by")
# 
# 	def __init__(self, *args, **kwargs):
# 		super(FacturaForm, self).__init__(*args, **kwargs)
# 		
# 
# class NotaCreditoForm(ModelForm):
# 
# 	class Meta:
# 		model = NotaCredito
# 		widgets = {
#         }
# 
# 		exclude = ("created_at", "updated_at","created_by","updated_by")
# 
# 	def __init__(self, *args, **kwargs):
# 		super(NotaCreditoForm, self).__init__(*args, **kwargs)
# 		

class RegistrarCobroPagoForm(ModelForm):

	class Meta:
		model = RegistrarCobroPago
		widgets = {
        }

		exclude = ("created_at", "updated_at","created_by","updated_by")

	def __init__(self, *args, **kwargs):
		super(RegistrarCobroPagoForm, self).__init__(*args, **kwargs)


class CruceDocumentoForm(ModelForm):

	class Meta:
		model = CruceDocumento
		widgets = {
        }

		exclude = ("created_at", "updated_at","created_by","updated_by")

	def __init__(self, *args, **kwargs):
		super(CruceDocumentoForm, self).__init__(*args, **kwargs)
		
		
		
class TipoGuiasForm(ModelForm):
	class Meta:
		model = TipoGuia
		
		exclude = ("created_at", "updated_at","created_by","updated_by")

	def __init__(self, *args, **kwargs):
		super(TipoGuiasForm, self).__init__(*args, **kwargs)
		