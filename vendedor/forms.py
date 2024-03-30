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



class VendedoresForm(forms.ModelForm):
    activo = models.BooleanField(default=False)
    externo = models.BooleanField(default=False)
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = Vendedor
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo","nombre","activo","externo")

    def __init__(self, *args, **kwargs):
        super(VendedoresForm, self).__init__(*args, **kwargs)
