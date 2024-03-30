# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
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

class OrdenServicioForm(ModelForm):
	pedido_codigo = forms.CharField(required=False)
	orden_produccion_codigo = forms.CharField(required=False)
	guia_remision_codigo = forms.CharField(required=False)
	class Meta:
		model = OrdenServicio
		widgets = {
			'novedades': Textarea(attrs={'cols': 100, 'rows': 8}),
			'reporte_visita': Textarea(attrs={'cols': 5, 'rows': 8}),
			'trabajos_realizar': Textarea(attrs={'cols': 5, 'rows': 8}),
			'observaciones': Textarea(attrs={'cols': 5, 'rows': 8}),
		}
		exclude = ("orden_id","created_at","updated_at","created_by","updated_by")