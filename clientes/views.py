# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, \
    eliminarByPkView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import simplejson as json
import datetime
from .forms import *
from .tables import *
from .filters import *
from clientes.models import *
from inventario.models import *
from config.models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

from django.db import connection, transaction
from django.views.generic import TemplateView

from django.forms.extras.widgets import *
from django.contrib.auth import authenticate, login

import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
from cgi import escape

# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template.loader import render_to_string
from django.db import IntegrityError, transaction


# ===============CLIENTE=====================#
def ClienteListView(request):
    cursor = connection.cursor()
    sql="select c.id_cliente,c.codigo_cliente,c.nombre_cliente,c.ruc,c.direccion1,c.telefono1,count(p.id),count(f.id),count(m.id) from cliente c LEFT JOIN proforma p ON p.cliente_id =c.id_cliente LEFT JOIN documento_venta f ON f.cliente_id=c.id_cliente LEFT JOIN movimiento m ON m.cliente_id=c.id_cliente where c.activo=True group by c.id_cliente,c.codigo_cliente,c.nombre_cliente,c.ruc,c.direccion1,c.telefono1"
    cursor.execute(sql)
    ro = cursor.fetchall()
    #clientes = Cliente.objects.filter(activo=True)
    return render_to_response('clientes/index.html', {'clientes': ro}, RequestContext(request))
    
@login_required()
@transaction.atomic
def ClienteCreateView(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                new_client = form.save()
                new_client.created_by = request.user.get_full_name()
                new_client.updated_by = request.user.get_full_name()
                new_client.created_at = datetime.now()
                new_client.updated_at = datetime.now()
                new_client.activo = True
                new_client.save()
                try:

                    secuencial = Secuenciales.objects.get(modulo='cliente')
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
                    print('entro comoqw' + str(i))
                    if int(i) > int(contador):
                        print('entrosd')
                        break
                    else:
                        if 'id_kits' + str(i) in request.POST:
                            cont = request.POST["id_kits" + str(i)]
                            if cont:
                                razons = RazonSocial.objects.get(id=request.POST["id_kits" + str(i)])
                                proformadetalle = RazonSocialClientes()
                                proformadetalle.cliente_id = new_client.id_cliente
                                proformadetalle.razon_social_id = request.POST["id_kits" + str(i)]
                                proformadetalle.save()

                    print(i)
                    print('contadorsd prueba' + str(contador))

                return HttpResponseRedirect('/clientes/clientes/')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = ClienteForm
        razonsocial = RazonSocial.objects.values('id', 'codigo_razon_social', 'nombre')

    return render_to_response('clientes/create.html', {'form': form,'razonsocial':razonsocial,}, RequestContext(request))


class ClienteUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        cliente = Cliente.objects.get(id_cliente=kwargs['pk'])
        razonsocial = RazonSocial.objects.values('id', 'codigo_razon_social', 'nombre')

        form = ClienteForm(instance=cliente)
        detalle = RazonSocialClientes.objects.filter(cliente_id=cliente.id_cliente)

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'form': form,
            'razonsocial': razonsocial,
            'detalle': detalle,
            'cliente': cliente
        }

        return render_to_response(
            'clientes/create.html', context, context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        cliente = Cliente.objects.get(id_cliente=kwargs['pk'])
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        p_id = kwargs['pk']
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        razonsocial = RazonSocial.objects.values('id', 'codigo_razon_social', 'nombre')

        if form.is_valid():

            new_orden = form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            contador = request.POST["columnas_receta"]

            i = 0
            while int(i) <= int(contador):
                i += 1
                print('Tiene i' + str(i))
                if int(i) > int(contador):
                    print('entrosd')
                    print('Salio con i' + str(i))
                    print('Salio con contador' + str(contador))
                    break
                else:
                    if 'id_kits' + str(i) in request.POST:
                        cont = request.POST["id_kits" + str(i)]
                        if cont:
                            product = RazonSocial.objects.get(id=request.POST["id_kits" + str(i)])

                            if 'id_detalle' + str(i) in request.POST:
                                detalle_id = request.POST["id_detalle" + str(i)]
                                print('detalle_id:' + str(detalle_id))
                                if detalle_id:
                                    detallecompra = RazonSocialClientes.objects.get(id=detalle_id)
                                    detallecompra.updated_by = request.user.get_full_name()
                                    detallecompra.razon_social = product
                                    detallecompra.cliente_id = new_orden.id_cliente
                                    detallecompra.save()

                                print('Tiene detalle' + str(i))
                            else:
                                comprasdetalle = RazonSocialClientes()
                                comprasdetalle.cliente_id = new_orden.id_cliente
                                comprasdetalle.razon_social = product
                                comprasdetalle.save()
                                #i += 1
                                print('No Tiene detalle' + str(i))
                                print('contadorsd prueba' + str(contador))


            detalle = RazonSocialClientes.objects.filter(cliente_id=p_id)
            razonsocial = RazonSocial.objects.values('id', 'codigo_razon_social', 'nombre')

            # context = {
            #     'section_title': 'Actualizar Proforma',
            #     'button_text': 'Actualizar',
            #     'form': form,
            #     'detalle': detalle,
            #     'razonsocial': razonsocial,
            #     'cliente': cliente,
            #     'mensaje': 'Proforma actualizada con exito'}
            #
            # return render_to_response(
            #     'clientes/create.html',
            #     context,
            #     context_instance=RequestContext(request))
            return HttpResponseRedirect('/clientes/clientes/')

        else:
            form = ClienteForm(request.POST)
            detalle = RazonSocialClientes.objects.filter(cliente_id=cliente.id_cliente)
            razonsocial = RazonSocial.objects.values('id', 'codigo_razon_social', 'nombre')

            context = {
                'section_title': 'Actualizar Proforma',
                'button_text': 'Actualizar',
                'form': form,
                'detalle': detalle,
                'razonsocial': razonsocial,
                'cliente': cliente,
                'mensaje': 'Cliente actualizada con exito'}

            return render_to_response(
                'clientes/create.html',
                context,
                context_instance=RequestContext(request))


# =====================================================#
class ClienteDetailView(ObjectDetailView):
    model = Cliente
    template_name = 'cliente/detail.html'

@login_required()
def clienteEliminarView(request):
    return eliminarView(request, Cliente, 'cliente-producto-list')


# =====================================================#
@login_required()
def clienteEliminarByPkView(request, pk):
    obj = Cliente.objects.get(id_cliente=pk)

    if obj:
        obj.activo = False
        obj.save()

    return HttpResponseRedirect('/clientes/clientes')


# ======================================================#
@login_required()
@csrf_exempt
def misClientesGuardar(request):
    item = {'exito': 0}
    if request.method == 'POST':
        try:

            clientes = request.POST['data']
            clientes = json.loads(clientes)

            for cliente in clientes:
                if not cliente['codigo_cliente'] == "" and not cliente['codigo_cliente'] == None:
                    try:
                        a = Cliente()
                        a.codigo_cliente = cliente['codigo_cliente']
                        a.nombre_cliente = cliente['nombre_cliente']
                        a.created_by = request.user
                        a.updated_at = datetime.now()
                        a.save()

                    except:
                        messages.error(request, "Oh, No se pudo guardar al estudiante")
                        pass

                    item = {'exito': 1}

            if item['exito'] == 1:
                messages.info(request, 'Categorias guardadas!')

        except Exception as e:
            messages.error(request, "Oh por favor vuelva a intentarlo.")
            print e
            item = {'exito': 0}
            pass

    return HttpResponse(json.dumps(item), content_type='application/json')


def RazonSocialListView(request):
    if request.method == 'POST':
        razonsocial = RazonSocial.objects.all()
        return render_to_response('razonsocial/index.html', {'razonsocial': razonsocial}, RequestContext(request))
    else:
        razonsocial = RazonSocial.objects.all()
        return render_to_response('razonsocial/index.html', {'razonsocial': razonsocial}, RequestContext(request))


def RazonSocialNuevoView(request):
    if request.method == 'POST':
        form = RazonSocialForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:

                secuencial = Secuenciales.objects.get(modulo='razonsocial')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/clientes/razonsocial/')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = RazonSocialForm

    return render_to_response('razonsocial/nuevo.html', {'form': form,}, RequestContext(request))


class RazonSocialUpdateView(ObjectUpdateView):
    model = RazonSocial
    form_class = RazonSocialForm
    template_name = 'razonsocial/nuevo.html'
    url_success = 'razonsocial-list'
    url_cancel = 'razonsocial-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Razon Social actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def razonsocialEliminarView(request):
    return eliminarView(request, RazonSocial, 'razonsocial-list')


# =====================================================#
@login_required()
def razonsocialEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, RazonSocial)


@login_required()
@csrf_exempt
def eliminarRazonSocialCliente(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = RazonSocialClientes.objects.get(id=id)



        try:
            detalle.delete()
        except Exception as e:
            # Tools.manejadorErrores(e)
            messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

        return HttpResponse(

        )
    else:
        id = request.POST.get('id')
        detalle = RazonSocialCliente.objects.get(id=id)

        try:
            detalle.delete()
        except Exception as e:
            # Tools.manejadorErrores(e)
            messages.error(request, 'Ocurrio un Error al Intentar Eliminar, Inténtelo nuevamente.')

        return HttpResponse(

        )
@login_required()
@csrf_exempt
def obtenerRazonSocial(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        objetos = RazonSocial.objects.get(id = id)

        
        item = {
            'ruc': objetos.ruc,
            'telefono': objetos.telefono1,
            'direccion': objetos.direccion1,

        }
    return HttpResponse(json.dumps(item), content_type='application/json')


@login_required()
@csrf_exempt
def validarRucCliente(request):
    if request.method == 'POST':
      ruc = request.POST.get('ruc')
      ruc2 = request.POST.get('ruc2')
      id = request.POST.get('id')
      #objetos = Proveedor.objects.get(ruc = ruc)
      #modulo_secuencial = objetos.proveedor_id
      
      cursor = connection.cursor()
      if id == '0':
            query = "select id_cliente,nombre_cliente,ruc from cliente where ruc='" + (ruc) + "' or ruc='" + (ruc2) + "';"
      else:
            query = "select id_cliente,nombre_cliente,ruc from cliente  where (ruc='" + (ruc) + "' or ruc='" + (ruc2) + "') and id_cliente!="+ (id) +";"
      print query
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")


    else:
        raise Http404
    
    
    
    

@login_required()
@csrf_exempt
def validarRucRazonSocial(request):
    if request.method == 'POST':
      ruc = request.POST.get('ruc')
      ruc2 = request.POST.get('ruc2')
      id = request.POST.get('id')
      #objetos = Proveedor.objects.get(ruc = ruc)
      #modulo_secuencial = objetos.proveedor_id
      
      cursor = connection.cursor()
      if id == '0':
            query = "select id,nombre,ruc from razon_social where ruc='" + (ruc) + "' or ruc='" + (ruc2) + "';"
      else:
            query = "select id,nombre,ruc from razon_social where (ruc='" + (ruc) + "' or ruc='" + (ruc2) + "') and id!="+ (id) +";"
      print query
      cursor.execute(query)
      ro = cursor.fetchall()
      json_resultados = json.dumps(ro)
      return HttpResponse(json_resultados, content_type="application/json")


    else:
        raise Http404