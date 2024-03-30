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
#from login.lib.tools import Tools
from inventario.models import *
from config.models import *
from proforma.models import *


# import ho.pisa as pisa
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes

from login.lib.tools import Tools

# Create your views here.

#=========================GuiaRemision============================#

class GuiaRemisionListView(ObjectListView):
    model = GuiaRemision
    paginate_by = 100
    template_name = 'guiaremision/index.html'
    table_class = GuiaRemisionTable
    filter_class = GuiaRemisionFilter
    context_object_name = 'guiaremision'


    def get_context_data(self, **kwargs):
        context = super(GuiaRemisionListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('guiaremision-delete')
        return context 


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

def GuiaRemisionCreateView(request):
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

    return render_to_response('guiaremision/create.html', { 'guiaremision_form': guiaremision_form,'productos':productos,'proformas':proformas},  RequestContext(request))


def GuiaRemisionUpdateView(request,pk):
    if request.method == 'POST':
        guiaremision=GuiaRemision.objects.get(guia_id=pk)
        guiaremision_form=GuiaRemisionForm(request.POST,request.FILES,instance=guiaremision)
        print guiaremision_form.is_valid(), guiaremision_form.errors, type(guiaremision_form.errors)

        if guiaremision_form.is_valid():
            guia=guiaremision_form.save()
            
        

            return HttpResponseRedirect('/facturacion/guiaremision')
        else:
    
            guiaremision_form=GuiaRemisionForm(request.POST)
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
class GuiaremisionListAprobarView(ObjectListView):
    model = GuiaRemision
    paginate_by = 100
    table_class = GuiaRemisionTable
    filter_class = GuiaRemisionFilter
    template_name = 'guiaremision/aprobada.html'
    context_object_name = 'guias'

    def get_context_data(self, **kwargs):
        context = super(GuiaremisionListAprobarView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('guiaremision-delete')
        return context
@login_required()
def GuiaRemisionAprobarByPkView(request, pk):

    objetos = GuiaRemision.objects.get(guia_id= pk)
    objetos.aprobada = True
    objetos.save()
    obj = GuiaDetalle.objects.filter(guia_id_id= pk)

    for o in obj:
        k=Kardex()
        k.nro_documento =objetos.nro_guia
        k.producto_id=o.producto_id_id
        k.cantidad=o.cantidad
        if objetos.egreso:
            k.descripcion='Orden de Egreso por Guia Remision'
            k.fecha_egreso=datetime.now()

        else:
            k.descripcion='Orden de Ingreso por Guia Remision'
            k.fecha_ingreso=datetime.now()
        k.bodega_id=3
        k.modulo=objetos.guia_id
        k.cliente_id=objetos.cliente_id
        k.save()
        try:
            objetose = ProductoEnBodega.objects.get(producto_id= o.producto_id_id,bodega_id=3)
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
            f.producto_id=o.producto_id_id
            f.bodega_id=3
            cant=0
            if objetos.egreso:
                f.cantidad=cant-float(o.cantidad)
            else:
                f.cantidad=cant+float(o.cantidad)

            f.updated_at = datetime.now()
            f.updated_by = request.user.get_full_name()
            f.save()



    return HttpResponseRedirect('/facturacion/guiaremisionAprobar')
@csrf_exempt
def obtenerDetalleGuia(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
     

        detalle = GuiaDetalle.objects.filter(guia_id_id=modulo)
        html=''
        for detal in detalle:
            product=Producto.objects.get(producto_id=detal.producto_id_id)

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

    objetos = GuiaRemision.objects.filter(id= pk)
    for obj in objetos:
        obj.anulada= True
        obj.save()
    
    return HttpResponseRedirect('/facturacion/guiaremisionAprobar')

def index(request,pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    guia=GuiaRemision.objects.get(guia_id=pk)
    detalle =GuiaDetalle.objects.filter(guia_id_id=guia.guia_id)
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