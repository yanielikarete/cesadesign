from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
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
from .tables import *
from .forms import *

from clientes.models import *
from ambiente.models import *
from django.views.decorators.csrf import csrf_exempt
from inventario.models import *
from django.db import connection, transaction
from reunion.models import *
from config.models import *
from pedido.models import *
from proforma.models import *
from ordenproduccion.models import *
from facturacion.models import *
from subordenproduccion.models import *
from OrdenesdeCompra.models import *
from ordenIngreso.models import *
from ordenEgreso.models import *

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
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes
from django.utils.dateparse import parse_date



from login.lib.tools import Tools
from django.contrib import auth
from datetime import datetime
# Create your views here.
@login_required()
def liquidacionesListView(request):
    if request.method == 'POST':
        liquidaciones = LiquidacionComisiones.objects.all()
        clientes = Cliente.objects.all()

        return render_to_response('liquidaciones/list.html', { 'liquidaciones': liquidaciones,'clientes':clientes},  RequestContext(request))

    else:
        liquidaciones = LiquidacionComisiones.objects.all()
        clientes = Cliente.objects.all()

        return render_to_response('liquidaciones/list.html', { 'liquidaciones': liquidaciones,'clientes':clientes},  RequestContext(request))

@login_required()
def liquidacionesCreateView(request):
    if request.method == 'POST':
        form=LiquidacionComisionesForm(request.POST)
        
        if form.is_valid():
            new_orden=form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            # new_orden.subtotal = request.POST["subtotal"]
            # new_orden.iva = request.POST["iva"]
            # new_orden.retencion_fuente = request.POST["retencion_fuente"]
            # new_orden.retencion_iva = request.POST["retencion_iva"]
            try:
                porcentaje_iva = Parametros.objects.get(clave='iva').valor
            
            except Parametros.DoesNotExist:
                porcentaje_iva = None
            if porcentaje_iva:
                new_orden.porcentaje_iva = porcentaje_iva
            
            new_orden.adelanto = request.POST["adelanto"]
            
            new_orden.save()
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
                    if 'proforma_id'+str(i) in request.POST:
                        liquidaciondetalle=LiquidacionComisionesDetalle()
                        liquidaciondetalle.proforma_id = request.POST["proforma_id"+str(i)]
                        liquidaciondetalle.vendedor_id = new_orden.vendedor_id
                        liquidaciondetalle.proforma_codigo=request.POST["proforma"+str(i)]
                        liquidaciondetalle.fecha=request.POST["fecha"+str(i)]
                        liquidaciondetalle.cliente_id=request.POST["cliente_id"+str(i)]
                        liquidaciondetalle.detalle=request.POST["detalle"+str(i)]
                        liquidaciondetalle.subtotal=request.POST["subtotal"+str(i)]
                        liquidaciondetalle.iva=request.POST["iva"+str(i)]
                        liquidaciondetalle.total=request.POST["total"+str(i)]
                        liquidaciondetalle.valor_cancelado=request.POST["valor_cancelado"+str(i)]
                        liquidaciondetalle.saldo=request.POST["saldo"+str(i)]
                        liquidaciondetalle.valor_cancelado_sin_iva=request.POST["valor_cancelado_sin_iva"+str(i)]
                        liquidaciondetalle.porcentaje_comision=request.POST["porcentaje_comisiones"+str(i)]
                        liquidaciondetalle.total_comision=request.POST["total_comision"+str(i)]
                        liquidaciondetalle.liquidacion_comisiones_id=new_orden.id
                        liquidaciondetalle.save()
                    
                
            
            liquidaciones = LiquidacionComisiones.objects.all()
            clientes = Cliente.objects.all()

            return render_to_response('liquidaciones/list.html', { 'liquidaciones': liquidaciones,'clientes':clientes},  RequestContext(request))



        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        liquidaciones = LiquidacionComisiones.objects.all()
        clientes = Cliente.objects.all()
        vendedor = Vendedor.objects.values('id', 'codigo','nombre')
        form=LiquidacionComisionesForm()
        iva = Parametros.objects.get(clave='iva')



        return render_to_response('liquidaciones/reporte.html', { 'vendedor': vendedor,'clientes':clientes,'form':form,'iva':iva},  RequestContext(request))

       

        
      
@login_required()
@csrf_exempt
def obtenerLiquidacionesComisiones(request):
    if request.method == 'POST':
        fechainicial = request.POST.get('fechainicial')
        fechafin = request.POST.get('fechafin')
        vendedor = request.POST.get('vendedor')
       
        fechainicial = datetime.strptime(fechainicial, "%d/%m/%Y")
        fechafin = datetime.strptime(fechafin, "%d/%m/%Y")
        iva = Parametros.objects.get(clave='iva')

        cursor = connection.cursor();
        #sql="select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,c.id_cliente,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,v.nombre from proforma p,cliente c,vendedor v ,documento_compra_detalle rpcd, documento_compra rcp where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True'and p.vendedor_id="+str(vendedor)+" and documento_compra.fecha_emision>='"+str(fechainicial)+"' and rcp.fecha_emision<='"+str(fechafin)+"' and rcp.id=rpcd.documento_compra_id and rpc.proforma_id=p.id "
        #sql="select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,c.id_cliente,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,v.nombre from proforma p,cliente c,vendedor v  where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True'and p.vendedor_id="+str(vendedor)+" and p.fecha_emision>='"+str(fechainicial)+"' and rcp.fecha_emision<='"+str(fechafin)+"' and rcp.id=rpcd.documento_compra_id and rpc.proforma_id=p.id "
        sql="select distinct p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,c.id_cliente,c.nombre_cliente,p.vendedor_id,p.subtotal,p.iva,p.total,v.nombre,sum(dav.abono) from proforma p,cliente c,vendedor v ,documento_abono_venta dav where p.cliente_id=c.id_cliente and v.id=p.vendedor_id and p.aprobada='True'and p.vendedor_id="+str(vendedor)+" and dav.created_at>='"+str(fechainicial)+"' and dav.created_at<='"+str(fechafin)+"' and dav.proforma_id=p.id  group by p.id,p.tipo,p.fecha,p.codigo,p.descripcion,p.detalle,p.cantidad,c.id_cliente,c.nombre_cliente,p.vendedor_id,p.total,v.nombre"
        cursor.execute(sql)
        row = cursor.fetchall();
        cont=0;
        total_comision=0;
        print(sql);
        #detalle = Pedido.objects.filter(orden_egreso_id=modulo)
        html=''
        for p in row:
            cont=cont+1
            html+='<tr><td><input type="text" name="fecha'+str(cont)+'" id="fecha'+str(cont)+'" value="'+str(p[2])+'" /></td>'
            html+='<td><input type="text" name="vendedor'+str(cont)+'" id="vendedor'+str(cont)+'" value="'+str(p[13])+'"/><input type="hidden" name="vendedor_id'+str(cont)+'" id="vendedor_id'+str(cont)+'" value="'+str(p[3])+'" /></td>'
            html+='<td><input type="text" name="proforma'+str(cont)+'" id="proforma'+str(cont)+'" value="'+str(p[3])+'" /><input type="hidden" name="proforma_id'+str(cont)+'" id="proforma_id'+str(cont)+'" value="'+str(p[0])+'" /></td>'
            html+='<td><input type="text" name="cliente'+str(cont)+'" id="cliente'+str(cont)+'" value="'+str(p[8])+'"/><input type="hidden" name="cliente_id'+str(cont)+'" id="cliente_id'+str(cont)+'" value="'+str(p[7])+'" /></td>'
            html+='<td><textarea name="detalle'+str(cont)+'" id="detalle'+str(cont)+'" class="detall">'
            ped=ProformaDetalle.objects.filter(proforma_id=str(p[0]))
            for pe in ped:
                html+=''+str(pe.cantidad)+' '+str(pe.nombre)+'\r\n'
            html+='</textarea></td>'
            cursor2 = connection.cursor();
            #cursor2.execute("select sum(rpcd.valor_a_pagar) from registrar_cobro_pago_detalle rpcd, registrar_cobro_pago rcp, proforma pf where rcp.fecha>='"+str(fechainicial)+"' and rcp.fecha<='"+str(fechafin)+"' and rcp.id=rpcd.registrar_cobro_pago_id and rpcd.proforma_id=pf.id and pf.vendedor_id="+str(vendedor)+"");
            #row2 = cursor2.fetchall();
            #print("select sum(rpcd.valor_a_pagar) from registrar_cobro_pago_detalle rpcd, registrar_cobro_pago rcp, proforma pf where rpcd.fecha_pago>='"+str(fechainicial)+"' and rpcd.fecha_pago<='"+str(fechafin)+"' and rcp.id=rpcd.registrar_cobro_pago_id and rpcd.proforma_id=pf.id and pf.vendedor_id="+str(vendedor)+"");
            html+='<td><input type="text" name="subtotal'+str(cont)+'" id="subtotal'+str(cont)+'" value="'+str(p[10])+'" readonly="readonly"/></td>'
            html+='<td><input type="text" name="iva'+str(cont)+'" id="iva'+str(cont)+'" value="'+str(p[11])+'" readonly="readonly"/></td>'
            html+='<td><input type="text" name="total'+str(cont)+'" id="total'+str(cont)+'" value="'+str(p[12])+'" readonly="readonly"/></td>'
            html+='<td><input type="text" name="valor_cancelado'+str(cont)+'" id="valor_cancelado'+str(cont)+'"value="'+str(p[14])+'" readonly="readonly"/></td>'
            saldo=float(p[12])-float(p[14])
            iva_considera=float(float(iva.valor)/100)
            #valor_cancelado_sin_iva=row2[0][0]-(row2[0][0]*iva_considera)
            valor_cancelado_sin_iva=float(p[14])-(float(p[14])*float(iva_considera))
            html+='<td><input type="text" name="saldo'+str(cont)+'" id="saldo'+str(cont)+'" value="'+str(saldo)+'" readonly="readonly"/></td>'
            html+='<td><input type="text" name="valor_cancelado_sin_iva'+str(cont)+'" id="valor_cancelado_sin_iva'+str(cont)+'" value="'+str(valor_cancelado_sin_iva)+'" readonly="readonly"/></td>'
            html+='<td><input type="text" name="porcentaje_comisiones'+str(cont)+'" id="porcentaje_comisiones'+str(cont)+'" value="3" onkeyup="actualizarComision('+str(cont)+')"/></td>'
            total_comision=(p[12]*3)/100
            html+='<td><input type="text" name="total_comision'+str(cont)+'" id="total_comision'+str(cont)+'" value="'+str(total_comision)+'" readonly="readonly" /></td>'
            html+='></tr>'

        return HttpResponse(
                html
            )
    else:
        raise Http404
@login_required()
def liquidacionesUpdateView(request,pk):
    if request.method == 'POST':
        liquidacion = LiquidacionComisiones.objects.get(id=pk)
        form = LiquidacionComisionesForm(request.POST,request.FILES,instance=liquidacion)
        #form=LiquidacionComisionesForm(request.POST)
        
        if form.is_valid():
            new_orden=form.save()
            #new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            #new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            # new_orden.subtotal = request.POST["subtotal"]
            # new_orden.iva = request.POST["iva"]
            # new_orden.retencion_fuente = request.POST["retencion_fuente"]
            # new_orden.retencion_iva = request.POST["retencion_iva"]
            new_orden.adelanto = request.POST["adelanto"]
            new_orden.save()
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
                    if 'id_detalle'+str(i) in request.POST:
                        detalle_id=request.POST["id_detalle"+str(i)]
                        liquidaciondetalle=LiquidacionComisionesDetalle.objects.get(id=detalle_id)
                        liquidaciondetalle.proforma_id = request.POST["proforma_id"+str(i)]
                        liquidaciondetalle.vendedor_id = new_orden.vendedor_id
                        liquidaciondetalle.proforma_codigo=request.POST["proforma"+str(i)]
                        liquidaciondetalle.fecha=request.POST["fecha"+str(i)]
                        liquidaciondetalle.cliente_id=request.POST["cliente_id"+str(i)]
                        liquidaciondetalle.detalle=request.POST["detalle"+str(i)]
                        liquidaciondetalle.subtotal=request.POST["subtotal"+str(i)]
                        liquidaciondetalle.iva=request.POST["iva"+str(i)]
                        liquidaciondetalle.total=request.POST["total"+str(i)]
                        liquidaciondetalle.valor_cancelado=request.POST["valor_cancelado"+str(i)]
                        liquidaciondetalle.saldo=request.POST["saldo"+str(i)]
                        liquidaciondetalle.valor_cancelado_sin_iva=request.POST["valor_cancelado_sin_iva"+str(i)]
                        liquidaciondetalle.porcentaje_comision=request.POST["porcentaje_comisiones"+str(i)]
                        liquidaciondetalle.total_comision=request.POST["total_comision"+str(i)]
                        liquidaciondetalle.liquidacion_comisiones_id=new_orden.id
                        liquidaciondetalle.save()
                
            
            liquidaciones = LiquidacionComisiones.objects.all()
            clientes = Cliente.objects.all()
            return render_to_response('liquidaciones/list.html', { 'liquidaciones': liquidaciones,'clientes':clientes},  RequestContext(request))



        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        liquidacion = LiquidacionComisiones.objects.get(id=pk)
        form=LiquidacionComisionesForm(instance=liquidacion)  

        detalle = LiquidacionComisionesDetalle.objects.filter(liquidacion_comisiones_id=liquidacion.id)


        return render_to_response('liquidaciones/editar_reporte.html', { 'detalle': detalle,'form':form},  RequestContext(request))

       

@login_required()
def ComisionCreateView(request,pk):
    if request.method == 'POST':
        vendedor = Vendedor.objects.all()
        pr = Proforma.objects.get(id=pk)
        contador = request.POST["columnas_receta"]
        i = 0
        while int(i) <= int(contador):
                i += 1
                print('entro comoqw' + str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_detalle' + str(i) in request.POST:
                        detalle_id = request.POST["id_detalle" + str(i)]
                        detallecompra = ProformaComision.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        detallecompra.vendedor_id = request.POST["vendedor_kits" + str(i)]
                        detallecompra.porcentaje_comision = request.POST["porcentaje_kits" + str(i)]
                        detallecompra.valor = request.POST["valor_kits" + str(i)]
                        detallecompra.proforma_id = pk
                        detallecompra.save()
                    else:
                        comprasdetalle = ProformaComision()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.vendedor_id = request.POST["vendedor_kits" + str(i)]
                        comprasdetalle.porcentaje_comision = request.POST["porcentaje_kits" + str(i)]
                        comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                        comprasdetalle.proforma_id = pk
                        comprasdetalle.save()



        return HttpResponseRedirect('/liquidacion_comisiones/proformaComision')

    else:
        vendedor = Vendedor.objects.all()
        pr = Proforma.objects.get(id=pk)
        detalle = ProformaComision.objects.filter(proforma_id=pk)
        comision = Parametros.objects.get(clave="comision")
        comision_10000= Parametros.objects.get(clave="comision>10000")
        comision_6000 = Parametros.objects.get(clave="comision>6000")
        comision_externo = Parametros.objects.get(clave="comision-externo")
        comision_referida = Parametros.objects.get(clave="comision-referida")
        proforma = Proforma.objects.get(id=pk)
        cursor = connection.cursor();
        cursor.execute(
            "select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.detalle,pd.id,pd.proforma_id  from proforma p,proforma_detalle pd where p.id=pd.proforma_id and (pd.no_producir is NULL or pd.no_producir=False) and p.id=" + pk + " ORDER BY pd.id ASC ");
        row = cursor.fetchall();

        cursor = connection.cursor();
        cursor.execute(
            "select distinct pd.ambiente_id,am.descripcion from proforma p, proforma_detalle pd,ambiente am where p.id=pd.proforma_id and pd.ambiente_id=am.id and (pd.no_producir is NULL or pd.no_producir=False) and p.id=" + pk);
        row1 = cursor.fetchall();

        return render_to_response('liquidaciones/comision.html', {'vendedor': vendedor, 'pr': pr, 'detalle': detalle,'proforma':proforma,'row':row,'ambiente':row1,'comision': comision, 'comision_6000': comision_6000, 'comision_10000': comision_10000, 'comision_externo': comision_externo, 'comision_referida': comision_referida,},
                              RequestContext(request))


@login_required()
def ProformaComisionListView(request):
    if request.method == 'POST':
        proformas = Proforma.objects.filter(aprobada=True)

        return render_to_response('liquidaciones/proformalist.html', {'proformas': proformas},RequestContext(request))

    else:
        proformas = Proforma.objects.filter(aprobada=True)
        return render_to_response('liquidaciones/proformalist.html', {'proformas': proformas},RequestContext(request))

@login_required()
def AdelantoComisionView(request,pk):
    if request.method == 'POST':
        vendedor = Vendedor.objects.all()
        pr = ProformaComision.objects.get(id=pk)
        proforma=pr.proforma_id
        contador = request.POST["columnas_receta"]
        i = 0
        while int(i) <= int(contador):
                i += 1
                print('entro comoqw' + str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_detalle' + str(i) in request.POST:
                        detalle_id = request.POST["id_detalle" + str(i)]
                        detallecompra = ProformaComisionAbono.objects.get(id=detalle_id)
                        detallecompra.updated_by = request.user.get_full_name()
                        detallecompra.fecha = request.POST["fecha_kits" + str(i)]
                        detallecompra.abono = request.POST["valor_kits" + str(i)]
                        detallecompra.proforma_comision_id = pk
                        detallecompra.save()
                    else:
                        comprasdetalle = ProformaComisionAbono()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.fecha = request.POST["fecha_kits" + str(i)]
                        comprasdetalle.abono = request.POST["valor_kits" + str(i)]
                        comprasdetalle.proforma_comision_id = pk
                        comprasdetalle.save()



        return HttpResponseRedirect('/liquidacion_comisiones/liquidaciones/'+str(proforma)+'/relacionarComision/')

    else:
        comision = ProformaComision.objects.get(id=pk)
        vendedor = Vendedor.objects.all()
        pr = Proforma.objects.get(id=comision.proforma_id)
        detalle = ProformaComisionAbono.objects.filter(proforma_comision_id=pk)
        proforma = Proforma.objects.get(id=comision.proforma_id)
        cursor = connection.cursor();
        cursor.execute(
            "select distinct pd.ambiente_id,pd.nombre,pd.cantidad,pd.precio_compra,pd.total,pd.detalle,pd.id,pd.proforma_id  from proforma p,proforma_detalle pd where p.id=pd.proforma_id and (pd.no_producir is NULL or pd.no_producir=False) and p.id=" + str(comision.proforma_id) + " ORDER BY pd.id ASC ");
        row = cursor.fetchall();

        cursor = connection.cursor();
        cursor.execute(
            "select distinct pd.ambiente_id,am.descripcion from proforma p, proforma_detalle pd,ambiente am where p.id=pd.proforma_id and pd.ambiente_id=am.id and (pd.no_producir is NULL or pd.no_producir=False) and p.id=" + str(comision.proforma_id));
        row1 = cursor.fetchall();

        return render_to_response('liquidaciones/adelanto_comision.html', {'vendedor': vendedor, 'pr': pr, 'detalle': detalle,'proforma':proforma,'row':row,'ambiente':row1,'comision':comision},
                              RequestContext(request))



