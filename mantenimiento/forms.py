from django import forms
from .models import *
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

class RetencionForm(forms.ModelForm):
    class Meta:
        model = Retenciones

    def __init__(self, *args, **kwargs):
        super(RetencionForm, self).__init__(*args, **kwargs)
        self.fields['cuenta'].queryset = PlanDeCuentas.objects.filter(categoria="DETALLE", activo=True)

class PagosForm(forms.ModelForm):
    class Meta:
        model = FormaPago

    def __init__(self, *args, **kwargs):
        super(PagosForm, self).__init__(*args, **kwargs)

class SustentoTributarioForm(forms.ModelForm):
    class Meta:
        model = SustentoTributario

    def __init__(self, *args, **kwargs):
        super(SustentoTributarioForm, self).__init__(*args, **kwargs)