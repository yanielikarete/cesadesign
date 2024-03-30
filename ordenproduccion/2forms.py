# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm,Textarea,DateField,DateTimeField
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
import datetime



class OrdenProduccionForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())
   
    class Meta:
        model = OrdenProduccion
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza

        fields = ("codigo","fecha","cliente","descripcion","detalle","cantidad","fondo","largo","alto","madera","vidrio","hierro","marmol","enchape","enchape_detalle","tallado","tallado_detalle","tono","corredizo","oleo","conchaperla","tela_almacen","tela_cliente","agarraderas","imagen","guia","adicional","fechapedido","tipo","estado","tipo_mueb","doc","mate","semimate","brillante","pulido","aluminio","acero","abrillantado","pintado","satinado","fechacotizacion","engrampe","impulso","poroabierto","ingreso","cantaux","vendedor","tiempo_respuesta","fuera_ciudad","observacion","forma_pago","ambiente","maqueteado_proforma","terminado_maqueteado_proforma","pedido_codigo","pedido","total","codigo_item","profundidad","ancho","patina_color","retractil","pintado_mano","cuero_almacen","cuero_cliente","fechainicio","fechaentrega","created_at","created_by","updated_at","updated_by","metal_hierro","imagen_global","neumatico","venta_local","exportacion","acero_brillante","semiabierto","polyester","garantia","total","producto_creado")
        widgets = {
            'detalle': Textarea(attrs={'cols': 100, 'rows': 3}),
            'descripcion': Textarea(attrs={'cols': 50, 'rows': 1}),



        }
    def __init__(self, *args, **kwargs):
        super(OrdenProduccionForm, self).__init__(*args, **kwargs)

class RopForm(forms.ModelForm):
    #categoria = forms.ModelChoiceField(queryset=CategoriaProducto.objects.all())

    class Meta:
        model = Rop
        #cuenta_compra y cuenta_venta verificar donde se lo utiiza
        fields = ("codigo","fecha","cliente","descripcion","cantidad","fondo","largo","alto","madera","vidrio","hierro","marmol","enchape","enchape_detalle","tallado","tallado_detalle","tono","corredizo","oleo","conchaperla","tela_almacen","tela_cliente","agarraderas","imagen","guia","adicional","fechapedido","tipo","estado","tipo_mueb","doc","mate","semimate","brillante","pulido","aluminio","acero","abrillantado","pintado","satinado","fechacotizacion","engrampe","impulso","poroabierto","ingreso","cantaux","vendedor","tiempo_respuesta","fuera_ciudad","observacion","forma_pago","ambiente","total","codigo_item","profundidad","ancho","patina_color","retractil","pintado_mano","cuero_almacen","cuero_cliente","fechainicio","fechaentrega","created_at","created_by","updated_at","metal_hierro","detalle","codigo_orden_produccion","neumatico","venta_local","exportacion")
        widgets = {
            'detalle': Textarea(attrs={'cols': 100, 'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super(RopForm, self).__init__(*args, **kwargs)

