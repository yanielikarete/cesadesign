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



class PedidoForm(ModelForm):

    class Meta:
        model = Pedido
        exclude = ("created_at","updated_at","created_by","updated_by")
        widgets = {
            'tipo_lugar': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_lugar'].empty_label = None

class ImagenesPedidoForm(ModelForm):

    class Meta:
        model = ImagenesPedido
        exclude = ("created_at", "updated_at", "created_by", "updated_by","pedido_detalle")

    def __init__(self, *args, **kwargs):
        super(ImagenesPedidoForm, self).__init__(*args, **kwargs)


class PedidoActualizarView(TemplateView):

    def get(self, request, *args, **kwargs):
        
        pedido = Pedido.objects.get(id=kwargs['pk'])
        productos = Producto.objects.all()
        pedido_form=PedidoForm(instance=pedido)  
        detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':pedido_form,
        'productos':productos,
        'detalle':detalle
        }

        return render_to_response(
            'pedido/actualizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        pedido = Pedido.objects.get(id=kwargs['pk'])
        pedido_form = PedidoForm(request.POST,request.FILES,instance=pedido)
        p_id=kwargs['pk']
        print(p_id)
        print pedido_form.is_valid(), pedido_form.errors, type(pedido_form.errors)
        productos = Producto.objects.all()

        if pedido_form.is_valid() :
            
            pedido.save()

            new_orden=pedido.save()

            contador=request.POST["columnas_receta"]
           
            i=0
            while int(i) <= int(contador):
              	i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                	if 'id_kits'+str(i) in request.POST:
	                    product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
	                    detalle_id=request.POST["id_detalle"+str(i)]

	                    if detalle_id:
	                        detallecompra = PedidoDetalle.objects.get(id=detalle_id)
	                        detallecompra.updated_by = request.user.get_full_name()
	                        detallecompra.producto =product
	                        detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
	                        detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
	                        detallecompra.total=request.POST["total_kits"+str(i)]
	                        #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
	                        detallecompra.medida=request.POST["medida_kits"+str(i)]
	                        detallecompra.observaciones=request.POST["observacion_kits"+str(i)]

	                        #detallecompra.updated_at = datetime.now()
	                        #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
	                        detallecompra.save()
	                        
	                        print('Tiene detalle'+str(i))
	                    else:
	                        comprasdetalle=PedidoDetalle()
	                        comprasdetalle.pedido_id = new_orden.id
	                        comprasdetalle.producto=product
	                        comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
	                        comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
	                        comprasdetalle.total=request.POST["total_kits"+str(i)]
	                        comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
	                        comprasdetalle.observaciones=request.POST["observacion_kits"+str(i)]

	                        comprasdetalle.save()
	                        i+= 1
	                        print('No Tiene detalle'+str(i))
	                        print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = PedidoDetalle.objects.filter(pedido_id=p_id)
            productos = Producto.objects.all()

           
            context = {
           'section_title':'Actualizar Pedido',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'productos':productos,
            'mensaje':'Pedido actualizada con exito'}


            return render_to_response(
                'pedido/actualizar.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            pedido_form=PedidoForm(request.POST)
            detalle = PedidoDetalle.objects.filter(pedido_id=pedido.id)
            productos = Producto.objects.all()

            context = {
            'section_title':'Actualizar Pedido',
            'button_text':'Actualizar',
            'form':pedido_form,
            'detalle':detalle,
            'mensaje':'Pedido actualizada con exito'}

        return render_to_response(
            'pedido/actualizar.html', 
            context,
            context_instance=RequestContext(request))



