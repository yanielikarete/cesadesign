# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from login.middlewares import ThreadLocal
from .models import *
from os import path
from django.views.generic import TemplateView
from django.shortcuts import render_to_response,render

from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse,reverse_lazy
from .models import *


# -*- encoding: utf-8 -*-

from django.http import Http404
from django.contrib import messages
import simplejson as json
import datetime
from django.template import RequestContext, loader

from login.lib.tools import Tools

from config.models import Mensajes
from django.forms.extras.widgets import *
from django.contrib import auth
from django.contrib.auth import authenticate,login


class ReunionForm(forms.ModelForm):
    activo = models.BooleanField(default=False)
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = Reunion
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo","fecha","cliente","motivo","vendedor","observacion","tiempo_respuesta","observacion_tiempo_respuesta","created_by","updated_by","created_at","updated_at","respuesta_bodega","bodega","finalizado_bodega","direccion")
        widgets = {
            'observacion': Textarea(attrs={'cols': 100, 'rows': 8}),
            'observacion_tiempo_respuesta': Textarea(attrs={'cols': 5, 'rows': 8}),
        }
    def __init__(self, *args, **kwargs):
        super(ReunionForm, self).__init__(*args, **kwargs)

class ImagenesReunionForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = ImagenesReunion
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        exclude = ("created_by","created_at","updated_by","updated_at")
        widgets = {
            'descripcion': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
    def __init__(self, *args, **kwargs):
        super(ImagenesReunionForm, self).__init__(*args, **kwargs)

class ReunionActualizarView(TemplateView):

    def get(self, request, *args, **kwargs):
        
        reunion = Reunion.objects.get(id=kwargs['pk'])
        reunion_form=ReunionForm(instance=reunion)  

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'reunion_form':reunion_form,
      
        }

        return render_to_response(
            'reunion/actualizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        reunion = Reunion.objects.get(id=kwargs['pk'])
        reunion_form = ReunionForm(request.POST,request.FILES,instance=reunion)
        p_id=kwargs['pk']
        print(p_id)
        print reunion_form.is_valid(), reunion_form.errors, type(reunion_form.errors)

        if reunion_form.is_valid() :
            
            reunion.updated_by = request.user.get_full_name()
            reunion.updated_at = datetime.datetime.now()
            new_reunion=reunion.save()
            #new_reunion.save()
            context = {
           'section_title':'Actualizar Reunion',
            'button_text':'Actualizar',
            'reunion_form':reunion_form,
            'mensaje':'Reunion actualizada con exito'}


            return render_to_response(
                'reunion/actualizar.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            reunion_form=ReunionForm(request.POST)
            
            context = {
            'section_title':'Actualizar Reunion',
            'button_text':'Actualizar',
            'reunion_form':reunion_form,
           
            'mensaje':'Reunion actualizada con exito'}

        return render_to_response(
            'reunion/actualizar.html', 
            context,
            context_instance=RequestContext(request))

class RespuestaReunionBodegaView(TemplateView):

    def get(self, request, *args, **kwargs):
        
        reunion = Reunion.objects.get(id=kwargs['pk'])
        reunion_form=ReunionForm(instance=reunion)  

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'reunion_form':reunion_form,
      
        }

        return render_to_response(
            'reunion/respuesta_bodega.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        reunion = Reunion.objects.get(id=kwargs['pk'])
        reunion_form = ReunionForm(request.POST,request.FILES,instance=reunion)
        p_id=kwargs['pk']
        print(p_id)
        print reunion_form.is_valid(), reunion_form.errors, type(reunion_form.errors)

        if reunion_form.is_valid() :
            
            reunion.updated_by = request.user.get_full_name()
            reunion.updated_at = datetime.datetime.now()
            new_reunion=reunion.save()
            #new_reunion.save()
            context = {
           'section_title':'Actualizar Reunion',
            'button_text':'Actualizar',
            'reunion_form':reunion_form,
            'mensaje':'Reunion actualizada con exito'}


            return render_to_response(
                'reunion/respuesta_bodega.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            reunion_form=ReunionForm(request.POST)
            
            context = {
            'section_title':'Actualizar Reunion',
            'button_text':'Actualizar',
            'reunion_form':reunion_form,
           
            'mensaje':'Reunion actualizada con exito'}

        return render_to_response(
            'reunion/respuesta_bodega.html', 
            context,
            context_instance=RequestContext(request))
