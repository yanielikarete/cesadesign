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
import datetime
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
from django.utils.encoding import smart_str

#from login.lib.tools import Tools
from inventario.models import *
from config.models import *
from subordenproduccion.models import *

#from config.models import Mensajes

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes

from login.lib.tools import Tools
from django.contrib import auth
from django.db import IntegrityError, connection, transaction


@login_required()
def AjustesListView(request):

    cursor = connection.cursor()
    #1- 10
    query = "select A.id, A.codigo, A.tipo, A.fecha, A.hora, A.moneda, A.subtotal, A.total, A.comentario, "
    #11-20
    query += "A.asiento_id, A.kardex_id, A.anulado, A.created_by, A.updated_by, A.created_at, A.updated_at, A.aprobada, A.bodega_id, A.concepto_ajustes_id, B.nombre "
    query += "from ajustes A "
    query += "left join concepto_ajustes B on (A.concepto_ajustes_id = B.id) "

    cursor.execute(query)
    ajustes = cursor.fetchall()

    #ajustes=Ajustes.objects.all()
    #productos = Producto.objects.all()

    return render_to_response('ajustes/list.html', {'ajustes': ajustes}, RequestContext(request))

#=====================================================#
class AjustesDetailView(ObjectDetailView):
    model = Ajustes
    template_name = 'ajustes/detail.html'

#=====================================================#
@login_required()
@transaction.atomic
def AjustesCreateView(request):
    if request.method == 'POST':
        ajustes_form=AjustesForm(request.POST)
        #productos = Producto.objects.all()
        bodegas = Bodega.objects.all()

        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad,sum(pb.cantidad) '
        query += 'from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 group by p.producto_id, p.codigo_producto,p.descripcion_producto order by p.producto_id;'

        cursor.execute(query)
        productos_bodega = cursor.fetchall()

        if ajustes_form.is_valid():
            with transaction.atomic():
                new_orden=ajustes_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal= request.POST["total"]
                new_orden.aprobada = True

                subtotal=request.POST["total"]
                new_orden.total= request.POST["total"]
                idConcepto = new_orden.concepto_ajustes_id
                IdAjuste = new_orden.id
                IdBodega = bodega_id=request.POST["bodega"]

                Bods = Bodega.objects.filter(id=IdBodega)

                if Bods:
                    for bod in Bods:
                        objBod = bod.id

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ajustes')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                contador=request.POST["columnas_receta"]
                # print contador
                i=0
                while int(i)<=int(contador):
                     i+= 1
                     if int(i)> int(contador):
                         break
                     else:
                         if 'id_kits'+str(i) in request.POST:
                             product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                             ajustesdetalle=AjustesDetalle()

                             ajustesdetalle.ajustes_id = new_orden.id
                             ajustesdetalle.producto_id=request.POST["id_kits"+str(i)]
                             ajustesdetalle.bodega_id=request.POST["bodega"]
                             ajustesdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                             ajustesdetalle.costo=request.POST["costo_kits"+str(i)]
                             ajustesdetalle.total = request.POST["total_kits" + str(i)]
                             ajustesdetalle.created_by = request.user.get_full_name()
                             ajustesdetalle.updated_by = request.user.get_full_name()
                             ajustesdetalle.created_at = datetime.now()
                             ajustesdetalle.created_by = datetime.now()
                             ajustesdetalle.save()

                             prod1 = ProductoEnBodega.objects.filter(producto_id=request.POST["id_kits" + str(i)]).filter(bodega_id=request.POST["bodega"])
                             if prod1:
                                 for prod in prod1:
                                     if idConcepto == 1:
                                         prod.cantidad = float(prod.cantidad) + float(request.POST["cantidad_kits"+str(i)])
                                     else:
                                         prod.cantidad = float(prod.cantidad) - float(request.POST["cantidad_kits"+str(i)])
                                     prod.updated_at = new_orden.fecha
                                     prod.updated_by = request.user.get_full_name()
                                     prod.save()

                Detalles = AjustesDetalle.objects.filter(ajustes = IdAjuste)
                for obj in Detalles:
                    k = Kardex()
                    k.nro_documento = new_orden.codigo
                    k.producto = obj.producto
                    k.cantidad = obj.cantidad
                    k.costo = obj.costo
                    k.bodega = new_orden.bodega
                    k.modulo = new_orden.id
                    k.un_doc_soporte = 'Ajuste de Inventario No.' + str(new_orden.codigo)  # + ' Compra Local No.' + str(new_orden.codigo)
                    k.created_at = datetime.now()
                    k.created_by = request.user.get_full_name()
                    k.updated_at = datetime.now()
                    k.updated_by = request.user.get_full_name()
                    if idConcepto == 1:
                        k.fecha_ingreso = datetime.now()
                        k.egreso = False
                        k.descripcion = 'Ingreso por Ajuste de Inventario (Regularizacion)'
                    else:
                        k.fecha_egreso = new_orden.fecha
                        k.egreso = True
                        k.descripcion = 'Egreso por Ajuste de Inventario (Regularizacion)'

                    k.save()

            return HttpResponseRedirect('/ajustes/ajustes')
        else:
            print 'error'
            print ajustes_form.errors, len(ajustes_form.errors)
    else:
        ajustes_form=AjustesForm
        #productos = Producto.objects.all()
        areas=Areas.objects.all()
        concepto=ConceptoAjustes.objects.all()

        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio costo, p.unidad,sum(pb.cantidad) '
        query += 'from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 group by p.producto_id, p.codigo_producto,p.descripcion_producto order by p.producto_id;'

        cursor.execute(query)
        productos_bodega = cursor.fetchall()

    return render_to_response('ajustes/create.html', { 'ajustes_form': ajustes_form,'productos_bodega':productos_bodega,'areas':areas,'concepto':concepto},  RequestContext(request))

#=====================================================#
@login_required()
@transaction.atomic

def AjustesUpdateView(request,pk):
    if request.method == 'POST':
        ajustes=Ajustes.objects.get(id=pk)
        ajustes_form=AjustesForm(request.POST,request.FILES,instance=ajustes)
        print ajustes_form.is_valid(), ajustes_form.errors, type(ajustes_form.errors)

        if ajustes_form.is_valid():
            with transaction.atomic():
                new_orden=ajustes_form.save()
                new_orden.save()


                # contador=request.POST["columnas_receta"]
                # print contador
                # i=1
                # while int(i) <= int(contador):
                #
                #     if int(i) > int(contador):
                #         print('entrosd')
                #         break
                #     else:
                #         product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                #         detalle_id=request.POST["id_detalle"+str(i)]
                # #         if detalle_id:
                # #             detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
                # #             detallecompra.updated_by = request.user.get_full_name()
                # #             #detallecompra.updated_at = datetime.now()
                #
                # #             detallecompra.save()
                # #             nd=detallecompra.save()
                # #             i+= 1
                # #             print('entro holaaaa'+str(nd.compra_id))
                # #             if 'recibido_kits'+str(i) in request.POST:
                # #               print('entrorecibido')
                # #               nd.recibido=request.POST["recibido_kits"+str(i)]
                # #               nd.save()
                # #               kardez = Kardex.objects.get(modulo=detalle_id)
                # #               if kardez:
                # #                   print('ya existe')
                # #               else:
                # #                   k=Kardex()
                # #                   k.nro_documento =new_orden.nro_compra
                # #                   k.producto=product
                # #                   k.cantidad=nd.cantidad
                # #                   k.descripcion='Orden de Compra'
                # #                   k.costo=nd.precio_compra
                # #                   k.bodega=new_orden.bodega
                # #                   k.modulo=detalle_id
                # #                   k.fecha_ingreso=datetime.now()
                # #                   k.save()
                #
                # #         else:
                # #             comprasdetalle=ComprasDetalle()
                # #             comprasdetalle.compra_id = new_orden.compra_id
                # #             comprasdetalle.producto=product
                # #             comprasdetalle.proveedor=new_orden.proveedor
                # #             comprasdetalle.bodega=new_orden.bodega
                # #             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                # #             #kits.costo=float(request.POST["costo_kits1"])
                # #             comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                # #             comprasdetalle.total=request.POST["total_kits"+str(i)]
                # #             comprasdetalle.save()
                # #             i+= 1
                # #             print('No Tiene detalle'+str(i))
                # #             print('contadorsd prueba'+str(contador))
                # # #ordencompra_form=OrdenCompraForm(request.POST)
                # print('El id de la compra'+str(pk))

                detalle = AjustesDetalle.objects.filter(ajustes_id=pk)
                # areas=Areas.objects.all()
                concepto=ConceptoAjustes.objects.all()

                context = {
                'section_title':'Actualizar Ajustes',
                'button_text':'Actualizar',
                'ajustes_form':ajustes_form,
                'concepto':concepto,
                'detalle':detalle }


                return render_to_response(
                    'ajustes/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            ajustes_form=AjustesForm(request.POST)
            detalle = AjustesDetalle.objects.filter(ajustes_id=ajustes.id)
            #areas=Areas.objects.all()
            concepto=ConceptoAjustes.objects.all()

            context = {
            'section_title':'Actualizar Ajustes',
            'button_text':'Actualizar',
            'ajustes_form':ajustes_form,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ajustes/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ajustes=Ajustes.objects.get(id=pk)
        ajustes_form=AjustesForm(instance=ajustes)
        detalle =AjustesDetalle.objects.filter(ajustes_id=ajustes.id)
        concepto=ConceptoAjustes.objects.all()

        context = {
            'section_title':'Actualizar Ajustes',
            'button_text':'Actualizar',
            'ajustes_form':ajustes_form,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ajustes/actualizar.html',
            context,
            context_instance=RequestContext(request))



#=====================================================#
@login_required()
def ajustesEliminarView(request):
    return eliminarView(request, Ajustes, 'ajustes-list')

#=====================================================#
@login_required()
def ajustesEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Ajustes)

#MUEDIRSA
@login_required()
def AjustesListAprobarView(request):
    ajustes=Ajustes.objects.all()

    return render_to_response('ajustes/aprobada.html', {'ajustes': ajustes}, RequestContext(request))



#=====================================================#
@login_required()
def ajustesAprobarByPkView(request, pk):

    objetos = Ajustes.objects.filter(id= pk)
    for obj in objetos:
        obj.aprobada = True
        obj.save()

    ol = Ajustes.objects.get(id= pk)
    fecha=ol.fecha



    # if ol.producto_terminado:
    #     codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
    #     secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
    #     parametro_acreedora = Parametros.objects.get(clave='cuenta_acreedora_ingreso_inventario')
    #     parametro_deudora = Parametros.objects.get(clave='cuenta_deudora_ingreso_inventario')
    #     asiento = Asiento()
    #     asiento.codigo_asiento = "OI" + str(fecha.year) + "000" + str(codigo_asiento)
    #     asiento.fecha = fecha
    #     asiento.glosa = 'Orden Ingreso de Product. Terminado ' + str(ol.codigo)
    #     asiento.modulo= 'Orden Ingreso'
    #     asiento.gasto_no_deducible = False
    #     asiento.save()
    #     ol.asiento_id=asiento.asiento_id
    #     ol.save()
    #
    #     Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
    #     try:
    #         plan_deudora = PlanDeCuentas.objects.get(codigo_plan=parametro_deudora.valor)
    #     except PlanDeCuentas.DoesNotExist:
    #         plan_deudora = None
    #     if plan_deudora:
    #         asiento_detalle = AsientoDetalle()
    #         asiento_detalle.asiento_id = int(asiento.asiento_id)
    #         asiento_detalle.cuenta_id = plan_deudora.plan_id
    #         asiento_detalle.debe = ol.total
    #         asiento_detalle.haber = 0
    #         asiento_detalle.save()
    #
    #     try:
    #         plan_acreedora = PlanDeCuentas.objects.get(codigo_plan=parametro_acreedora.valor)
    #
    #
    #     except PlanDeCuentas.DoesNotExist:
    #         plan_acreedora = None
    #     if plan_acreedora:
    #         asiento_detalle = AsientoDetalle()
    #         asiento_detalle.asiento_id = int(asiento.asiento_id)
    #         asiento_detalle.cuenta_id = plan_acreedora.plan_id
    #         asiento_detalle.debe = 0
    #         asiento_detalle.haber = ol.total
    #         asiento_detalle.save()
    #
    #
    #
    # try:
    #     op = OrdenProduccion.objects.get(codigo=ol.orden_produccion_codigo)
    # except OrdenProduccion.DoesNotExist:
    #     op = None


    objetose = AjustesDetalle.objects.filter(ajustes_id= pk)
    orden_ing = Ajustes.objects.get(id= pk)
    conceptoop=ConceptoAjustes.objects.get(id=orden_ing.concepto_ajustes_id)
    # if conceptoop.op == True:
    #     codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
    #     secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
    #     asiento = Asiento()
    #     asiento.codigo_asiento = "OI" + str(fecha.year)  + "000" + str(codigo_asiento)
    #     asiento.fecha = fecha
    #     asiento.glosa = 'Orden Ingreso por devolucion '+str(orden_ing.codigo)
    #     asiento.modulo= 'Orden Ingreso'
    #     asiento.total_debe=orden_ing.subtotal
    #     asiento.total_haber=orden_ing.subtotal
    #     asiento.secuencia_asiento = codigo_asiento
    #     asiento.gasto_no_deducible = False
    #     asiento.save()
    #     orden_ing.asiento_id=asiento.asiento_id
    #     orden_ing.save()
    #
    #     Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
    # else:
    #     codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
    #     secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
    #     asiento = Asiento()
    #     asiento.codigo_asiento = "OI" + str(fecha.year)  + "000" + str(codigo_asiento)
    #     asiento.fecha = fecha
    #     asiento.glosa = 'Orden Ingreso por '+str(ol.concepto_orden_ingreso)+' de '+str(orden_ing.codigo)
    #     asiento.modulo= 'Orden Ingreso'
    #     asiento.total_debe=orden_ing.subtotal
    #     asiento.total_haber=orden_ing.subtotal
    #     asiento.secuencia_asiento = codigo_asiento
    #     asiento.gasto_no_deducible = False
    #     asiento.save()
    #     orden_ing.asiento_id=asiento.asiento_id
    #     orden_ing.save()
    #
    #     Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
    #     for obj in objetose:
    #         tipo_producto_id = obj.producto.tipo_producto.id
    #
    #         try:
    #             prod_d = TipoProducto.objects.get(id=int(tipo_producto_id))
    #         except TipoProducto.DoesNotExist:
    #             prod_d = None
    #
    #         if prod_d:
    #             try:
    #                 plan_deudora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_inventario_productos_proceso_id)
    #             except PlanDeCuentas.DoesNotExist:
    #                 plan_deudora = None
    #
    #             if plan_deudora:
    #                 asiento_detalle = AsientoDetalle()
    #                 asiento_detalle.asiento_id = int(asiento.asiento_id)
    #                 asiento_detalle.cuenta_id = plan_deudora.plan_id
    #                 asiento_detalle.debe = 0
    #                 asiento_detalle.haber = obj.total
    #                 asiento_detalle.concepto = 'Ingreso de Producto' + smart_str(obj.producto.descripcion_producto)
    #                 asiento_detalle.save()
    #
    #
    #
    #
    #             try:
    #                 plan_acreedora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_contable_id)
    #             except PlanDeCuentas.DoesNotExist:
    #                 plan_acreedora = None
    #             if plan_acreedora:
    #                 asiento_detalle = AsientoDetalle()
    #                 asiento_detalle.asiento_id = int(asiento.asiento_id)
    #                 asiento_detalle.cuenta_id = plan_acreedora.plan_id
    #                 asiento_detalle.debe = obj.total
    #                 asiento_detalle.haber = 0
    #                 asiento_detalle.concepto = 'Ingreso de Producto' + str(obj.producto.descripcion_producto.encode('utf8'))
    #                 asiento_detalle.save()
    #
    #
    #
    # for obj in objetose:
    #     if op:
    #         try:
    #             opb = OrdenProduccionBodega.objects.get(producto_id=obj.producto_id, orden_produccion_id=op.id)
    #         except OrdenProduccionBodega.DoesNotExist:
    #             opb = None
    #
    #         if opb:
    #             cant_sobr= opb.cantidad_recibida
    #             opb.ingresado_bodega=True
    #             opb.cantidad_sobrante = cant_sobr
    #             opb.cantidad_despachada = 0
    #             opb.bodega=orden_ing.bodega
    #             opb.save()
    #     if obj.op:
    #         try:
    #             opr = OrdenProduccionReceta.objects.get(id=obj.orden_produccion_receta_id)
    #         except OrdenProduccionReceta.DoesNotExist:
    #             opr = None
    #         if opr:
    #             if opr.ingresos:
    #                 ing=opr.ingresos
    #             else:
    #                 ing=0
    #
    #             if ing == '' or  ing == 'None':
    #                 ing=0
    #             total_ing=ing+obj.cantidad
    #             opr.ingresos=total_ing
    #             opr.save()
    #             #Asiento en caso de devolucion de OP
    #
    #             tipo_producto_id = obj.producto.tipo_producto.id
    #
    #             try:
    #                 prod_d = TipoProducto.objects.get(id=int(tipo_producto_id))
    #             except TipoProducto.DoesNotExist:
    #                 prod_d = None
    #
    #             if prod_d:
    #                 try:
    #                     plan_deudora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_inventario_productos_proceso_id)
    #                 except PlanDeCuentas.DoesNotExist:
    #                     plan_deudora = None
    #
    #                 if plan_deudora:
    #                     asiento_detalle = AsientoDetalle()
    #                     asiento_detalle.asiento_id = int(asiento.asiento_id)
    #                     asiento_detalle.cuenta_id = plan_deudora.plan_id
    #                     asiento_detalle.debe = 0
    #                     asiento_detalle.haber = obj.total
    #                     asiento_detalle.concepto = 'Ingreso de Producto' + smart_str(obj.producto.descripcion_producto)
    #                     asiento_detalle.save()
    #
    #
    #
    #
    #
    #                 try:
    #                     plan_acreedora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_contable_id)
    #                 except PlanDeCuentas.DoesNotExist:
    #                     plan_acreedora = None
    #                 if plan_acreedora:
    #                     asiento_detalle = AsientoDetalle()
    #                     asiento_detalle.asiento_id = int(asiento.asiento_id)
    #                     asiento_detalle.cuenta_id = plan_acreedora.plan_id
    #                     asiento_detalle.debe = obj.total
    #                     asiento_detalle.haber = 0
    #                     asiento_detalle.concepto = 'Ingreso de Producto' + str(obj.producto.descripcion_producto.encode('utf8'))
    #                     asiento_detalle.save()
        
            
        # k=Kardex()
        # k.nro_documento =orden_ing.codigo
        # k.producto=obj.producto
        # k.cantidad=obj.cantidad
        # k.descripcion='Orden de Ingreso'
        # k.costo=obj.precio_compra
        # k.bodega=orden_ing.bodega
        # k.modulo=orden_ing.id
        # k.fecha_ingreso=fecha
        # k.save()
        # print('entro comoqw'+str(obj.producto_id))
        # try:
        #     objetose = ProductoEnBodega.objects.get(producto_id= obj.producto_id,bodega_id= orden_ing.bodega_id)
        # except ProductoEnBodega.DoesNotExist:
        #     objetose = None
        #
        # if objetose:
        #     cant=objetose.cantidad
        #     objetose.cantidad=cant+float(obj.cantidad)
        #     objetose.updated_at = datetime.now()
        #     objetose.updated_by = request.user.get_full_name()
        #     objetose.save()
        # else:
        #     k=ProductoEnBodega()
        #     cant=obj.cantidad
        #     k.cantidad =cant
        #     k.producto_id=obj.producto_id
        #     k.bodega_id=orden_ing.bodega_id
        #     k.created_by = request.user.get_full_name()
        #     k.updated_by = request.user.get_full_name()
        #     k.created_at = fecha
        #     k.updated_at = datetime.now()
        #     k.save()



    return HttpResponseRedirect('/ajustes/ajustesAprobar/')

@login_required()
def aprobarByPkView(request, pk):
    try:
        aprobar(request, pk, Ajustes)
    except Exception as e:
        #Tools.manejadorErrores(e)
        messages.error(request, 'Ocurrio un Error.')

    return HttpResponse('')

#=====================================================#
@login_required()
def aprobar(request, ids, Model):
    objetos = Model.objects.filter(id__in = ids)
    for obj in objetos:
        obj.aprobada = True
        obj.save()
#obj.delete()
    if not objetos:
        messages.error(request, 'Los Datos Predeterminados No Pueden ser Eliminados.')
        return 0
    return 1

# class IngresoOrdenIngresoListView(ObjectListView):
#     model = IngresoOrdenIngreso
#     paginate_by = 100
#     template_name = 'ingresoordeningreso/list.html'
#
#     context_object_name = 'ingresoordeningresos'
#
#     def get_context_data(self, **kwargs):
#         context = super(IngresoOrdenIngresoListView, self).get_context_data(**kwargs)
#         context['url_delete'] = reverse_lazy('ingresoordeningreso-delete')
#         return context

# @login_required()
# @transaction.atomic
# def IngresoOrdenIngresoCreateView(request):
#       if request.method == 'POST':
#         ingresos_orden_form=IngresoOrdenIngresoForm(request.POST)
#         productos = Producto.objects.all()
#
#         if ingresos_orden_form.is_valid():
#             with transaction.atomic():
#                 new_orden=ingresos_orden_form.save()
#                 new_orden.created_by = request.user.get_full_name()
#                 new_orden.updated_by = request.user.get_full_name()
#                 new_orden.created_at = datetime.now()
#                 new_orden.updated_at = datetime.now()
#                 new_orden.subtotal=request.POST["subtotal"]
#                 new_orden.iva=request.POST["iva"]
#                 new_orden.total=request.POST["total"]
#                 new_orden.orden_ingreso_id=request.POST["orden_ingreso_id"]
#                 new_orden.concepto=request.POST["concepto"]
#                 new_orden.save()
#                 objet= OrdenIngresoDetalle.objects.filter(orden_ingreso_id= request.POST["orden_ingreso_id"])
#                 for ob in objet:
#                     if ob.disminuir_kardex:
#                         ob.disminuir_kardex = True
#                         ob.save()
#
#                     else:
#                         if ob.despachar:
#                             ob.disminuir_kardex = True
#                             ob.save()
#                             k=Kardex()
#                             k.nro_documento =new_orden.codigo
#                             k.producto=ob.producto
#                             k.cantidad=ob.cantidad
#                             k.descripcion='Orden de Ingreso'
#                             k.costo=ob.precio_compra
#                            # k.bodega=new_orden.bodega
#                             k.modulo=new_orden.id
#                             k.fecha_ingreso=datetime.now()
#                             k.save()
#
#
#
#                 try:
#                     secuencial = Secuenciales.objects.get(modulo='ingresoordeningreso')
#                     secuencial.secuencial=secuencial.secuencial+1
#                     secuencial.created_by = request.user.get_full_name()
#                     secuencial.updated_by = request.user.get_full_name()
#                     secuencial.created_at = datetime.now()
#                     secuencial.updated_at = datetime.now()
#                     secuencial.save()
#                 except Secuenciales.DoesNotExist:
#                     secuencial = None
#
#                 return HttpResponseRedirect('/ordenIngreso/IngresoOrdenIngreso')
#         else:
#             print 'error'
#             print ingresos_orden_form.errors, len(ingresos_orden_form.errors)
#       else:
#         ingresos_orden_form=IngresoOrdenIngresoForm
#         productos = Producto.objects.all()
#
#
#       return render_to_response('ingresoordeningreso/create.html', { 'ingresos_orden_form': ingresos_orden_form,'productos':productos},  RequestContext(request))

# @login_required()
# @transaction.atomic
# def IngresoOrdenIngresoUpdateView(request,pk):
#     if request.method == 'POST':
#         ordeningreso=IngresoOrdenIngreso.objects.get(id=pk)
#         # orden=OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)
#         ingresoordeningreso_form=IngresoOrdenIngresoForm(request.POST,request.FILES,instance=ordeningreso)
#         print ingresoordeningreso_form.is_valid(), ingresoordeningreso_form.errors, type(ingresoordeningreso_form.errors)
#
#         if ingresoordeningreso_form.is_valid():
#             with transaction.atomic():
#                 new_orden=ingresoordeningreso_form.save()
#                 #new_orden.nro_fact_proveedor=request.POST["nro_fact_proveedor"]
#                 new_orden.save()
#                 objet= OrdenIngresoDetalle.objects.filter(orden_ingreso_id= request.POST["orden_ingreso_id"])
#
#                 for ob in objet:
#                     if ob.disminuir_kardex!=True and ob.despachar==True:
#                         ob.disminuir_kardex = True
#                         ob.save()
#                         k=Kardex()
#                         k.nro_documento =new_orden.codigo
#                         k.producto=ob.producto
#                         k.cantidad=ob.cantidad
#                         k.descripcion='Orden de Ingreso'
#                         k.costo=ob.precio_compra
#                         k.bodega=new_orden.bodega
#                         k.modulo=new_orden.id
#                         k.fecha_ingreso=datetime.now()
#                         k.save()
#
#                 contador=request.POST["columnas_receta"]
#                 print contador
#                 i=1
#
#                 print('El id de la compra'+str(pk))
#                 detalle = IngresoDetalle.objects.filter(orden_ingreso_id=new_orden.orden_ingreso_id)
#
#                 context = {
#                'section_title':'Actualizar Orden Ingreso',
#                 'button_text':'Actualizar',
#                 'ingresoordeningreso_form':ingresoordeningreso_form,
#                 'detalle':detalle,
#
#                  }
#
#
#                 return render_to_response(
#                     'ingresoordeningreso/actualizar.html',
#                     context,
#                     context_instance=RequestContext(request))
#         else:
#
#             ingresoordeningreso_form=IngresoOrdenIngresoForm(request.POST)
#             detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordencompra.orden_ingreso_id)
#
#             context = {
#             'section_title':'Actualizar Compras Locales',
#             'button_text':'Actualizar',
#             'ingresoordeningreso_form':ingresoordeningreso_form,
#             'detalle':detalle, }
#
#         return render_to_response(
#             'ingresoordeningreso/actualizar.html',
#             context,
#             context_instance=RequestContext(request))
#     else:
#         ordencompra=IngresoOrdenIngreso.objects.get(id=pk)
#         ingresoordeningreso_form=IngresoOrdenIngresoForm(instance=ordencompra)
#         detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordencompra.orden_ingreso_id)
#         orden=OrdenIngreso.objects.get(id=ordencompra.orden_ingreso_id)
#
#         context = {
#             'section_title':'Actualizar Orden Ingreso',
#             'button_text':'Actualizar',
#             'ingresoordeningreso_form':ingresoordeningreso_form,
#             'detalle':detalle,
#             'orden': orden, }
#
#         return render_to_response(
#             'ingresoordeningreso/actualizar.html',
#             context,
#             context_instance=RequestContext(request))

@login_required()
@transaction.atomic

def ajustesNuevoRecepcionByPkView(request,pk):
      if request.method == 'POST':
        ajustes_form=AjustesForm(request.POST)
        productos = Producto.objects.all()

        if ajustes_form.is_valid():
            with transaction.atomic():
                new_orden=ajustes_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                #new_orden.producto_terminado=True

                #ordenproduccionbodega = OrdenProduccionBodega.objects.get(id=pk)
                #ordenproduccionbodega.numero_orden_ingreso=new_orden.codigo
                #cant_sobr = ordenproduccionbodega.cantidad_recibida
                #ordenproduccionbodega.cantidad_sobrante = cant_sobr
                #ordenproduccionbodega.cantidad_despachada = 0
                #ordenproduccionbodega.save()

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ajustes')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                #contador=request.POST["columnas_receta"]
                # print contador
                # i=0
                # total = 0
                # while int(i)<=int(contador):
                #     i+= 1
                #     print('entro comoqw'+str(i))
                #     if int(i)> int(contador):
                #         print('entrosd')
                #         break
                #     else:
                #         if 'id_kits'+str(i) in request.POST:
                #
                #             product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                #             comprasdetalle=OrdenIngresoDetalle()
                #             comprasdetalle.orden_ingreso_id = new_orden.id
                #             comprasdetalle.producto_id=request.POST["id_kits"+str(i)]
                #             comprasdetalle.bodega_id=request.POST["bodega"]
                #             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                #             if ordenproduccionbodega.orden_produccion.pedido_detalle:
                #                 print('entro total' + str(total))
                #                 print('precio_compra' + str(ordenproduccionbodega.orden_produccion.pedido_detalle.precio_compra))
                #                 print('cantidad' + str(comprasdetalle.cantidad))
                #                 cant=float(comprasdetalle.cantidad)
                #                 precio=float(ordenproduccionbodega.orden_produccion.pedido_detalle.precio_compra)
                #                 total=cant*precio
                #                 comprasdetalle.precio_compra=cant*precio
                #             #kits.costo=float(request.POST["costo_kits1"])
                #             comprasdetalle.save()
                #
                #     print(i)
                #     print('contadorsd prueba'+str(contador))
                #

                #if ordenproduccionbodega.orden_produccion.pedido_detalle:
                #    new_orden.subtotal = total
                #    new_orden.total = total

                new_orden.save()
                return HttpResponseRedirect('/ajustes/ajustes/list/')
        else:
            print 'error'
            print ajustes_form.errors, len(ajustes_form.errors)
      else:
        ajustes_form=AjustesForm
        productos = Producto.objects.all()

        #ordenproduccionbodega = OrdenProduccionBodega.objects.filter(id=pk)
        #cliente=OrdenProduccionBodega.objects.get(id=pk)

      return render_to_response('ajustes/create.html', { 'ajustes_form': ajustes_form,'productos':productos},  RequestContext(request))


def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    ajustes=Ajustes.objects.get(id=pk)
    detalle =AjustesDetalle.objects.filter(ajustes=ajustes.id)

    html = render_to_string('ajustes/imprimir.html', {'pagesize':'A4','ajustes':ajustes,'detalle':detalle}, context_instance=RequestContext(request))
    return generar_pdf(html)


def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))




@login_required()
@transaction.atomic
def AjustesActualizarView(request, pk):
    if request.method == 'POST':
        ajustes_form = AjustesForm(request.POST)
        productos = Producto.objects.all()
        
        if ajustes_form.is_valid():
            with transaction.atomic():
                ajustes = Ajustes.objects.get(pk=pk)
                ajustes.comentario = ajustes_form.cleaned_data['comentario']
                ajustes.bodega = ajustes_form.cleaned_data['bodega']
                ajustes.concepto_ajustes = ajustes_form.cleaned_data['concepto_ajustes']
                ajustes.total = request.POST["total"]
                ajustes.fecha = ajustes_form.cleaned_data['fecha']
                ajustes.save()
    
                new_orden=ajustes.save()
    
                #contador=request.POST["columnas_receta"]
               
                # i=0
                # while int(i) <= int(contador):
                #     i+= 1
                #     if int(i) > int(contador):
                #         print('entrosd')
                #         break
                #     else:
                #         if 'id_kits'+str(i) in request.POST:
                #             product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                #
                #             if 'id_detalle'+str(i) in request.POST:
                #                 detallecompra = OrdenIngresoDetalle.objects.get(id=request.POST["id_detalle"+str(i)])
                #                 detallecompra.updated_by = request.user.get_full_name()
                #                 detallecompra.producto =product
                #                 detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                #                 detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                #                 detallecompra.total=request.POST["total_kits"+str(i)]
                #                 if 'areas_kits'+str(i) in request.POST:
                #                     detallecompra.areas_id=request.POST["areas_kits"+str(i)]
                #
                #                 if ordeningreso.concepto_orden_ingreso_id:
                #                     conceptoop=ConceptoOrdenIngreso.objects.get(id=ordeningreso.concepto_orden_ingreso_id)
                #                     if conceptoop.op == True:
                #                         if 'subopid_kits'+str(i) in request.POST:
                #                             detallecompra.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                #                             detallecompra.op=True
                #                 #detallecompra.updated_at = datetime.now()
                #                 #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                #                 detallecompra.save()
                #
                #                 print('Tiene detalle'+str(i))
                #             else:
                #                 comprasdetalle=OrdenIngresoDetalle()
                #                 comprasdetalle.orden_ingreso_id = ordeningreso.id
                #                 comprasdetalle.producto=product
                #                 comprasdetalle.bodega=ordeningreso.bodega
                #                 comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                #                 #kits.costo=float(request.POST["costo_kits1"])
                #                 comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                #                 comprasdetalle.total=request.POST["total_kits"+str(i)]
                #                 if 'areas_kits'+str(i) in request.POST:
                #                     comprasdetalle.areas_id=request.POST["areas_kits"+str(i)]
                #
                #                 conceptoop=ConceptoOrdenIngreso.objects.get(id=ordeningreso.concepto_orden_ingreso_id)
                #                 if conceptoop.op == True:
                #                     if 'subopid_kits'+str(i) in request.POST:
                #                         comprasdetalle.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                #                         comprasdetalle.op=True
                #                 comprasdetalle.save()
                #                 i+= 1
                #                 print('No Tiene detalle'+str(i))
                #                 print('contadorsd prueba'+str(contador))
                #ordencompra_form=OrdenCompraForm(request.POST)

                detalle = AjustesDetalle.objects.filter(orden_ingreso_id=pk)
                productos = Producto.objects.all()
                #areas=Areas.objects.all()
                concepto=ConceptoAjustes.objects.get(op=True)
    
    
               
                context = {
                'section_title':'Actualizar Ajustes',
                'button_text':'Actualizar',
                'ajustes_form':ajustes_form,
                'detalle':detalle,
                'productos':productos,
                'concepto':concepto,
                'mensaje':'Ajuste actualizado con exito'}
    
    
                return render_to_response(
                    'ajustes/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:
            ajustes_form=AjustesForm(request.POST)
            detalle = AjustesDetalle.objects.filter(ajustes_id=pk)
            productos = Producto.objects.all()
            #areas=Areas.objects.all()
            concepto=ConceptoAjustes.objects.get(op=True)
    
    
            context = {
                'section_title':'Actualizar Ajuste',
                'button_text':'Actualizar',
                'ajustes_form':ajustes_form,
                'detalle':detalle,
                #'areas':areas,
                'concepto':concepto,
                'mensaje':'Ajuste actualizado con exito'}
        
                
    
            return render_to_response(
                'ajustes/actualizar.html',
                context,
                context_instance=RequestContext(request))

    else:
        ajustes = Ajustes.objects.get(id=pk)
        productos = Producto.objects.all()
        ajustes_form=AjustesForm(instance=ajustes)
        detalle = AjustesDetalle.objects.filter(ajustes_id=ajustes.id)
        #areas=Areas.objects.all()
        concepto=ConceptoAjustes.objects.get(op=True)


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'ajustes_form':ajustes_form,
        'productos':productos,
        #'areas':areas,
        'concepto':concepto,
        'detalle':detalle
        }

        return render_to_response(
            'ajustes/actualizar.html', context,context_instance=RequestContext(request))


        
        
@login_required()
def ConceptoAjustesListView(request):
    conceptos = ConceptoAjustes.objects.all()
    
    return render_to_response('conceptosAjustes/index.html', {'conceptos': conceptos}, RequestContext(request))

class ConceptoAjustesCreateView(ObjectCreateView):
    model = ConceptoAjustes
    form_class = ConceptoAjustesForm
    template_name = 'conceptosAjustes/create.html'
    url_success = 'concepto-ajustes-list'
    url_success_other = 'concepto-ajustes-create'
    url_cancel = 'concepto-ajustes-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()


        return super(ConceptoAjustesCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo concepto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class ConceptoAjustesUpdateView(ObjectUpdateView):
    model = ConceptoAjustes
    form_class = ConceptoAjustesForm
    template_name = 'conceptosAjustes/create.html'
    url_success = 'concepto-ajustes-list'
    url_cancel = 'concepto-ajustes-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Conceptos actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



def corregirAjustesAsiento(request,pk):
    ajustes=Ajustes.objects.get(id=pk)
    fecha=ajustes.fecha
    codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
    secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
    asiento = Asiento()
    asiento.codigo_asiento = "AJ" + str(fecha.year)  + "000" + str(codigo_asiento)
    asiento.fecha = fecha
    asiento.glosa = 'Ajuste por '+str(ajustes.concepto_ajustes)+' de '+str(ajustes.codigo)
    asiento.modulo= 'Ajustes'
    asiento.total_debe=ajustes.subtotal
    asiento.total_haber=ajustes.subtotal
    asiento.secuencia_asiento = codigo_asiento
    asiento.gasto_no_deducible = False
    asiento.save()
    ajustes.asiento_id=asiento.asiento_id
    ajustes.save()
    objetose = AjustesDetalle.objects.filter(ajustes_id= pk)

        
    Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
    for obj in objetose:
        tipo_producto_id = obj.producto.tipo_producto.id
                
        try:
            prod_d = TipoProducto.objects.get(id=int(tipo_producto_id))
        except TipoProducto.DoesNotExist:
            prod_d = None

        if prod_d:
            try:
                plan_deudora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_inventario_productos_proceso_id)
            except PlanDeCuentas.DoesNotExist:
                plan_deudora = None
                                    
            if plan_deudora:
                asiento_detalle = AsientoDetalle()
                asiento_detalle.asiento_id = int(asiento.asiento_id)
                asiento_detalle.cuenta_id = plan_deudora.plan_id
                asiento_detalle.debe = 0
                asiento_detalle.haber = obj.total
                asiento_detalle.concepto = 'Ingreso de Producto' + smart_str(obj.producto.descripcion_producto)
                asiento_detalle.save()
                        
                                        
                                            

            try:
                plan_acreedora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_contable_id)
            except PlanDeCuentas.DoesNotExist:
                plan_acreedora = None
            if plan_acreedora:
                asiento_detalle = AsientoDetalle()
                asiento_detalle.asiento_id = int(asiento.asiento_id)
                asiento_detalle.cuenta_id = plan_acreedora.plan_id
                asiento_detalle.debe = obj.total
                asiento_detalle.haber = 0
                asiento_detalle.concepto = 'Ingreso de Producto' + str(obj.producto.descripcion_producto.encode('utf8'))
                asiento_detalle.save()
            

