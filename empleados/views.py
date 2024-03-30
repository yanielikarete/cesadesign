# -*- encoding: utf-8 -*-
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
from .forms import *
from .tables import *
from .filters import *
from config.models import *





import datetime
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
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse
#from config.models import Mensajes



from login.lib.tools import Tools
from django.contrib import auth
#=========================Empleado============================#
@login_required()
def EmpleadoListView(request):
    empleados = Empleado.objects.all().order_by('empleado_id')
    return render_to_response('empleado/list.html', {'empleados':empleados},  RequestContext(request))


class EmpleadoDetailView(ObjectDetailView):
    model = Empleado
    template_name = 'empleado/detail.html'


@login_required()
def EmpleadoCreateView(request):
      if request.method == 'POST':
        form=EmpleadoForm(request.POST)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
        etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')

        if form.is_valid():
            new_orden=form.save()
            new_orden.created_by = 'admin'
            new_orden.updated_by = 'admin'
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            if 'imagen' in request.FILES:
                new_orden.imagen = request.FILES["imagen"]
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='empleados')
                secuencial.secuencial=secuencial.secuencial+1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            # contador=request.POST["columnas_receta"]
            # print contador
            # i=0
            # while int(i)<=int(contador):
            #     i+= 1
            #     print('entro comoqw'+str(i))
            #     if int(i)> int(contador):
            #         print('entrosd')
            #         break
            #     else:
            #         if 'tipo_kits'+str(i) in request.POST:
            #             print('entro tipo'+str(i))
            #             valor_m=request.POST["valor_mensual_kits"+str(i)]
            #             if valor_m:
            #                 ingresos=IngresosProyectadosEmpleado()
            #                 ingresos.empleado_id = new_orden.empleado_id
            #                 ingresos.tipo_ingreso_egreso_empleado_id=request.POST["tipo_kits"+str(i)]
            #                 ingresos.nombre=request.POST["nombre_kits"+str(i)]
            #                 ingresos.valor_mensual=request.POST["valor_mensual_kits"+str(i)]
            #                 ingresos.valor_diario=request.POST["valor_diario_kits"+str(i)]
            #                 ingresos.deducible=request.POST.get('deducible_kits'+str(i), False)
            #                 ingresos.aportaciones=request.POST.get('aportacion_kits'+str(i), False)
            #                 ingresos.save()
            #
            #     print(i)
            #     print('Ingreso contadorsd prueba'+str(contador))
            #
            # econtador=request.POST["ecolumnas_receta"]
            # print econtador
            # ei=0
            # while int(ei)<=int(econtador):
            #     ei+= 1
            #     print('entro comoqw'+str(ei))
            #     if int(ei)> int(econtador):
            #         print('entrosegreso')
            #         break
            #     else:
            #         if 'etipo_kits'+str(ei) in request.POST:
            #             print('entro tipo'+str(ei))
            #             evalor_m=request.POST["evalor_mensual_kits"+str(ei)]
            #             if evalor_m:
            #                 egresos=EgresosProyectadosEmpleado()
            #                 egresos.empleado_id = new_orden.empleado_id
            #                 egresos.tipo_ingreso_egreso_empleado_id=request.POST["etipo_kits"+str(ei)]
            #                 egresos.nombre=request.POST["enombre_kits"+str(ei)]
            #                 egresos.valor_mensual=request.POST["evalor_mensual_kits"+str(ei)]
            #                 egresos.valor_diario=request.POST["evalor_diario_kits"+str(ei)]
            #                 egresos.deducible=request.POST.get('ededucible_kits'+str(ei), False)
            #                 egresos.aportaciones=request.POST.get('eaportacion_kits'+str(ei), False)
            #                 egresos.save()
            #
            #     print(ei)
            #     print('EGRESO contadorsd prueba'+str(econtador))

            return HttpResponseRedirect('/empleados/empleado')
        else:
            print 'error'
            print form.errors, len(form.errors)
      else:
        form=EmpleadoForm
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
        etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')



      return render_to_response('empleado/create.html', { 'form': form,'tipos':tipos,'etipos':etipos},  RequestContext(request))

class EmpleadoUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        emplea = Empleado.objects.get(empleado_id=kwargs['pk'])
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
        etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')

        form=EmpleadoForm(instance=emplea)
        detalle = IngresosProyectadosEmpleado.objects.filter(empleado_id=emplea.empleado_id)
        edetalle = EgresosProyectadosEmpleado.objects.filter(empleado_id=emplea.empleado_id)

        context = {
        'section_title':'Actualizar Presupuesto',
        'button_text':'Actualizar',
        'form':form,
        'tipos':tipos,
        'etipos':etipos,
        'detalle':detalle,
        'edetalle':edetalle,
        'empleado':emplea
        }

        return render_to_response(
            'empleado/create.html', context,context_instance=RequestContext(request))


    def post(sel, request, *args, **kwargs):
        emplea = Empleado.objects.get(empleado_id=kwargs['pk'])
        form = EmpleadoForm(request.POST,request.FILES,instance=emplea)
        p_id=kwargs['pk']
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
        etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')

        if form.is_valid() :

            new_orden=form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            if 'imagen' in request.FILES:
                new_orden.imagen = request.FILES["imagen"]

            new_orden.save()


            # contador=request.POST["columnas_receta"]
            #
            # i=0
            # while int(i) <= int(contador):
            #     i+= 1
            #     if int(i) > int(contador):
            #         print('entrosd')
            #         break
            #     else:
            #         if 'tipo_kits'+str(i) in request.POST:
            #             if 'id_detalle'+str(i) in request.POST:
            #                 detalle_id=request.POST["id_detalle"+str(i)]
            #                 detallecompra = IngresosProyectadosEmpleado.objects.get(id=detalle_id)
            #                 detallecompra.updated_by = request.user.get_full_name()
            #                 detallecompra.tipo_ingreso_egreso_empleado_id =request.POST["tipo_kits"+str(i)]
            #                 detallecompra.nombre=request.POST["nombre_kits"+str(i)]
            #                 detallecompra.valor_mensual=request.POST["valor_mensual_kits"+str(i)]
            #                 detallecompra.valor_diario=request.POST["valor_diario_kits"+str(i)]
            #                 detallecompra.deducible=request.POST.get('deducible_kits'+str(i), False)
            #                 detallecompra.aportaciones=request.POST.get('aportacion_kits'+str(i), False)
            #                 detallecompra.updated_at = datetime.now()
            #                 #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
            #                 detallecompra.save()
            #
            #                 print('Tiene detalle'+str(i))
            #             else:
            #                 valor_m = request.POST["valor_mensual_kits" + str(i)]
            #                 if valor_m:
            #                     comprasdetalle=IngresosProyectadosEmpleado()
            #                     comprasdetalle.empleado_id = new_orden.empleado_id
            #                     comprasdetalle.tipo_ingreso_egreso_empleado_id =request.POST["tipo_kits"+str(i)]
            #                     comprasdetalle.nombre=request.POST["nombre_kits"+str(i)]
            #                     comprasdetalle.valor_mensual=request.POST["valor_mensual_kits"+str(i)]
            #                     comprasdetalle.valor_diario=request.POST["valor_diario_kits"+str(i)]
            #                     comprasdetalle.deducible=request.POST.get('deducible_kits'+str(i), False)
            #                     comprasdetalle.aportaciones=request.POST.get('aportacion_kits'+str(i), False)
            #                     comprasdetalle.created_at = datetime.now()
            #                     comprasdetalle.updated_at = datetime.now()
            #                     comprasdetalle.save()
            #                     i+= 1
            #                     print('No Tiene detalle'+str(i))
            #                     print('contadorsd prueba'+str(contador))
            #
            #
            # econtador=request.POST["ecolumnas_receta"]
            #
            # ei=0
            # while int(ei) <= int(econtador):
            #     ei+= 1
            #     if int(ei) > int(econtador):
            #         print('entrosd')
            #         break
            #     else:
            #         if 'etipo_kits'+str(ei) in request.POST:
            #             if 'eid_detalle'+str(ei) in request.POST:
            #                 edetalle_id=request.POST["eid_detalle"+str(i)]
            #                 edetallecompra = EgresosProyectadosEmpleado.objects.get(id=edetalle_id)
            #                 edetallecompra.updated_by = request.user.get_full_name()
            #                 edetallecompra.tipo_ingreso_egreso_empleado_id =request.POST["etipo_kits"+str(ei)]
            #                 edetallecompra.nombre=request.POST["enombre_kits"+str(ei)]
            #                 edetallecompra.valor_mensual=request.POST["evalor_mensual_kits"+str(ei)]
            #                 edetallecompra.valor_diario=request.POST["evalor_diario_kits"+str(ei)]
            #                 edetallecompra.deducible=request.POST.get('ededucible_kits'+str(ei), False)
            #                 edetallecompra.aportaciones=request.POST.get('eaportacion_kits'+str(ei), False)
            #                 edetallecompra.updated_at = datetime.now()
            #                 #detallecompra.recibido=request.POST.get("recibido_kits"+str(i), False)
            #                 edetallecompra.save()
            #
            #                 print('Tiene detalle'+str(ei))
            #             else:
            #                 valor_m=request.POST["evalor_mensual_kits"+str(ei)]
            #                 if len(valor_m):
            #                     ecomprasdetalle=EgresosProyectadosEmpleado()
            #                     ecomprasdetalle.empleado_id = new_orden.empleado_id
            #                     ecomprasdetalle.tipo_ingreso_egreso_empleado_id =request.POST["etipo_kits"+str(ei)]
            #                     ecomprasdetalle.nombre=request.POST["enombre_kits"+str(ei)]
            #                     ecomprasdetalle.valor_mensual=request.POST["evalor_mensual_kits"+str(ei)]
            #                     ecomprasdetalle.valor_diario=request.POST["evalor_diario_kits"+str(ei)]
            #                     ecomprasdetalle.deducible=request.POST.get('ededucible_kits'+str(ei), False)
            #                     ecomprasdetalle.aportaciones=request.POST.get('eaportacion_kits'+str(ei), False)
            #                     ecomprasdetalle.created_at = datetime.now()
            #                     ecomprasdetalle.updated_at = datetime.now()
            #                     ecomprasdetalle.save()
            #                     ei+= 1
            #                     print('No Tiene detalle'+str(ei))
            #                     print('contadorsd prueba'+str(econtador))
            #
            # #ordencompra_form=OrdenCompraForm(request.POST)
            # detalle = IngresosProyectadosEmpleado.objects.filter(empleado_id=p_id)
            # edetalle = EgresosProyectadosEmpleado.objects.filter(empleado_id=p_id)
            # tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
            # etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')

            context = {
           'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':form,
            #'detalle':detalle,
            #'edetalle':edetalle,
            'tipos':tipos,
            'etipos':etipos,
            'empleado':emplea,
            'mensaje':'actualizada con exito'}


            return render_to_response(
                'empleado/create.html',
                context,
                context_instance=RequestContext(request))
        else:

            emplea = Empleado.objects.get(empleado_id=kwargs['pk'])
            tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
            etipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')
            form=EmpleadoForm(instance=emplea)
            detalle = IngresosProyectadosEmpleado.objects.filter(empleado_id=emplea.empleado_id)
            edetalle = EgresosProyectadosEmpleado.objects.filter(empleado_id=emplea.empleado_id)

            context = {
            'section_title':'Actualizar Proforma',
            'button_text':'Actualizar',
            'form':form,
            'detalle':detalle,
            'edetalle':edetalle,
            'tipos':tipos,
            'etipos':etipos,
            'mensaje':'Proforma actualizada con exito'}

        return render_to_response(
            'empleado/create.html',
            context,
            context_instance=RequestContext(request))


#=====================================================#
@login_required()
def empleadoEliminarView(request):
    return eliminarView(request, Empleado, 'empleado-list')

#=====================================================#
@login_required()
def empleadoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Empleado)


#=========================TipoEmpleado============================#
@login_required()
def TipoEmpleadoListView(request):
    cargos = TipoEmpleado.objects.all()

    return render_to_response('tipoempleado/index.html', {'cargos': cargos}, RequestContext(request))


class TipoEmpleadoDetailView(ObjectDetailView):
    model = TipoEmpleado
    template_name = 'tipoempleado/detail.html'


@login_required()
def TipoEmpleadoCreateView(request):
    if request.method == 'POST':
        form = TipoEmpleadoForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            return HttpResponseRedirect('/empleados/tipoempleado/')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = TipoEmpleadoForm

    return render_to_response('tipoempleado/create.html', {'form': form},
                              RequestContext(request))



class TipoEmpleadoUpdateView(ObjectUpdateView):
    model = TipoEmpleado
    form_class = TipoEmpleadoForm
    template_name = 'tipoempleado/create.html'
    url_success = 'tipoempleado-list'
    url_cancel = 'tipoempleado-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()


        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo de Empleado actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



#=====================================================#
@login_required()
def tipoEmpleadoEliminarView(request):
    return eliminarView(request, Empleado, 'tipoempleado-list')

#=====================================================#
@login_required()
def tipoEmpleadoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, TipoEmpleado)


#=========================Vendedor============================#
@login_required()
def VendedorListView(request):
    if request.method == 'POST':
        empleados = Vendedor.objects.all().order_by('nombre')
        return render_to_response('vendedor/index.html', {'vendedores': empleados}, RequestContext(request))
    else:
        empleados = Vendedor.objects.all().order_by('nombre')
        return render_to_response('vendedor/index.html', {'vendedores': empleados}, RequestContext(request))

class VendedorDetailView(ObjectDetailView):
    model = Vendedor
    template_name = 'vendedor/detail.html'

class VendedorCreateView(ObjectCreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/create.html'
    url_success = 'vendedor-list'
    url_success_other = 'vendedor-create'
    url_cancel = 'vendedor-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_vendedor = str(self.object.codigo_vendedor).upper()
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(VendedorCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Vendedor."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class VendedorUpdateView(ObjectUpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'vendedor/create.html'
    url_success = 'vendedores-list'
    url_cancel = 'vendedores-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_vendedor = str(self.object.codigo_vendedor).upper()
        self.object.updated_by = self.request.user
        self.object.save()


        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Vendedor actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



#=====================================================#
@login_required()
def vendedorEliminarView(request):
    return eliminarView(request, Vendedor, 'empleado-list')

#=====================================================#
@login_required()
def vendedorEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Vendedor)


#=========================Chofer============================#
class ChoferListView(ObjectListView):
    model = Chofer
    paginate_by = 100
    template_name = 'chofer/index.html'
    table_class = ChoferTable
    filter_class = ChoferFilter

    def get_context_data(self, **kwargs):
        context = super(ChoferListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('chofer-delete')
        return context

class ChoferDetailView(ObjectDetailView):
    model = Chofer
    template_name = 'chofer/detail.html'

class ChoferCreateView(ObjectCreateView):
    model = Chofer
    form_class = ChoferForm
    template_name = 'chofer/create.html'
    url_success = 'chofer-list'
    url_success_other = 'chofer-create'
    url_cancel = 'chofer-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_chofer = str(self.object.codigo_chofer).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ChoferCreateView, self).form_valid(form)


    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Chofer."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class ChoferUpdateView(ObjectUpdateView):
    model = Chofer
    form_class = ChoferForm
    template_name = 'chofer/create.html'
    url_success = 'chofer-list'
    url_cancel = 'chofer-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo_chofer = str(self.object.codigo_chofer).upper()
        self.object.updated_by = self.request.user
        self.object.save()


        return super(ObjectUpdateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Chofer actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



#=====================================================#
@login_required()
def choferEliminarView(request):
    return eliminarView(request, Chofer, 'empleado-list')

#=====================================================#
@login_required()
def choferEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Chofer)


#=========================Vehiculo============================#
class VehiculoListView(ObjectListView):
    model = Vehiculo
    paginate_by = 100
    template_name = 'vehiculo/index.html'
    table_class = VehiculoTable
    filter_class = VehiculoFilter


    def get_context_data(self, **kwargs):
        context = super(VehiculoListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('vehiculo-delete')
        return context

class VehiculoDetailView(ObjectDetailView):
    model = Vehiculo
    template_name = 'vehiculo/detail.html'

class VehiculoCreateView(ObjectCreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/create.html'
    url_success = 'vehiculo-list'
    url_success_other = 'vehiculo-create'
    url_cancel = 'vehiculo-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.placa = str(self.object.placa).upper()
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(VehiculoCreateView, self).form_valid(form)


    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Vehiculo."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class VehiculoUpdateView(ObjectUpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculo/create.html'
    url_success = 'vehiculo-list'
    url_cancel = 'vehiculo-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.placa = str(self.object.placa).upper()
        self.object.updated_by = self.request.user
        self.object.save()


        return super(ObjectUpdateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Vehiculo actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

#=====================================================#
@login_required()
def vehiculoEliminarView(request):
    return eliminarView(request, Vehiculo, 'empleado-list')

#=====================================================#
@login_required()
def vehiculoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Vehiculo)

@login_required()
def DepartamentoListView(request):
    if request.method == 'POST':

        departamentos = Departamento.objects.all()
        return render_to_response('departamento/index.html', {'departamentos': departamentos}, RequestContext(request))
    else:
        departamentos = Departamento.objects.all()
        return render_to_response('departamento/index.html', {'departamentos': departamentos}, RequestContext(request))

class DepartamentoDetailView(ObjectDetailView):
    model = Departamento
    template_name = 'departamento/detail.html'

class DepartamentoCreateView(ObjectCreateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'departamento/create.html'
    url_success = 'departamento-list'
    url_success_other = 'departamento-create'
    url_cancel = 'departamento-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        objetos = Secuenciales.objects.get(modulo = 'departamento')

        modulo_secuencial = objetos.secuencial+1
        objetos.secuencial=modulo_secuencial
        objetos.save()

        return super(DepartamentoCreateView, self).form_valid(form)


    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Departamento."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class DepartamentoUpdateView(ObjectUpdateView):
    model = Departamento
    form_class = DepartamentoForm
    template_name = 'departamento/create.html'
    url_success = 'departamento-list'
    url_cancel = 'departamento-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.codigo = str(self.object.codigo).upper()
        self.object.updated_by = self.request.user
        self.object.save()


        return super(ObjectUpdateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Departamento actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



#=====================================================#
@login_required()
def departamentoEliminarView(request):
    return eliminarView(request, Departamento, 'departamento-list')

#=====================================================#
@login_required()
def departamentoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Departamento)

@login_required()
def eliminarIngresosView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        objetos = IngresosProyectadosEmpleado.objects.filter(id=id)
        for obj in objetos:
            obj.delete()
        modulo_secuencial="Guardado con exito"


        return HttpResponse(
                modulo_secuencial
            )
    else:
        raise Http404

@login_required()
def eliminarEgresosView(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        objetos = EgresosProyectadosEmpleado.objects.filter(id=id)
        for obj in objetos:
            obj.delete()
        modulo_secuencial="Guardado con exito"


        return HttpResponse(
                modulo_secuencial
            )
    else:
        raise Http404


@login_required()
def TipoContratoListView(request):
    if request.method == 'POST':

        tipos = TipoContrato.objects.all()
        return render_to_response('tipo_contrato/index.html', {'tipos': tipos}, RequestContext(request))
    else:
        tipos = TipoContrato.objects.all()
        return render_to_response('tipo_contrato/index.html', {'tipos': tipos}, RequestContext(request))

class TipoContratoCreateView(ObjectCreateView):
    model = TipoContrato
    form_class = TipoContratoForm
    template_name = 'tipo_contrato/create.html'
    url_success = 'tipo-contrato-list'
    url_success_other = 'tipo-contrato-create'
    url_cancel = 'tipo-contrato-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.updated_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()


        return super(TipoContratoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo tipo de contrato."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class TipoContratoUpdateView(ObjectUpdateView):
    model = TipoContrato
    form_class = TipoContratoForm
    template_name = 'tipo_contrato/create.html'
    url_success = 'tipo-contrato-list'
    url_cancel = 'tipo-contrato-list'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)


    def get_success_url(self):
        messages.success(self.request, 'Tipo Contrato actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def GrupoPagoListView(request):
    if request.method == 'POST':

        tipos = GrupoPago.objects.all()
        return render_to_response('grupo_pago/index.html', {'tipos': tipos}, RequestContext(request))
    else:
        tipos = GrupoPago.objects.all()
        return render_to_response('grupo_pago/index.html', {'tipos': tipos}, RequestContext(request))

class GrupoPagoCreateView(ObjectCreateView):
    model = GrupoPago
    form_class = GrupoPagoForm
    template_name = 'grupo_pago/create.html'
    url_success = 'grupo-pago-list'
    url_success_other = 'grupo-pago-create'
    url_cancel = 'grupo-pago-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()


        return super(GrupoPagoCreateView, self).form_valid(form)


    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo grupo pago."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

class GrupoPagoUpdateView(ObjectUpdateView):
    model = GrupoPago
    form_class = GrupoPagoForm
    template_name = 'grupo_pago/create.html'
    url_success = 'grupo-pago-list'
    url_cancel = 'grupo-pago-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Grupo Pago actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
def ConsultarEmpleadosView(request):
  cargos = TipoEmpleado.objects.all()
  banco = Banco.objects.all()
  empleados = Empleado.objects.all()
  departamentos = Departamento.objects.all()
  return render_to_response('empleado/consultar_empleado.html',
                                  { 'cargos': cargos,
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))


@login_required()
@csrf_exempt
def obtenerEmpleadosConsulta(request):
    if request.method == 'POST':

        activo = request.POST["activo"]
        cargo = request.POST["cargo"]
        departamento = request.POST["departamento"]
        empleado = request.POST["empleado"]
        fecha = request.POST["fecha"]
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        cursor = connection.cursor()
        sql = 'select e.empleado_id,e.codigo_empleado,e.cedula_empleado,e.nombre_empleado,e.activo,e.fecha_nacimiento,e.sexo,e.cargas_familiares,e.fecha_ini_reconocida,e.codigo_reloj,de.nombre,ca.cargo_empleado from departamento de,empleados_empleado e, empleados_tipoempleado ca where  e.departamento_id=de.id and e.tipo_empleado_id=ca.tipo_empleado_id and  1=1 '
        if activo != '0':
            sql += ' and e.activo=' + activo
        if cargo != '0':
            sql += " and e.tipo_empleado_id='" + cargo + "' "
        if fecha != '':
            sql += " and e.fecha_ini_reconocida='" + fecha + "' "
        if empleado != '0':
            sql += ' and e.empleado_id=' + empleado
        if departamento != '0':
            sql += ' and de.id=' + departamento

        sql += ' order by e.nombre_empleado;'
        cursor.execute(sql)
        rol = cursor.fetchall()

        # try:
        #   rol = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena,anio=anio,mes=mes)
        # except DiasNoLaboradosRolEmpleado.DoesNotExist:
        #   rol = None

        if rol:

            for r in rol:
                detal = Empleado.objects.get(empleado_id=r[0])
                i += 1
                try:
                    sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                     tipo_ingreso_egreso_empleado_id=24)
                except IngresosProyectadosEmpleado.DoesNotExist:
                    sueldo = 0

                html += '<tr>'
                html += '<td>' + str(i) + '</td>'
                html += '<td>' + str(detal.codigo_empleado.encode('utf8')) + '</td>'
                html += '<td>' + str(detal.nombre_empleado.encode('utf8')) + '</td>'
                html += '<td>' + str(detal.cedula_empleado.encode('utf8')) + '</td>'
                html += '<td>' + str(detal.departamento) + '</td>'
                if detal.tipo_empleado:
                    html += '<td>' + str(detal.tipo_empleado) + '</td>'
                else:
                    html += '<td></td>'
                html += '<td>' + str(detal.fecha_nacimiento) + '</td>'
                if detal.sexo:
                    html += '<td>' + str(detal.sexo) + '</td>'
                else:
                    html += '<td></td>'

                if detal.estado_civil:
                    html += '<td>' + str(detal.estado_civil.nombre) + '</td>'
                else:
                    html += '<td></td>'
                if detal.activo:
                    html += '<td>SI</td>'
                else:
                    html += '<td>NO</td>'
                html += '<td>' + str(detal.fecha_ini_reconocida) + '</td>'
                if sueldo:
                    html += '<td>' + str(sueldo.valor_mensual) + '</td>'
                else:
                    html += '<td>' + str(sueldo) + '</td>'

                html += '<td>' + str(detal.cargas_familiares) + '</td>'
                html += '<td>' + str(detal.codigo_reloj) + '</td>'
                html += '</tr>'


        else:
            html += '<tr><td colspan="8">No existen datos</td></tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404
