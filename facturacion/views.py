from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView
from django.core.urlresolvers import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render,render_to_response
from django.contrib import messages
import simplejson as json
from .models import *
from .forms import *
from .tables import *
from .filters import *
from clientes.models import *
from django.views.generic import TemplateView
from django import forms
from models import *
from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
from inventario.tables import *
#from login.lib.tools import Tools
from inventario.models import *
from config.models import *
from proforma.models import *
from recursos_humanos.models import *
from subordenproduccion.models import OrdenProduccionBodega



# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes

from login.lib.tools import Tools

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.contrib import messages
import simplejson as json
import datetime
from .models import *
from clientes.models import *
from .forms import *
from ambiente.models import *

from .tables import *
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from inventario.models import *
from django.db import connection, transaction
from reunion.models import *
from config.models import *
from django.views.generic import TemplateView

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate,login
#from login.lib.tools import Tools


import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db import transaction, DatabaseError

#from config.models import Mensajes

import pyodbc

from login.lib.tools import Tools
from django.contrib import auth

# Create your views here.

#=========================GuiaRemision============================#
@login_required()
def GuiaRemisionListView(request):
    guias = GuiaRemision.objects.all()
    template = loader.get_template('guiaremision/index.html')
    context = RequestContext(request, {'guias': guias})
    return HttpResponse(template.render(context))







class GuiaRemisionDetailView(ObjectDetailView):
    model = GuiaRemision
    template_name = 'guiaremision/detail.html'


# def GuiaRemisionCreateView(request):
#     if request.method == 'POST':
#         guiaremision_form = GuiaRemisionForm(request.POST)
#         detalle_form = GuiaDetalleForm(request.POST)

#         if guiaremision_form.is_valid() and detalle_form.is_valid():
#             new_guia=guiaremision_form.save()
#             detalle_form.save()
#             detalle_form.guia_id=new_guia
#             detalle_form.save()
#             return HttpResponseRedirect('guiaremision/')
#     else:
#         guiaremision_form=GuiaRemisionForm
#         detalle_form=GuiaDetalleForm
#     return render_to_response('guiaremision/create.html', { 'guiaremision_form': guiaremision_form,  'detalle_form': detalle_form },  RequestContext(request))

@transaction.atomic
def GuiaRemisionCreateView(request):
    puntos_venta = ''
    if request.method == 'POST':
        guiaremision_form=GuiaRemisionForm(request.POST)


        if guiaremision_form.is_valid():
            with transaction.atomic():
                new_guia=guiaremision_form.save()
                new_guia.activo=True
                new_guia.created_by = request.user.get_full_name()
                new_guia.updated_by = request.user.get_full_name()
                new_guia.created_at = datetime.now()
                new_guia.updated_at = datetime.now()
                new_guia.total=request.POST["total"]
                new_guia.puntos_venta_id=request.POST["punto_venta_descripcion"]

                new_guia.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='guiaremision')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None
                    
                    
                try:
                    pv = PuntosVenta.objects.get(id=new_guia.puntos_venta_id)
                    sec=pv.secuencial_guia_electronica+1
                    pv.secuencial_guia_electronica=sec
                    
                    pv.save()
                except PuntosVenta.DoesNotExist:
                    pv = None

                contador=request.POST["columnas_receta"]
                print contador
                i=0
                while int(i)<=int(contador):
                    i+= 1
                    print('entro comoqw'+str(i))
                    if int(i)> int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits'+str(i) in request.POST:
                            product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                            guiasdetalle=GuiaDetalle()
                            guiasdetalle.guia = new_guia
                            guiasdetalle.producto=Producto.objects.get(pk=request.POST["id_kits"+str(i)])
                            guiasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            guiasdetalle.precio_compra=request.POST["valor_kits"+str(i)]
                            guiasdetalle.total=request.POST["total_kits"+str(i)]
                            guiasdetalle.descripcion = request.POST["descripcion_kits" + str(i)]
                            guiasdetalle.bodega_id = request.POST["bodega_kits" + str(i)]
                            guiasdetalle.nro_documento = request.POST["documento_kits" + str(i)]
                            guiasdetalle.save()

                    print(i)
                    print('contadorsd prueba'+str(contador))

                return HttpResponseRedirect('/facturacion/guiaremision')
        else:
            print 'error'
            print guiaremision_form.errors, len(guiaremision_form.errors)
    else:
        guiaremision_form=GuiaRemisionForm
        puntos_venta = PuntosVenta.objects.all().order_by('id')

    return render_to_response('guiaremision/create.html', { 'guiaremision_form': guiaremision_form,'puntos_venta': puntos_venta,},  RequestContext(request))


@transaction.atomic
def GuiaRemisionUpdateView(request,pk):
    if request.method == 'POST':
        guiaremision=GuiaRemision.objects.get(guia_id=pk)
        guiaremision_form=GuiaRemisionForm(request.POST,request.FILES,instance=guiaremision)
        print guiaremision_form.is_valid(), guiaremision_form.errors, type(guiaremision_form.errors)

        if guiaremision_form.is_valid():
            with transaction.atomic():
                guia=guiaremision_form.save()
                guia.updated_by = request.user.get_full_name()
                guia.updated_at = datetime.now()
                guia.total=request.POST["total"]
                guia.save()

                contador = request.POST["columnas_receta"]
                print contador
                i = 0
                while int(i) <= int(contador):
                    i += 1
                    print('entro comoqw' + str(i))
                    if int(i) > int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits' + str(i) in request.POST:
                            if 'id_detalle' + str(i) in request.POST:
                                product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                                id=request.POST["id_detalle" + str(i)]
                                guiasdetalle = GuiaDetalle.objects.get(detalle_id=id)
                                guiasdetalle.producto = Producto.objects.get(pk=request.POST["id_kits" + str(i)])
                                guiasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                                guiasdetalle.precio_compra=request.POST["valor_kits"+str(i)]
                                guiasdetalle.total=request.POST["total_kits"+str(i)]

                                guiasdetalle.descripcion = request.POST["descripcion_kits" + str(i)]
                                # if 'bodega_kits' + str(i) in request.POST:
                                #     guiasdetalle.bodega_id = request.POST["bodega_kits" + str(i)]
                                guiasdetalle.bodega_id = guiaremision.bodega.id
                                guiasdetalle.nro_documento = request.POST["documento_kits" + str(i)]
                                guiasdetalle.save()
                            else:
                                product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                                guiasdetalle = GuiaDetalle()
                                guiasdetalle.guia_id=guia.guia_id
                                guiasdetalle.producto = Producto.objects.get(pk=request.POST["id_kits" + str(i)])
                                guiasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                                guiasdetalle.descripcion = request.POST["descripcion_kits" + str(i)]
                                guiasdetalle.precio_compra=request.POST["valor_kits"+str(i)]
                                guiasdetalle.total=request.POST["total_kits"+str(i)]
                                # if 'bodega_kits' + str(i) in request.POST:
                                #     guiasdetalle.bodega_id = request.POST["bodega_kits" + str(i)]
                                guiasdetalle.bodega_id = guiaremision.bodega.id
                                guiasdetalle.nro_documento = request.POST["documento_kits" + str(i)]
                                guiasdetalle.save()


            return HttpResponseRedirect('/facturacion/guiaremision')
        else:
    
            guiaremision_form=GuiaRemisionForm(request.POST)
            detalle = GuiaDetalle.objects.filter(guia_id=guiaremision.guia_id)
           
            context = {
            'section_title':'Actualizar Guia Remision',
            'button_text':'Actualizar',
            'guiaremision_form':guiaremision_form,
            'detalle':detalle }

        return render_to_response(
            'guiaremision/factura.html', 
            context,
            context_instance=RequestContext(request))
    else:
        guiaremision=GuiaRemision.objects.get(guia_id=pk)
        guiaremision_form=GuiaRemisionForm(instance=guiaremision)
        detalle = GuiaDetalle.objects.filter(guia_id=guiaremision.guia_id)
           
        context = {
            'section_title':'Actualizar Guia Remision',
            'button_text':'Actualizar',
            'guiaremision_form':guiaremision_form,
            'guiaremision':guiaremision,
            
            'detalle':detalle }

        return render_to_response(
            'guiaremision/factura.html', 
            context,
            context_instance=RequestContext(request))


#=====================================================#
@login_required()
def guiaremisionEliminarView(request):
    return eliminarView(request, Empleado, 'guiaremision-list')

#=====================================================#
@login_required()
def guiaremisionEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Empleado)

def GuiaRemisionCrearProformaView(request,pk):
    if request.method == 'POST':
        guiaremision_form=GuiaRemisionForm(request.POST)
        productos = Producto.objects.all()
        proformas = Proforma.objects.filter(aprobada=True)

        if guiaremision_form.is_valid():
            new_guia=guiaremision_form.save()
            new_guia.created_by = request.user.get_full_name()
            new_guia.updated_by = request.user.get_full_name()
            new_guia.created_at = datetime.now()
            new_guia.updated_at = datetime.now()

            new_guia.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='guiaremision')
                secuencial.secuencial=secuencial.secuencial+1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            contador=request.POST["columnas_receta"]
            print contador
            i=0
            while int(i)<=int(contador):
                i+= 1
                print('entro comoqw'+str(i))
                if int(i)> int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits'+str(i) in request.POST:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        guiasdetalle=GuiaDetalle()
                        guiasdetalle.guia_id = new_guia
                        guiasdetalle.producto_id=Producto.objects.get(pk=request.POST["id_kits"+str(i)])
                        guiasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                        guiasdetalle.save()
                
                print(i)
                print('contadorsd prueba'+str(contador))

            return HttpResponseRedirect('/facturacion/guiaremision')
        else:
            print 'error'
            print guiaremision_form.errors, len(guiaremision_form.errors)
    else:
        guiaremision_form=GuiaRemisionForm
        productos = Producto.objects.all()
        proformas = Proforma.objects.filter(aprobada=True)
        proforma_selec = Proforma.objects.get(id = pk)
        detalle_proforma = ProformaDetalle.objects.filter(proforma_id = pk)
    return render_to_response('guiaremision/proforma-create.html', { 'guiaremision_form': guiaremision_form,'productos':productos,'proformas':proformas,'detalle_proforma':detalle_proforma,'proforma_selec':proforma_selec},  RequestContext(request))

@csrf_exempt
def obtenerTipo(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
     

        objetos = TipoGuia.objects.get(id = modulo)
        
        modulo_secuencial = objetos.accion

        return HttpResponse(
                modulo_secuencial
            )
    else:
        raise Http404

@login_required()
def GuiaremisionListAprobarView(request):
    guias = GuiaRemision.objects.exclude(activo=False)
    template = loader.get_template('guiaremision/aprobada.html')
    context = RequestContext(request, {'guias': guias})
    return HttpResponse(template.render(context))

@login_required()
def GuiaRemisionAprobarByPkView(request, pk):

    objetos = GuiaRemision.objects.get(guia_id= pk)
    objetos.aprobada = True
    objetos.save()
    obj = GuiaDetalle.objects.filter(guia_id= pk)
    bodega_id=3
    if objetos.puntos_venta_id == 2:
        bodega_id=7
    if objetos.puntos_venta_id == 3:
        bodega_id=8
    print('bodega'+str(bodega_id))
    print('puntos_venta'+str(objetos.puntos_venta_id))

    for o in obj:
        k=Kardex()
        k.nro_documento =objetos.nro_guia
        k.producto_id=o.producto_id
        k.cantidad=o.cantidad
        if objetos.egreso:
            k.descripcion='Orden de Egreso por Guia Remision'
            k.fecha_egreso=datetime.now()

        else:
            k.descripcion='Orden de Ingreso por Guia Remision'
            k.fecha_ingreso=datetime.now()
        k.bodega_id=bodega_id
        k.modulo=objetos.guia_id
        k.cliente_id=objetos.cliente_id
        k.save()
        try:
            objetose = ProductoEnBodega.objects.get(producto_id= o.producto_id,bodega_id=bodega_id)
        except ProductoEnBodega.DoesNotExist:
            objetose = None
            
        if objetose:
            cant=objetose.cantidad
            if objetos.egreso:
                objetose.cantidad=cant-float(o.cantidad)
            else:
                objetose.cantidad=cant+float(o.cantidad)

            objetose.updated_at = datetime.now()
            objetose.updated_by = request.user.get_full_name()
            objetose.save()
        else:
            f=ProductoEnBodega()
            f.producto_id=o.producto_id
            f.bodega_id=bodega_id
            cant=0
            if objetos.egreso:
                f.cantidad=cant-float(o.cantidad)
            else:
                f.cantidad=cant+float(o.cantidad)

            f.updated_at = datetime.now()
            f.updated_by = request.user.get_full_name()
            f.save()

        if objetos.tipo_guia_id == 1:
            try:
                objetospb = OrdenProduccionBodega.objects.get(id=o.nro_documento)
            except OrdenProduccionBodega.DoesNotExist:
                objetospb = None

            if objetospb:
                cant_recibida=objetospb.cantidad_recibida
                if objetospb.cantidad_sobrante:
                    cant_sobrante=objetospb.cantidad_sobrante
                else:
                    cant_sobrante=objetospb.cantidad_recibida

                if objetospb.cantidad_despachada:
                    cant_dep = objetospb.cantidad_despachada
                else:
                    cant_dep=0

                cant_total=float(cant_sobrante)-float(o.cantidad)
                cant_total_des = float(cant_dep)+ float(o.cantidad)
                objetospb.cantidad_despachada=cant_total_des
                objetospb.cantidad_sobrante = cant_total
                objetospb.save()
            
                
        try:
            tipos = TipoGuia.objects.get(id=objetos.tipo_guia_id)
        except TipoGuia.DoesNotExist:
            tipos = None
        if tipos:
            if tipos.cuenta_contable_acreedora:
                codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                asiento = Asiento()
                asiento.codigo_asiento = "GR" + str(datetime.now().year) + "000" + str(codigo_asiento)
                asiento.fecha = datetime.now()
                asiento.glosa = 'GUIA DE REMISION POR '+str( tipos.descripcion)+ ' NO.' + str(objetos.nro_guia)
                asiento.modulo= 'Guia de Remision'
                asiento.gasto_no_deducible = False
                asiento.save()
                objetos.asiento_id=asiento.asiento_id
                objetos.save()
        
                Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
                try:
                    plan_deudora = PlanDeCuentas.objects.get(plan_id=tipos.cuenta_contable_deudora_id)
                except PlanDeCuentas.DoesNotExist:
                    plan_deudora = None
                if plan_deudora:
                    asiento_detalle = AsientoDetalle()
                    asiento_detalle.asiento_id = int(asiento.asiento_id)
                    asiento_detalle.cuenta_id = plan_deudora.plan_id
                    asiento_detalle.debe = objetos.total
                    asiento_detalle.haber = 0
                    asiento_detalle.save()
        
                try:
                    plan_acreedora = PlanDeCuentas.objects.get(plan_id=tipos.cuenta_contable_acreedora_id)
        
        
                except PlanDeCuentas.DoesNotExist:
                    plan_acreedora = None
                if plan_acreedora:
                    asiento_detalle = AsientoDetalle()
                    asiento_detalle.asiento_id = int(asiento.asiento_id)
                    asiento_detalle.cuenta_id = plan_acreedora.plan_id
                    asiento_detalle.debe = 0
                    asiento_detalle.haber = objetos.total
                    asiento_detalle.save()

    return HttpResponseRedirect('/facturacion/guiaremisionAprobar')
@csrf_exempt
def obtenerDetalleGuia(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
     

        detalle = GuiaDetalle.objects.filter(guia_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id)

            html+='<tr><td>'+product.codigo_producto+'</td>'
            html+='<td>'+str(product.descripcion_producto)+'</td>'
            html+='<td>'+str(detal.cantidad)+'</td>'

        return HttpResponse(
                html
            )
    else:
        raise Http404
@login_required()
def GuiaremisionAnularByPkView(request, pk):

    objetos = GuiaRemision.objects.filter(guia_id= pk)
    for obj in objetos:
        obj.anulada= True
        obj.activo= False
        obj.save()
    
    return HttpResponseRedirect('/facturacion/guiaremisionAprobar')


@csrf_exempt
def obtenerDetalleProformaFactura(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = ProformaDetalle.objects.get(id = codigo)
        product = Producto.objects.get(producto_id = objetos.producto_id)
        codigo=product.codigo_producto
        

        item = {
            'nombre': objetos.nombre,
            'producto': objetos.producto_id,
            'cantidad': objetos.cantidad,
            'precio_compra': objetos.precio_compra,
            'medida': objetos.medida,
            'total': objetos.total,
            'codigo': codigo,
            'id': objetos.id,
            'reparacion': objetos.reparacion,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')

#NOTA CREDITO#
# class NotaCreditoListView(ObjectListView):
#     model = NotaCredito
#     paginate_by = 100
#     template_name = 'nota_credito/index.html'
#     table_class = NotaCreditoTable
#     filter_class = NotaCreditoFilter
#     context_object_name = 'notascredito'
#     def get_context_data(self, **kwargs):
#         context = super(NotaCreditoListView, self).get_context_data(**kwargs)
#         context['url_delete'] = reverse_lazy('factura-delete')
#         return context
# 
# 
# #=====================================================#
# def NotaCreditoCreateView(request):
#     if request.method == 'POST':
#         form=NotaCreditoForm(request.POST)
#         productos = Producto.objects.all()
#         proformas = Factura.objects.all()
#         nota=NotaCredito()
#         nota.cliente_id=request.POST["cliente_descripcion"]
#         nota.vendedor_id=request.POST["vendedor"]
#         nota.fecha=request.POST["fecha_vencimiento"]
#         nota.razon_social_id=request.POST["razon_social_descripcion"]
#         nota.puntos_venta_id=request.POST["puntos_venta"]
#         nota.nro_nota_credito=request.POST["nro_nota_credito"]
#         nota.observacion=request.POST["descripcion"]
#         nota.clte_direccion1=request.POST["cliente_direccion"]
#         nota.ruc=request.POST["cliente_ruc"]
#         nota.campo1=request.POST["cliente_telefono"]
#         nota.created_by = request.user.get_full_name()
#         nota.updated_by = request.user.get_full_name()
#         nota.created_at = datetime.now()
#         nota.updated_at = datetime.now()
#         nota.total=request.POST["monto"]
#         nota.save()
#         try:
#             secuencial = Secuenciales.objects.get(modulo='nota_credito')
#             secuencial.secuencial=secuencial.secuencial+1
#             secuencial.created_by = request.user.get_full_name()
#             secuencial.updated_by = request.user.get_full_name()
#             secuencial.created_at = datetime.now()
#             secuencial.updated_at = datetime.now()
#             secuencial.save()
#         except Secuenciales.DoesNotExist:
#             secuencial = None
# 
#                 
#         contador=request.POST["columnas_receta_f"]
#         i=0
#         while int(i)<=int(contador):
#             i+= 1
#             if int(i)> int(contador):
#                 print('entrosd')
#                 break
#             else:
#                 print('entroAguardar')
#                 if 'id_kits'+str(i) in request.POST:
#                      notad=NotaCreditoDetalle()
#                      notad.documento_venta_id=request.POST["id_kits"+str(i)]
#                      notad.total=request.POST["abono_kits"+str(i)]
#                      notad.detalle=request.POST["observacion_kits"+str(i)]
#                      notad.nota_credito=nota
#                      notad.created_by = request.user.get_full_name()
#                      notad.updated_by = request.user.get_full_name()
#                      notad.created_at = datetime.now()
#                      notad.updated_at = datetime.now()
#                      notad.save()
# 
#                 print('contadorsd prueba'+str(contador))
#         asientos = json.loads(request.POST['arreglo_asientos'])
#         if len(asientos) > 0:
#             codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
#             secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
#             asiento = Asiento()
#             asiento.codigo_asiento = "NC" + str(datetime.now().year) + "000" + str(codigo_asiento)
#             asiento.fecha = nota.fecha
#             asiento.glosa = 'NOTA de credito ' + str(nota.cliente.nombre_cliente.encode('utf8')) + str(nota.nro_nota_credito)
#             asiento.gasto_no_deducible = False
#             asiento.secuencia_asiento = codigo_asiento
#             total_debe = request.POST['total-debe-asiento']
#             total_haber = request.POST['total-haber-asiento']
#             asiento.total_debe = total_debe
#             asiento.total_haber = total_haber
#             asiento.save()
#             Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
#             for item_asiento in asientos:
#                 asiento_detalle = AsientoDetalle()
#                 asiento_detalle.asiento_id = int(asiento.asiento_id)
#                 asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
#                 asiento_detalle.debe = item_asiento['debe']
#                 asiento_detalle.haber = item_asiento['haber']
#                 asiento_detalle.concepto = item_asiento['concepto']
#                 asiento_detalle.save()
# 
#             nota.asiento_id = asiento.asiento_id
#             nota.save()
#                         
# 
# 
#         return HttpResponseRedirect('/facturacion/nota_credito')
# 
#                 
#                 
#                 
#             
#         
#     else:
#         form=NotaCreditoForm
#         clientes= Cliente.objects.all()
#         cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
#         
#         proformas = Factura.objects.all()
#         return render_to_response('nota_credito/create.html', { 'form': form,'clientes':clientes,'proformas':proformas,'cuentas':cuentas},  RequestContext(request))
# 
# #===========================================
# class NotaCreditoUpdateView(ObjectUpdateView):
#     
#     def get(self, request, *args, **kwargs):
#         
#         nota_credito = NotaCredito.objects.get(id=kwargs['pk'])
#         productos = Producto.objects.all()
# 
#         form=NotaCreditoForm(instance=nota_credito)  
#         detalle = NotaCreditoDetalle.objects.filter(id=nota_credito.id)
# 
#         context = {
#         'section_title':'Actualizar Pedido',
#         'button_text':'Actualizar',
#         'form':form,
#         'productos':productos,
#         'detalle':detalle,
#         'nota_credito':nota_credito
#         }
# 
#         return render_to_response(
#             'nota_credito/actualizar.html', context,context_instance=RequestContext(request))
# 
#     def post(sel, request, *args, **kwargs):
#         nota_credito = NotaCredito.objects.get(factura_id=kwargs['pk'])
#         form = NotaCreditoForm(request.POST,request.FILES,instance=nota_credito)
#         p_id=kwargs['pk']
#         print(p_id)
#         print form.is_valid(), form.errors, type(form.errors)
#         productos = Producto.objects.all()
# 
#         if form.is_valid() :
#             
#             new_orden=form.save()
#             new_orden.updated_by = request.user.get_full_name()
#             new_orden.updated_at = datetime.now()
#             new_orden.save()
#             contador=request.POST["columnas_receta"]
#            
#             i=0
#             while int(i) <= int(contador):
#                 i+= 1
#                 if int(i) > int(contador):
#                     print('entrosd')
#                     break
#                 else:
#                     if 'id_kits'+str(i) in request.POST:
#                         product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
#                         if 'id_detalle'+str(i) in request.POST:
#                             detalle_id=request.POST["id_detalle"+str(i)]
#                             detallecompra = NotaCreditoDetalle.objects.get(id=detalle_id)
#                             print('product_id:'+str(product.producto_id))
#                             detallecompra.updated_by = request.user.get_full_name()
#                             detallecompra.producto =product
#                             detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
#                             detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
#                             detallecompra.total=request.POST["total_kits"+str(i)]
#                             detallecompra.medida=request.POST["medida_kits"+str(i)]
#                             detallecompra.nombre=request.POST["nombre_kits"+str(i)]
#                             #detallecompra.updated_at = datetime.now()
#                             #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
#                             detallecompra.save()
#                             
#                             print('Tiene detalle'+str(i))
#                         else:
#                             comprasdetalle=NotaCreditoDetalle()
#                             comprasdetalle.nota_credito_id = new_orden.id
#                             comprasdetalle.producto=product
#                             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
#                             comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
#                             comprasdetalle.total=request.POST["total_kits"+str(i)]
#                             #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
#                             comprasdetalle.medida=request.POST["medida_kits"+str(i)]
#                             comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
#                             comprasdetalle.save()
#                             i+= 1
#                             print('No Tiene detalle'+str(i))
#                             print('contadorsd prueba'+str(contador))
#             #ordencompra_form=OrdenCompraForm(request.POST)
#             detalle = NotaCreditoDetalle.objects.filter(factura_id=p_id)
#             productos = Producto.objects.all()
# 
#            
#             context = {
#            'section_title':'Actualizar Proforma',
#             'button_text':'Actualizar',
#             'form':form,
#             'detalle':detalle,
#             'productos':productos,
#             'nota_credito':nota_credito,
#             'mensaje':'Pedido actualizada con exito'}
# 
# 
#             return render_to_response(
#                 'nota_credito/actualizar.html', 
#                 context,
#                 context_instance=RequestContext(request))
#         else:
#     
#             form=NotaCreditoForm(request.POST)
#             detalle = NotaCreditoDetalle.objects.filter(nota_credito_id=nota_credito.id)
#             productos = Producto.objects.all()
# 
#             context = {
#             'section_title':'Actualizar Proforma',
#             'button_text':'Actualizar',
#             'form':form,
#             'detalle':detalle,
#             'mensaje':'Pedido actualizada con exito'}
# 
#         return render_to_response(
#             'nota_credito/actualizar.html', 
#             context,
#             context_instance=RequestContext(request))
# 
# 
# #=====================================================#
# @login_required()
# def notaCreditoEliminarView(request):
#     return eliminarView(request, NotaCredito, 'nota-credito-list')
# 
# #=====================================================#
# @login_required()
# def notaCreditoEliminarByPkView(request, pk):
#     return eliminarByPkView(request, pk, NotaCredito)

@csrf_exempt
def obtenerDetalleFactura(request):
    if request.method == 'POST':
        codigo = request.POST.get('id')

        objetos = FacturaDetalle.objects.get(id = codigo)
        product = Producto.objects.get(producto_id = objetos.producto_id)
        codigo=product.codigo_producto
        

        item = {
            'nombre': objetos.nombre,
            'producto': objetos.producto_id,
            'cantidad': objetos.cantidad,
            'precio_compra': objetos.precio_compra,
            'medida': objetos.medida,
            'total': objetos.total,
            'codigo': codigo,
            'id': objetos.id,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')

@csrf_exempt
def obtenerProforma(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = Proforma.objects.get(codigo = codigo)
        
        modulo_secuencial = objetos.cliente_id
    
        detalle = ProformaDetalle.objects.filter(proforma_id = objetos.id)
        ids_detalle=""
        for detl in detalle:
            ids=detl.id
            ids_detalle+=str(ids)+','



        item = {
            'cliente': objetos.cliente_id,
            'vendedor': objetos.vendedor_id,
            'tipo_lugar': objetos.tipo_lugar_id,
            'puntos_venta': objetos.puntos_venta_id,
            'abreviatura_codigo': objetos.abreviatura_codigo,
            'fechapedido': str(objetos.fechapedido),
            'fecha': str(objetos.fecha),
            'descripcion': objetos.descripcion,
            'fuera_ciudad': objetos.fuera_ciudad,
            'tiempo_respuesta': objetos.tiempo_respuesta,
            'observacion': objetos.observacion,
            'ambiente': objetos.ambiente_id,
            'total': objetos.total,
            'subtotal': objetos.subtotal,
            'iva': objetos.iva,
            'porcentaje_descuento': objetos.porcentaje_descuento,
            'descuento': objetos.descuento,
            'id': objetos.id,
            'detalle':ids_detalle,
            'direccion': objetos.direccion_entrega,
            'forma_pago': objetos.forma_pago_id,
            'ruc': objetos.cliente.ruc,
            'puntos_venta': objetos.puntos_venta_id,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')
@csrf_exempt
def obtenerFactura(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        codigo = request.POST.get('id')

        objetos = Factura.objects.get(nro_factura = codigo)
        
        modulo_secuencial = objetos.cliente_id
    
        detalle = FacturaDetalle.objects.filter(factura_id = objetos.factura_id)
        ids_detalle=""
        for detl in detalle:
            ids=detl.id
            ids_detalle+=str(ids)+','



        item = {
            'cliente': objetos.cliente_id,
            'vendedor': objetos.vendedor_id,
            'puntos_venta': objetos.puntos_venta_id,
            'fecha': str(objetos.fecha),
            'total': objetos.total,
            'subtotal': objetos.subtotal,
            'iva': objetos.iva_monto,
            'porcentaje_descuento': objetos.dscto_pciento,
            'descuento': objetos.dscto_monto,
            'id': objetos.factura_id,
            'detalle':ids_detalle,
            'direccion': objetos.clte_direccion1,
            'ruc': objetos.cliente.ruc,
            'puntos_venta': objetos.puntos_venta_id,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')



def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    guia=GuiaRemision.objects.get(guia_id=pk)
    detalle =GuiaDetalle.objects.filter(guia_id=guia.guia_id)
    now = datetime.now()
        
    html = render_to_string('guiaremision/imprimir.html', {'pagesize':'A4','guia':guia,'detalle':detalle,'fecha':now}, context_instance=RequestContext(request))
    return generar_pdf(html)

def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def RegistrarCobroPagoListView(request):
      if request.method == 'POST':
        pagos = RegistrarCobroPago.objects.all()
        
        return render_to_response('pago/index.html', {'pagos':pagos},  RequestContext(request))
      else:
        pagos = RegistrarCobroPago.objects.all()
        return render_to_response('pago/index.html', {'pagos':pagos},  RequestContext(request))


def RegistrarCobroPagoCreateView(request):
      if request.method == 'POST':
        form=RegistrarCobroPagoForm(request.POST)
        productos = Producto.objects.all()
        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()

        if form.is_valid():
            new_orden=form.save()
        
            new_orden.total=request.POST["total"]
            
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='registrarcobropago')
                secuencial.secuencial=secuencial.secuencial+1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            contador=request.POST["columnas_receta"]
            print contador
            i=0
            while int(i)<=int(contador):
                i+= 1
                print('entro cw'+str(i))
                if int(i)> int(contador):
                    print('entrosd')
                    break
                else:
                    print('entroAguardar')
                    if 'id_kits'+str(i) in request.POST:
                        #product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        pedidodetalle=RegistrarCobroPagoDetalle()
                        pedidodetalle.registrar_cobro_pago_id = new_orden.id
                        pedidodetalle.codigo=request.POST["codigo_kits"+str(i)]
                        pedidodetalle.fecha_emision=request.POST["fecha_kits"+str(i)]
                        pedidodetalle.tipo_documento=request.POST["tipo_documento_kits"+str(i)]
                        pedidodetalle.valor=request.POST["valor_kits"+str(i)]
                        #kits.costo=float(request.POST["costo_kits1"])
                        pedidodetalle.saldo=request.POST["saldo_kits"+str(i)]
                        pedidodetalle.valor_a_pagar=request.POST["valor_pagar_kits"+str(i)]
                        tip=request.POST["tipos_kits"+str(i)]
                        if tip=='PR':
                            pedidodetalle.proforma_id=request.POST["id_kits"+str(i)]
                        else:
                            pedidodetalle.factura_id=request.POST["id_kits"+str(i)]

                        pedidodetalle.save()
                        print('se guardo'+str(contador))

                
                print(i)
                print('contadorsd prueba'+str(contador))

            return HttpResponseRedirect('/facturacion/registrarCobroPago')
        else:
            print 'error'
            print form.errors, len(form.errors)
      else:
        form=RegistrarCobroPagoForm

        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()


      return render_to_response('pago/create.html', { 'form': form,'facturas':facturas,'proformas':proformas,},  RequestContext(request))

#===========================================
class RegistrarCobroPagoUpdateView(ObjectUpdateView):
    
    def get(self, request, *args, **kwargs):
        
        factura = RegistrarCobroPago.objects.get(id=kwargs['pk'])

        form=RegistrarCobroPagoForm(instance=factura)  
        detalle = RegistrarCobroPagoDetalle.objects.filter(registrar_cobro_pago_id=factura.id)
        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()

        context = {
        'section_title':'Actualizar Pedido',
        'button_text':'Actualizar',
        'form':form,
        'proformas':proformas,
        'facturas':facturas,
        'detalle':detalle,
        'factura':factura
        }

        return render_to_response(
            'pago/actualizar.html', context,context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        factura = RegistrarCobroPago.objects.get(id=kwargs['pk'])
        form = RegistrarCobroPagoForm(request.POST,request.FILES,instance=factura)
        p_id=kwargs['pk']
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()

        if form.is_valid() :
            
            new_orden=form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.total=request.POST["total"]
            
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
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
                        if 'id_detalle'+str(i) in request.POST:
                            detalle_id=request.POST["id_detalle"+str(i)]
                            detallecompra = RegistrarCobroPagoDetalle.objects.get(id=detalle_id)
                            detallecompra.updated_by = request.user.get_full_name()
                            detallecompra.codigo=request.POST["codigo_kits"+str(i)]
                            detallecompra.fecha_emision=request.POST["fecha_kits"+str(i)]
                            detallecompra.tipo_documento=request.POST["tipo_documento_kits"+str(i)]
                            detallecompra.valor_a_pagar=request.POST["valor_pagar_kits"+str(i)]
                            detallecompra.valor=request.POST["valor_kits"+str(i)]
                            detallecompra.saldo=request.POST["saldo_kits"+str(i)]
                            tip=request.POST["tipos_kits"+str(i)]
                            if tip=='PR':
                                detallecompra.proforma_factura_id=request.POST["id_kits"+str(i)]
                            else:
                                detallecompra.factura_id=request.POST["id_kits"+str(i)]

                            #detallecompra.updated_at = datetime.now()
                            #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                            detallecompra.save()
                            
                            print('Tiene detalle'+str(i))
                        else:
                            comprasdetalle=RegistrarCobroPagoDetalle()
                            comprasdetalle.registrar_cobro_pago_id = new_orden.id
                            comprasdetalle.codigo=request.POST["codigo_kits"+str(i)]
                            comprasdetalle.fecha_emision=request.POST["fecha_kits"+str(i)]
                            comprasdetalle.tipo_documento=request.POST["tipo_documento_kits"+str(i)]
                            comprasdetalle.valor_a_pagar=request.POST["valor_pagar_kits"+str(i)]
                            #comprasdetalle.imagen=request.POST["imagen_kits"+str(i)]
                            comprasdetalle.saldo=request.POST["saldo_kits"+str(i)]
                            tip=request.POST["tipos_kits"+str(i)]
                            if tip=='PR':
                                comprasdetalle.proforma_factura_id=request.POST["id_kits"+str(i)]
                            else:
                                comprasdetalle.factura_id=request.POST["id_kits"+str(i)]
                            comprasdetalle.save()
                            i+= 1
                            print('No Tiene detalle'+str(i))
                            print('contadorsd prueba'+str(contador))
            #ordencompra_form=OrdenCompraForm(request.POST)
            detalle = RegistrarCobroPagoDetalle.objects.filter(registrar_cobro_pago_id=p_id)
            proformas = Proforma.objects.filter(aprobada=True)
            facturas = Factura.objects.all()

           
            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':form,
            'detalle':detalle,
            'proformas':proformas,
            'facturas':facturas,
            'mensaje':'Pedido actualizada con exito'}


            return render_to_response(
                'pago/actualizar.html', 
                context,
                context_instance=RequestContext(request))
        else:
    
            form=RegistrarCobroPagoForm(request.POST)
            detalle = RegistrarCobroPagoDetalle.objects.filter(registrar_cobro_pago_id=factura.id)
            proformas = Proforma.objects.filter(aprobada=True)
            facturas = Factura.objects.all()

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':form,
            'detalle':detalle,
            'proformas':proformas,
            'facturas':facturas,
            'mensaje':'Pedido actualizada con exito'}

        return render_to_response(
            'pago/actualizar.html', 
            context,
            context_instance=RequestContext(request))



def MostrarDocumentoView(request):
  if request.method == 'POST':
    tipo=request.POST["tipo"]
    cliente=request.POST["cliente"]
    fila=request.POST["fila"]
    
    proformas = RegistroDocumento.objects.filter(cliente_id=cliente)
    facturas = Factura.objects.filter(cliente_id=cliente)
    return render_to_response('pago/mostrar_documento.html', {'proformas':proformas,'facturas':facturas,'fila':fila,'tipo':tipo},  RequestContext(request))


  else:
    tipo=request.POST["tipo"]
    cliente=request.POST["cliente"]
    fila=request.POST["fila"]
    
    proformas = RegistroDocumento.objects.filter(cliente_id=cliente)
    facturas = Factura.objects.filter(cliente_id=cliente)
    return render_to_response('pago/mostrar_documento.html', {'proformas':proformas,'facturas':facturas,'fila':fila,'tipo':tipo},  RequestContext(request))



def MostrarPersonasView(request):
    if request.method == 'POST':
        tipo = request.POST["tipo"]
        if tipo=='1':
            personas = Cliente.objects.filter(cliente_activo=True)
            persona_titulo='Clientes'
        else:
            personas = Proveedor.objects.filter(proveedor_activo=True)
            persona_titulo = 'Proveedores'

        return render_to_response('pago/mostrar_personas.html',
                                  {'personas': personas,'persona_titulo':persona_titulo, 'tipo': tipo},
                                  RequestContext(request))


    else:
        tipo = request.POST["tipo"]
        if tipo == '1':
            personas = Clientes.objects.filter(cliente_activo=True)
            persona_titulo = 'Clientes'

        else:
            personas = Proveedor.objects.filter(proveedor_activo=True)
            persona_titulo = 'Proveedores'

        return render_to_response('pago/mostrar_personas.html',
                                  {'personas': personas, 'persona_titulo': persona_titulo, 'tipo': tipo},
                                  RequestContext(request))


def CruceDocumentosCreateView(request):
    if request.method == 'POST':
        form = CruceDocumentoForm(request.POST)
        productos = Producto.objects.all()
        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()

        if form.is_valid():
            new_orden = form.save()

            new_orden.total = request.POST["total"]

            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='registrarcobropago')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            contador = request.POST["columnas_receta"]
            print contador
            i = 0
            while int(i) <= int(contador):
                i += 1
                print('entro cw' + str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    print('entroAguardar')
                    if 'id_kits' + str(i) in request.POST:
                        # product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        pedidodetalle = RegistrarCobroPagoDetalle()
                        pedidodetalle.registrar_cobro_pago_id = new_orden.id
                        pedidodetalle.codigo = request.POST["codigo_kits" + str(i)]
                        pedidodetalle.fecha_emision = request.POST["fecha_kits" + str(i)]
                        pedidodetalle.tipo_documento = request.POST["tipo_documento_kits" + str(i)]
                        pedidodetalle.valor = request.POST["valor_kits" + str(i)]
                        # kits.costo=float(request.POST["costo_kits1"])
                        pedidodetalle.saldo = request.POST["saldo_kits" + str(i)]
                        pedidodetalle.valor_a_pagar = request.POST["valor_pagar_kits" + str(i)]
                        tip = request.POST["tipos_kits" + str(i)]
                        if tip == 'PR':
                            pedidodetalle.proforma_id = request.POST["id_kits" + str(i)]
                        else:
                            pedidodetalle.factura_id = request.POST["id_kits" + str(i)]

                        pedidodetalle.save()
                        print('se guardo' + str(contador))

                print(i)
                print('contadorsd prueba' + str(contador))

            return HttpResponseRedirect('/facturacion/registrarCobroPago')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = CruceDocumentoForm

        proformas = Proforma.objects.filter(aprobada=True)
        facturas = Factura.objects.all()

    return render_to_response('pago/cruce_documentos.html', {'form': form, 'proformas': proformas,},
                              RequestContext(request))


def MostrarDocumentoGeneralView(request):
    if request.method == 'POST':
        tipo = request.POST["tipo"]
        cliente = request.POST["cliente"]
        fila = request.POST["fila"]

        proformas = TransaccionesRegistrodocumento.objects.filter(cliente_id=cliente)
        facturas = Factura.objects.filter(cliente_id=cliente)
        return render_to_response('pago/mostrar_documento_general.html',
                                  {'proformas': proformas, 'facturas': facturas, 'fila': fila, 'tipo': tipo},
                                  RequestContext(request))


    else:
        tipo = request.POST["tipo"]
        cliente = request.POST["cliente"]
        fila = request.POST["fila"]

        proformas = TransaccionesRegistrodocumento.objects.filter(cliente_id=cliente)
        facturas = Factura.objects.filter(cliente_id=cliente)
        return render_to_response('pago/mostrar_documento_general.html',
                                  {'proformas': proformas, 'facturas': facturas, 'fila': fila, 'tipo': tipo},
                                  RequestContext(request))


def CruceDocumentoListView(request):
    if request.method == 'POST':
        pagos = CruceDocumento.objects.all()

        return render_to_response('pago/cruce_documento_list.html', {'pagos': pagos}, RequestContext(request))
    else:
        pagos = CruceDocumento.objects.all()
        return render_to_response('pago/cruce_documento_list.html', {'pagos': pagos}, RequestContext(request))



def MostrarCuentaView(request):
    if request.method == 'POST':
        tipo = request.POST["tipo"]
        if tipo=='1':
            personas = PlanDeCuentas.objects.all()
            persona_titulo='Cobro'
        else:
            personas = PlanDeCuentas.objects.all()
            persona_titulo = 'Pago'

        return render_to_response('pago/mostrar_cuenta.html',
                                  {'personas': personas,'persona_titulo':persona_titulo, 'tipo': tipo},
                                  RequestContext(request))


    else:
        tipo = request.POST["tipo"]
        if tipo=='1':
            personas = PlanDeCuentas.objects.all()
            persona_titulo='Cobro'
        else:
            personas = PlanDeCuentas.objects.all()
            persona_titulo = 'Pago'

        return render_to_response('pago/mostrar_cuenta.html',
                                  {'personas': personas, 'persona_titulo': persona_titulo, 'tipo': tipo},
                                  RequestContext(request))


def MostrarCuentaPersonaView(request):
    if request.method == 'POST':
        tipo = request.POST["tipo"]
        persona_id = request.POST["persona_id"]
        fila = request.POST["fila"]
        if tipo=='1':
            personas = PlanDeCuentas.objects.all()
            persona_titulo='Cobro'
        else:
            personas = PlanDeCuentas.objects.all()
            persona_titulo = 'Pago'

        return render_to_response('pago/mostrar_cuenta_persona.html',
                                  {'personas': personas,'persona_titulo':persona_titulo, 'tipo': tipo,'fila': fila,},
                                  RequestContext(request))


    else:
        tipo = request.POST["tipo"]
        persona_id = request.POST["persona_id"]
        fila = request.POST["fila"]
        if tipo=='1':
            personas = PlanDeCuentas.objects.all()
            persona_titulo='Cobro'
        else:
            personas = PlanDeCuentas.objects.all()
            persona_titulo = 'Pago'

        return render_to_response('pago/mostrar_cuenta_persona.html',
                                  {'personas': personas, 'persona_titulo': persona_titulo, 'tipo': tipo,'fila': fila,},
                                  RequestContext(request))


@login_required()
def MostrarOPView(request):
    cliente = request.POST["id_cliente"]
    bodega = request.POST["id_bodega"]
    tipo_guia = request.POST["id_tipo_guia"]
    cursor = connection.cursor()
    print(tipo_guia)
    if tipo_guia == '1':
        # sql = 'select opb.id, opb.producto_id, p.descripcion_producto, opb.cantidad_sobrante, opb.bodega_id,
        # op.costo_final,op.costo_final,op.codigo_item,opb.medida,opb.orden_produccion_id,opb.cantidad_recibida,opb.ingresado_bodega,
        # op.cliente_id,op.descripcion
        #   from orden_produccion_bodega opb,orden_produccion op,producto p where  p.producto_id=opb.producto_id and opb.orden_produccion_id=op.id and opb.ingresado_bodega=true and op.cliente_id='+str(cliente)+' and opb.bodega_id='+str(bodega)+' and opb.cantidad_sobrante>0 ;'

        sql = ('''SELECT op.id, p.producto_id,p.descripcion_producto, op.cantidad, op.costo_final,
                op.costo_final, op.codigo_item, op.cliente_id,op.descripcion
                FROM orden_produccion op
                INNER JOIN pedido_detalle pd ON op.pedido_detalle_id = pd.id
                INNER JOIN producto p on pd.producto_id = p.producto_id
                WHERE op.cliente_id='''+str(cliente)+'''
                UNION
                select pb.producto_bodega_id, pb.producto_id,p.descripcion_producto,pb.cantidad, 
                p.costo,p.costo, p.codigo_producto, p.producto_id, p.descripcion_producto 
                from producto p
                inner join producto_en_bodega pb on p.producto_id=pb.producto_id 
                where pb.cantidad > 0''')
        print(sql)
    else:
        # sql = 'select pb.producto_bodega_id, pb.producto_id,p.descripcion_producto,pb.cantidad, pb.bodega_id,p.precio1,p.costo,p.codigo_producto from producto p,producto_en_bodega pb where p.producto_id=pb.producto_id and pb.cantidad>0 and pb.bodega_id=' + str(bodega) + ';'

        sql = '''select pb.producto_bodega_id, pb.producto_id,p.descripcion_producto,pb.cantidad, 
                p.costo,p.costo, p.codigo_producto, p.producto_id, p.descripcion_producto
                from producto p
                inner join producto_en_bodega pb on p.producto_id=pb.producto_id 
                where pb.cantidad > 0 and pb.bodega_id=''' + str(bodega) + ''';'''
        print(sql)


    cursor.execute(sql)
    row= cursor.fetchall()

    if request.method == 'POST':
        return render_to_response('guiaremision/mostrar_op.html',{'row': row,'tipo_guia': tipo_guia}, RequestContext(request))
    else:
        return render_to_response('guiaremision/mostrar_op.html', {'row': row}, RequestContext(request))


@csrf_exempt
def cargarDireccionBodega(request):
    if request.method == 'POST':
        bodega = request.POST.get('bodega_id')



        bodega_base = Bodega.objects.get(id=bodega)

        direccion_partida=''

        if bodega_base:
            direccion_partida=bodega_base.direccion1

        item = {
            'direccion_partida': direccion_partida

        }
        return HttpResponse(json.dumps(item), content_type='application/json')

    else:
        raise Http404



@csrf_exempt
def cargarDireccionCliente(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente_id')
        clientes_base = Cliente.objects.get(id_cliente=cliente)

        direccion_llegada=''
        if clientes_base:
            direccion_llegada=clientes_base.direccion2

        item = {
            'direccion_llegada': direccion_llegada,

        }
        return HttpResponse(json.dumps(item), content_type='application/json')

    else:
        raise Http404
    
    

@login_required()
def TipoGuiasListView(request):
    tipos = TipoGuia.objects.all()
    return render_to_response('tipo_guia/index.html', {'tipos': tipos}, RequestContext(request))
   

# =====================================================#

class TipoGuiasCreateView(ObjectCreateView):
    model = TipoGuia
    form_class = TipoGuiasForm
    template_name = 'tipo_guia/create.html'
    url_success = 'tipoguias-list'
    url_success_other = 'tipoguias-create'
    url_cancel = 'tipoguias-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        objetos = Secuenciales.objects.get(modulo='tipo_guia')

        modulo_secuencial = objetos.secuencial + 1
        objetos.secuencial = modulo_secuencial
        objetos.save()

        return super(TipoGuiasCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo tipo guia."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#

class TipoGuiasUpdateView(ObjectUpdateView):
    model = TipoGuia
    form_class = TipoGuiasForm
    template_name = 'tipo_guia/create.html'
    url_success = 'tipoguias-list'
    url_cancel = 'tipoguias-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo Guia actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


            
@login_required()
@transaction.atomic
def consultar_guia_remision_electronica(request):
    #db = MySQLdb.connect(host="104.192.6.75, user="sa",passwd="U7BKm3eayFCn9cTx", db="FacturaNotaCreditoYDebito")
    with transaction.atomic():
        id = request.POST['id']
        try:
            factura = GuiaRemision.objects.get(guia_id=id)
        except GuiaRemision.DoesNotExist:
            factura = None
        
        ambiente=''
        tipoEmision='1'
        razonSocial=''
        nombreComercial=''
        dirMatriz=''
        contribuyenteEspecial=''
        obligadoContabilidad='SI'
        moneda=''
        
        
        valor_ambiente = Parametros.objects.get(clave='fe_ambiente').valor
        ambiente=valor_ambiente
        
        tipoEmision='1'
        #Factura(01) NotaCredito(04) NotaDebito(05) GuiaRemision(06) ComprobanteRetencion(07)    
        codDoc='06'
        valor_razonSocial=Parametros.objects.get(clave='fe_razonSocial').valor
        razonSocial=valor_razonSocial
        
        valor_nombreComercial=Parametros.objects.get(clave='fe_nombreComercial').valor
        nombreComercial=valor_nombreComercial
        
        valor_dirMatriz=Parametros.objects.get(clave='fe_direccion').valor
        dirMatriz=valor_dirMatriz
        
        valor_contribuyenteEspecial=Parametros.objects.get(clave='fe_contribuyenteEspecial').valor
        contribuyenteEspecial=valor_contribuyenteEspecial
        
        valor_moneda=Parametros.objects.get(clave='fe_moneda').valor
        moneda=valor_moneda
        
        dirEstablecimiento=Parametros.objects.get(clave='fe_direccion').valor
        ruc=Parametros.objects.get(clave='fe_ruc').valor
        iva=Parametros.objects.get(clave='iva').valor
        estab=''
        ptoEmi=''
        secuencial=''
        #dirEstablecimiento=''
        dirPartida=''
        razonSocialTransportista=''
        tipoIdentificacionTransportista=''
        rucTransportista=''
        obligadoContabilidad='SI'
        contribuyenteEspecial=''
        fechaIniTransporte=''
        fechaFinTransporte=''
        placa=''

        direccion=''
        telefono=''
        email=''
        
    
        if factura:
            razonSocialTransportista=factura.chofer.nombre
            if len(factura.chofer.ruc)>9:
                rucTransportista=factura.chofer.ruc
                tipoIdentificacionTransportista='04'
                    
            else:
                rucTransportista=factura.chofer.cedula
                tipoIdentificacionTransportista='05'


            
            dirPartida=factura.partida
            email=factura.cliente.email1
               
    
                
            direccion=factura.destino
            telefono=factura.cliente.telefono1
            direccionComprador=factura.cliente.direccion1
            fechaIniTransporte=factura.fecha_inicio
            fechaFinTransporte=factura.fecha_fin
            placa=factura.vehiculo.placa
            festablecimiento=factura.puntos_venta.establecimiento
            fpunto_emision=factura.puntos_venta.punto_emision
            logn_nro_guia=len(str(factura.nro_guia))
            if logn_nro_guia<9:
                fsecuencial=str(factura.nro_guia).zfill(9) 
            else:
                fsecuencial=factura.nro_guia
            fecha_emision=factura.fecha_emision
            secuencialTransaccion=''
            tipoDocTransaccion=''

            
            
            
            print 'CONEXION'
            id=factura.guia_id
            
        
            conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
            cursor = conn.cursor()
            sqlCommanf="INSERT INTO infoGuiaRemision(id,ambiente,tipoEmision,razonSocial,nombreComercial,ruc,codDoc,estab,ptoEmi,secuencial,secuencialTransaccion,tipoDocTransaccion,dirMatriz,dirEstablecimiento,dirPartida,razonSocialTransportista,tipoIdentificacionTransportista,rucTransportista,obligadoContabilidad,contribuyenteEspecial,fechaIniTransporte,fechaFinTransporte,placa,direccion,telefono,email) values ("+str(id)+",'"+str(ambiente)+"','"+str(tipoEmision)+"','"+str(razonSocial)+"','"+str(nombreComercial)+"','"+str(ruc)+"','"+str(codDoc.encode('utf8'))+"','"+str(festablecimiento)+"','"+str(fpunto_emision)+"','"+str(fsecuencial)+"','"+str(secuencialTransaccion)+"','"+str(tipoDocTransaccion.encode('utf8'))+"','"+str(dirMatriz.encode('utf8'))+"','"+str(dirEstablecimiento.encode('utf8'))+"','"+str(dirPartida.encode('utf8'))+"','"+str(razonSocialTransportista.encode('utf8'))+"','"+str(tipoIdentificacionTransportista.encode('utf8'))+"','"+str(rucTransportista)+"','"+str(obligadoContabilidad)+"','"+str(contribuyenteEspecial)+"','"+str(fechaIniTransporte)+"','"+str(fechaFinTransporte)+"','"+str(placa.encode('utf8'))+"','"+str(direccion.encode('utf8'))+"','"+str(telefono)+"','"+str(email)+"')"
            print sqlCommanf
            cursor.execute(sqlCommanf)
            conn.commit()
            
            #post_id = cursor.lastrowid
            post_id = factura.guia_id
            print post_id
    
            
            secuencia=1
            
            codigoPrincipal=''
            codigoAuxiliar=''
            fdescripcion=''
            precioUnitario=0
            cantidad=0
            
            try:
                factura_detalle = GuiaDetalle.objects.filter(guia_id=factura.guia_id)
            except GuiaDetalle.DoesNotExist:
                factura_detalle = None
            secuencia=1
            if  factura_detalle:
                for f in factura_detalle:
                    secuenciaDestinatario=1
                    
                    codigoInterno=f.producto.codigo_producto
                    codigoAdicional=f.producto.codigo_producto
                    descripcion=f.descripcion
                    cantidad=f.cantidad

                    
                    sqlComman1="INSERT INTO detalleInfoGuiaRemision (id,secuenciaDestinatario,secuencia,codigoInterno,codigoAdicional,descripcion,cantidad) values ("+str(post_id)+","+str(secuenciaDestinatario)+","+str(secuencia)+",'"+str(codigoInterno)+"','"+str(codigoAdicional)+"','"+str(descripcion.encode('utf8'))+"',"+str(cantidad)+")"
                    print sqlComman1
                    cursor.execute(sqlComman1)
                    conn.commit()
                    secuencia=secuencia+1
            
            
            
            # try:
            #     factura_fpago = DocumentoVentaFormaPago.objects.filter(documento_venta_id=factura_detalles.documento_venta_id)
            # except DocumentoVentaFormaPago.DoesNotExist:
            #     factura_fpago = None
            # 
            # secuenciafpago=1
            # if factura_fpago:
            #     formaPago=factura_fpago.forma_pago_ventas.codigo
            #     fptotal=factura_fpago.documento_venta.total
            #     v_plazo=Parametros.objects.get(clave='fe_dias_plazo').valor
            #     fpplazo=v_plazo
            #     fpunidadTiempo='dias'
            #     sqlComman2="INSERT INTO infoFormaPago (id,secuencia,formaPago,total,plazo,unidadTiempo) values ("+str(post_id)+","+str(secuenciafpago)+",'"+str(formaPago)+"',"+str(fptotal)+",'"+str(fpplazo)+"','"+str(fpunidadTiempo)+"')"
            #     print sqlComman2
            #     cursor.execute(sqlComman2)
            #     conn.commit()
            #     
            #     
            #     secuenciafpago=secuenciafpago+1
            
            fsecuencia=1
            if factura.cliente.ruc:
                identificacionDestinatario=factura.cliente.ruc
            else:
                identificacionDestinatario=factura.cliente.cedula
            razonSocialDestinatario=factura.cliente.nombre_cliente
            dirDestinatario=factura.partida
            motivoTraslado=factura.tipo_guia.descripcion
            docAduaneroUnico=''
            codEstabDestino='001'
            ruta=''
            codDocSustento=''
            numDocSustento=''
            numAutDocSustento=''
            fechaEmisionDocSustento=None
            
            
            # try:
            #     fventa = DocumentoVenta.objects.get(guia_remision_id=id)
            # except DocumentoVenta.DoesNotExist:
            #     fventa = None
            # 
            # if fventa:
            #     codDocSustento='01'
            #     numDocSustento=fventa.establecimiento+'-'+fventa.punto_emision+'-'+fventa.secuencial
            #     numAutDocSustento=fventa.autorizacion
            #     fechaEmisionDocSustento=fventa.fecha_emision

            sqlComman2="INSERT INTO destinatarioInfoGuiaRemision (id,secuencia,identificacionDestinatario,razonSocialDestinatario,dirDestinatario,motivoTraslado,docAduaneroUnico,codEstabDestino,ruta,codDocSustento,numDocSustento,numAutDocSustento,fechaEmisionDocSustento) values ("+str(post_id)+","+str(fsecuencia)+",'"+str(identificacionDestinatario)+"','"+str(razonSocialDestinatario.encode('utf8'))+"','"+str(dirDestinatario.encode('utf8'))+"','"+str(motivoTraslado.encode('utf8'))+"','"+str(docAduaneroUnico)+"','"+str(codEstabDestino)+"','"+str(ruta)+"','"+str(codDocSustento)+"','"+str(numDocSustento)+"','"+str(numAutDocSustento)+"',NULL)"
            print sqlComman2
            cursor.execute(sqlComman2)
            conn.commit()


            html='Se ingreso la guia de Remision electronicamente'
            factura.facturacion_eletronica=True
            factura.save()
            
            return HttpResponse(html)
    
        else:
            raise Http404    
        
             
