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
from django.db import IntegrityError, transaction


@login_required()
def OrdenIngresoListView(request):
    ordenesingresos=OrdenIngreso.objects.all()

    return render_to_response('ordeningreso/list.html', {'ordenesingresos': ordenesingresos}, RequestContext(request))

#=====================================================#
class OrdenIngresoDetailView(ObjectDetailView):
    model = OrdenIngreso
    template_name = 'ordeningreso/detail.html'

#=====================================================#
@login_required()
@transaction.atomic
def OrdenIngresoCreateView(request):
      if request.method == 'POST':
        ordeningreso_form=OrdenIngresoForm(request.POST)
        productos = Producto.objects.all()

        if ordeningreso_form.is_valid():
            with transaction.atomic():
                new_orden=ordeningreso_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal=request.POST["total"]
                subtotal=request.POST["total"]
                impuesto_mont=float(request.POST["total"])*0.12
                new_orden.impuesto_monto=float(request.POST["total"])*0.12
                new_orden.total=round (float(subtotal)+float(impuesto_mont),2)

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordeningreso')
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
                            comprasdetalle=OrdenIngresoDetalle()
                            comprasdetalle.orden_ingreso_id = new_orden.id
                            comprasdetalle.producto_id=request.POST["id_kits"+str(i)]
                            comprasdetalle.bodega_id=request.POST["bodega"]
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            if 'areas_kits'+str(i) in request.POST:
                                comprasdetalle.areas_id=request.POST["areas_kits"+str(i)]
                            
                            conceptoop=ConceptoOrdenIngreso.objects.get(id=new_orden.concepto_orden_ingreso_id)
                            if conceptoop.op == True:
                                if 'subopid_kits'+str(i) in request.POST:
                                    comprasdetalle.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                    comprasdetalle.op=True
                            #kits.costo=float(request.POST["costo_kits1"])
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            comprasdetalle.total=request.POST["total_kits"+str(i)]
                            comprasdetalle.save()

                    print(i)
                    print('contadorsd prueba'+str(contador))

                return HttpResponseRedirect('/ordenIngreso/ordenIngreso')
        else:
            print 'error'
            print ordeningreso_form.errors, len(ordeningreso_form.errors)
      else:
        ordeningreso_form=OrdenIngresoForm
        productos = Producto.objects.all()
        areas=Areas.objects.all()
        concepto=ConceptoOrdenIngreso.objects.get(op=True)


      return render_to_response('ordeningreso/create.html', { 'ordeningreso_form': ordeningreso_form,'productos':productos,'areas':areas,'concepto':concepto},  RequestContext(request))

#=====================================================#
@login_required()
@transaction.atomic

def OrdenIngresoUpdateView(request,pk):
    if request.method == 'POST':
        ordeningreso=OrdenIngreso.objects.get(id=pk)
        ordeningreso_form=OrdenIngresoForm(request.POST,request.FILES,instance=ordeningreso)
        print ordeningreso_form.is_valid(), ordeningreso_form.errors, type(ordeningreso_form.errors)

        if ordeningreso_form.is_valid():
            with transaction.atomic():
                new_orden=ordeningreso_form.save()
                new_orden.save()


                contador=request.POST["columnas_receta"]
                print contador
                i=1
                while int(i) <= int(contador):

                    if int(i) > int(contador):
                        print('entrosd')
                        break
                    else:
                        product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                        detalle_id=request.POST["id_detalle"+str(i)]
                #         if detalle_id:
                #             detallecompra = ComprasDetalle.objects.get(compras_detalle_id=detalle_id)
                #             detallecompra.updated_by = request.user.get_full_name()
                #             #detallecompra.updated_at = datetime.now()

                #             detallecompra.save()
                #             nd=detallecompra.save()
                #             i+= 1
                #             print('entro holaaaa'+str(nd.compra_id))
                #             if 'recibido_kits'+str(i) in request.POST:
                #               print('entrorecibido')
                #               nd.recibido=request.POST["recibido_kits"+str(i)]
                #               nd.save()
                #               kardez = Kardex.objects.get(modulo=detalle_id)
                #               if kardez:
                #                   print('ya existe')
                #               else:
                #                   k=Kardex()
                #                   k.nro_documento =new_orden.nro_compra
                #                   k.producto=product
                #                   k.cantidad=nd.cantidad
                #                   k.descripcion='Orden de Compra'
                #                   k.costo=nd.precio_compra
                #                   k.bodega=new_orden.bodega
                #                   k.modulo=detalle_id
                #                   k.fecha_ingreso=datetime.now()
                #                   k.save()

                #         else:
                #             comprasdetalle=ComprasDetalle()
                #             comprasdetalle.compra_id = new_orden.compra_id
                #             comprasdetalle.producto=product
                #             comprasdetalle.proveedor=new_orden.proveedor
                #             comprasdetalle.bodega=new_orden.bodega
                #             comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                #             #kits.costo=float(request.POST["costo_kits1"])
                #             comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                #             comprasdetalle.total=request.POST["total_kits"+str(i)]
                #             comprasdetalle.save()
                #             i+= 1
                #             print('No Tiene detalle'+str(i))
                #             print('contadorsd prueba'+str(contador))
                # #ordencompra_form=OrdenCompraForm(request.POST)
                print('El id de la compra'+str(pk))
                detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=pk)
                areas=Areas.objects.all()
                concepto=ConceptoOrdenIngreso.objects.get(op=True)

                context = {
               'section_title':'Actualizar Orden Ingreso',
                'button_text':'Actualizar',
                'ordencompra_form':ordeningreso_form,
                'areas':areas,
                'concepto':concepto,
                'detalle':detalle }


                return render_to_response(
                    'ordeningreso/factura.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            ordeningreso_form=OrdenIngresoForm(request.POST)
            detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordeningreso.id)
            areas=Areas.objects.all()
            concepto=ConceptoOrdenIngreso.objects.get(op=True)

            context = {
            'section_title':'Actualizar Orden Ingreso',
            'button_text':'Actualizar',
            'ordeningreso_form':ordeningreso_form,
            'areas':areas,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ordeningreso/factura.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordeningreso=OrdenIngreso.objects.get(id=pk)
        ordeningreso_form=OrdenIngresoForm(instance=ordeningreso)
        detalle =OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordeningreso.id)
        areas=Areas.objects.all()
        concepto=ConceptoOrdenIngreso.objects.get(op=True)

        context = {
            'section_title':'Actualizar Orden Ingreso',
            'button_text':'Actualizar',
            'ordeningreso_form':ordeningreso_form,
            'areas':areas,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ordeningreso/factura.html',
            context,
            context_instance=RequestContext(request))



#=====================================================#
@login_required()
def ordeningresoEliminarView(request):
    return eliminarView(request, OrdenIngreso, 'ordeningreso-list')

#=====================================================#
@login_required()
def ordeningresoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, OrdenIngreso)

#MUEDIRSA
@login_required()
def OrdenIngresoListAprobarView(request):
    ordenesingresos=OrdenIngreso.objects.all()

    return render_to_response('ordeningreso/aprobada.html', {'ordenesingresos': ordenesingresos}, RequestContext(request))



#=====================================================#
@login_required()
def ordeningresoAprobarByPkView(request, pk):

    objetos = OrdenIngreso.objects.filter(id= pk)
    for obj in objetos:
        obj.aprobada = True
        obj.save()

    ol = OrdenIngreso.objects.get(id= pk)
    fecha=ol.fecha



    if ol.producto_terminado:
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        parametro_acreedora = Parametros.objects.get(clave='cuenta_acreedora_ingreso_inventario')
        parametro_deudora = Parametros.objects.get(clave='cuenta_deudora_ingreso_inventario')
        asiento = Asiento()
        asiento.codigo_asiento = "OI" + str(fecha.year) + "000" + str(codigo_asiento)
        asiento.fecha = fecha
        asiento.glosa = 'Orden Ingreso de Product. Terminado ' + str(ol.codigo)
        asiento.modulo= 'Orden Ingreso'
        asiento.gasto_no_deducible = False
        asiento.save()
        ol.asiento_id=asiento.asiento_id
        ol.save()

        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
        try:
            plan_deudora = PlanDeCuentas.objects.get(codigo_plan=parametro_deudora.valor)
        except PlanDeCuentas.DoesNotExist:
            plan_deudora = None
        if plan_deudora:
            asiento_detalle = AsientoDetalle()
            asiento_detalle.asiento_id = int(asiento.asiento_id)
            asiento_detalle.cuenta_id = plan_deudora.plan_id
            asiento_detalle.debe = ol.total
            asiento_detalle.haber = 0
            asiento_detalle.save()

        try:
            plan_acreedora = PlanDeCuentas.objects.get(codigo_plan=parametro_acreedora.valor)


        except PlanDeCuentas.DoesNotExist:
            plan_acreedora = None
        if plan_acreedora:
            asiento_detalle = AsientoDetalle()
            asiento_detalle.asiento_id = int(asiento.asiento_id)
            asiento_detalle.cuenta_id = plan_acreedora.plan_id
            asiento_detalle.debe = 0
            asiento_detalle.haber = ol.total
            asiento_detalle.save()


    
    try:
        op = OrdenProduccion.objects.get(codigo=ol.orden_produccion_codigo)
    except OrdenProduccion.DoesNotExist:
        op = None


    objetose = OrdenIngresoDetalle.objects.filter(orden_ingreso_id= pk)
    orden_ing = OrdenIngreso.objects.get(id= pk)
    conceptoop=ConceptoOrdenIngreso.objects.get(id=orden_ing.concepto_orden_ingreso_id)
    if conceptoop.op == True:
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        asiento = Asiento()
        asiento.codigo_asiento = "OI" + str(fecha.year)  + "000" + str(codigo_asiento)
        asiento.fecha = fecha
        asiento.glosa = 'Orden Ingreso por devolucion '+str(orden_ing.codigo)
        asiento.modulo= 'Orden Ingreso'
        asiento.total_debe=orden_ing.subtotal
        asiento.total_haber=orden_ing.subtotal
        asiento.secuencia_asiento = codigo_asiento
        asiento.gasto_no_deducible = False
        asiento.save()
        orden_ing.asiento_id=asiento.asiento_id
        orden_ing.save()
        
        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
    else:
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        asiento = Asiento()
        asiento.codigo_asiento = "OI" + str(fecha.year)  + "000" + str(codigo_asiento)
        asiento.fecha = fecha
        asiento.glosa = 'Orden Ingreso por '+str(ol.concepto_orden_ingreso)+' de '+str(orden_ing.codigo)
        asiento.modulo= 'Orden Ingreso'
        asiento.total_debe=orden_ing.subtotal
        asiento.total_haber=orden_ing.subtotal
        asiento.secuencia_asiento = codigo_asiento
        asiento.gasto_no_deducible = False
        asiento.save()
        orden_ing.asiento_id=asiento.asiento_id
        orden_ing.save()
        
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
            
        
        
    for obj in objetose:
        if op:
            try:
                opb = OrdenProduccionBodega.objects.get(producto_id=obj.producto_id, orden_produccion_id=op.id)
            except OrdenProduccionBodega.DoesNotExist:
                opb = None

            if opb:
                cant_sobr= opb.cantidad_recibida
                opb.ingresado_bodega=True
                opb.cantidad_sobrante = cant_sobr
                opb.cantidad_despachada = 0
                opb.bodega=orden_ing.bodega
                opb.save()
        if obj.op:
            try:
                opr = OrdenProduccionReceta.objects.get(id=obj.orden_produccion_receta_id)
            except OrdenProduccionReceta.DoesNotExist:
                opr = None
            if opr:
                if opr.ingresos:
                    ing=opr.ingresos
                else:
                    ing=0
                
                if ing == '' or  ing == 'None':
                    ing=0
                total_ing=ing+obj.cantidad
                opr.ingresos=total_ing
                opr.save()
                #Asiento en caso de devolucion de OP
                
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
        
            
        k=Kardex()
        k.nro_documento =orden_ing.codigo
        k.producto=obj.producto
        k.cantidad=obj.cantidad
        k.descripcion='Orden de Ingreso'
        k.costo=obj.precio_compra
        k.bodega=orden_ing.bodega
        k.modulo=orden_ing.id
        k.fecha_ingreso=fecha
        k.save()
        print('entro comoqw'+str(obj.producto_id))
        try:
            objetose = ProductoEnBodega.objects.get(producto_id= obj.producto_id,bodega_id= orden_ing.bodega_id)
        except ProductoEnBodega.DoesNotExist:
            objetose = None

        if objetose:
            cant=objetose.cantidad
            objetose.cantidad=cant+float(obj.cantidad)
            objetose.updated_at = datetime.now()
            objetose.updated_by = request.user.get_full_name()
            objetose.save()
        else:
            k=ProductoEnBodega()
            cant=obj.cantidad
            k.cantidad =cant
            k.producto_id=obj.producto_id
            k.bodega_id=orden_ing.bodega_id
            k.created_by = request.user.get_full_name()
            k.updated_by = request.user.get_full_name()
            k.created_at = fecha
            k.updated_at = datetime.now()
            k.save()



    return HttpResponseRedirect('/ordenIngreso/ordenIngresoAprobar/')

@login_required()
def aprobarByPkView(request, pk):
    try:
        aprobar(request, pk, OrdenIngreso)
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

class IngresoOrdenIngresoListView(ObjectListView):
    model = IngresoOrdenIngreso
    paginate_by = 100
    template_name = 'ingresoordeningreso/list.html'

    context_object_name = 'ingresoordeningresos'

    def get_context_data(self, **kwargs):
        context = super(IngresoOrdenIngresoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('ingresoordeningreso-delete')
        return context

@login_required()
@transaction.atomic
def IngresoOrdenIngresoCreateView(request):
      if request.method == 'POST':
        ingresos_orden_form=IngresoOrdenIngresoForm(request.POST)
        productos = Producto.objects.all()

        if ingresos_orden_form.is_valid():
            with transaction.atomic():
                new_orden=ingresos_orden_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal=request.POST["subtotal"]
                new_orden.iva=request.POST["iva"]
                new_orden.total=request.POST["total"]
                new_orden.orden_ingreso_id=request.POST["orden_ingreso_id"]
                new_orden.concepto=request.POST["concepto"]
                new_orden.save()
                objet= OrdenIngresoDetalle.objects.filter(orden_ingreso_id= request.POST["orden_ingreso_id"])
                for ob in objet:
                    if ob.disminuir_kardex:
                        ob.disminuir_kardex = True
                        ob.save()

                    else:
                        if ob.despachar:
                            ob.disminuir_kardex = True
                            ob.save()
                            k=Kardex()
                            k.nro_documento =new_orden.codigo
                            k.producto=ob.producto
                            k.cantidad=ob.cantidad
                            k.descripcion='Orden de Ingreso'
                            k.costo=ob.precio_compra
                           # k.bodega=new_orden.bodega
                            k.modulo=new_orden.id
                            k.fecha_ingreso=datetime.now()
                            k.save()



                try:
                    secuencial = Secuenciales.objects.get(modulo='ingresoordeningreso')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                return HttpResponseRedirect('/ordenIngreso/IngresoOrdenIngreso')
        else:
            print 'error'
            print ingresos_orden_form.errors, len(ingresos_orden_form.errors)
      else:
        ingresos_orden_form=IngresoOrdenIngresoForm
        productos = Producto.objects.all()


      return render_to_response('ingresoordeningreso/create.html', { 'ingresos_orden_form': ingresos_orden_form,'productos':productos},  RequestContext(request))

@login_required()
@transaction.atomic
def IngresoOrdenIngresoUpdateView(request,pk):
    if request.method == 'POST':
        ordeningreso=IngresoOrdenIngreso.objects.get(id=pk)
        # orden=OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)
        ingresoordeningreso_form=IngresoOrdenIngresoForm(request.POST,request.FILES,instance=ordeningreso)
        print ingresoordeningreso_form.is_valid(), ingresoordeningreso_form.errors, type(ingresoordeningreso_form.errors)

        if ingresoordeningreso_form.is_valid():
            with transaction.atomic():
                new_orden=ingresoordeningreso_form.save()
                #new_orden.nro_fact_proveedor=request.POST["nro_fact_proveedor"]
                new_orden.save()
                objet= OrdenIngresoDetalle.objects.filter(orden_ingreso_id= request.POST["orden_ingreso_id"])

                for ob in objet:
                    if ob.disminuir_kardex!=True and ob.despachar==True:
                        ob.disminuir_kardex = True
                        ob.save()
                        k=Kardex()
                        k.nro_documento =new_orden.codigo
                        k.producto=ob.producto
                        k.cantidad=ob.cantidad
                        k.descripcion='Orden de Ingreso'
                        k.costo=ob.precio_compra
                        k.bodega=new_orden.bodega
                        k.modulo=new_orden.id
                        k.fecha_ingreso=datetime.now()
                        k.save()

                contador=request.POST["columnas_receta"]
                print contador
                i=1

                print('El id de la compra'+str(pk))
                detalle = IngresoDetalle.objects.filter(orden_ingreso_id=new_orden.orden_ingreso_id)

                context = {
               'section_title':'Actualizar Orden Ingreso',
                'button_text':'Actualizar',
                'ingresoordeningreso_form':ingresoordeningreso_form,
                'detalle':detalle,

                 }


                return render_to_response(
                    'ingresoordeningreso/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            ingresoordeningreso_form=IngresoOrdenIngresoForm(request.POST)
            detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordencompra.orden_ingreso_id)

            context = {
            'section_title':'Actualizar Compras Locales',
            'button_text':'Actualizar',
            'ingresoordeningreso_form':ingresoordeningreso_form,
            'detalle':detalle, }

        return render_to_response(
            'ingresoordeningreso/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordencompra=IngresoOrdenIngreso.objects.get(id=pk)
        ingresoordeningreso_form=IngresoOrdenIngresoForm(instance=ordencompra)
        detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordencompra.orden_ingreso_id)
        orden=OrdenIngreso.objects.get(id=ordencompra.orden_ingreso_id)

        context = {
            'section_title':'Actualizar Orden Ingreso',
            'button_text':'Actualizar',
            'ingresoordeningreso_form':ingresoordeningreso_form,
            'detalle':detalle,
            'orden': orden, }

        return render_to_response(
            'ingresoordeningreso/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@transaction.atomic

def ordeningresoNuevoRecepcionByPkView(request,pk):
      if request.method == 'POST':
        ordeningreso_form=OrdenIngresoForm(request.POST)
        productos = Producto.objects.all()

        if ordeningreso_form.is_valid():
            with transaction.atomic():
                new_orden=ordeningreso_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.producto_terminado=True

                ordenproduccionbodega = OrdenProduccionBodega.objects.get(id=pk)
                ordenproduccionbodega.numero_orden_ingreso=new_orden.codigo
                cant_sobr = ordenproduccionbodega.cantidad_recibida
                ordenproduccionbodega.cantidad_sobrante = cant_sobr
                ordenproduccionbodega.cantidad_despachada = 0
                ordenproduccionbodega.save()

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordeningreso')
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
                total = 0
                while int(i)<=int(contador):
                    i+= 1
                    print('entro comoqw'+str(i))
                    if int(i)> int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits'+str(i) in request.POST:

                            product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                            comprasdetalle=OrdenIngresoDetalle()
                            comprasdetalle.orden_ingreso_id = new_orden.id
                            comprasdetalle.producto_id=request.POST["id_kits"+str(i)]
                            comprasdetalle.bodega_id=request.POST["bodega"]
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                            if ordenproduccionbodega.orden_produccion.pedido_detalle:
                                print('entro total' + str(total))
                                print('precio_compra' + str(ordenproduccionbodega.orden_produccion.pedido_detalle.precio_compra))
                                print('cantidad' + str(comprasdetalle.cantidad))
                                cant=float(comprasdetalle.cantidad)
                                precio=float(ordenproduccionbodega.orden_produccion.pedido_detalle.precio_compra)
                                total=cant*precio
                                comprasdetalle.precio_compra=cant*precio
                            #kits.costo=float(request.POST["costo_kits1"])
                            comprasdetalle.save()

                    print(i)
                    print('contadorsd prueba'+str(contador))


                if ordenproduccionbodega.orden_produccion.pedido_detalle:
                    new_orden.subtotal = total
                    new_orden.total = total

                new_orden.save()
                return HttpResponseRedirect('/subordenproduccion/recepcionBodega/list/')
        else:
            print 'error'
            print ordeningreso_form.errors, len(ordeningreso_form.errors)
      else:
        ordeningreso_form=OrdenIngresoForm
        productos = Producto.objects.all()

        ordenproduccionbodega = OrdenProduccionBodega.objects.filter(id=pk)
        cliente=OrdenProduccionBodega.objects.get(id=pk)

      return render_to_response('ordeningreso/create_bodega.html', { 'ordeningreso_form': ordeningreso_form,'productos':productos,'ordenproduccionbodega':ordenproduccionbodega,"cliente":cliente},  RequestContext(request))


def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    orden=OrdenIngreso.objects.get(id=pk)
    detalle =OrdenIngresoDetalle.objects.filter(orden_ingreso_id=orden.id)

    html = render_to_string('ordeningreso/imprimir.html', {'pagesize':'A4','orden':orden,'detalle':detalle}, context_instance=RequestContext(request))
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
def OrdenIngresoActualizarView(request, pk):
    if request.method == 'POST':
        ordeningreso_form = OrdenIngresoForm(request.POST)
        productos = Producto.objects.all()
        
        if ordeningreso_form.is_valid():
            with transaction.atomic():
                ordeningreso = OrdenIngreso.objects.get(pk=pk)
                ordeningreso.comentario = ordeningreso_form.cleaned_data['comentario']
                ordeningreso.notas = ordeningreso_form.cleaned_data['notas']
                ordeningreso.bodega = ordeningreso_form.cleaned_data['bodega']
                ordeningreso.concepto_orden_ingreso = ordeningreso_form.cleaned_data['concepto_orden_ingreso']
                ordeningreso.total = request.POST["total23"]
                ordeningreso.fecha = ordeningreso_form.cleaned_data['fecha']
                ordeningreso.save()
    
                new_orden=ordeningreso.save()
    
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
                                detallecompra = OrdenIngresoDetalle.objects.get(id=request.POST["id_detalle"+str(i)])
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.producto =product
                                detallecompra.cantidad=request.POST["cantidad_kits"+str(i)]
                                detallecompra.precio_compra=request.POST["costo_kits"+str(i)]
                                detallecompra.total=request.POST["total_kits"+str(i)]
                                if 'areas_kits'+str(i) in request.POST:
                                    detallecompra.areas_id=request.POST["areas_kits"+str(i)]
                                
                                if ordeningreso.concepto_orden_ingreso_id:
                                    conceptoop=ConceptoOrdenIngreso.objects.get(id=ordeningreso.concepto_orden_ingreso_id)
                                    if conceptoop.op == True:
                                        if 'subopid_kits'+str(i) in request.POST:
                                            detallecompra.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                            detallecompra.op=True
                                #detallecompra.updated_at = datetime.now()
                                #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                                detallecompra.save()
                                
                                print('Tiene detalle'+str(i))
                            else:
                                comprasdetalle=OrdenIngresoDetalle()
                                comprasdetalle.orden_ingreso_id = ordeningreso.id
                                comprasdetalle.producto=product
                                comprasdetalle.bodega=ordeningreso.bodega
                                comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                                #kits.costo=float(request.POST["costo_kits1"])
                                comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                                comprasdetalle.total=request.POST["total_kits"+str(i)]
                                if 'areas_kits'+str(i) in request.POST:
                                    comprasdetalle.areas_id=request.POST["areas_kits"+str(i)]
                                
                                conceptoop=ConceptoOrdenIngreso.objects.get(id=ordeningreso.concepto_orden_ingreso_id)
                                if conceptoop.op == True:
                                    if 'subopid_kits'+str(i) in request.POST:
                                        comprasdetalle.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                        comprasdetalle.op=True
                                comprasdetalle.save()
                                i+= 1
                                print('No Tiene detalle'+str(i))
                                print('contadorsd prueba'+str(contador))
                #ordencompra_form=OrdenCompraForm(request.POST)
                detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=pk)
                productos = Producto.objects.all()
                areas=Areas.objects.all()
                concepto=ConceptoOrdenIngreso.objects.get(op=True)
    
    
               
                context = {
               'section_title':'Actualizar Orden Compra1',
                'button_text':'Actualizar',
                'ordeningreso_form':ordeningreso_form,
                'detalle':detalle,
                'productos':productos,
                'areas':areas,
                'concepto':concepto,
                'mensaje':'Orden de Ingreso actualizada con exito'}
    
    
                return render_to_response(
                    'ordeningreso/actualizar.html', 
                    context,
                    context_instance=RequestContext(request))
        else:
            ordeningreso_form=OrdenIngresoForm(request.POST)
            detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=pk)
            productos = Producto.objects.all()
            areas=Areas.objects.all()
            concepto=ConceptoOrdenIngreso.objects.get(op=True)
    
    
            context = {
                'section_title':'Actualizar Orden Compra2',
                'button_text':'Actualizar',
                'ordeningreso_form':ordeningreso_form,
                'detalle':detalle,
                'areas':areas,
                'concepto':concepto,
                'mensaje':'Orden de Compra actualizada con exito'}
        
                
    
            return render_to_response(
                'ordeningreso/actualizar.html', 
                context,
                context_instance=RequestContext(request))

    else:
        ordencompra = OrdenIngreso.objects.get(id=pk)
        productos = Producto.objects.all()
        ordeningreso_form=OrdenIngresoForm(instance=ordencompra)  
        detalle = OrdenIngresoDetalle.objects.filter(orden_ingreso_id=ordencompra.id)
        areas=Areas.objects.all()
        concepto=ConceptoOrdenIngreso.objects.get(op=True)


        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'ordeningreso_form':ordeningreso_form,
        'productos':productos,
        'areas':areas,
        'concepto':concepto,
        'detalle':detalle
        }

        return render_to_response(
            'ordeningreso/actualizar.html', context,context_instance=RequestContext(request))


        
        
@login_required()
def ConceptoOrdenIngresoListView(request):
    conceptos = ConceptoOrdenIngreso.objects.all()
    
    return render_to_response('conceptosIngreso/index.html', {'conceptos': conceptos}, RequestContext(request))

class ConceptoOrdenIngresoCreateView(ObjectCreateView):
    model = ConceptoOrdenIngreso
    form_class = ConceptoOrdenIngresoForm
    template_name = 'conceptosIngreso/create.html'
    url_success = 'concepto-orden-ingreso-list'
    url_success_other = 'concepto-orden-ingreso-create'
    url_cancel = 'concepto-orden-ingreso-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()


        return super(ConceptoOrdenIngresoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo concepto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class ConceptoOrdenIngresoUpdateView(ObjectUpdateView):
    model = ConceptoOrdenIngreso
    form_class = ConceptoOrdenIngresoForm
    template_name = 'conceptosIngreso/create.html'
    url_success = 'concepto-orden-ingreso-list'
    url_cancel = 'concepto-orden-ingreso-list'


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



def corregirOrdenIngresoAsiento(request,pk):
    ordeningreso=OrdenIngreso.objects.get(id=pk)
    fecha=ordeningreso.fecha
    codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
    secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
    asiento = Asiento()
    asiento.codigo_asiento = "OI" + str(fecha.year)  + "000" + str(codigo_asiento)
    asiento.fecha = fecha
    asiento.glosa = 'Orden Ingreso por '+str(ordeningreso.concepto_orden_ingreso)+' de '+str(ordeningreso.codigo)
    asiento.modulo= 'Orden Ingreso'
    asiento.total_debe=ordeningreso.subtotal
    asiento.total_haber=ordeningreso.subtotal
    asiento.secuencia_asiento = codigo_asiento
    asiento.gasto_no_deducible = False
    asiento.save()
    ordeningreso.asiento_id=asiento.asiento_id
    ordeningreso.save()
    objetose = OrdenIngresoDetalle.objects.filter(orden_ingreso_id= pk)

        
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
            

