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
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.forms.extras.widgets import *
from django.core.validators import RegexValidator


class EjercicioContableForm(ModelForm):
    class Meta:
        model = EjercicioContable
        exclude = ("ejercicio_id", "created_at", "updated_at", "created_by", "updated_by")


class PlanDeCuentasForm(ModelForm):
    class Meta:
        model = PlanDeCuentas
        exclude = ("plan_id", "created_at", "updated_at", "created_by", "updated_by")


class TipoCuentaForm(ModelForm):
    class Meta:
        model = TipoCuenta
        exclude = ("tipo_id", "created_at", "updated_at", "created_by", "updated_by")


class CentroCostoForm(ModelForm):
    class Meta:
        model = CentroCosto
        exclude = ("centro_id", "created_at", "updated_at", "created_by", "updated_by")


class AsientoForm(ModelForm):
    class Meta:
        model = Asiento
        exclude = ("asiento_id", "created_at", "updated_at", "created_by", "updated_by","secuencia_asiento")
