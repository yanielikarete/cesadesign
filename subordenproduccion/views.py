
# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView
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

from django.conf import settings
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape


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
#======================PROFORMA=============================#


def SubOrdenProduccionListView(request, pk):
    if request.method == 'POST':
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        ambientes = Areas.objects.all()


        id=pk
        contador=request.POST["columnas_receta"]

        i=0
        while int(i) <= int(contador):
            i+= 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'suborden_id'+str(i) in request.POST:
                    detalle_id=request.POST["suborden_id"+str(i)]
                    subor = SubordenProduccion.objects.get(id=detalle_id)
                    subor.updated_by = request.user.get_full_name()
                    subor.areas_id =request.POST["id_areas"+str(i)]
                    subor.secuencia=request.POST["secuencia_guardar"+str(i)]
                    subor.observaciones=request.POST["observaciones"+str(i)].strip()
                    subor.finalizada=request.POST.get('finalizada'+str(i), False)
                    subor.updated_at = datetime.now()
                    subor.save()

                    print('Tiene detalle'+str(i))
                else:
        			print('No tiene detalle'+str(i))
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        subordenes_finalizadas = SubordenProduccion.objects.filter(orden_produccion_id=pk).filter(finalizada=True)
        finalizada = 0
        if subordenes.count() == subordenes_finalizadas.count():
            finalizada = 1
            #op = OrdenProduccion.objects.get(id=pk)
            #op.finalizada=True
            #op.save()
        id=pk
        ambientes = Areas.objects.all()
        op = OrdenProduccion.objects.get(id=pk)
        return render_to_response('subordenproduccion/list.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes,'op':op,'finalizada':finalizada},  RequestContext(request))



    else:
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        subordenes_finalizadas= SubordenProduccion.objects.filter(orden_produccion_id=pk).filter(finalizada=True)
        finalizada=0
        if subordenes.count()==subordenes_finalizadas.count():
            finalizada=1
        id=pk
        ambientes = Areas.objects.all()
        op = OrdenProduccion.objects.get(id=pk)



     	return render_to_response('subordenproduccion/list.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes,'op':op,'finalizada':finalizada},  RequestContext(request))



@csrf_exempt
def agregarSubordenproduccion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        secuencia = request.POST.get('secuencia')
        ambiente = request.POST.get('ambiente')
        reproceso = request.POST.get('reproceso', False)

        reproceso = request.POST.get('reproceso', False)
        print('ireproceso:  '+str(reproceso))
        if request.POST['reproceso']=='true':
            print('entro1')
            r=True
            print('valorreproceso:  '+str(r))
            re=SubordenProduccion()
            re.orden_produccion_id=id
            re.areas_id=ambiente
            re.secuencia=secuencia
            re.reproceso=True
            re.save()

        else:
            print('entro2')
            r=False
            print('valorreproceso:  '+str(r))
            re=SubordenProduccion()
            re.orden_produccion_id=id
            re.areas_id=ambiente
            re.secuencia=secuencia
            re.reproceso=False
            re.save()


        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=id).order_by('secuencia')


        ambientes = Areas.objects.all()



        return render_to_response('subordenproduccion/list.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes},  RequestContext(request))

    else:
        raise Http404
@csrf_exempt
def eliminarSubordenproduccion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = SubordenProduccion.objects.get(id=id)
        detalle.delete()


        return HttpResponse(

            )
    else:
        raise Http404

def manoObraView(request, pk):
    if request.method == 'POST':
        contador=request.POST["columnas_receta"]
        id=request.POST["id_subop"]
        fecha_hoy=datetime.now()
        total = 0
        t_hora = 0

        i = 1
        while i <= contador:
            print('i'+str(i))
            print('cont'+str(contador))
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                print('ert'+str(i))
                if 'fecha_kits'+str(i) in request.POST:

                    if 'id_detalle_kits'+str(i) in request.POST:
                        detalle_id=request.POST["id_detalle_kits"+str(i)]
                        detallecompra = SubordenProduccionDetalle.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        fec=request.POST["fecha_kits"+str(i)]
                        if len(fec)>0:
                            detallecompra.fecha =request.POST["fecha_kits"+str(i)]
                        detallecompra.operacion_unitaria = request.POST["operacion_kits" + str(i)]
                        detallecompra.empleado = request.POST["empleado_kits" + str(i)]
                        empleado_inter=request.POST["empleado_interno_kits" + str(i)]
                        if empleado_inter != '0':
                            detallecompra.empleado_interno_id= request.POST["empleado_interno_kits" + str(i)]
                        detallecompra.externo = request.POST.get('externo_kits' + str(i), False)
                        detallecompra.hora_inicio = request.POST["hora_inicio_kits" + str(i)]
                        detallecompra.hora_fin = request.POST["hora_fin_kits" + str(i)]
                        detallecompra.hora_total = request.POST["hora_total_kits" + str(i)]
                        detallecompra.costo_hora = request.POST["costo_hora_kits" + str(i)]
                        detallecompra.tipo_hora = request.POST["tipo_hora_kits" + str(i)]
                        detallecompra.total=request.POST["total_kits"+str(i)]
                        detallecompra.suborden_produccion_id=id
                        detallecompra.updated_at = datetime.now()
                        detallecompra.save()
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)
                        t2 = request.POST["hora_total_kits" + str(i)]
                        t_hora = t_hora + float(t2)

                        print('Tiene detalle'+str(i))
                    else:
                        comprasdetalle=SubordenProduccionDetalle()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        fec=request.POST["fecha_kits"+str(i)]
                        if len(fec)>0:
                            comprasdetalle.fecha =request.POST["fecha_kits"+str(i)]
                        comprasdetalle.operacion_unitaria =request.POST["operacion_kits"+str(i)]
                        comprasdetalle.empleado=request.POST["empleado_kits"+str(i)]
                        comprasdetalle.externo = request.POST.get('externo_kits' + str(i), False)
                        empleado_inter=request.POST["empleado_interno_kits" + str(i)]
                        if empleado_inter != '0':
                            comprasdetalle.empleado_interno_id= request.POST["empleado_interno_kits" + str(i)]
                        comprasdetalle.hora_inicio=request.POST["hora_inicio_kits"+str(i)]
                        comprasdetalle.hora_fin=request.POST["hora_fin_kits"+str(i)]
                        comprasdetalle.hora_total=request.POST["hora_total_kits"+str(i)]
                        comprasdetalle.costo_hora=request.POST["costo_hora_kits"+str(i)]
                        comprasdetalle.total=request.POST["total_kits"+str(i)]
                        comprasdetalle.tipo_hora=request.POST["tipo_hora_kits"+str(i)]
                        comprasdetalle.suborden_produccion_id=id
                        comprasdetalle.save()
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)
                        t2 = request.POST["hora_total_kits" + str(i)]
                        t_hora = t_hora + float(t2)
                        print('No Tiene detalle'+str(i))
                else:
                    print('OJOOOO'+str(i))
            i=i+1
            #ordencompra_form=OrdenCompraForm(request.POST)
        suborden = SubordenProduccionDetalle.objects.filter(suborden_produccion_id=pk).order_by('id')
        subop = SubordenProduccion.objects.get(id=pk)
        if total:
            subop.costo_horas = total
        else:
            subop.costo_horas = 0

        if subop.costo_materiales:
            total_final=subop.costo_materiales+total
        else:
            total_final = total


        subop.total = total_final
        subop.horas=t_hora
        subop.save()
        empleados = Empleado.objects.filter(departamento_id=6)
        cursor = connection.cursor()
        sql='select e.empleado_id,e.nombre_empleado,d.produccion from empleados_empleado e,departamento d where e.departamento_id=d.id and d.produccion is True'
        cursor.execute(sql)
        empleados_produccion= cursor.fetchall()


        context = {
           'section_title':'Actualizar Mano de Obra',
            'button_text':'Actualizar mano de Obra',
            'suborden':suborden,
            'id':pk,
            'subop':subop,
             'empleados': empleados,
             'fecha_hoy':fecha_hoy,
             'empleados_produccion':empleados_produccion,
            'mensaje':'Actualizada con exito1'}


        return render_to_response(
               'subordenproduccion/manoobra.html',
                context,
                context_instance=RequestContext(request))



    else:
        suborden = SubordenProduccionDetalle.objects.filter(suborden_produccion_id=pk).order_by('id')
        empleados = Empleado.objects.filter(departamento_id=6)
        fecha_hoy=datetime.now()
        cursor = connection.cursor()
        sql='select e.empleado_id,e.nombre_empleado,d.produccion from empleados_empleado e,departamento d where e.departamento_id=d.id and d.produccion is True'
        cursor.execute(sql)
        empleados_produccion= cursor.fetchall()
        subop = SubordenProduccion.objects.get(id=pk)
        context = {
        'section_title':'Actualizar SubOrdenProduccion',
        'button_text':'Actualizar',
        'id':pk,
        'subop':subop,
        'empleados': empleados,
        'fecha_hoy':fecha_hoy,
        'empleados_produccion':empleados_produccion,
        'suborden':suborden
        }

        return render_to_response(
            'subordenproduccion/manoobra.html', context,context_instance=RequestContext(request))




def recetaView(request, pk):
    if request.method == 'POST':
        contador=request.POST["columnas_receta"]
        id=request.POST["id_subop"]
        fecha_hoy=datetime.now()
        total = 0

        i = 1
        while i <= contador:
            print('i'+str(i))
            print('cont'+str(contador))
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                print('ert'+str(i))
                if 'material_kits'+str(i) in request.POST:

                    if 'id_detalle_kits'+str(i) in request.POST:
                        prod=request.POST["producto_kits"+str(i)]
                        print ('PRODUCTO'+str(prod))
                        detalle_id=request.POST["id_detalle_kits"+str(i)]
                        detallecompra = OrdenProduccionReceta.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        detallecompra.cantidad =request.POST["cantidad_kits"+str(i)]
                        detallecompra.medida=request.POST["medida_kits"+str(i)]
                        detallecompra.costo=request.POST["costo_kits"+str(i)]
                        f=request.POST["fecha_kits"+str(i)]
                        if f:
                            print ('fecha'+str(f))
                            detallecompra.fecha=request.POST["fecha_kits"+str(i)]
                        detallecompra.material=request.POST["material_kits"+str(i)]
                        if prod == 'None':
                            print ('No hay')
                        else:
                            detallecompra.producto_id=request.POST["producto_kits"+str(i)]
                        detallecompra.total=request.POST["total_kits"+str(i)]
                        detallecompra.suborden_produccion_id=id
                        detallecompra.otros_costos = request.POST.get('otros_costos_kits' + str(i), False)
                        detallecompra.nombre = request.POST["material_kits" + str(i)]

                        #detallecompra.imagen=request.POST["imagen_kits"+str(i)]
                        #detallecompra.updated_at = datetime.now()
                        #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
                        detallecompra.save()

                        print('Tiene detalle'+str(i))
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)
                    else:
                        prod = request.POST["producto_kits" + str(i)]
                        comprasdetalle=OrdenProduccionReceta()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.cantidad =request.POST["cantidad_kits"+str(i)]
                        comprasdetalle.medida=request.POST["medida_kits"+str(i)]
                        comprasdetalle.costo=request.POST["costo_kits"+str(i)]
                        f=request.POST["fecha_kits"+str(i)]
                        if f:
                            print ('fecha'+str(f))
                            comprasdetalle.fecha=request.POST["fecha_kits"+str(i)]
                        comprasdetalle.material=request.POST["material_kits"+str(i)]
                        if prod == 'None':
                            print ('No hay')
                        else:
                            comprasdetalle.producto_id=request.POST["producto_kits"+str(i)]
                        comprasdetalle.total=request.POST["total_kits"+str(i)]
                        comprasdetalle.suborden_produccion_id=id
                        comprasdetalle.otros_costos = request.POST.get('otros_costos_kits' + str(i), False)
                        comprasdetalle.nombre = request.POST["material_kits" + str(i)]
                        comprasdetalle.save()
                        t1 = request.POST["total_kits" + str(i)]
                        total = total + float(t1)

                        print('No Tiene detalle'+str(i))
                else:
                        print('OJOOOO'+str(i))
            i=i+1
            #ordencompra_form=OrdenCompraForm(request.POST)
        suborden = OrdenProduccionReceta.objects.filter(suborden_produccion_id=pk).order_by('id')
        subop = SubordenProduccion.objects.get(id=pk)
        if total:
            subop.costo_materiales = total
        else:
            subop.costo_materiales = 0

        if subop.costo_horas:
            total_final=subop.costo_horas+total
        else:
            total_final = total
        subop.total=total_final
        subop.save()
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo_promedio','precio1','precio2','unidad').filter(tipo_producto=2)
        context = {
           'section_title':'Actualizar Mano de Obra',
            'button_text':'Actualizar mano de Obra',
            'suborden':suborden,
            'id':pk,
            'subop':subop,
            'fecha_hoy':fecha_hoy,
            'productos':productos,
            'mensaje':'Actualizada con exito1'}


        return render_to_response(
               'subordenproduccion/receta.html',
                context,
                context_instance=RequestContext(request))



    else:
        suborden = OrdenProduccionReceta.objects.filter(suborden_produccion_id=pk).order_by('id')
        fecha_hoy=datetime.now()
        subop = SubordenProduccion.objects.get(id=pk)
        productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo_promedio','precio1','precio2','unidad').exclude(tipo_producto=2)

        context = {
        'section_title':'Actualizar SubOrdenProduccion',
        'button_text':'Actualizar',
        'id':pk,
        'subop':subop,
        'productos':productos,
        'fecha_hoy':fecha_hoy,
        'suborden':suborden
        }

        return render_to_response(
            'subordenproduccion/receta.html', context,context_instance=RequestContext(request))


@csrf_exempt
def enviarBodegaView(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        ordenes = OrdenProduccion.objects.get(id=id)
        try:
            ped = PedidoDetalle.objects.get(id=ordenes.pedido_detalle_id)
        except PedidoDetalle.DoesNotExist:
            ped = None

        if ped:
            prod = Producto.objects.get(producto_id=ped.producto_id)
        else:
            prod = Producto.objects.get(producto_id=ordenes.producto_creado_id)

        if ordenes:
            re=OrdenProduccionBodega()
            re.orden_produccion_id=id
            re.producto_id=prod.producto_id
            re.cantidad=ordenes.cantidad
            if ped:
                re.ambiente_id=ped.ambiente_id
            re.largo=ordenes.largo
            re.fondo=ordenes.fondo
            re.alto=ordenes.alto
            re.bodega_id=3
            re.save()
            ordenes.finalizada=True
            ordenes.fecha_finalizacion = datetime.now()
            ordenes.save()
            html='Guardado con exito'
            return HttpResponse(
                html
            )
        else:
            raise Http404


    else:
        raise Http404

def BodegaRecepcionView(request):
    if request.method == 'POST':
        subordenes = OrdenProduccionBodega.objects.all()
        ambientes = Areas.objects.all()
        contador=request.POST["columnas_receta"]

        i=0
        while int(i) <= int(contador):
            i+= 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'suborden_id'+str(i) in request.POST:
                    detalle_id=request.POST["suborden_id"+str(i)]
                    subor = OrdenProduccionBodega.objects.get(id=detalle_id)
                    subor.updated_by = request.user.get_full_name()
                    subor.cantidad_recibida =request.POST["cantidad_guardar"+str(i)]
                    subor.observaciones=request.POST["observaciones"+str(i)].strip()
                    subor.updated_at = datetime.now()
                    subor.save()

                    print('Tiene detalle'+str(i))
                else:
                    print('No tiene detalle'+str(i))
        subordenes = OrdenProduccionBodega.objects.all()
        ambientes = Areas.objects.all()

        return render_to_response('subordenproduccion/listbodega.html', { 'subordenes': subordenes,'ambientes':ambientes},  RequestContext(request))



    else:
        subordenes = OrdenProduccionBodega.objects.all()
        ambientes = Areas.objects.all()



        return render_to_response('subordenproduccion/listbodega.html', { 'subordenes': subordenes,'ambientes':ambientes},  RequestContext(request))

def enviarBodegaCrudoView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        subopid = request.POST.get('subopid')

        orden = SubordenProduccion.objects.get(id=subopid)
        ordenes = OrdenProduccion.objects.get(id=id)
        try:
            ped = PedidoDetalle.objects.get(id=ordenes.pedido_detalle_id)
        except PedidoDetalle.DoesNotExist:
            ped = None

        if ped:
            prod = Producto.objects.get(producto_id=ped.producto_id)
        else:
            prod = Producto.objects.get(producto_id=ordenes.producto_creado_id)

        if ordenes:
            re=OrdenProduccionBodega()
            re.orden_produccion_id=id
            re.producto_id=prod.producto_id
            re.cantidad=ordenes.cantidad
            re.ambiente_id=ped.ambiente_id
            re.largo=ordenes.largo
            re.fondo=ordenes.fondo
            re.alto=ordenes.alto
            re.bodega_id=4
            re.observaciones='Producto no terminado'
            re.suborden_produccion_id=subopid
            re.save()
            ordenes.bodega_productos_blanco=True
            ordenes.save()
            html='Guardado con exito'
            return HttpResponse(
                html
            )
        else:
            raise Http404


    else:
        raise Http404
def OrdenProduccionBodegaUpdateView(request,pk):
    if request.method == 'POST':
        orden = OrdenProduccionBodega.objects.get(id=pk)
        ordenproduccion_form = OrdenProduccionBodegaForm(request.POST,request.FILES,instance=orden)

        if ordenproduccion_form.is_valid():
            new_orden=ordenproduccion_form.save()
            new_orden.save()

            context = {
           'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'mensaje':'Registro actualizado con exito',
            'id':pk,
            'form':ordenproduccion_form
             }


            return render_to_response(
                'subordenproduccion/updaterecepcionbodega.html',
                context,
                context_instance=RequestContext(request))
        else:

            ordenproduccion_form=OrdenProduccionBodegaForm(request.POST)
            #detalle = ComprasDetalle.objects.filter(compra_id=ordencompra.compra_id)


            context = {
            'section_title':'Actualizar Orden Produccion',
            'button_text':'Actualizar',
            'mensaje': 'No se actualizado',
            'id': pk,
            'form':ordenproduccion_form
            }

            return render_to_response(
            'subordenproduccion/updaterecepcionbodega.html',
            context,
            context_instance=RequestContext(request))
    else:
        ordenproduccion=OrdenProduccionBodega.objects.get(id=pk)
        ordenproduccion_form=OrdenProduccionBodegaForm(instance=ordenproduccion)

        context = {
            'section_title':'Actualizar Orden Compra',
            'button_text':'Actualizar',
            'id': pk,
            'form':ordenproduccion_form
            }

        return render_to_response(
            'subordenproduccion/updaterecepcionbodega.html',
            context,
            context_instance=RequestContext(request))

def SubOrdenProduccionListDetalleView(request, pk):
    if request.method == 'POST':
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        ambientes = Areas.objects.all()
        id=pk
        contador=request.POST["columnas_receta"]

        i=0
        while int(i) <= int(contador):
            i+= 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'suborden_id'+str(i) in request.POST:
                    detalle_id=request.POST["suborden_id"+str(i)]
                    subor = SubordenProduccion.objects.get(id=detalle_id)
                    subor.updated_by = request.user.get_full_name()
                    subor.areas_id =request.POST["id_areas"+str(i)]
                    subor.secuencia=request.POST["secuencia_guardar"+str(i)]
                    subor.observaciones=request.POST["observaciones"+str(i)].strip()
                    subor.finalizada=request.POST.get('finalizada'+str(i), False)
                    subor.updated_at = datetime.now()
                    subor.save()

                    print('Tiene detalle'+str(i))
                else:
                    print('No tiene detalle'+str(i))
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        op = OrdenProduccion.objects.get(id=pk)
        id=pk
        ambientes = Areas.objects.all()
        cursor = connection.cursor()
        sql='select c.anio,c.mes,c.fecha,cd.orden_produccion_id,sum(cd.total_cf) from costo_fabricacion c,costo_fabricacion_detalle cd where cd.costo_fabricacion_id=c.id and cd.orden_produccion_id='+str(pk)+' and c.anulado is not True group by c.anio,c.mes,c.fecha,cd.orden_produccion_id'
        cursor.execute(sql)
        costos_fabricacion= cursor.fetchall()
        return render_to_response('subordenproduccion/listsubordenesdetalle.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes,'op':op,'costos_fabricacion':costos_fabricacion},  RequestContext(request))



    else:
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        id=pk
        ambientes = Areas.objects.all()
        op = OrdenProduccion.objects.get(id=pk)
        porcentaje=op.porcentaje_costo
        html=''
        i=0
        j=0
        total_r=0
        html_rep=''
        total=0
        total_d=0
        total_reproceso=0
        for orden in subordenes:
            if orden.reproceso:
                j = j + 1
                costo_m = 0
                costo_h = 0
                html_rep += '<tr><td><input type="hidden" id="suborden_id' + str(j) + '" name="suborden_id' + str(
                    j) + '" value="' + str(
                    orden.id) + '"><a class="btn btn-danger remove_fields" onclick="eliminar( ' + str(
                    orden.id) + ',' + str(id) + ')"><i class=" glyphicon glyphicon-trash icon-white"></i></a></td>'
                html_rep += '<td>' + str(orden.areas.descripcion) + '</td>'
                html_rep += '<td>' + str(orden.secuencia) + '</td>'
                html_rep += '<td>' + str(orden.horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m = orden.costo_materiales
                else:
                    costo_m = 0
                if orden.costo_horas:
                    costo_h = orden.costo_horas
                else:
                    costo_h = 0

                total_r = costo_h + costo_m
                total_reproceso = total_reproceso + total_r
                html_rep += '<td>' + str(total_r) + '</td>'
                html_rep += '<td>' + str(orden.observaciones) + '</td>'
                if orden.finalizada:
                    html_rep += '<td>Finalizada</td>'
                else:
                    html_rep += '<td>En proceso</td>'
                html_rep += '<td><a href="/subordenproduccion/subordenproduccion/' + str(
                    orden.id) + '/manoObra/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Mano de Obra</button>	</a>'
                html_rep += '<a href="/subordenproduccion/subordenproduccion/' + str(
                    orden.id) + '/receta/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Materiales</button>	</a>'
                html_rep += '</td>'
                html_rep += '</tr>'

            else:
                i=i+1
                costo_m=0
                costo_h=0
                html += '<tr><td><input type="hidden" id="suborden_id'+str(i)+'" name="suborden_id'+str(i)+'" value="'+str(orden.id)+'"><a class="btn btn-danger remove_fields" onclick="eliminar( '+str(orden.id)+','+str(id)+')"><i class=" glyphicon glyphicon-trash icon-white"></i></a></td>'
                html += '<td>' + str(orden.areas.descripcion ) + '</td>'
                html += '<td>' + str(orden.secuencia) + '</td>'
                html += '<td>' + str(orden.horas ) + '</td>'
                html += '<td>' + str(orden.costo_horas ) + '</td>'
                html += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m=orden.costo_materiales
                else:
                    costo_m=0
                if orden.costo_horas:
                    costo_h=orden.costo_horas
                else:
                    costo_h=0

                total_d=costo_h+costo_m
                total=total+total_d
                html += '<td>' + str(total_d) + '</td>'
                html += '<td>' + str(orden.observaciones ) + '</td>'
                if orden.finalizada:
                    html += '<td>Finalizada</td>'
                else:
                    html += '<td>En proceso</td>'
                html += '<td><a href="/subordenproduccion/subordenproduccion/'+str(orden.id)+'/manoObra/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Mano de Obra</button>	</a>'
                html +='<a href="/subordenproduccion/subordenproduccion/'+str(orden.id)+'/receta/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Materiales</button>	</a>'
                html += '</td>'
                html += '</tr>'

        html_total = ''
        html_total += '<tr><td colspan="6" style="text-align:right"><b>TOTAL</b></td>'
        html_total += '<td>' + str(total) + '</td>'
        html_total += '<td></td>'
        html_total += '<td></td>'
        html_total += '<td></td>'
        html_total += '</tr>'
        if porcentaje:
            porcentaje=porcentaje
        else:
            porcentaje=0
        
        op.costo=total
        op.porcentaje_costo=porcentaje
        
        costo_fijo=porcentaje*total/100
        total_f=total+costo_fijo
        op.costo_directo=costo_fijo
        op.costo_final=total_f
        op.save()

        html_total_rep = ''
        html_total_rep += '<tr><td colspan="6" style="text-align:right"><b>TOTAL</b></td>'
        html_total_rep += '<td>' + str(total_reproceso) + '</td>'
        html_total_rep += '<td></td>'
        html_total_rep += '<td></td>'
        html_total_rep += '<td></td>'
        html_total_rep += '</tr>'
        cursor = connection.cursor()
        sql='select c.anio,c.mes,c.fecha,cd.orden_produccion_id,sum(cd.total_cf) from costo_fabricacion c,costo_fabricacion_detalle cd where cd.costo_fabricacion_id=c.id and cd.orden_produccion_id='+str(pk)+' and c.anulado is not True group by c.anio,c.mes,c.fecha,cd.orden_produccion_id'
        cursor.execute(sql)
        costos_fabricacion= cursor.fetchall()


        return render_to_response('subordenproduccion/listsubordenesdetalle.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes,'op':op,'html':html,'html_total':html_total,'html_rep':html_rep,'html_total_rep':html_total_rep,'total_d':total,'costos_fabricacion':costos_fabricacion},  RequestContext(request))

def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    subop=SubordenProduccion.objects.get(id=pk)
    ordenproduccion=OrdenProduccion.objects.get(id=subop.orden_produccion_id)
    pedido=PedidoDetalle.objects.get(id=ordenproduccion.pedido_detalle_id)
    p=Pedido.objects.get(id=pedido.pedido_id)


    html = render_to_string('subordenproduccion/imprimir.html', {'pagesize':'A4','subop':subop,'pedido':p,'ordenproduccion':ordenproduccion}, context_instance=RequestContext(request))
    return generar_pdf(html)
    # context = {
    #         'ordenproduccion':ordenproduccion,
    #         }

    # return render_to_response(
    #         'ordenproduccion/imprimir.html',
    #         context,
    #         context_instance=RequestContext(request))

def generar_pdf(html):
    # Funci?n para generar el archivo PDF y devolverlo mediante HttpResponse
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))

@csrf_exempt
def eliminarManoObra(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = SubordenProduccionDetalle.objects.get(id=id)
	detalle.delete()
        return HttpResponse(

            )



    else:
        subordenes = SubordenProduccionDetalle.objects.get(id=id)
	detalle.delete()
        id=id
        ambientes = Areas.objects.all()
	subordenes =SubordenProducccion.objects.all()



        return render_to_response('subordenproduccion/list.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes},  RequestContext(request))


@login_required()
def EliminarRecetaSubopView(request):
    pk = request.POST["id"]
    objetos = OrdenProduccionReceta.objects.get(id=pk)

    #id = objetos.padre_id
    objetos.delete()
    return HttpResponse(

    )

def SubOrdenProduccionListDetalleImprimirView(request, pk):
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk).order_by('secuencia')
        id=pk
        ambientes = Areas.objects.all()
        op = OrdenProduccion.objects.get(id=pk)
        html=''
        i=0
        total=0
        total_r = 0
        html_rep = ''
        total_reproceso = 0
        for orden in subordenes:
            if orden.reproceso:
                j = j + 1
                costo_m = 0
                costo_h = 0
                html_rep += '<tr>'
                html_rep += '<td>' + str(orden.areas.descripcion) + '</td>'
                html_rep += '<td>' + str(orden.secuencia) + '</td>'
                html_rep += '<td>' + str(orden.horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m = orden.costo_materiales
                else:
                    costo_m = 0
                if orden.costo_horas:
                    costo_h = orden.costo_horas
                else:
                    costo_h = 0

                total_r = costo_h + costo_m
                total_reproceso = total_reproceso + total_r
                html_rep += '<td>' + str(total_r) + '</td>'
                html_rep += '<td>' + str(orden.observaciones) + '</td>'

                html_rep += '</tr>'

            else:
                i=i+1
                costo_m=0
                costo_h=0
                html += '<tr>'
                html += '<td>' + str(orden.areas.descripcion ) + '</td>'
                html += '<td>' + str(orden.secuencia) + '</td>'
                html += '<td>' + str(orden.horas ) + '</td>'
                html += '<td>' + str(orden.costo_horas ) + '</td>'
                html += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m=orden.costo_materiales
                else:
                    costo_m=0
                if orden.costo_horas:
                    costo_h=orden.costo_horas
                else:
                    costo_h=0

                total_d=costo_h+costo_m
                total=total+total_d
                html += '<td>' + str(total_d) + '</td>'
                html += '<td>' + str(orden.observaciones ) + '</td>'
                # if orden.finalizada:
                #     html += '<td>Finalizada</td>'
                # else:
                #     html += '<td>En proceso</td>'
                #
                # html += '</tr>'

        html_total = ''
        html_total += '<tr><td colspan="5" style="text-align:right"><b>TOTAL</b></td>'
        html_total += '<td>' + str(total) + '</td>'
        html_total += '<td></td>'

        html_total += '</tr>'
        html_total_rep = ''
        html_total_rep += '<tr><td colspan="5" style="text-align:right"><b>TOTAL</b></td>'
        html_total_rep += '<td>' + str(total_reproceso) + '</td>'
        html_total_rep += '<td></td>'

        html_total_rep += '</tr>'
        total_final = 0
        total_final = total + total_reproceso

        html_total_final = ''
        html_total_final += '<table border="0" ><tr><td colspan="6" style="text-align:right"><b>TOTAL DE COSTO DE PRODUCCION:</b></td>'
        html_total_final += '<td style="text-align:right"><b>$' + str(total_final) + '</b></td>'

        html_total_final += '</tr></table>'


        html1 = render_to_string('subordenproduccion/subordenes_imprimir_costo.html',
                                {'pagesize': 'A4', 'op':op,'html':html,'html_total':html_total,'html_rep':html_rep,'html_total_rep':html_total_rep,'html_total_final':html_total_final,'media_root':settings.MEDIA_ROOT},
                                context_instance=RequestContext(request))
        return generar_pdf(html1)
        # return render_to_response('subordenproduccion/subordenes_imprimir_costo.html', { 'op':op,'html':html,'html_total':html_total},  RequestContext(request))


@login_required()
@csrf_exempt
def guardarCosto(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        pk=id
        porcentaje = request.POST.get('porcentaje')
        total = request.POST.get('total')
        costo = request.POST.get('costo_produccion')
        costo_fijo = request.POST.get('costo_fijo')
        print costo
        print costo_fijo
        try:
            ordenp =OrdenProduccion.objects.filter(id=id)
        except OrdenProduccion.DoesNotExist:
            ordenp = None

        if ordenp:
            for orden in ordenp:
                orden.porcentaje_costo=porcentaje
                orden.costo=costo
                orden.costo_directo=costo_fijo
                orden.costo_final=total
                orden.save()
        
        subordenes = SubordenProduccion.objects.filter(orden_produccion_id=pk)
        id=pk
        ambientes = Areas.objects.all()
        op = OrdenProduccion.objects.get(id=pk)
        html=''
        i=0
        j=0
        total_r=0
        html_rep=''
        total=0
        total_reproceso=0
        for orden in subordenes:
            if orden.reproceso:
                j = j + 1
                costo_m = 0
                costo_h = 0
                html_rep += '<tr><td><input type="hidden" id="suborden_id' + str(j) + '" name="suborden_id' + str(
                    j) + '" value="' + str(
                    orden.id) + '"><a class="btn btn-danger remove_fields" onclick="eliminar( ' + str(
                    orden.id) + ',' + str(id) + ')"><i class=" glyphicon glyphicon-trash icon-white"></i></a></td>'
                html_rep += '<td>' + str(orden.areas.descripcion) + '</td>'
                html_rep += '<td>' + str(orden.secuencia) + '</td>'
                html_rep += '<td>' + str(orden.horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_horas) + '</td>'
                html_rep += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m = orden.costo_materiales
                else:
                    costo_m = 0
                if orden.costo_horas:
                    costo_h = orden.costo_horas
                else:
                    costo_h = 0

                total_r = costo_h + costo_m
                total_reproceso = total_reproceso + total_r
                html_rep += '<td>' + str(total_r) + '</td>'
                html_rep += '<td>' + str(orden.observaciones) + '</td>'
                if orden.finalizada:
                    html_rep += '<td>Finalizada</td>'
                else:
                    html_rep += '<td>En proceso</td>'
                html_rep += '<td><a href="/subordenproduccion/subordenproduccion/' + str(
                    orden.id) + '/manoObra/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Mano de Obra</button>	</a>'
                html_rep += '<a href="/subordenproduccion/subordenproduccion/' + str(
                    orden.id) + '/receta/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Materiales</button>	</a>'
                html_rep += '</td>'
                html_rep += '</tr>'

            else:
                i=i+1
                costo_m=0
                costo_h=0
                html += '<tr><td><input type="hidden" id="suborden_id'+str(i)+'" name="suborden_id'+str(i)+'" value="'+str(orden.id)+'"><a class="btn btn-danger remove_fields" onclick="eliminar( '+str(orden.id)+','+str(id)+')"><i class=" glyphicon glyphicon-trash icon-white"></i></a></td>'
                html += '<td>' + str(orden.areas.descripcion ) + '</td>'
                html += '<td>' + str(orden.secuencia) + '</td>'
                html += '<td>' + str(orden.horas ) + '</td>'
                html += '<td>' + str(orden.costo_horas ) + '</td>'
                html += '<td>' + str(orden.costo_materiales) + '</td>'
                if orden.costo_materiales:
                    costo_m=orden.costo_materiales
                else:
                    costo_m=0
                if orden.costo_horas:
                    costo_h=orden.costo_horas
                else:
                    costo_h=0

                total_d=costo_h+costo_m
                total=total+total_d
                html += '<td>' + str(total_d) + '</td>'
                html += '<td>' + str(orden.observaciones ) + '</td>'
                if orden.finalizada:
                    html += '<td>Finalizada</td>'
                else:
                    html += '<td>En proceso</td>'
                html += '<td><a href="/subordenproduccion/subordenproduccion/'+str(orden.id)+'/manoObra/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Mano de Obra</button>	</a>'
                html +='<a href="/subordenproduccion/subordenproduccion/'+str(orden.id)+'/receta/"><button type="button" class="btn btn-info btn-xs"><i class="fa fa-cog"></i> Materiales</button>	</a>'
                html += '</td>'
                html += '</tr>'

        html_total = ''
        html_total += '<tr><td colspan="6" style="text-align:right"><b>TOTAL</b></td>'
        html_total += '<td>' + str(total) + '</td>'
        html_total += '<td></td>'
        html_total += '<td></td>'
        html_total += '<td></td>'
        html_total += '</tr>'

        html_total_rep = ''
        html_total_rep += '<tr><td colspan="6" style="text-align:right"><b>TOTAL</b></td>'
        html_total_rep += '<td>' + str(total_reproceso) + '</td>'
        html_total_rep += '<td></td>'
        html_total_rep += '<td></td>'
        html_total_rep += '<td></td>'
        html_total_rep += '</tr>'


        return render_to_response('subordenproduccion/listsubordenesdetalle.html', { 'subordenes': subordenes,'id':id,'ambientes':ambientes,'op':op,'html':html,'html_total':html_total,'html_rep':html_rep,'html_total_rep':html_total_rep,'total_d':total_d},  RequestContext(request))



    else:
        raise Http404

def export_to_excel_mano_obra(request,pk):
    suborden = SubordenProduccionDetalle.objects.filter(suborden_produccion_id=pk)
    subop = SubordenProduccion.objects.get(id=pk)
    context = {
        'section_title':'Actualizar SubOrdenProduccion',
        'button_text':'Actualizar',
        'id':pk,
        'subop':subop,
        'suborden':suborden
        }
      
   
    response = render_to_response('subordenproduccion/mano_obra_imprimir.html', context,context_instance=RequestContext(request))

    # this is the output file
    nombre='MANODEOBRA_'+subop.orden_produccion.tipo+'-'+subop.orden_produccion.codigo
    filename = nombre+'.xls'

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response



def export_to_excel_receta(request,pk):
    suborden = OrdenProduccionReceta.objects.filter(suborden_produccion_id=pk)
    subop = SubordenProduccion.objects.get(id=pk)
    productos = Producto.objects.values('producto_id', 'codigo_producto','descripcion_producto', 'tipo_producto','bloquea','medida_peso','costo_promedio','precio1','precio2','unidad').exclude(tipo_producto=2)
    context = {
        'section_title':'Actualizar SubOrdenProduccion',
        'button_text':'Actualizar',
        'id':pk,
        'subop':subop,
        'productos':productos,
        'suborden':suborden
        }

      
   
    response = render_to_response('subordenproduccion/receta_imprimir.html', context,context_instance=RequestContext(request))

    # this is the output file
    nombre='RECETA_'+subop.orden_produccion.tipo+'-'+subop.orden_produccion.codigo
    filename = nombre+'.xls'

    response['Content-Disposition'] = 'attachment; filename='+filename
    response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-16'
    return response



@login_required()
def consultar_subop_receta(request):
    if request.method == "POST":
        fila = request.POST['fila']
        areas = request.POST['areas']
        cursor = connection.cursor()
        query = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.codigo_producto,p.descripcion_producto,opr.cantidad,a.id,a.descripcion,p.unidad,p.costo_promedio as costo,opr.egresos,opr.ingresos from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id '
        if areas:
            query+=' and subop.areas_id='+str(areas)
        query+= ' left join orden_produccion o ON o.id=subop.orden_produccion_id  left join areas a ON a.id=subop.areas_id '
        query+= ' where o.finalizada is not True and o.despachar is True and opr.egresos < opr.cantidad '
        query+= ' order by o.id'
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('subordenproduccion/mostrar_subop_receta.html',
                                  {'ro': ro, 'fila': fila,},RequestContext(request))
    else:
        fila = request.POST['fila']
        areas = request.POST['areas']
        cursor = connection.cursor()
        query = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.codigo_producto,p.descripcion_producto,opr.cantidad,a.id,a.descripcion,p.unidad,p.costo_promedio as costo,opr.egresos,opr.ingresos from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id left join orden_produccion o ON o.id=subop.orden_produccion_id left join areas a ON a.id=subop.areas_id '
        query+= ' where o.finalizada is not True and o.despachar is True and opr.egresos < opr.cantidad order by o.id'
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('subordenproduccion/mostrar_subop_receta.html',
                                  {'ro': ro, 'fila': fila,},RequestContext(request))
    
@login_required()
def SubOrdenProduccionListDespacharView(request):
    #ordenes = OrdenProduccion.objects.filter(aprobada=True).order_by('id')
    query='select distinct o.id,o.tipo,o.codigo,o.fecha,o.descripcion,o.detalle,c.nombre_cliente,o.cantidad,o.aprobada from orden_produccion o,cliente c,orden_produccion_receta opr,suborden_produccion sp where c.id_cliente=o.cliente_id and sp.orden_produccion_id=o.id  and opr.suborden_produccion_id=sp.id and opr.aprobacion_despachar is not True'
    cursor = connection.cursor()
    cursor.execute(query)
    ro = cursor.fetchall()


    return render_to_response('subordenproduccion/aprobada.html', {'ordenes': ro}, RequestContext(request))



@login_required()
@transaction.atomic
def OrdenProduccionAprobarDespachoByPkView(request, pk):
    with transaction.atomic():

        objetos = OrdenProduccion.objects.get(id= pk)
        objetos.despachar = True
        objetos.fecha_aprobacion_despacho = datetime.now()
        objetos.save()
        cursor = connection.cursor()
        query = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.codigo_producto,p.descripcion_producto,opr.cantidad,a.id,a.descripcion,p.unidad,p.costo_promedio as costo,opr.egresos,opr.ingresos,opr.nombre,opr.otros_costos from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id left join orden_produccion o ON o.id=subop.orden_produccion_id  left join areas a ON a.id=subop.areas_id where  o.id='+str(pk)+' order by o.id'
        cursor.execute(query)
        ro = cursor.fetchall()
        for o in ro:
            try:
                opr = OrdenProduccionReceta.objects.get(id=o[0])
            except OrdenProduccionReceta.DoesNotExist:
                opr = None
            if opr:
                opr.aprobacion_despachar=True
                if opr.aprobado_por:
                    print 'ya aprobao'
                else:
                    opr.aprobado_por= request.user.get_full_name()
                    
                opr.save()
            
        
       
    return HttpResponseRedirect('/subordenproduccion/subordenproduccionDespachar')



@login_required()
def consultar_subopxarea_receta(request):
    if request.method == "POST":
        #fila = request.POST['fila']
        fila=0
        id = request.POST['id']
        cursor = connection.cursor()
        query = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.codigo_producto,p.descripcion_producto,opr.cantidad,a.id,a.descripcion,p.unidad,p.costo_promedio as costo,opr.egresos,opr.ingresos,opr.nombre,opr.otros_costos,opr.aprobacion_despachar from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id left join orden_produccion o ON o.id=subop.orden_produccion_id  left join areas a ON a.id=subop.areas_id where  o.id='+str(id)+' order by o.id'
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('subordenproduccion/mostrar_subop_recetaxareas_completa.html',
                                  {'ro': ro, 'fila': fila,},RequestContext(request))
    else:
        #fila = request.POST['fila']
        cursor = connection.cursor()
        id = request.POST['id']
        fila=0
        query = 'select distinct opr.id,o.tipo,o.codigo,o.id,p.producto_id,p.codigo_producto,p.descripcion_producto,opr.cantidad,a.id,a.descripcion,p.unidad,p.costo_promedio as costo,opr.egresos,opr.ingresos,opr.nombre,opr.otros_costos,opr.aprobacion_despachar from orden_produccion_receta opr left join producto p ON p.producto_id=opr.producto_id left join suborden_produccion subop ON subop.id=opr.suborden_produccion_id left join orden_produccion o ON o.id=subop.orden_produccion_id left join areas a ON a.id=subop.areas_id where o.id='+str(id)+' order by o.id'
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('subordenproduccion/mostrar_subop_recetaxareas_completa.html',
                                  {'ro': ro, 'fila': fila,},RequestContext(request))
    
    
    
    
def analisisManoObra(request):
    return render_to_response('subordenproduccion/analisis_costo_horas_asignadas.html', {}, RequestContext(request))

@csrf_exempt
def obtenerAnalisisManoObra(request):
    return render_to_response('subordenproduccion/analisis_costo_horas_asignadas.html', {}, RequestContext(request))
@csrf_exempt
def obtenerAnalisisMano(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
       

        cursor = connection.cursor()
        cursor.execute("select distinct sdd.empleado,sdd.empleado_interno_id,sum(sdd.hora_total),sum(sdd.costo_hora),sum(sdd.total),sd.areas_id,a.descripcion from suborden_produccion_detalle sdd,suborden_produccion sd,areas a where sdd.suborden_produccion_id=sd.id and a.id=sd.areas_id and sdd.fecha>='" + fechainicial + "' and sdd.fecha<='" + fechafin + "'  group by sdd.empleado,sdd.empleado_interno_id,sd.areas_id,a.descripcion order by sdd.empleado")
        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead><tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        html+= '<th >Areas</th>'
        html+= '<th style="width:120px !important">Empleado</th>'
        #html+= '<th>Operario</th>'
        html+= '<th>Horas</th>'
        html+= '<th>Cto.Horas</th>'
        html+= '<th>Total</th>'
        
        html+= '<th>Horas Trabajadas</th>'
        html+= '<th>Costo Horas</th>'
        html+= '<th>Total</th>'
        
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
           
            
            html += '<td style="text-align:center">' + str(p[6].encode('utf8')) + '</td>'
            #html += '<td style="text-align:center">' + str(p[10]) + '</td>'
            html += '<td>' + str(p[0].encode('utf8')) + '</td>'
            # html += '<td>' + str(p[15]) + '</td>'
            # html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            # html += '<td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[3]) + '</td>'
            html += '<td>' + str(p[4]) + '</td>'
            sql1="select em.empleado_id,sum(e.valor),sum(e.horas),sum(d.valor),sum(d.dias) from empleados_empleado em left join ingresos_rol_empleado e  on e.empleado_id=em.empleado_id  and e.pagar is True and (e.tipo_ingreso_egreso_empleado_id=5 or e.tipo_ingreso_egreso_empleado_id=25 or e.tipo_ingreso_egreso_empleado_id=26 ) left join dias_no_laborados_rol_empleado d  on d.empleado_id=em.empleado_id  and d.descontar is True and (d.tipo_ausencia_id=3 or d.tipo_ausencia_id=7 or d.tipo_ausencia_id=8 ) where 1=1  and em.empleado_id="+str(p[1])+" and em.empleado_id IN (select er.empleado_id from rol_pago_detalle er,rol_pago r where er.rol_pago_id=r.id)   group by em.empleado_id "
            cursor.execute(sql1)
            row2 = cursor.fetchall()
            cant_horase=0
            total_horas_e=0
            cant_horasdesc=0
            total_horasdesc=0
            for p2 in row2:
                cant_horase=p[1]
                total_horas_e=p[2]
                cant_horasdesc=p[3]
                total_horasdesc=p[4]

            html += '<td style="text-align:right">' + str("%2.2f" % cant_horase).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % total_horas_e).replace('.', ',') + '</td>'
            diferencia_cantidad=float(p[1])-float(cant_horase)
            diferencia_costo=float(p[2])-float(total_horas_e)
            
            html += '<td style="text-align:right">' + str("%2.2f" % diferencia_cantidad).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % diferencia_costo).replace('.', ',') + '</td>'

            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404



def analisisCostoMateriales(request):
    return render_to_response('subordenproduccion/analisis_costo_materiales.html', {}, RequestContext(request))

@csrf_exempt
def obtenerAnalisisCostoMateriales(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        
        

        cursor = connection.cursor();
        
        cursor.execute("select distinct sdd.material,sdd.producto_id,p.unidad,sum(sdd.costo),sum(sdd.total),sd.areas_id,a.descripcion,sum(sdd.cantidad) from orden_produccion_receta sdd,suborden_produccion sd,areas a,producto p where p.producto_id=sdd.producto_id and sdd.suborden_produccion_id=sd.id and a.id=sd.areas_id and sdd.fecha>='" + fechainicial + "'and sdd.fecha<='" + fechafin + "'  group by sdd.material,sdd.producto_id,p.unidad,sd.areas_id,a.descripcion order by sdd.material");
        row = cursor.fetchall();
        total = 0
        subtotal = 0
        iva = 0
        # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html = '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead>'
        html += '<tr>'
        html += '<th colspan="3" >PRODUCTO</th>'
        html += '<th colspan="3" style="text-align:center">Produccion</th>'
        html += '<th colspan="2" style="text-align:center" >Orden de Egreso</th>'
        html += '<th colspan="2">Resultados</th>'
        html += '</tr>'
        
        html += '<tr>'
        #html = '<th>RUC del Proveedor</th><th>Codigo del Proveedor</th>'
        # html+= '<th style="width:120px !important">Fecha</th>'
        # html+= '<th style="width:120px !important">OP-OR</th>'
        html+= '<th>Areas</th>'
        #html+= '<th style="width:300px !important">Produccion</th>'
        html+= '<th style="width:100px !important">Material</th>'
        html+= '<th>Unid</th>'
        html+= '<th >Cantidad</th>'
        html+= '<th>Costo Unid.</th>'
        html+= '<th>Total</th>'
        html+= '<th>Cantidad Orden de Egreso</th>'
        html+= '<th>Total</th>'
        html+= '<th>Diferencia en Cantidad</th>'
        html+= '<th>Diferencia Total</th>'
        
    
        ##html+='<th>Proveedor</th>'
        ##html+='<th>Forma de Pago</th>'
       
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        
        for p in row:
            diferencia_cantidad=0
            diferencia_costo=0
            
           
            
            html += '<td style="text-align:center">' + str(p[6].encode('utf8')) + '</td>'
            html += '<td style="text-align:center">' + str(p[0].encode('utf8')) + '</td>'
            #html += '<td>' + str(p[8].encode('utf8')) + '</td>'
            #html += '<td>' + str(p[13].encode('utf8')) + '</td>'
            #html += '<td>' + str(p[1].encode('utf8')) + '</td>'
            html += '<td>' + str(p[2]) + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % p[7]).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % p[3]).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % p[4]).replace('.', ',') + '</td>'
            sql1="select distinct sdd.producto_id,sum(sdd.cantidad),sum(sdd.total),sdd.areas_id,a.descripcion from orden_egreso_detalle sdd,egreso_orden_egreso sd,areas a,producto p where p.producto_id=sdd.producto_id and a.id=sdd.areas_id and sd.fecha>='" + fechainicial + "'and sd.fecha<='" + fechafin + "' and sd.orden_egreso_id=sdd.orden_egreso_id and sdd.areas_id="+ str(p[5]) + " and sdd.producto_id="+ str(p[1]) + " group by sdd.producto_id,sdd.areas_id,a.descripcion  "
            cursor.execute(sql1)
            row2 = cursor.fetchall()
            cant_egreso=0
            total_egreso=0
            for p2 in row2:
                cant_egreso=p2[1]
                total_egreso=p2[2]

            html += '<td style="text-align:right">' + str("%2.2f" % cant_egreso).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % total_egreso).replace('.', ',') + '</td>'
            diferencia_cantidad=float(p[7])-float(cant_egreso)
            diferencia_costo=float(p[4])-float(total_egreso)
            
            html += '<td style="text-align:right">' + str("%2.2f" % diferencia_cantidad).replace('.', ',') + '</td>'
            html += '<td style="text-align:right">' + str("%2.2f" % diferencia_costo).replace('.', ',') + '</td>'
            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404
    
    
def cierreMensualProduccion(request):
    if request.method == 'POST':
        form = CostoFabricacionForm(request.POST)
        print "ingresa a crear el movimiento"
        try:
            if form.is_valid():
                print "validar  form"
                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    costo = CostoFabricacion()
                    costo.mes = int(cleaned_data.get('mes'))
                    costo.anio = int(cleaned_data.get('anio'))
                    costo.updated_by = request.user.get_full_name()
                    costo.created_by = request.user.get_full_name()
                    costo.updated_at = datetime.now()
                    costo.created_at = datetime.now()
                    costo.fecha = datetime.now()
                    costo.save()
                    arreglo_costeos = json.loads(request.POST['arreglo_costeos'])
                    print arreglo_costeos
                    if len(arreglo_costeos) > 0:
                        print "entro"
                        for item in arreglo_costeos:
                            print item['id']
                           
                            costeo_detalle = CostoFabricacionDetalle()
                            costeo_detalle.costo_fabricacion_id = costo.id
                            costeo_detalle.orden_produccion_id = item['id']
                            costeo_detalle.horas_subop = item['horas'].replace(',', '.')
                            costeo_detalle.factor_horas = item['factor'].replace(',', '.')
                            costeo_detalle.horas_nomina = item['nomina'].replace(',', '.')
                            costeo_detalle.mod = item['nomina_md'].replace(',', '.')
                            costeo_detalle.nomina_mod = item['nomina_md'].replace(',', '.')
                            costeo_detalle.bodega = item['bodega'].replace(',', '.')
                            costeo_detalle.factor_calculo_horas = item['factor'].replace(',', '.')
                            costeo_detalle.moi = item['nomina_mi'].replace(',', '.')
                            costeo_detalle.bs_mod = item['bs_md'].replace(',', '.')
                            costeo_detalle.bs_moi = item['bs_mi'].replace(',', '.')
                            costeo_detalle.alimentacion = item['alimentacion'].replace(',', '.')
                            costeo_detalle.otros_prod = item['otros'].replace(',', '.')
                            costeo_detalle.serv_planta = item['planta'].replace(',', '.')
                            costeo_detalle.mantenimiento = item['mantenimiento'].replace(',', '.')
                            costeo_detalle.depreciacion = item['depreciacion'].replace(',', '.')
                            costeo_detalle.aport_patronal = item['aporte_patronal'].replace(',', '.')
                            costeo_detalle.fondo_reserva = item['fondo_reserva'].replace(',', '.')
                            costeo_detalle.impto_renta = item['imp_renta'].replace(',', '.')
                            costeo_detalle.iess_asumido = item['iess_asumido'].replace(',', '.')
                            costeo_detalle.total_cf = item['total'].replace(',', '.')
                            costeo_detalle.created_by = request.user.get_full_name()
                            costeo_detalle.updated_by = request.user.get_full_name()
                            costeo_detalle.created_at = datetime.now()
                            costeo_detalle.updated_at = datetime.now()

                            costeo_detalle.save()
                            
        except Exception as e:
            print (e.message)
        mensaje='Costeo ingresado con exito'
        item = {
            'id': costo.id,
            'mensaje': mensaje,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")
    else:
        texto = "text"
        anio = Anio.objects.all()
        return render_to_response('subordenproduccion/cierre_mensual.html', {'texto': texto,'anio': anio}, RequestContext(request))




def costeoProduccionList(request):
    texto = "text"
    costeos = CostoFabricacion.objects.all()
    return render_to_response('subordenproduccion/list_costeo.html', {'texto': texto,'costeos': costeos}, RequestContext(request))



def costeoProduccionVer(request, pk):
    costeo = CostoFabricacion.objects.get(id=pk)
    costeo_detalle= CostoFabricacionDetalle.objects.filter(costo_fabricacion_id=pk)
    return render_to_response('subordenproduccion/ver_costeo.html', { 'costeo': costeo,'costeo_detalle':costeo_detalle},  RequestContext(request))


@csrf_exempt
def obtenerAnalisisCostoMaterialesMes(request):
    if request.method == 'POST':
        anio = request.POST.get('anio')
        mes = request.POST.get('mes')
        
        

        cursor = connection.cursor()
        html=''
        
        cursor.execute("select distinct o.id,o.tipo,o.codigo,c.nombre_cliente ,sum(opsm.hora_total),sum(opsm.costo),sum(opsr.total),o.descripcion from orden_produccion o left join cliente c on  c.id_cliente=o.cliente_id  left join orden_produccion_subop_mano_obra opsm on  opsm.orden_produccion_id=o.id and Extract(year from opsm.fecha_subop)='" + str(anio) + "' and Extract(month from opsm.fecha_subop)='" + str(mes) + "' left join orden_produccion_subop_receta opsr on  opsr.orden_produccion_id=o.id and Extract(year from opsr.fecha_despacho)='" + str(anio) + "' and Extract(month from opsr.fecha_despacho)='" + str(mes) + "' where 1=1 and (o.id in (select cf.orden_produccion_id from  costeo_fabricacion_facturas cf where Extract(year from cf.fecha)='" + str(anio) + "' and Extract(month from cf.fecha)='" + str(mes) + "') or o.id in (select osm.orden_produccion_id from  orden_produccion_subop_mano_obra osm where Extract(year from osm.fecha_subop)='" + str(anio) + "' and Extract(month from osm.fecha_subop)='" + str(mes) + "') or o.id in (select osr.orden_produccion_id from  orden_produccion_subop_receta osr where Extract(year from osr.fecha_despacho)='" + str(anio) + "' and Extract(month from osr.fecha_despacho)='" + str(mes) + "')) group by o.id,o.tipo,o.codigo,c.nombre_cliente")
        row = cursor.fetchall()
        total = 0
        subtotal = 0
        iva = 0
        suma_horas=0
        
        cursor.execute("select sum(total_horas) from empleados_horas_mes_subop where anio="+ str(anio) +" and mes='" + str(mes) + "' ")
        row2 = cursor.fetchall()
        if len(row2):
            for p2 in row2:
                if p2[0]:
                    suma_horas=suma_horas+p2[0]
            
        suma_horas_nomina=0    
        cursor.execute("select count(rd.empleado_id) from rol_pago_detalle rd,empleados_empleado e,rol_pago r where r.id=rd.rol_pago_id and e.empleado_id=rd.empleado_id and r.anio='"+ str(anio) +"' and r.mes=" + str(mes) + "  and (e.grupo_pago_id=6 or e.grupo_pago_id=5)")  
        row3 = cursor.fetchall()
        if row3:
            for p3 in row3:
                if p3[0]:
                    suma_horas_nomina=float(suma_horas_nomina)+float(p3[0])
            suma_horas_nomina=30*8 *float(suma_horas_nomina)
        
        suma_horas_ausentes=0
        cursor.execute(" select sum(horas) from rol_ausencia_empleado where  anio='"+ str(anio) +"' and mes=" + str(mes) + "  and descontar is True and  (tipo_ausencia_id=3 or tipo_ausencia_id=7 or tipo_ausencia_id=8) and (grupo_pago_id=6 or grupo_pago_id=5) ")  
        row4 = cursor.fetchall()
        if row4:
            for p4 in row4:
                if p4[0]:
                    suma_horas_ausentes=float(suma_horas_ausentes)+float(p4[0])
            suma_horas_ausentes=30*8 *float(suma_horas_ausentes)
        
        total_horas_nomina=suma_horas_nomina-suma_horas_ausentes
        
        
        suma_horas_nomina_md=0
        total_empl_nomina=0
        cursor.execute("select count(rd.empleado_id) from rol_pago_detalle rd,empleados_empleado e,rol_pago r where r.id=rd.rol_pago_id and e.empleado_id=rd.empleado_id and r.anio='"+ str(anio) +"' and r.mes=" + str(mes) + "  and  e.grupo_pago_id=5")  
        row5 = cursor.fetchall()
        if row5:
            for p5 in row5:
                if p5[0]:
                    total_empl_nomina=float(suma_horas_nomina_md)+float(p5[0])
                    suma_horas_nomina_md=float(suma_horas_nomina_md)+float(p5[0])
            suma_horas_nomina_md=30*8 *float(suma_horas_nomina_md)
        
        suma_horas=total_empl_nomina*22*8
        suma_horas_ausentes_md=0
        cursor.execute(" select sum(horas) from rol_ausencia_empleado where  anio='"+ str(anio) +"' and mes=" + str(mes) + "  and descontar is True and  (tipo_ausencia_id=3 or tipo_ausencia_id=7 or tipo_ausencia_id=8) and grupo_pago_id=5 ")  
        row6 = cursor.fetchall()
        if row6:
            for p6 in row6:
                if p6[0]:
                    suma_horas_ausentes_md=float(suma_horas_ausentes_md)+float(p6[0])
            suma_horas_ausentes_md=30*8 *float(suma_horas_ausentes_md)
        
        total_horas_md=suma_horas_nomina_md-suma_horas_ausentes_md
        suma_horas=suma_horas-suma_horas_ausentes_md
        
        suma_horas_nomina_mi=0
        cursor.execute("select count(rd.empleado_id) from rol_pago_detalle rd,empleados_empleado e,rol_pago r where r.id=rd.rol_pago_id and e.empleado_id=rd.empleado_id and r.anio='"+ str(anio) +"' and r.mes=" + str(mes) + "  and  e.grupo_pago_id=6")  
        row7 = cursor.fetchall()
        if row7:
            for p7 in row7:
                if p7[0]:
                    suma_horas_nomina_mi=float(suma_horas_nomina_mi)+float(p7[0])
            suma_horas_nomina_mi=30*8 *float(suma_horas_nomina_mi)
        
        suma_horas_ausentes_mi=0
        cursor.execute(" select sum(horas) from rol_ausencia_empleado where  anio='"+ str(anio) +"' and mes=" + str(mes) + "  and descontar is True and  (tipo_ausencia_id=3 or tipo_ausencia_id=7 or tipo_ausencia_id=8) and grupo_pago_id=6 ")  
        row8 = cursor.fetchall()
        if row8:
            for p8 in row8:
                if p8[0]:
                    suma_horas_ausentes_mi=float(suma_horas_ausentes_mi)+float(p8[0])
            suma_horas_ausentes_mi=30*8 *float(suma_horas_ausentes_mi)
        
        total_horas_mi=suma_horas_nomina_mi-suma_horas_ausentes_mi
        # # 
        beneficios_sociales=0
        suma_sueldos=0
        cursor.execute(" select sum(valor_mensual)  from rol_pago_ingresos_grupo  where anio='"+ str(anio) +"' and mes=" + str(mes) + "  and grupo_pago_id=5 ")  
        row9 = cursor.fetchall()
        if row9:
            for r9 in row9:
                if r9[0]:
                    suma_sueldos=float(suma_sueldos)+float(r9[0])
        
        decimo_tercero=float(suma_sueldos)/12
        decimo_cuarto=(375/360)*30*float(total_empl_nomina)
        vacaciones=float(suma_sueldos)/24
        iess=float(suma_sueldos)*0.1215
        fondo_reserva=float(suma_sueldos)/12
        total_benef_mod=decimo_tercero+decimo_cuarto+vacaciones+iess+fondo_reserva
        # 
        
        suma_sueldos_moi=0
        cursor.execute(" select sum(valor_mensual)  from rol_pago_ingresos_grupo  where anio='"+ str(anio) +"' and mes=" + str(mes) + "  and grupo_pago_id=6 ")  
        row_sueldos_moi = cursor.fetchall()
        if row_sueldos_moi:
            for rst in row_sueldos_moi:
                if rst[0]:
                    suma_sueldos_moi=float(suma_sueldos_moi)+float(rst[0])
        # #
        decimo_tercero_i=float(suma_sueldos_moi)/12
        decimo_cuarto_i=(375/360)*30*float(total_empl_nomina)
        vacaciones_i=float(suma_sueldos_moi)/24
        iess_mi=float(suma_sueldos_moi)*0.1215
        fondo_reserva_mi=float(suma_sueldos_moi)/12
        total_benef_moi=decimo_tercero_i+decimo_cuarto_i+vacaciones_i+iess_mi+fondo_reserva_mi
        
        suma_alimentacion=0
        cursor.execute(" select sum(total)  from costeo_fabricacion_facturas  where Extract(year from fecha)='"+ str(anio) +"' and Extract(month from fecha)=" + str(mes) + " and rubro='ALIMENTACION' ")  
        row_sueldos_ali= cursor.fetchall()
        if row_sueldos_ali:
            for ra in row_sueldos_ali:
                if ra[0]:
                    suma_alimentacion=float(suma_alimentacion)+float(ra[0])
                
        # 
        suma_otros=0
        cursor.execute(" select sum(total)  from costeo_fabricacion_facturas  where Extract(year from fecha)='"+ str(anio) +"' and Extract(month from fecha)=" + str(mes) + " and rubro='OTROS PRODUCCION' ")  
        row_ot= cursor.fetchall()
        if row_ot:
            for ot in row_ot:
                if ot[0]:
                    suma_otros=float(suma_otros)+float(ot[0])
            
        suma_planta=0
        cursor.execute(" select sum(total)  from costeo_fabricacion_facturas  where Extract(year from fecha)='"+ str(anio) +"' and Extract(month from fecha)=" + str(mes) + " and rubro='PLANTA' ")  
        row_pl= cursor.fetchall()
        if row_pl:
            for rp in row_pl:
                if rp[0]:
                    suma_planta=float(suma_planta)+float(rp[0])
        
        
        suma_mantenimiento=0
        cursor.execute(" select sum(total)  from costeo_fabricacion_facturas  where Extract(year from fecha)='"+ str(anio) +"' and Extract(month from fecha)=" + str(mes) + " and rubro='MANTENIMIENTO' ")  
        row_m= cursor.fetchall()
        if row_m:
            for rm in row_m:
                if rm[0]:
                    suma_mantenimiento=float(suma_mantenimiento)+float(rm[0])
                
            
            
        suma_depreciacion=0
        cursor.execute(" select sum(c.debe),sum(c.haber) from contabilidad_asientodetalle c ,contabilidad_asiento a where a.asiento_id=c.asiento_id and Extract(year from a.fecha)='"+ str(anio) +"' and Extract(month from a.fecha)=" + str(mes) + " and a.anulado is not True ")  
        row_d= cursor.fetchall()
        if row_d:
            for rd in row_d:
                if rd[0]:
                    suma_depreciacion=float(suma_depreciacion)+float(rd[0])-float(rd[1])
                
            
        suma_aporte_patronal=iess+iess_mi
        suma_fondo_reserva=fondo_reserva+fondo_reserva_mi
        suma_impto_renta=0
        # 
        cursor.execute(" select sum(c.valor) from otros_ingresos_rol_empleado c,empleados_empleado e  where e.empleado_id=c.empleado_id and tipo_ingreso_egreso_empleado_id=28  and c.anio='"+ str(anio) +"' and c.mes=" + str(mes) + " and c.pagar is True")  
        row_ir= cursor.fetchall()
        if row_ir:
            for rdr in row_ir:
                if rdr[0]:
                    suma_impto_renta=float(suma_impto_renta)+float(rdr[0])
        
        suma_iess_asumido=0
        
        cursor.execute(" select sum(c.valor) from otros_ingresos_rol_empleado c,empleados_empleado e  where e.empleado_id=c.empleado_id and tipo_ingreso_egreso_empleado_id=27  and c.anio='"+ str(anio) +"' and c.mes=" + str(mes) + " and c.pagar is True")  
        row_ia= cursor.fetchall()
        if row_ia:
            for rda in row_ia:
                if rda[0]:
                    suma_iess_asumido=float(suma_iess_asumido)+float(rda[0])
        
        
        
        
        
        # # detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html += '<table id="tabla" class="table table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead>'
        
        html += '<tr>'
        html += '<th>OP</th><th>Cliente</th><th>Producto</th><th>HORAS</th><th>Factor</th>'
        html += '<th>MOD NOMINA</th>'
        html += '<th>MATERIALES</th><th>	MOI</th><th>BS MOD</th>'
        html += '<th>BS MOI</th><th>	ALIMENTAC.</th><th>OTROS PROD.</th><th>	SERV. PLANTA</th><th>MANTENI.	</th>'
        html += '<th>DEPRECIAC</th><th>	APOR. PATRO</th><th>FONDO RESERV</th><th>IMPTO.RENTA</th><th>IESS ASUMIDO</th><th>TOTAL CF</th>'
        
        html+='</tr></thead>'
        html+='<tbody><tr>'
        # 
        for p in row:
            diferencia_cantidad=0
            diferencia_costo=0
            
           
            
           
            html += '<td style="text-align:right">' + str(p[1]) + '-'+str(p[2])+'<input type="hidden" name="op_id" value="' +str(p[0])+'" /></td>'
            html += '<td style="text-align:right" >' + str(p[3].encode('utf8')) + '</td>'
            html += '<td style="text-align:right">' + str(p[7].encode('utf8')) + '</td>'
            if str(p[4]) == 'None' or p[4] == '':
                cont=0
            else:
                cont=p[4]
            
            html += '<td style="text-align:right" name="horas">' + str(cont)  + '</td>'
            factor=float(cont)/suma_horas
            
                
            
            nomina=total_horas_nomina*factor
            
            
            
            html += '<td style="text-align:right" name="factor">' + str("%2.2f" % factor).replace('.', ',') + '</td>'
            #html += '<td style="text-align:right" name="nomina">' + str("%2.2f" % nomina).replace('.', ',') + '</td>'
            nomina_md=total_horas_md*factor
            html += '<td style="text-align:right" name="nomina_md">' + str("%2.2f" % nomina_md).replace('.', ',') + '</td>'
            cursor.execute("select  sum (s.total) from orden_produccion_subop_receta s where  Extract(year from s.fecha_despacho)='"+ str(anio) +"' and Extract(month from s.fecha_despacho)=" + str(mes) + "  and s.orden_produccion_id =" + str(p[0]) )
            rowop= cursor.fetchall()
            bodega=0
            if rowop:
                for op1 in rowop:
                    if not op1[0] :
                        print "h"
                    else:
                        bodega=bodega+float(op1[0])
            html += '<td style="text-align:right" name="bodega">' + str("%2.2f" % bodega).replace('.', ',') + '</td>'
            
            
            nomina_mi=total_horas_mi*factor
            html += '<td style="text-align:right" name="nomina_mi">' + str("%2.2f" % nomina_mi).replace('.', ',') + '</td>'
            total_bs_md=total_benef_mod*factor
            total_bs_mi=total_benef_moi*factor
            html += '<td style="text-align:right" name="bs_md">' + str("%2.2f" % total_bs_md).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="bs_mi">' + str("%2.2f" % total_bs_mi).replace('.', ',') + '</td>'
            
            total_alimentacion=suma_alimentacion*factor
            total_otros=suma_otros*factor
            total_planta=suma_planta*factor
            total_mantenimiento=suma_mantenimiento*factor
            total_depreciacion=suma_depreciacion*factor
            total_aporte_patronal=suma_aporte_patronal*factor
            total_fondo_reserva=suma_fondo_reserva*factor
            total_impto_renta=suma_impto_renta*factor
            total_iess_asumido=suma_iess_asumido*factor
            total_final=nomina_md+bodega+nomina_mi+total_bs_md+total_bs_mi+total_alimentacion+total_otros+total_planta+total_mantenimiento+total_depreciacion+total_aporte_patronal+total_fondo_reserva+total_impto_renta+total_iess_asumido
            
            html += '<td style="text-align:right" name="alimentacion">' + str("%2.2f" % total_alimentacion).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="otros">' + str("%2.2f" % total_otros).replace('.', ',') + '</td>'
            
            
            html += '<td style="text-align:right" name="planta">' + str("%2.2f" % total_planta).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="mantenimiento">' + str("%2.2f" % total_mantenimiento).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="depreciacion">' + str("%2.2f" % total_depreciacion).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="aporte_patronal">' + str("%2.2f" % total_aporte_patronal).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="fondo_reserva">' + str("%2.2f" % total_fondo_reserva).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="imp_renta">' + str("%2.2f" % total_impto_renta).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="iess_asumido">' + str("%2.2f" % total_iess_asumido).replace('.', ',') + '</td>'
            html += '<td style="text-align:right" name="total">' + str("%2.2f" % total_final).replace('.', ',') + '</td>'
            html += '</tr>'
                    
             
            
        html+='</tbody>'
        html+='</table>'

        return HttpResponse(
            html
        )
    else:
        raise Http404
  
