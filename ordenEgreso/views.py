# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView,anularByPkView
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
#from login.lib.tools import Tools
from inventario.models import *
from config.models import *
# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.utils.encoding import smart_str

from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes

from ordenproduccion.models import *
from subordenproduccion.models import *

from login.lib.tools import Tools
from django.contrib import auth

from django.db import IntegrityError, transaction
from django.db import connection, transaction
#now = datetime.datetime.now()

#   import easygui as eg

@login_required()
def ConceptoOrdenEgresoListView(request):
    if request.method == 'POST':
        conceptos = ConceptoOrdenEgreso.objects.all()
        return render_to_response('conceptos/index.html', {'conceptos': conceptos}, RequestContext(request))
    else:
        conceptos = ConceptoOrdenEgreso.objects.all()
        return render_to_response('conceptos/index.html', {'conceptos': conceptos}, RequestContext(request))

class ConceptoOrdenEgresoCreateView(ObjectCreateView):
    model = ConceptoOrdenEgreso
    form_class = ConceptoOrdenEgresoForm
    template_name = 'conceptos/create.html'
    url_success = 'concepto-orden-egreso-list'
    url_success_other = 'concepto-orden-egreso-create'
    url_cancel = 'concepto-orden-egreso-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()


        return super(ConceptoOrdenEgresoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo concepto."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class ConceptoOrdenEgresoUpdateView(ObjectUpdateView):
    model = ConceptoOrdenEgreso
    form_class = ConceptoOrdenEgresoForm
    template_name = 'conceptos/create.html'
    url_success = 'concepto-orden-egreso-list'
    url_cancel = 'concepto-orden-egreso-list'


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

@login_required()
def OrdenEgresoListView(request):
    if request.method == 'POST':
        #ordenesegresos = OrdenEgreso.objects.all()
        return render_to_response('ordenegreso/list.html', {}, RequestContext(request))
    else:
        #ordenesegresos = OrdenEgreso.objects.all()
        return render_to_response('ordenegreso/list.html', {}, RequestContext(request))

# @login_required()
# def OrdenEgresoRevListView(request):
#     if request.method == 'POST':
#         ordenesegresos = OrdenEgreso.objects.filter(aprobada=True)
#         return render_to_response('ordenegreso/revaprobacion.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
#     else:
#         ordenesegresos = OrdenEgreso.objects.all()
#         return render_to_response('ordenegreso/revaprobacion.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))


# def OrdenEgresoListAprobarView(request):
#     if request.method == 'POST':
#         ordenesegresos = OrdenEgreso.objects.all()
#         return render_to_response('ordenegreso/aprobada.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
#     else:
#         ordenesegresos = OrdenEgreso.objects.all()
#         return render_to_response('ordenegreso/aprobada.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))


@login_required()
def OrdenEgresoListHistoricoView(request):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.id,p.codigo,p.notas,p.total,p.fecha,p.aprobada,p.anulado,t.id as egreso_orden_egreso from orden_egreso p LEFT JOIN egreso_orden_egreso t ON p.id=t.orden_egreso_id ")
    ordenesegresos = cursor.fetchall()

    return render_to_response('ordenegreso/list_historico.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))


#=====================================================#
class OrdenEgresoDetailView(ObjectDetailView):
    model = OrdenEgreso
    template_name = 'ordenegreso/detail.html'

#=====================================================#
@login_required()
@transaction.atomic

def OrdenEgresoCreateView(request):
      if request.method == 'POST':
        ordenegreso_form=OrdenEgresoForm(request.POST)
        #productos = Producto.objects.all()
        p = OrdenProduccionReceta.objects.all()
        iva = Parametros.objects.get(clave='iva')
        iva_valor=float(iva.valor)
        #tot_form= Parametros.objects.get(clave='total')


        if ordenegreso_form.is_valid():
            #if ordenegreso_form.total > 0:
            #    transaccion = 1

            with transaction.atomic():

                new_orden=ordenegreso_form.save()

                #ordenegreso_form.error_class

                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal=request.POST["total"]
                try:
                    concepto = ConceptoOrdenEgreso.objects.get(id=new_orden.concepto_orden_egreso_id)
                except ConceptoOrdenEgreso.DoesNotExist:
                    concepto = None
                if concepto:
                    new_orden.notas=concepto.nombre
                subtotal=request.POST["total"]
                impuesto_mont=float(request.POST["total"])*iva_valor/100
                new_orden.impuesto_monto=float(request.POST["total"])*iva_valor/100
                new_orden.total=round (float(subtotal)+float(impuesto_mont),2)

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='ordenegreso')
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                contador=request.POST["columnas_receta"]
                print contador
                i=0
                while int(i)<=int(contador):
                    i+= 1
                    print('entro como qw'+str(i))
                    if int(i)> int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits'+str(i) in request.POST:
                            
                            product=Producto.objects.get(producto_id=request.POST["id_kits"+str(i)])
                            mensaje="El id"+str(i)+" entro con el id_kits"
                            # mensaje="El id"+str(i)+" entro con el id_kits"+str(product.descripcion_producto)
                            # print mensaje
                            comprasdetalle=OrdenEgresoDetalle()
                            comprasdetalle.orden_egreso_id = new_orden.id
                            comprasdetalle.producto_id=request.POST["id_kits"+str(i)]
                            comprasdetalle.bodega_id=request.POST["bodega"]
                            comprasdetalle.cantidad=request.POST["cantidad_kits"+str(i)]
                                #kits.costo=float(request.POST["costo_kits1"])
                            comprasdetalle.precio_compra=request.POST["costo_kits"+str(i)]
                            if 'areas_kits'+str(i) in request.POST:
                                comprasdetalle.areas_id=request.POST["areas_kits"+str(i)]
                            
                            conceptoop=ConceptoOrdenEgreso.objects.get(id=new_orden.concepto_orden_egreso_id)
                            if conceptoop.op == True:
                                if 'subopid_kits'+str(i) in request.POST:
                                    comprasdetalle.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                    comprasdetalle.op=True
                            comprasdetalle.created_by = request.user.get_full_name()
                            comprasdetalle.updated_by = request.user.get_full_name()
                            comprasdetalle.created_at = datetime.now()
                            comprasdetalle.updated_at = datetime.now()
                            if 'medida_kits' + str(i) in request.POST:
                                comprasdetalle.unidad_medida=request.POST["medida_kits"+str(i)]
                            if 'total_kits' + str(i) in request.POST:
                                comprasdetalle.total=request.POST["total_kits"+str(i)]
                            comprasdetalle.save()
                            print comprasdetalle.id
                        else:
                            print('hola')
                            mensaje="NO ENTRO El id"+str(i)+" entro con el id_kits"
                            print mensaje

                return HttpResponseRedirect('/ordenEgreso/OrdenEgreso')
        else:
            cursor = connection.cursor()
            query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad, pb.cantidad ' #- coalesce(od.unidades, 0) saldo '
            query += 'from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) '
            #query += 'left join requisiciones_pendientes od ON (pb.producto_id = od.producto_id)  '
            query += 'where pb.bodega_id=1 '
            #Editado
            #query += 'and pb.cantidad>0 '
            #query += 'group by p.producto_id, p.producto_id, p.codigo_producto, p.descripcion_producto, p.medida_peso, p.costo_promedio, p.unidad, pb.cantidad '
            query += 'order by p.producto_id;'
            cursor.execute(query)
            productos_bodega = cursor.fetchall()
            #print 'error'
            print ordenegreso_form.errors, len(ordenegreso_form.errors)
      else:
          #Aqui Carga la tabla de Productos por Bodega
        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad, pb.cantidad ' #- coalesce(od.unidades, 0) saldo '
        query += 'from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) '
        #query += 'left join requisiciones_pendientes od ON (pb.producto_id = od.producto_id) '
        query += 'where  pb.bodega_id=1 '
        #Editado
        # query += 'and pb.cantidad>0 '
        #query += 'group by p.producto_id, p.producto_id, p.codigo_producto, p.descripcion_producto, p.medida_peso, p.costo_promedio, p.unidad, pb.cantidad '
        query += 'order by p.producto_id;'
        cursor.execute(query)
        productos_bodega = cursor.fetchall()
        ordenegreso_form=OrdenEgresoForm
        
        #query2 = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.descripcion_producto,opr.cantidad,a.id,a.descripcion from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id left join orden_produccion o ON o.id=subop.orden_produccion_id left join areas a ON a.id=subop.areas_id where o.finalizada is not True order by o.id;'
        #cursor.execute(query2)
        #p = cursor.fetchall()
        areas=Areas.objects.filter(activo=True)
        concepto=ConceptoOrdenEgreso.objects.get(op=True)
        #p = OrdenProduccionReceta.objects.values('id', 'producto_id', 'cantidad', 'suborden_produccion_id','areas_id').all()

      return render_to_response('ordenegreso/create.html', { 'ordenegreso_form': ordenegreso_form,'productos_bodega':productos_bodega,'areas': areas,'concepto':concepto},  RequestContext(request))

      #return render_to_response('ordenegreso/create.html', { 'ordenegreso_form': ordenegreso_form,'ordenproduccionreceta':p,'productos_bodega':productos_bodega,'areas': areas,'concepto':concepto},  RequestContext(request))

#=====================================================#
@login_required()
def OrdenEgresoUpdateView(request,pk):
    if request.method == 'POST':
    	ordenegreso=OrdenEgreso.objects.get(id=pk)
        ordenegreso_form=OrdenEgresoForm(request.POST,request.FILES,instance=ordenegreso)
        print ordenegreso_form.is_valid(), ordenegreso_form.errors, type(ordenegreso_form.errors)

        if ordenegreso_form.is_valid():
            new_orden=ordenegreso_form.save()
            new_orden.save()
            try:
                concepto = ConceptoOrdenEgreso.objects.get(id=new_orden.concepto_orden_egreso_id)
                   
            except ConceptoOrdenEgreso.DoesNotExist:
                    concepto = None
            if concepto:
                new_orden.notas=concepto.nombre
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
            #             	print('entrorecibido')
            #             	nd.recibido=request.POST["recibido_kits"+str(i)]
            #             	nd.save()
            #             	kardez = Kardex.objects.get(modulo=detalle_id)
            #             	if kardez:
            #             		print('ya existe')
            #             	else:
            #             		k=Kardex()
            #             		k.nro_documento =new_orden.nro_compra
            #             		k.producto=product
            #             		k.cantidad=nd.cantidad
            #             		k.descripcion='Orden de Compra'
            #             		k.costo=nd.precio_compra
            #             		k.bodega=new_orden.bodega
            #             		k.modulo=detalle_id
            #             		k.fecha_ingreso=datetime.now()
            #             		k.save()

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
            detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=pk)
            areas=Areas.objects.all()
            concepto=ConceptoOrdenEgreso.objects.get(op=True)


            context = {
            'section_title':'Actualizar Orden Egreso',
            'button_text':'Actualizar',
            'areas': areas,
            'concepto':concepto,
            'ordencompra_form':ordenegreso_form,
            'detalle':detalle }


            return render_to_response(
                'ordenegreso/factura.html',
                context,
                context_instance=RequestContext(request))
        else:

            ordenegreso_form=OrdenEgresoForm(request.POST)
            detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)
            areas=Areas.objects.all()
            concepto=ConceptoOrdenEgreso.objects.get(op=True)


            context = {
            'section_title':'Actualizar Orden Egreso',
            'button_text':'Actualizar',
            'ordenegreso_form':ordenegreso_form,
            'areas': areas,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ordenegreso/factura.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenegreso=OrdenEgreso.objects.get(id=pk)
        ordenegreso_form=OrdenEgresoForm(instance=ordenegreso)
        detalle =OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)
        areas=Areas.objects.all()
        concepto=ConceptoOrdenEgreso.objects.get(op=True)

        context = {
            'section_title':'Actualizar Orden Egreso',
            'button_text':'Actualizar',
            'ordenegreso_form':ordenegreso_form,
            'areas': areas,
            'concepto':concepto,
            'detalle':detalle }

        return render_to_response(
            'ordenegreso/factura.html',
            context,
            context_instance=RequestContext(request))


#=====================================================#
@login_required()
def ordenegresoEliminarView(request):
    return anularByPkView(request, OrdenEgreso, 'ordenegreso-list')

#=====================================================#
@login_required()
def ordenegresoEliminarByPkView(request, pk):
    return anularByPkView(request, pk, OrdenEgreso, 'ordenegreso-list')

#MUEDIRSA
def OrdenEgresoListAprobarView(request):
    if request.method == 'POST':

        ordenesegresos = OrdenEgreso.objects.all()
        return render_to_response('ordenegreso/aprobada.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
    else:
        ordenesegresos = OrdenEgreso.objects.all()
        return render_to_response('ordenegreso/aprobada.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))

#=====================================================#
#NUEVO
def OrdenEgresoListReversarView(request):
    if request.method == 'POST':

        ordenesegresos = OrdenEgreso.objects.all()
        #return render_to_response('ordenegreso/list2.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
        return render_to_response('ordenegreso/listreversa.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
    else:
        ordenesegresos = OrdenEgreso.objects.all()

        #return render_to_response('ordenegreso/list2.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))
        return render_to_response('ordenegreso/listreversa.html', {'ordenesegresos': ordenesegresos}, RequestContext(request))



#=====================================================#
@login_required()
def ordenegresoAprobarByPkView(request, pk):

    cursor = connection.cursor()
    objetos = OrdenEgreso.objects.filter(id= pk)
    lAprobar = True
    for obj in objetos:
        oIdOrden = obj.id
        oBod = obj.bodega.id
        Error = 0
        lcSql = 'select A.orden_egreso_id, A.producto_id, A.cantidad, B.cantidad stock '
        lcSql += 'from orden_egreso_detalle A '
        lcSql += 'left join producto_en_bodega B on (A.producto_id = B.producto_id) '
        lcSql += 'where A.orden_egreso_id = ' + str(oIdOrden) + ' and B.bodega_id = ' + str(oBod)
        cursor.execute(lcSql)
        saldos = cursor.fetchall()

        for sSku in saldos:
            oCanti = 0
            oStock = 0
            if sSku[2]:
                oCanti = sSku[2]
            if sSku[3]:
                oStock = sSku[3]

            if oCanti>oStock:
                Error = Error + 1
                break

    Error = 0
    if Error == 0:
        obj.aprobada = True
        obj.aprobado_por = request.user.get_full_name()
        obj.aprobado_at = datetime.now()
        obj.save()
        return HttpResponseRedirect('/ordenEgreso/OrdenEgresoAprobar')
    else:
        obj.aprobada = False
        obj.save()
        messages.error(request, 'Ocurrió un Error. Stock Insuficiente para Aprobar ')
        return HttpResponseRedirect('/ordenEgreso/error500')

@login_required()
def ordenegresoReversarByPkView(request, pk):

    cursor = connection.cursor()
    objetos = OrdenEgreso.objects.filter(id= pk)
    lAprobar = True
    for obj in objetos:
        oIdOrden = obj.id
        oBod = obj.bodega.id
        lcSql = "select orden_egreso_id, count(*) TotLineas, sum (case when disminuir_kardex = 't' then 1 else 0 end ) LinDesp "
        lcSql += "from orden_egreso_detalle  "
        lcSql += "where orden_egreso_id = " + str(oIdOrden) + " and bodega_id = " + str(oBod) + " "
        lcSql += "group by orden_egreso_id "
        cursor.execute(lcSql)
        egresos = cursor.fetchall()

        for oId in egresos:
            oLineasTotal = 0
            oLineasDespa = 0

            if oId[1]:
                oLineasTotal = oId[1]
            if oId[2]:
                oLineasDespa = oId[2]

            if oLineasDespa == 0:
                lAprobar = True
                break

        lAprobar = True
        if lAprobar == True:
            obj.aprobada = False
            obj.aprobado_por = request.user.get_full_name()
            obj.aprobado_at = datetime.now()
            obj.save()
            return HttpResponseRedirect('/ordenEgreso/OrdenEgresoReversar')
        else:
            print 'error'
            #print egresos_orden_form.errors, len(egresos_orden_form.errors)
            messages.error(request, 'Ocurrió un Error. Orden de Egreso con Movimientos ')
            return HttpResponseRedirect('/ordenEgreso/error500')


@login_required()
def aprobarByPkView(request, pk):
    try:
        aprobar(request, pk, OrdenEgreso)
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


def BadError500(request):
    if request.method == 'POST':
        #ordenesegresos=''
        return render_to_response('egresoordenegreso/500.html', {}, RequestContext(request))
    else:
        item = {
            'id': '111',
            'sku': '00001',
            'producto': 'xxxxxxxxxxxxxxxx',
        }

        return render_to_response('egresoordenegreso/500.html', {'itemerror':item}, RequestContext(request))


def EgresoOrdenEgresoListView(request):
    if request.method == 'POST':
        messages.error()
        #ordenesegresos = EgresoOrdenEgreso.objects.all()
        ordenesegresos=''
        return render_to_response('egresoordenegreso/list.html', {'egresoordenegresos': ordenesegresos}, RequestContext(request))
    else:
        #ordenesegresos = EgresoOrdenEgreso.objects.all()
        ordenesegresos=""

        return render_to_response('egresoordenegreso/list.html', {'egresoordenegresos': ordenesegresos}, RequestContext(request))


@login_required()
@transaction.atomic

def EgresoOrdenEgresoCreateView(request):
      if request.method == 'POST':
          with transaction.atomic():
            egresos_orden_form=EgresoOrdenEgresoForm(request.POST)
            #productos = Producto.objects.all()

            lControlError = 0

            if egresos_orden_form.is_valid():
                new_orden=egresos_orden_form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.subtotal=request.POST["subtotal"]
                new_orden.iva=request.POST["iva"]
                new_orden.total=request.POST["total"]
                new_orden.orden_egreso_id=request.POST["orden_egreso_id"]
                new_orden.concepto=request.POST["concepto"]

                new_orden.save()
                try:
                    orden_egreso = OrdenEgreso.objects.get(id=request.POST["orden_egreso_id"])

                except OrdenEgreso.DoesNotExist:
                    orden_egreso = None

                try:
                    secuencial = Secuenciales.objects.get(modulo='egresoordenegreso')
                    print('Secuencial en la base' + str(secuencial.secuencial))
                    print('Secuencial de la EOE' + str(new_orden.codigo))
                    if secuencial.secuencial!=new_orden.codigo:
                        print('ENTRO Secuencial en la base' + str(secuencial.secuencial))
                        print('ENTRO Secuencial de la EOE' + str(new_orden.codigo))

                        new_orden.codigo=secuencial.secuencial
                        new_orden.save()
                    secuencial.secuencial=secuencial.secuencial+1
                    secuencial.created_by = request.user.get_full_name()
                    secuencial.updated_by = request.user.get_full_name()
                    secuencial.created_at = datetime.now()
                    secuencial.updated_at = datetime.now()
                    secuencial.save()
                except Secuenciales.DoesNotExist:
                    secuencial = None

                fecha=new_orden.fecha

                if orden_egreso:
                    #print('tamanio de OP' + str(len(orden_egreso.orden_produccion_codigo)))
                    #print('OP' + str(orden_egreso.orden_produccion_codigo))
                    conceptoop=ConceptoOrdenEgreso.objects.get(id=orden_egreso.concepto_orden_egreso_id)
                    cuentaop = str(conceptoop.cuenta)

                    if conceptoop.op == True:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        parametro_acreedora = Parametros.objects.get(clave='cuenta_acreedora_inventario_productos_en_proceso')
                        parametro_deudora = Parametros.objects.get(clave='cuenta_deudora_inventario_materia_prima')

                        asiento = Asiento()
                        asiento.codigo_asiento =  "EOE"+str(fecha.year)+"00"+str(codigo_asiento)
                        asiento.fecha = fecha
                        asiento.glosa = 'Egreso por Orden Egreso '+str(new_orden.codigo)+' de la OP: ' + str(orden_egreso.orden_produccion_codigo.encode('utf8'))
                        asiento.gasto_no_deducible = False
                        asiento.modulo= 'Egreso por Orden Egreso '
                        asiento.total_debe=new_orden.subtotal
                        asiento.total_haber=new_orden.subtotal
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.save()
                        new_orden.asiento_id=asiento.asiento_id
                        new_orden.save()

                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                    else:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        parametro_acreedora = Parametros.objects.get(clave='cuenta_acreedora_inventario_materia_prima_general')
                        parametro_deudora = Parametros.objects.get(clave='cuenta_deudora_inventario_materia_prima_general')

                        asiento = Asiento()
                        asiento.codigo_asiento =  "EOE"+str(fecha.year)+"00"+str(codigo_asiento)
                        asiento.fecha =fecha
                        asiento.glosa = 'Egreso por Orden Egreso '+str(new_orden.codigo)+' GENERAL'
                        asiento.gasto_no_deducible = False
                        asiento.modulo= 'Egreso por Orden Egreso '
                        asiento.total_debe=new_orden.subtotal
                        asiento.total_haber=new_orden.subtotal
                        asiento.secuencia_asiento = codigo_asiento
                        asiento.save()
                        new_orden.asiento_id=asiento.asiento_id
                        new_orden.save()

                        try:
                            if len(cuentaop) > 0:
                                plan_deudorasp = PlanDeCuentas.objects.get(codigo_plan=conceptoop.cuenta)
                            else:
                                plan_deudorasp = PlanDeCuentas.objects.get(codigo_plan=parametro_deudora.valor)

                        except PlanDeCuentas.DoesNotExist:
                            plan_deudorasp = None

                        if plan_deudorasp:
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = plan_deudorasp.plan_id
                            asiento_detalle.debe = new_orden.subtotal
                            asiento_detalle.haber = 0
                            asiento_detalle.concepto = 'Egreso por Orden Egreso '+str(new_orden.codigo)+' GENERAL'
                            asiento_detalle.save()

                        try:
                            plan_acreedorap = PlanDeCuentas.objects.get(codigo_plan=parametro_acreedora.valor)
                        except PlanDeCuentas.DoesNotExist:
                            plan_acreedorap = None

                        if plan_acreedorap:

                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                            asiento_detalle.cuenta_id = plan_acreedorap.plan_id
                            asiento_detalle.debe = 0
                            asiento_detalle.haber = new_orden.subtotal
                            asiento_detalle.concepto = 'Egreso por Orden Egreso '+str(new_orden.codigo)+' GENERAL'
                            asiento_detalle.save()

                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)

                objet= OrdenEgresoDetalle.objects.filter(orden_egreso_id= request.POST["orden_egreso_id"])
                egre= OrdenEgreso.objects.get(id= request.POST["orden_egreso_id"])

                for ob in objet:
                    if ob.op:
                        try:
                            opr = OrdenProduccionReceta.objects.get(id=ob.orden_produccion_receta_id)
                        except OrdenProduccionReceta.DoesNotExist:
                            opr = None
                        if opr:
                            if opr.egresos:
                                eg=opr.egresos
                            else:
                                eg=0
                            print 'cantidad'
                            print eg
                            if eg == '' or  eg == 'None':
                                eg=0
                            total_eg=eg+ob.cantidad
                            opr.egresos=total_eg
                            opr.save()
                    try:
                        kardex = ProductoEnBodega.objects.get(producto_id=ob.producto_id,bodega_id=egre.bodega_id)

                    except ProductoEnBodega.DoesNotExist:
                        kardex = None

                    if kardex:
                        if kardex.bodega_id == ob.bodega_id:
                            inventario = kardex.cantidad
                            if ob.cantidad <= kardex.cantidad:
                                print('SE DESPACHO' + str(ob.producto_id))
                                ob.disminuir_kardex = True
                                ob.despachar = True
                                ob.save()

                                k = Kardex()
                                k.nro_documento = new_orden.codigo
                                k.producto = ob.producto
                                k.cantidad = ob.cantidad
                                k.descripcion = 'Orden de Egreso'
                                k.costo = ob.precio_compra
                                k.bodega = egre.bodega
                                k.modulo = new_orden.id
                                k.fecha_egreso = fecha
                                k.un_doc_soporte = 'Orden de Egreso No.' + str(
                                    egre.codigo) + ' Egreso por Orden de Egreso No.' + str(new_orden.codigo)
                                k.egreso = True
                                k.created_by = request.user.get_full_name()
                                k.updated_by = request.user.get_full_name()
                                k.created_at = datetime.now()
                                k.updated_at = datetime.now()
                                k.save()
                                print('El id de la bodegasss' + str(egre.bodega_id))
                                print('El id de la productosss' + str(ob.producto_id))

                                try:
                                    objetose = ProductoEnBodega.objects.filter(producto_id=ob.producto_id).filter(
                                        bodega_id=egre.bodega_id).latest('producto_bodega_id')
                                    cant = objetose.cantidad
                                    objetose.cantidad = cant - float(ob.cantidad)
                                    objetose.updated_at = datetime.now()
                                    objetose.updated_by = request.user.get_full_name()
                                    objetose.save()

                                except ProductoEnBodega.DoesNotExist:
                                    objetose = None

                                tipo_producto_id = ob.producto.tipo_producto.id
                                print('tipo Producto' + str(tipo_producto_id))

                                try:
                                    prod_d = TipoProducto.objects.get(id=int(tipo_producto_id))
                                    print('TIENE TIPO DE PRODUCTO')


                                except TipoProducto.DoesNotExist:
                                    prod_d = None
                                    print('NO TIENE TIPO DE PRODUCTO')

                                if prod_d:
                                    try:
                                        plan_deudora = PlanDeCuentas.objects.get(
                                            plan_id=prod_d.cuenta_inventario_productos_proceso_id)

                                    except PlanDeCuentas.DoesNotExist:
                                        plan_deudora = None
                                        print('NO TIENE CUENTA DEUDORA')

                                    if plan_deudora:
                                        conceptoop=ConceptoOrdenEgreso.objects.get(id=orden_egreso.concepto_orden_egreso_id)
                                        if conceptoop.op == True:
                                        #if len(orden_egreso.orden_produccion_codigo)!=0:

                                            asiento_detalle = AsientoDetalle()
                                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                                            asiento_detalle.cuenta_id = plan_deudora.plan_id
                                            asiento_detalle.debe = ob.total
                                            asiento_detalle.haber = 0
                                            asiento_detalle.concepto = 'Egreso de Producto' + smart_str(
                                                ob.producto.descripcion_producto)
                                            asiento_detalle.save()

                                    try:
                                        plan_acreedora = PlanDeCuentas.objects.get(plan_id=prod_d.cuenta_contable_id)

                                    except PlanDeCuentas.DoesNotExist:
                                        plan_acreedora = None
                                        print('NO TIENE CUENTA ACREEDORA')
                                    if plan_acreedora:
                                        conceptoop=ConceptoOrdenEgreso.objects.get(id=orden_egreso.concepto_orden_egreso_id)
                                        if conceptoop.op == True:
                                        #if len(orden_egreso.orden_produccion_codigo)!=0:
                                            asiento_detalle = AsientoDetalle()
                                            asiento_detalle.asiento_id = int(asiento.asiento_id)
                                            asiento_detalle.cuenta_id = plan_acreedora.plan_id
                                            asiento_detalle.debe = 0
                                            asiento_detalle.haber = ob.total
                                            asiento_detalle.concepto = 'Egreso de Producto' + str(
                                                ob.producto.descripcion_producto.encode('utf8'))
                                            asiento_detalle.save()
                            else:
                                oSkuError = ob.producto
                                lControlError = lControlError + 1
                                ob.disminuir_kardex = False
                                ob.despachar = False
                                ob.save()
                                #transaction.abort()
                                print('NO SE DESPACHO' + str(ob.producto_id))
                        else:
                            lControlError = lControlError + 1
                            print('NO SE DESPACHO' + str(ob.producto_id))
                            ob.disminuir_kardex = False
                            ob.despachar = False
                            ob.save()
                            #transaction.abort()

                lControlError = 0
                if lControlError > 0:
                    #print ('No se Graba la Transaccion, Existieron Inconsistencias')
                    transaction.set_rollback(True)
                    messages.error(request, 'No se Graba la Transaccion, Existieron Inconsistencias...')
                    # item = {
                    #     'id': '111',
                    #     'sku': '00001',
                    #     'producto': 'xxxxxxxxxxxxxxxx',
                    # }

                    return HttpResponseRedirect('/ordenEgreso/error500')

                return HttpResponseRedirect('/ordenEgreso/EgresoOrdenEgreso')
            else:
                print 'error'
                print egresos_orden_form.errors, len(egresos_orden_form.errors)
      else:
          #Aqui cambiar la consulta por la de Stocks OExE
        egresos_orden_form=EgresoOrdenEgresoForm
        #productos1 = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto', 'bloquea', 'medida_peso', 'costo').exclude(tipo_producto=2)

        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.tipo_producto, p.bloquea, p.medida_peso, p.costo_promedio as costo, p.unidad, sum(pb.cantidad) as existencia '
        query += 'from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 and pb.cantidad>0 '
        query += 'group by p.producto_id, p.codigo_producto,p.descripcion_producto, p.tipo_producto  order by p.producto_id;'
        cursor.execute(query)
        productos = cursor.fetchall()

      return render_to_response('egresoordenegreso/create.html', { 'egresos_orden_form': egresos_orden_form, 'productos':productos },  RequestContext(request))

@login_required()
@transaction.atomic

def EgresoOrdenEgresoUpdateView(request,pk):
    if request.method == 'POST':
    	ordenegreso=EgresoOrdenEgreso.objects.get(id=pk)
    	# orden=OrdenCompra.objects.get(compra_id=ordencompra.orden_compra_id)
        egresoordenegreso_form=EgresoOrdenEgresoForm(request.POST,request.FILES,instance=ordenegreso)
        print egresoordenegreso_form.is_valid(), egresoordenegreso_form.errors, type(egresoordenegreso_form.errors)

        if egresoordenegreso_form.is_valid():
            with transaction.atomic():
                new_orden=egresoordenegreso_form.save()
                #new_orden.nro_fact_proveedor=request.POST["nro_fact_proveedor"]
                new_orden.save()
                objet= OrdenEgresoDetalle.objects.filter(orden_egreso_id= request.POST["orden_egreso_id"])

                for ob in objet:
                    if ob.disminuir_kardex!=True and ob.despachar==True:
                        ob.disminuir_kardex = True
                        ob.save()
                        k=Kardex()
                        k.nro_documento =new_orden.codigo
                        k.producto=ob.producto
                        k.cantidad=ob.cantidad
                        k.descripcion='Orden de Egreso'
                        k.costo=ob.precio_compra
                        k.bodega=new_orden.bodega
                        k.modulo=new_orden.id
                        k.fecha_egreso=datetime.now()
                        k.egreso = True
                        k.save()

                contador=request.POST["columnas_receta"]
                print contador
                i=1

                print('El id de la compra'+str(pk))
                detalle = EgresoDetalle.objects.filter(orden_egreso_id=new_orden.orden_egreso_id)

                context = {
               'section_title':'Actualizar Orden Egreso',
                'button_text':'Actualizar',
                'egresoordenegreso_form':egresoordenegreso_form,
                'detalle':detalle,

                 }


                return render_to_response(
                    'egresoordenegreso/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:

            egresoordenegreso_form=EgresoOrdenEgresoForm(request.POST)
            detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordencompra.orden_egreso_id)

            context = {
            'section_title':'Actualizar Compras Locales',
            'button_text':'Actualizar',
            'egresoordenegreso_form':egresoordenegreso_form,
            'detalle':detalle, }

        return render_to_response(
            'egresoordenegreso/actualizar.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordencompra=EgresoOrdenEgreso.objects.get(id=pk)
        egresoordenegreso_form=EgresoOrdenEgresoForm(instance=ordencompra)
        detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordencompra.orden_egreso_id)
        orden=OrdenEgreso.objects.get(id=ordencompra.orden_egreso_id)

        context = {
            'section_title':'Actualizar Orden Egreso',
            'button_text':'Actualizar',
            'egresoordenegreso_form':egresoordenegreso_form,
            'detalle':detalle,
            'orden': orden, }

        return render_to_response(
            'egresoordenegreso/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    ordenegreso=OrdenEgreso.objects.get(id=pk)
    detalle =OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)

    html = render_to_string('ordenegreso/imprimir_ordenegreso.html', {'pagesize':'A4','ordenegreso':ordenegreso,'detalle':detalle}, context_instance=RequestContext(request))
    return generar_pdf(html)


def imprimirEgresoxOrden(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    egresopororden=EgresoOrdenEgreso.objects.get(id=pk)
    ordenegreso=OrdenEgreso.objects.get(id=egresopororden.orden_egreso_id)
    detalle =OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)

    html = render_to_string('egresoordenegreso/imprimir.html', {'pagesize':'A5','egresopororden':egresopororden,'ordenegreso':ordenegreso,'detalle':detalle}, context_instance=RequestContext(request))
    return generar_pdf(html)

def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

@login_required()
def export_to_excel(request,pk):


    # your excel html format
    template_name = "ordenesegresos.html"

    ordenegreso=OrdenEgreso.objects.get(id=pk)
    if ordenegreso:
        try:
            egresopororden = EgresoOrdenEgreso.objects.get(orden_egreso_id=pk)
        except EgresoOrdenEgreso.DoesNotExist:
            egresopororden = None

    detalle =OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)


    response = render_to_response('egresoordenegreso/imprimir.html', {'egresopororden':egresopororden,'ordenegreso':ordenegreso,'detalle':detalle})

    # this is the output file
    filename = "egreso_orden_egreso.xls"

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response


@login_required()
@transaction.atomic
def OrdenEgresoActualizarView(request, pk):
    if request.method == 'POST':
        form = OrdenEgresoForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo_promedio', 'precio1', 'precio2').exclude(tipo_producto=1)
        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad,sum(pb.cantidad) from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 group by p.producto_id, p.codigo_producto,p.descripcion_producto order by p.producto_id;'
        cursor.execute(query)
        productos_bodega = cursor.fetchall()

        iva = Parametros.objects.get(clave='iva')
        iva_valor=float(iva.valor)
        print iva_valor
        if form.is_valid():
            with transaction.atomic():
                cleaned_data = form.cleaned_data
                ordenegreso = OrdenEgreso.objects.get(pk=pk)
                ordenegreso.comentario =cleaned_data.get('comentario')
                ordenegreso.concepto_orden_egreso = cleaned_data.get('concepto_orden_egreso')
                ordenegreso.bodega = cleaned_data.get('bodega')
                ordenegreso.subtotal = request.POST["total23"]
                subtotal = request.POST["total23"]
                impuesto_mont = float(request.POST["total23"] )* iva_valor / 100
                ordenegreso.impuesto_monto = float(request.POST["total23"]) * iva_valor / 100
                ordenegreso.total = round(float(subtotal) + float(impuesto_mont), 2)
                ordenegreso.fecha = form.cleaned_data.get('fecha')
                ordenegreso.updated_by = request.user.get_full_name()
                ordenegreso.updated_at = datetime.now()
                try:
                    concepto = ConceptoOrdenEgreso.objects.get(id=ordenegreso.concepto_orden_egreso_id)
                   
                except ConceptoOrdenEgreso.DoesNotExist:
                    concepto = None
                if concepto:
                    ordenegreso.notas=concepto.nombre
                ordenegreso.save()


                contador = request.POST["columnas_receta"]
                print ('contador' + str(contador))
                i = 0
                while int(i) <= int(contador):
                    i+= 1
                    
                    if int(i) >int(contador):
                        
                        break
                    else:
                        print ('Entro con el secuencial' + str(i))
                        if 'id_kits' + str(i) in request.POST:
                            product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                            if 'id_detalle' + str(i) in request.POST:
                                detallecompra = OrdenEgresoDetalle.objects.get(id=request.POST["id_detalle" + str(i)])
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.producto = product
                                detallecompra.cantidad = request.POST["cantidad_kits" + str(i)]
                                detallecompra.precio_compra = request.POST["costo_kits" + str(i)]
                                detallecompra.unidad_medida = request.POST["medida_kits" + str(i)]
                                detallecompra.total = request.POST["total_kits" + str(i)]
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.updated_at = datetime.now()
                                if 'areas_kits'+str(i) in request.POST:
                                    detallecompra.areas_id=request.POST["areas_kits"+str(i)]
                            
                                conceptoop=ConceptoOrdenEgreso.objects.get(id=ordenegreso.concepto_orden_egreso_id)
                                if conceptoop.op == True:
                                    if 'subopid_kits'+str(i) in request.POST:
                                        detallecompra.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                        detallecompra.op=True
                                detallecompra.save()

                            else:
                                product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                                comprasdetalle = OrdenEgresoDetalle()
                                comprasdetalle.orden_egreso_id = ordenegreso.id
                                comprasdetalle.producto = product
                                comprasdetalle.bodega = ordenegreso.bodega
                                comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                                comprasdetalle.precio_compra = request.POST["costo_kits" + str(i)]
                                comprasdetalle.total = request.POST["total_kits" + str(i)]
                                comprasdetalle.unidad_medida = request.POST["medida_kits" + str(i)]
                                comprasdetalle.created_by = request.user.get_full_name()
                                comprasdetalle.updated_by = request.user.get_full_name()
                                comprasdetalle.created_at = datetime.now()
                                comprasdetalle.updated_at = datetime.now()
                                if 'areas_kits'+str(i) in request.POST:
                                    comprasdetalle.areas_id=request.POST["areas_kits"+str(i)]
                            
                                conceptoop=ConceptoOrdenEgreso.objects.get(id=ordenegreso.concepto_orden_egreso_id)
                                if conceptoop.op == True:
                                    if 'subopid_kits'+str(i) in request.POST:
                                        comprasdetalle.orden_produccion_receta_id=request.POST["subopid_kits"+str(i)]
                                        comprasdetalle.op=True
                                comprasdetalle.save()
                                
                        else:
                            print('Validacion' + str(contador))
                            print('Secuencial validacion' + str(i))
                            print('contador validacion' + str(contador))
                            # ordencompra_form=OrdenCompraForm(request.POST)

                detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=pk)
                productos = Producto.objects.all()
                cursor = connection.cursor()
                query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad,sum(pb.cantidad) from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 group by p.producto_id, p.codigo_producto,p.descripcion_producto order by p.producto_id;'
                cursor.execute(query)
                productos_bodega = cursor.fetchall()

                cursor = connection.cursor()
                query_detalle = 'select o.id, o.producto_id,p.codigo_producto,p.descripcion_producto, p.unidad,o.cantidad, o.precio_compra, o.total,sum(pb.cantidad),o.areas_id,o.op,o.orden_produccion_receta_id,ord.codigo,ord.tipo,opr1.cantidad,opr1.egresos,opr1.ingresos,opr1.cantidad-opr1.egresos from orden_egreso_detalle o left join producto p ON (o.producto_id=p.producto_id) left join orden_produccion_receta opr ON (o.orden_produccion_receta_id=opr.id) left join suborden_produccion sub ON (sub.id=opr.suborden_produccion_id) left join orden_produccion ord ON (ord.id=sub.orden_produccion_id) left join orden_produccion_receta opr1 ON (o.orden_produccion_receta_id=opr1.id) left join producto_en_bodega pb ON (o.producto_id=pb.producto_id) and pb.bodega_id=1 where o.producto_id=p.producto_id and o.orden_egreso_id='+ str(pk)+' group by o.id, o.producto_id,p.codigo_producto,p.descripcion_producto,o.cantidad, o.precio_compra, o.total, p.unidad,o.areas_id,o.op,o.orden_produccion_receta_id,ord.codigo,ord.tipo,opr1.cantidad,opr1.egresos,opr1.ingresos order by o.id'
                #query_detalle = 'select o.id, o.producto_id,p.codigo_producto,p.descripcion_producto, p.unidad,o.cantidad, o.precio_compra, o.total,sum(pb.cantidad) from orden_egreso_detalle o  left join producto p ON (o.producto_id=p.producto_id) left join producto_en_bodega pb ON (o.producto_id=pb.producto_id) and pb.bodega_id=1 where o.producto_id=p.producto_id and o.orden_egreso_id=' + str(pk) + ' group by o.id, o.producto_id,p.codigo_producto,p.descripcion_producto,o.cantidad, o.precio_compra, o.total, p.unidad order by o.producto_id'
                cursor.execute(query_detalle)
                detalle_egresos = cursor.fetchall()
                areas=Areas.objects.all()
                concepto=ConceptoOrdenEgreso.objects.get(op=True)


                context = {
                    'section_title': 'Actualizar Orden Compra1',
                    'button_text': 'Actualizar',
                    'ordenegreso_form': form,
                    'detalle': detalle,
                    'productos': productos,
                    'areas': areas,
                    'concepto': concepto,
                    'productos_bodega': productos_bodega,
                    'pk': pk,
                    'detalle_egresos': detalle_egresos,
                    'mensaje': 'Orden de Egreso actualizada con exito'}

                return render_to_response(
                    'ordenegreso/actualizar.html',
                    context,
                    context_instance=RequestContext(request))
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        ordencompra = OrdenEgreso.objects.get(id=pk)
        productos = Producto.objects.all()
        ordenegreso_form = OrdenEgresoForm(instance=ordencompra)
        detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordencompra.id)
        cursor = connection.cursor()
        query = 'select p.producto_id, p.codigo_producto,p.descripcion_producto,p.medida_peso, p.costo_promedio as costo, p.unidad,sum(pb.cantidad) from producto p left join producto_en_bodega pb ON (p.producto_id=pb.producto_id) where  pb.bodega_id=1 group by p.producto_id, p.codigo_producto,p.descripcion_producto order by p.producto_id;'
        cursor.execute(query)
        productos_bodega = cursor.fetchall()

        cursor= connection.cursor()
        query_detalle = 'select o.id, o.producto_id,p.codigo_producto,p.descripcion_producto, p.unidad,o.cantidad, o.precio_compra, o.total,sum(pb.cantidad),o.areas_id,o.op,o.orden_produccion_receta_id,ord.codigo,ord.tipo,opr1.cantidad,opr1.egresos,opr1.ingresos,opr1.cantidad-opr1.egresos from orden_egreso_detalle o left join producto p ON (o.producto_id=p.producto_id) left join orden_produccion_receta opr ON (o.orden_produccion_receta_id=opr.id) left join suborden_produccion sub ON (sub.id=opr.suborden_produccion_id) left join orden_produccion ord ON (ord.id=sub.orden_produccion_id) left join orden_produccion_receta opr1 ON (o.orden_produccion_receta_id=opr1.id) left join producto_en_bodega pb ON (o.producto_id=pb.producto_id) and pb.bodega_id=1 where o.producto_id=p.producto_id and o.orden_egreso_id='+ str(ordencompra.id)+' group by o.id, o.producto_id,p.codigo_producto,p.descripcion_producto,o.cantidad, o.precio_compra, o.total, p.unidad,o.areas_id,o.op,o.orden_produccion_receta_id,ord.codigo,ord.tipo,opr1.cantidad,opr1.egresos,opr1.ingresos order by o.id'
        cursor.execute(query_detalle)
        detalle_egresos = cursor.fetchall()
        areas=Areas.objects.all()
        concepto=ConceptoOrdenEgreso.objects.get(op=True)


        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'ordenegreso_form': ordenegreso_form,
            'productos': productos,
            'productos_bodega':productos_bodega,
            'pk': pk,
            'areas': areas,
            'concepto': concepto,
            'detalle_egresos':detalle_egresos,
            'detalle': detalle
        }

        return render_to_response(
            'ordenegreso/actualizar.html', context, context_instance=RequestContext(request))



@login_required()
@transaction.atomic
def OrdenEgresoActualizarHistoricoView(request, pk):
    if request.method == 'POST':
        form = OrdenEgresoForm(request.POST)
        productos = Producto.objects.values('producto_id', 'codigo_producto', 'descripcion_producto', 'tipo_producto',
                                            'bloquea', 'medida_peso', 'costo_promedio', 'precio1', 'precio2').exclude(tipo_producto=1)
        if form.is_valid():
            with transaction.atomic():
                iva = Parametros.objects.get(clave='iva')
                iva_valor = float(iva.valor)
                cleaned_data = form.cleaned_data
                ordenegreso = OrdenEgreso.objects.get(pk=pk)
                ordenegreso.comentario = form.cleaned_data['comentario']
                ordenegreso.concepto_orden_egreso = form.cleaned_data['concepto_orden_egreso']
                ordenegreso.bodega = form.cleaned_data['bodega']
                ordenegreso.aprobada = form.cleaned_data['aprobada']
                ordenegreso.anulado = form.cleaned_data['anulado']
                anulado=form.cleaned_data['anulado']
                aprob=form.cleaned_data['aprobada']
                print ('anulado' + str(anulado))
                print ('aprobado' + str(aprob))
                ordenegreso.subtotal = request.POST["total23"]
                subtotal = request.POST["total23"]
                impuesto_mont = float(request.POST["total23"]) * float(iva.valor) / 100
                ordenegreso.impuesto_monto = float(request.POST["total23"]) * float(iva.valor) / 100
                ordenegreso.total = round(float(subtotal) + float(impuesto_mont), 2)
                ordenegreso.fecha = form.cleaned_data['fecha']
                ordenegreso.updated_by = request.user.get_full_name()
                ordenegreso.updated_at = datetime.now()
                try:
                    concepto = ConceptoOrdenEgreso.objects.get(id=ordenegreso.concepto_orden_egreso_id)
                   
                except ConceptoOrdenEgreso.DoesNotExist:
                    concepto = None
                if concepto:
                    ordenegreso.notas=concepto.nombre
                ordenegreso.save()


                contador = request.POST["columnas_receta"]
                print ('contador' + str(contador))
                i = 0
                while int(i) <= int(contador):
                    i+= 1
                    print ('secuencial' + str(i))
                    print ('contador' + str(contador))
                    if int(i) >int(contador):
                        print('entrosd')
                        print ('sale' + str(i))
                        print ('sale contador' + str(contador))
                        break
                    else:
                        print ('Entro con el secuencial' + str(i))
                        if 'id_kits' + str(i) in request.POST:
                            product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                            if 'id_detalle' + str(i) in request.POST:
                                detallecompra = OrdenEgresoDetalle.objects.get(id=request.POST["id_detalle" + str(i)])
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.producto = product
                                detallecompra.cantidad = request.POST["cantidad_kits" + str(i)]
                                detallecompra.precio_compra = request.POST["costo_kits" + str(i)]
                                detallecompra.unidad_medida = request.POST["medida_kits" + str(i)]
                                detallecompra.total = request.POST["total_kits" + str(i)]
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.updated_at = datetime.now()
                                detallecompra.save()

                            else:
                                product = Producto.objects.get(producto_id=request.POST["id_kits" + str(i)])
                                comprasdetalle = OrdenEgresoDetalle()
                                comprasdetalle.orden_egreso_id = ordenegreso.id
                                comprasdetalle.producto = product
                                comprasdetalle.bodega = ordenegreso.bodega
                                comprasdetalle.cantidad = request.POST["cantidad_kits" + str(i)]
                                comprasdetalle.precio_compra = request.POST["costo_kits" + str(i)]
                                comprasdetalle.total = request.POST["total_kits" + str(i)]
                                comprasdetalle.unidad_medida = request.POST["medida_kits" + str(i)]
                                comprasdetalle.created_by = request.user.get_full_name()
                                comprasdetalle.updated_by = request.user.get_full_name()
                                comprasdetalle.created_at = datetime.now()
                                comprasdetalle.updated_at = datetime.now()
                                comprasdetalle.save()
                                print('No Tiene detalle' + str(i))
                                print('contadorsd prueba' + str(contador))
                        else:
                            print('Validacion' + str(contador))
                            print('Secuencial validacion' + str(i))
                            print('contador validacion' + str(contador))
                            # ordencompra_form=OrdenCompraForm(request.POST)

                detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=pk)
                productos = Producto.objects.all()

                context = {
                    'section_title': 'Actualizar Orden Compra1',
                    'button_text': 'Actualizar',
                    'ordenegreso_form': form,
                    'detalle': detalle,
                    'productos': productos,
                    'mensaje': 'Orden de Egreso actualizada con exito'}

                return render_to_response(
                    'ordenegreso/actualizar_historico.html',
                    context,
                    context_instance=RequestContext(request))
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        ordencompra = OrdenEgreso.objects.get(id=pk)
        productos = Producto.objects.all()
        ordenegreso_form = OrdenEgresoForm(instance=ordencompra)
        detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordencompra.id)

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'ordenegreso_form': ordenegreso_form,
            'productos': productos,
            'detalle': detalle
        }

        return render_to_response(
            'ordenegreso/actualizar_historico.html', context, context_instance=RequestContext(request))


def indexOrdenEgreso(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    ordenegreso = OrdenEgreso.objects.get(id=pk)
    detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)

    html = loader.get_template('ordenegreso/imprimir_nuevo_orden_egreso.html')
    context = RequestContext(request, {'ordenegreso': ordenegreso, 'detalle': detalle})
    return HttpResponse(html.render(context))

def imprimirEgresoxOrdenNuevo(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    egresopororden=EgresoOrdenEgreso.objects.get(id=pk)
    ordenegreso=OrdenEgreso.objects.get(id=egresopororden.orden_egreso_id)
    detalle =OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id, disminuir_kardex=True)
    html = loader.get_template('egresoordenegreso/imprimir_nuevo.html')
    context = RequestContext(request, {'egresopororden':egresopororden,'ordenegreso':ordenegreso,'detalle':detalle})
    return HttpResponse(html.render(context))




def egresoporOrdenEgresoReversarListView(request):
    if request.method == 'POST':

        ordenesegresos = EgresoOrdenEgreso.objects.all()
        return render_to_response('egresoordenegreso/reversar_egreso.html', {'egresoordenegresos': ordenesegresos}, RequestContext(request))
    else:
        ordenesegresos = EgresoOrdenEgreso.objects.all()
        return render_to_response('egresoordenegreso/reversar_egreso.html', {'egresoordenegresos': ordenesegresos}, RequestContext(request))

def egresoporOrdenEgresoReversar(request, pk):

    objetos = EgresoOrdenEgreso.objects.get(id=pk)
    if objetos:
        asi=objetos.asiento_id
        objetos.anulado=True
        objetos.asiento_id = None
        objetos.save()
        ordenegreso = OrdenEgreso.objects.get(id=objetos.orden_egreso_id)
        detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)
        ordenegreso.aprobada= False
        ordenegreso.anulado = True
        ordenegreso.anulado_por = request.user.get_full_name()
        ordenegreso.anulado_at = datetime.now()
        ordenegreso.save()

        for ob in detalle:
            ob.disminuir_kardex = False
            ob.despachar = False
            ob.save()
            kardex = Kardex.objects.filter(nro_documento=objetos.codigo).filter(producto_id=ob.producto_id).filter(descripcion = 'Orden de Egreso').filter(bodega_id=ordenegreso.bodega_id).filter(modulo=objetos.id).filter(egreso=True)
            if kardex:
                for k in kardex:
                    k.delete()

                try:
                    objetose = ProductoEnBodega.objects.filter(producto_id=ob.producto_id).filter(
                        bodega_id=ordenegreso.bodega_id).latest('producto_bodega_id')
                    cant = objetose.cantidad
                    objetose.cantidad = cant + float(ob.cantidad)
                    objetose.updated_at = datetime.now()
                    objetose.updated_by = request.user.get_full_name()
                    objetose.save()

                except ProductoEnBodega.DoesNotExist:
                    objetose = None

        try:
            asiento = Asiento.objects.get(asiento_id=asi)
            if asiento:
                asiento_detalle = AsientoDetalle.objects.filter(asiento_id=asiento.asiento_id)
                for a in asiento_detalle:
                    a.delete()
                asiento.delete()


        except Asiento.DoesNotExist:
            asiento = None


    return HttpResponseRedirect('/ordenEgreso/egresoporOrdenEgresoReversarListView')


#PRUEBA
# ============oRDEN eGRESO=============#
@login_required()
def orden_egreso_list_prueba(request):
    #compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
    compras=0
    template = loader.get_template('ordenegreso/list_prueba.html')
    context = RequestContext(request, {'compras': compras})
    return HttpResponse(template.render(context))
@login_required()
@csrf_exempt
def orden_egreso_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql="select id,codigo,comentario,total, fecha,anulado,aprobada from orden_egreso where 1=1"
        
            
        if _search_value:
            sql+=" and codigo like '%"+_search_value+"%' or UPPER(comentario) like '%"+_search_value.upper()+"%' or CAST(fecha as VARCHAR)  like '%"+_search_value+"%' or CAST(total as VARCHAR)  like '%"+_search_value+"%'"
        
        if _search_value.upper()  in 'APROBADA':
            sql+=" or aprobada is True "
        
        if _search_value.upper()  in 'ESPERANDO APROBACION':
            sql+=" or aprobada is not True"
        if _search_value.upper()  in 'ANULADO':
            sql+=" or anulado is True"
           
    
        #sql +=" order by fecha"
        if _order == '0':
            sql +=" order by CAST(codigo AS Numeric(10,0)) "+_order_dir
        if _order == '1':
            sql +=" order by comentario "+_order_dir
        if _order == '2':
            sql +=" order by total "+_order_dir
        
        if _order == '3':
            sql +=" order by anulado "+_order_dir
            
        cursor.execute(sql)
        ordenesegresos = cursor.fetchall()
            
        ordenesegresos_filtered = ordenesegresos[_start:_start + _end]

        ordenesegresos_list = []
        for o in ordenesegresos_filtered:
            html=''
            mes=o[4].month
            anio=o[4].year
            cursor = connection.cursor()
            query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
            cursor.execute(query)
            ro = cursor.fetchall()
            
            ordenesegresos_obj = []
            ordenesegresos_obj.append(o[1])
            ordenesegresos_obj.append(o[2])
            ordenesegresos_obj.append(o[3])

            ordenesegresos_obj.append(o[4].strftime('%Y-%m-%d'))
            
            
    
            if o[5]:
                ordenesegresos_obj.append("Anulado")

            else:
                if o[6]:
                    ordenesegresos_obj.append("Aprobada")
                else:
                    ordenesegresos_obj.append("Esperando Aprobacion")
                    if ro:
                        r=1
                    else:
                        html+='<a href="'+str(o[0])+'/actualizar/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Editar</button></a>'
            
            html+='<a href="imprimirOrdenEgreso/'+str(o[0])+'/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir</button></a><a href="export/'+str(o[0])+'/">Export</a>'

            ordenesegresos_obj.append(html)

            ordenesegresos_list.append(ordenesegresos_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(ordenesegresos)
        response_data['recordsFiltered'] = len(ordenesegresos)
        response_data['data'] = ordenesegresos_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")




@login_required()
@csrf_exempt
def egreso_orden_egreso_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql="select eo.id,eo.codigo,eo.fecha,e.codigo,eo.comentario,eo.subtotal,eo.total,eo.anulado,a.codigo_asiento from egreso_orden_egreso eo left join orden_egreso e on e.id=eo.orden_egreso_id left join contabilidad_asiento a on a.asiento_id=eo.asiento_id where 1=1"
        if _search_value:
            sql+=" and eo.codigo like '%"+_search_value+"%' or UPPER(eo.comentario) like '%"+_search_value.upper()+"%' or UPPER(e.codigo) like '%"+_search_value.upper()+"%' or CAST(eo.fecha as VARCHAR)  like '%"+_search_value+"%' or CAST(eo.total as VARCHAR)  like '%"+_search_value+"%' or UPPER(a.codigo_asiento) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()=='ANULADO'  or _search_value.upper()=='AN' or _search_value.upper()=='ANU' or _search_value.upper()=='ANUL'  or _search_value.upper()=='ANULA' or _search_value.upper()=='ANULAD':
            sql+=" or eo.anulado is True"
        
        if _search_value.upper()=='ACTIVO' or _search_value.upper()=='AC' or _search_value.upper()=='ACT' or _search_value.upper()=='ACTI' or _search_value.upper()=='ACTIV':
            sql+=" or eo.anulado is not True"
        
           
    
        #sql +=" order by fecha"
        if _order == '0':
            sql +=" order by CAST(eo.codigo AS Numeric(10,0)) "+_order_dir
        if _order == '1':
            sql +=" order by eo.fecha "+_order_dir
        if _order == '2':
            sql +="  order by CAST(e.codigo AS Numeric(10,0))  "+_order_dir
        if _order == '3':
            sql +=" order by eo.concepto "+_order_dir
        if _order == '4':
            sql +=" order by eo.subtotal "+_order_dir
        if _order == '5':
            sql +=" order by eo.total "+_order_dir
        
        if _order == '6':
            sql +=" order by eo.anulado "+_order_dir
        if _order == '7':
            sql +=" order by a.codigo_asiento "+_order_dir
            
        cursor.execute(sql)
        ordenesegresos = cursor.fetchall()
            
        ordenesegresos_filtered = ordenesegresos[_start:_start + _end]

        ordenesegresos_list = []
        for o in ordenesegresos_filtered:
            ordenesegresos_obj = []
            ordenesegresos_obj.append(o[1])
            ordenesegresos_obj.append(o[2].strftime('%Y-%m-%d %H:%M:%S'))
            ordenesegresos_obj.append(o[3])
            ordenesegresos_obj.append(o[4])
            ordenesegresos_obj.append(o[5])
            ordenesegresos_obj.append(o[6])
            

            
    
            if o[7]:
                ordenesegresos_obj.append("Anulado")

            else:
                ordenesegresos_obj.append("Activo")
            
            ordenesegresos_obj.append(o[8])
            
            html='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenEgreso/EgresoOrdenEgreso/'+str(o[0])+'/editar/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Ver</button></a>'
            html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/ordenEgreso/OrdenEgreso/imprimirEgresoxOrdenNuevo/'+str(o[0])+'/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Imprimir</button></a>'
            

            ordenesegresos_obj.append(html)

            ordenesegresos_list.append(ordenesegresos_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(ordenesegresos)
        response_data['recordsFiltered'] = len(ordenesegresos)
        response_data['data'] = ordenesegresos_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def imprimir_orden_egreso_actual(request, pk):
    ordenegreso = OrdenEgreso.objects.get(id=pk)
    detalle = OrdenEgresoDetalle.objects.filter(orden_egreso_id=ordenegreso.id)

    html = loader.get_template('ordenegreso/imprimir_nuevo_orden_egreso_final.html')
    context = RequestContext(request, {'ordenegreso': ordenegreso, 'detalle': detalle})
    return HttpResponse(html.render(context))

       
def orden_egreso_aprobada_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql="select e.id,e.codigo,e.comentario,e.subtotal, e.fecha,e.anulado,e.aprobada,e.concepto_orden_egreso_id,c.nombre from orden_egreso e,concepto_orden_egreso c where 1=1 and c.id=e.concepto_orden_egreso_id and e.aprobada is not True and e.anulado is not True "
        
            
        if _search_value:
            sql+=" and e.codigo like '%"+_search_value+"%' or UPPER(e.comentario) like '%"+_search_value.upper()+"%' or CAST(e.fecha as VARCHAR)  like '%"+_search_value+"%' or CAST(c.nombre as VARCHAR)  like '%"+_search_value+"%' or CAST(e.subtotal as VARCHAR)  like '%"+_search_value+"%'"
        
        # if _search_value.upper()  in 'APROBADA':
        #     sql+=" or aprobada is True "
        # 
        # if _search_value.upper()  in 'ESPERANDO APROBACION':
        #     sql+=" or aprobada is not True"
        # if _search_value.upper()  in 'ANULADO':
        #     sql+=" or anulado is True"
           
    
        #sql +=" order by fecha"
        if _order == '0':
            sql +=" order by CAST(codigo AS Numeric(10,0)) "+_order_dir
        if _order == '1':
            sql +=" order by comentario "+_order_dir
        if _order == '2':
            sql +=" order by subtotal "+_order_dir
        
        if _order == '3':
            sql +=" order by anulado "+_order_dir
            
        cursor.execute(sql)
        ordenesegresos = cursor.fetchall()
            
        ordenesegresos_filtered = ordenesegresos[_start:_start + _end]

        ordenesegresos_list = []
        for o in ordenesegresos_filtered:
            html=''
            mes=o[4].month
            anio=o[4].year
            cursor = connection.cursor()
            query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
            cursor.execute(query)
            ro = cursor.fetchall()
            
            ordenesegresos_obj = []
            res='<a onclick="detalledeCompra('+str(o[0])+')"> '+str(o[1])+'</a>'
            ordenesegresos_obj.append(res)
            ordenesegresos_obj.append(o[8])
            ordenesegresos_obj.append(o[3])

            ordenesegresos_obj.append(o[4].strftime('%Y-%m-%d'))
            cursor = connection.cursor()
            sql="select distinct op.id,op.tipo,op.codigo,oe.orden_egreso_id from orden_produccion op, orden_egreso_detalle oe,suborden_produccion s,orden_produccion_receta orp where  oe.orden_produccion_receta_id=orp.id and orp.suborden_produccion_id=s.id and s.orden_produccion_id=op.id and oe.orden_egreso_id="+str(o[0])
            cursor.execute(sql)
            ros = cursor.fetchall()
            op=''
            if ros:
                for r in ros:
                    op+=r[1]+'-'+r[2]+' '
                
                
            
            ordenesegresos_obj.append(op)
            ordenesegresos_obj.append(o[2])
            
            if o[5]:
                ordenesegresos_obj.append("Anulado")

            else:
                if o[6]:
                    ordenesegresos_obj.append("Aprobada")
                else:
                    ordenesegresos_obj.append("Esperando Aprobacion")
                    if ro:
                        r=1
                    else:
                        html+='<a href="/ordenEgreso/OrdenEgreso/'+str(o[0])+'/aprobar/" onclick="return confirm(´Esta seguro que desea aprobar la orden de egreso '+str(o[1])+'?´)"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Aprobar</button></a>'
            

            ordenesegresos_obj.append(html)

            ordenesegresos_list.append(ordenesegresos_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(ordenesegresos)
        response_data['recordsFiltered'] = len(ordenesegresos)
        response_data['data'] = ordenesegresos_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")

#Nuevo
def orden_egreso_reversada_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order = request.GET['order[0][column]']
        _order_dir = request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql = "select e.id,e.codigo,e.comentario,e.subtotal, e.fecha,e.anulado,e.aprobada,e.concepto_orden_egreso_id,c.nombre from orden_egreso e,concepto_orden_egreso c where 1=1 and c.id=e.concepto_orden_egreso_id and e.aprobada is not True and e.anulado is not True "

        if _search_value:
            sql += " and e.codigo like '%" + _search_value + "%' or UPPER(e.comentario) like '%" + _search_value.upper() + "%' or CAST(e.fecha as VARCHAR)  like '%" + _search_value + "%' or CAST(c.nombre as VARCHAR)  like '%" + _search_value + "%' or CAST(e.subtotal as VARCHAR)  like '%" + _search_value + "%'"

        # if _search_value.upper()  in 'APROBADA':
        #     sql+=" or aprobada is True "
        #
        # if _search_value.upper()  in 'ESPERANDO APROBACION':
        #     sql+=" or aprobada is not True"
        # if _search_value.upper()  in 'ANULADO':
        #     sql+=" or anulado is True"

        # sql +=" order by fecha"
        if _order == '0':
            sql += " order by CAST(codigo AS Numeric(10,0)) " + _order_dir
        if _order == '1':
            sql += " order by comentario " + _order_dir
        if _order == '2':
            sql += " order by subtotal " + _order_dir

        if _order == '3':
            sql += " order by anulado " + _order_dir

        cursor.execute(sql)
        ordenesegresos = cursor.fetchall()

        ordenesegresos_filtered = ordenesegresos[_start:_start + _end]

        ordenesegresos_list = []
        for o in ordenesegresos_filtered:
            html = ''
            mes = o[4].month
            anio = o[4].year
            cursor = connection.cursor()
            query = "select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='" + str(
                anio) + "' and date_part('month',fecha)='" + str(mes) + "'"
            cursor.execute(query)
            ro = cursor.fetchall()

            ordenesegresos_obj = []
            res = '<a onclick="detalledeCompra(' + str(o[0]) + ')"> ' + str(o[1]) + '</a>'
            ordenesegresos_obj.append(res)
            ordenesegresos_obj.append(o[8])
            ordenesegresos_obj.append(o[3])

            ordenesegresos_obj.append(o[4].strftime('%Y-%m-%d'))
            cursor = connection.cursor()
            sql = "select distinct op.id,op.tipo,op.codigo,oe.orden_egreso_id from orden_produccion op, orden_egreso_detalle oe,suborden_produccion s,orden_produccion_receta orp where  oe.orden_produccion_receta_id=orp.id and orp.suborden_produccion_id=s.id and s.orden_produccion_id=op.id and oe.orden_egreso_id=" + str(
                o[0])
            cursor.execute(sql)
            ros = cursor.fetchall()
            op = ''
            if ros:
                for r in ros:
                    op += r[1] + '-' + r[2] + ' '

            ordenesegresos_obj.append(op)
            ordenesegresos_obj.append(o[2])

            if o[5]:
                ordenesegresos_obj.append("Anulado")

            else:
                if o[6]:
                    ordenesegresos_obj.append("Aprobada")
                else:
                    ordenesegresos_obj.append("Esperando Aprobacion")
                    if ro:
                        r = 1
                    else:
                        html += '<a href="/ordenEgreso/OrdenEgreso/' + str(o[
                                                                               0]) + '/aprobar/" onclick="return confirm(´Esta seguro que desea aprobar la orden de egreso ' + str(
                            o[
                                1]) + '?´)"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Aprobar</button></a>'

            ordenesegresos_obj.append(html)

            ordenesegresos_list.append(ordenesegresos_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(ordenesegresos)
        response_data['recordsFiltered'] = len(ordenesegresos)
        response_data['data'] = ordenesegresos_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")
