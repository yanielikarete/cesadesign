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



class ProformaForm(ModelForm):

    class Meta:
        model = Proforma
        widgets = {
            'descripcion': Textarea(attrs={'cols': 5, 'rows': 8}),
            'tipo_lugar': forms.RadioSelect(),
            'fecha': forms.DateInput(attrs={'readonly': 'readonly'}),
            'fechapedido': forms.DateInput(attrs={'readonly': 'readonly'}),
        }
        exclude = ("created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(ProformaForm, self).__init__(*args, **kwargs)
        self.fields['maqueteado_proforma'].label= ""
        self.fields['tipo_lugar'].empty_label = None
        self.fields['hierro_proforma'].label= "Hierro"


class ProformaFacturaForm(ModelForm):

    class Meta:
        model = ProformaFactura
        widgets = {
            'descripcion': Textarea(attrs={'cols': 5, 'rows': 8}),
            'tipo_lugar': forms.RadioSelect(),
            'fecha': forms.DateInput(format='%d-%m-%Y'),
        }
        
        exclude = ("created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(ProformaFacturaForm, self).__init__(*args, **kwargs)
        self.fields['maqueteado_proforma'].label= ""
        self.fields['tipo_lugar'].empty_label = None
        self.fields['hierro_proforma'].label= "Hierro"

class CotizacionProformaForm(ModelForm):

    class Meta:
        model = CotizacionProforma
        widgets = {
            'descripcion': Textarea(attrs={'cols': 5, 'rows': 8}),
            'tipo_lugar': forms.RadioSelect(),
            'fecha': forms.DateInput(attrs={'readonly':'readonly'}),
            'fechapedido': forms.DateInput(attrs={'readonly': 'readonly'}),
        }
        exclude = ("created_at","updated_at","created_by","updated_by")

    def __init__(self, *args, **kwargs):
        super(CotizacionProformaForm, self).__init__(*args, **kwargs)
        self.fields['maqueteado_proforma'].label= "Renderizar"
        self.fields['tipo_lugar'].empty_label = None

class ImagenesCotizacionProformaForm(ModelForm):

    class Meta:
        model = ImagenesCotizacionProforma

    def __init__(self, *args, **kwargs):
        super(ImagenesCotizacionProformaForm, self).__init__(*args, **kwargs)

class ProformaRenderView(TemplateView):

    def get(self, request, *args, **kwargs):
        
        proforma = Proforma.objects.get(id=kwargs['pk'])
        productos = Producto.objects.all()
        proforma_form=ProformaForm(instance=proforma)  
        detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id).order_by('id')

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'detalle':detalle
        }

        return render_to_response(
            'proforma/subir_render.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = Proforma.objects.get(id=kwargs['pk'])
        proforma_form = ProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = Producto.objects.all()

        if proforma_form.is_valid() :
            
            proforma.save()

            new_orden=proforma.save()

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
	                        detallecompra = ProformaDetalle.objects.get(id=detalle_id)
	                        detallecompra.updated_by = request.user.get_full_name()
	                        detallecompra.producto =product
                            detallecompra.largo=request.POST["largo_kits"+str(i)]
                            detallecompra.fondo=request.POST["fondo_kits"+str(i)]
                            detallecompra.alto=request.POST["alto_kits"+str(i)]
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.save()
                        else:
	                        comprasdetalle=ProformaDetalle()
	                        comprasdetalle.proforma_id = new_orden.id
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
            detalle = ProformaDetalle.objects.filter(proforma_id=p_id)
            productos = Producto.objects.all()

           
            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'proforma/subir_render.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            proforma_form=ProformaForm(request.POST)
            detalle = ProformaDetalle.objects.filter(proforma_id=proforma.id).order_by('id')
            productos = Producto.objects.all()

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'proforma/subir_render.html', 
            context,
            context_instance=RequestContext(request))



class CotizacionProformaRenderView(TemplateView):

    def get(self, request, *args, **kwargs):
        
        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        productos = ProductoGeneral.objects.all().order_by('descripcion')
        proforma_form=CotizacionProformaForm(instance=proforma)  
        detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':proforma_form,
        'productos':productos,
        'detalle':detalle
        }

        return render_to_response(
            'cotizacionproforma/subir_render.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        proforma = CotizacionProforma.objects.get(id=kwargs['pk'])
        proforma_form = CotizacionProformaForm(request.POST,request.FILES,instance=proforma)
        p_id=kwargs['pk']
        print(p_id)
        print proforma_form.is_valid(), proforma_form.errors, type(proforma_form.errors)
        productos = ProductoGeneral.objects.all().order_by('descripcion')

        if proforma_form.is_valid() :
            
            proforma.save()

            new_orden=proforma.save()

            contador=request.POST["columnas_receta"]
           
            i=0
            while int(i) <= int(contador):
                i+= 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=ProductoGeneral.objects.get(id=request.POST["id_kits"+str(i)])
                        detalle_id=request.POST["id_detalle"+str(i)]

                        if detalle_id:
                            detallecompra = CotizacionProformaDetalle.objects.get(id=detalle_id)
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.producto_general=product
                            detallecompra.observaciones=request.POST["observacion_kits"+str(i)]
                            detallecompra.save()
                        else:
                            comprasdetalle=CotizacionProformaDetalle()
                            comprasdetalle.cotizacion_proforma_id = new_orden.id
                            comprasdetalle.producto_general=product
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
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=p_id)
            productos = Producto.objects.all()

           
            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'productos':productos,
            'mensaje':'Proforma actualizada con exito'}


            return render_to_response(
                'cotizacionproforma/subir_render.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            proforma_form=CotizacionProformaForm(request.POST)
            detalle = CotizacionProformaDetalle.objects.filter(cotizacion_proforma_id=proforma.id).order_by('id')
            productos = ProductoGeneral.objects.all().order_by('descripcion')

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':proforma_form,
            'detalle':detalle,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'cotizacionproforma/subir_render.html', 
            context,
            context_instance=RequestContext(request))


