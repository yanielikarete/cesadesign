# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, Textarea
from .models import *
from models import *
from proveedores.models import *
from os import path
from django.views.generic import TemplateView
from django.core.exceptions import NON_FIELD_ERRORS
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from .models import *
from django.shortcuts import render_to_response


class OrdenCompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(queryset=Proveedor.objects.order_by('nombre_proveedor'))

    class Meta:
        model = OrdenCompra
        fields = ("notas","fecha","nro_compra","proveedor","bodega","comentario","created_at","updated_at","created_by","updated_by","nro_fact_proveedor","total","subtotal","subtotal_descuento","dscto_pciento","dscto_monto","impuesto_pciento","impuesto_monto")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }
class ComprasDetalleForm(forms.ModelForm):
    class Meta:
        model = ComprasDetalle
        #compra_id,proveedor y fecha se guarda automaticamente de la orden de compra
        exclude = ("compra_id","fecha","proveedor","bodega","impto2_pciento","impto2_monto","tipo_cambio","moneda","created_at","updated_at","created_by","updated_by",)

# class OrdenCompraActualizarView(TemplateView):
#
#     def get(self, request, *args, **kwargs):
#
#         ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
#         productos = Producto.objects.all()
#         ordencompra_form=OrdenCompraForm(instance=ordencompra)
#         detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
#
#         context = {
#         'section_title':'Actualizar Presupuesto',
#         'button_text':'Actualizar',
#         'ordencompra_form':ordencompra_form,
#         'productos':productos,
#         'detalle':detalle
#         }
#         print('ENTROO')
#
#         return render_to_response(
#             'ordenescompra/actualizar.html', context,context_instance=RequestContext(request))
#
#     def post(sel, request, *args, **kwargs):
#         ordencompra = OrdenCompra.objects.get(compra_id=kwargs['pk'])
#         ordencompra_form = OrdenCompraForm(request.POST,request.FILES,instance=ordencompra)
#         p_id=kwargs['pk']
#         print(p_id)
#         print ordencompra_form.is_valid(), ordencompra_form.errors, type(ordencompra_form.errors)
#         productos = Producto.objects.all()
#         print('HOLAAAA')
#
#         if ordencompra_form.is_valid() :
#             ordencompra.comentario = ordencompra_form.cleaned_data['comentario']
#             ordencompra.proveedor = ordencompra_form.cleaned_data['proveedor']
#             ordencompra.notas = ordencompra_form.cleaned_data['notas']
#             ordencompra.bodega = ordencompra_form.cleaned_data['bodega']
#             ordencompra.subtotal = request.POST["total23"]
#             ordencompra.fecha = ordencompra_form.cleaned_data['fecha']
#             ordencompra.total = request.POST["total_g"]
#             ordencompra.dscto_pciento = request.POST["porcentaje_descuento"]
#             ordencompra.dscto_monto = request.POST["descuento"]
#             ordencompra.impuesto_pciento = request.POST["porcentaje_iva"]
#             ordencompra.subtotal_descuento = request.POST["subtotal_desc"]
#             ordencompra.impuesto_monto = request.POST["iva"]
#             print ('Tiene impto'+str(request.POST["iva"]))
#             #ordencompra.save()
#
#             new_orden=ordencompra.save()
#
#             contador=request.POST["columnas_receta"]
#
#             i=0
#             while int(i) <= int(contador):
#               	i+= 1
#                 if int(i) > int(contador):
#                     print('entrosd')
#                     break
#                 else:
#                 	if 'id_kits'+str(i) in request.POST:
# 	                    product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
# 	                    detalle_id=request.POST["id_detalle"+str(i)]
#
# 	                    if detalle_id:
# 	                        detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
# 	                        detallecompra.updated_by = request.user.get_full_name()
# 	                        detallecompra.producto =product
# 	                        detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
# 	                        detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
# 	                        detallecompra.total=request.POST["total_kits"+str(i)]
#                             detallecompra.tipo_precio= request.POST["tipo_precio_kits" + str(i)]
#                             detallecompra.updated_at = datetime.now()
#                             detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
#                             detallecompra.save()
#                             print('Tiene detalle'+str(i))
#                         else:
#                             comprasdetalle=ComprasDetalle()
#                             comprasdetalle.compra_id = new_orden.compra_id
#                             comprasdetalle.producto=product
#                             comprasdetalle.proveedor=new_orden.proveedor
#                             comprasdetalle.bodega=new_orden.bodega
#                             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
#                             comprasdetalle.tipo_precio= request.POST["tipo_precio_kits" + str(i)]
#                             comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
#                             comprasdetalle.total=request.POST["total_kits"+str(i)]
#                             comprasdetalle.save()
#                             i+= 1
#                             print('No Tiene detalle'+str(i))
#                             print('contadorsd prueba'+str(contador))
#             #ordencompra_form=OrdenCompraForm(request.POST)
#             detalle = ComprasDetalle.objects.filter(compra_id=p_id)
#             productos = Producto.objects.all()
#
#
#             context = {
#            'section_title':'Actualizar Orden Compra1',
#             'button_text':'Actualizar',
#             'ordencompra_form':ordencompra_form,
#             'detalle':detalle,
#             'productos':productos,
#             'mensaje':'Orden de Compra actualizada con exito'}
#
#
#             return render_to_response(
#                 'ordenescompra/actualizar.html',
#                 context,
#                 context_instance=RequestContext(request))
#         else:
#
#             ordencompra_form=OrdenCompraForm(request.POST)
#             detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)
#             productos = Producto.objects.all()
#
#             context = {
#             'section_title':'Actualizar Orden Compra2',
#             'button_text':'Actualizar',
#             'ordencompra_form':ordencompra_form,
#             'detalle':detalle,
#             'mensaje':'Orden de Compra actualizada con exito'}
#
#         return render_to_response(
#             'ordenescompra/actualizar.html',
#             context,
#             context_instance=RequestContext(request))


class ComprasLocalesForm(forms.ModelForm):
    class Meta:
        model = ComprasLocales
        fields = ("codigo","fecha","orden_compra","proveedor","comentario","created_at","updated_at","created_by","updated_by","nro_fact_proveedor","total")
        widgets = {
            'comentario': Textarea(attrs={'cols': 100, 'rows': 8}),
        }