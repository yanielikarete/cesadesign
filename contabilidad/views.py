# -*- encoding: utf-8 -*-
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, \
    eliminarByPkView
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
from contabilidad.models import TipoCuenta
from django.core.serializers.json import DjangoJSONEncoder
from django.db import IntegrityError, transaction
from transacciones.models import DocumentoCompra,DocumentoAbono
from bancos.models import Movimiento
from proveedores.models import *
from django.template import loader, Context
from django.utils.dateformat import DateFormat
from decimal import *
import calendar

# =================== LIBRO DIARIO =================================#

@login_required()
def libro_diario_index(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    centro_costos = CentroCosto.objects.filter(activo=True).order_by('codigo')
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('registrar_libro_diario/registrar_libro_diario.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centro_costos': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))

@login_required()
def consultar_libro_diario(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['centro_costo']
        #desde = request.POST['desde']
        #hasta = request.POST['hasta']
        desde = fecha_desde
        hasta = fecha_hasta

        cursor = connection.cursor()

        if cuenta == "Todas": cuenta = "%"

        if desde != "" and hasta != "":
            if centroCosto != "0":
                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber,grupo_id, nombre_plan, '
                    'codigo_plan, nombre_tipo, nombre_centro '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and asiento.fecha between %s and %s'
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and nombre_plan like %s '
                    'and centro_costo_id=%s '
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (desde, hasta,cuenta,centroCosto))
            else:

                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber,grupo_id, nombre_plan, '
                    'codigo_plan, nombre_tipo, nombre_centro '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and asiento.fecha between %s and %s'
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and nombre_plan like %s '
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (desde, hasta,cuenta))

        else:
            if centroCosto != "0":
                cursor.execute(
                'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber,grupo_id, nombre_plan, '
                'codigo_plan, nombre_tipo, nombre_centro '
                'from contabilidad_asiento as asiento,  '
                'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                'LEFT JOIN contabilidad_centrocosto as ccosto '
                'ON adetalle.centro_costo_id = ccosto.centro_id '
                'where asiento.asiento_id = adetalle.asiento_id '
                'and adetalle.cuenta_id = cuenta.plan_id  '
                'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                'and nombre_plan like %s '
                'and asiento.fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') '
                'and centro_costo_id=%s '
                'ORDER BY asiento.fecha,asiento.codigo_asiento', (cuenta, fecha_desde, fecha_hasta,centroCosto))
            else:

                cursor.execute(
                'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber,grupo_id, nombre_plan, '
                'codigo_plan, nombre_tipo, nombre_centro '
                'from contabilidad_asiento as asiento,  '
                'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                'LEFT JOIN contabilidad_centrocosto as ccosto '
                'ON adetalle.centro_costo_id = ccosto.centro_id '
                'where asiento.asiento_id = adetalle.asiento_id '
                'and adetalle.cuenta_id = cuenta.plan_id  '
                'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                'and nombre_plan like %s '
                'and asiento.fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') '
                'ORDER BY asiento.fecha,asiento.codigo_asiento', (cuenta, fecha_desde, fecha_hasta))

        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)

    else:
        raise Http404

    return HttpResponse(json_resultados, content_type="application/json")


# ========================= MAYORES CONTABLES ==========================#


@login_required()
def MayoresContablesView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    return render_to_response('registrar_libro_diario/mayores_contables.html',
                              RequestContext(request, {'cuentas': plan_ctas}))


@login_required()
def ConsultaMayorView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']


        cursor = connection.cursor()

        cursor.execute(
            'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto '
            'from contabilidad_asiento as asiento,  '
            'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
            'LEFT JOIN contabilidad_centrocosto as ccosto '
            'ON adetalle.centro_costo_id = ccosto.centro_id '
            'where asiento.asiento_id = adetalle.asiento_id '
            'and adetalle.cuenta_id = cuenta.plan_id  '
            'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
            'and cuenta.plan_id = %s '
            'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
            'ORDER BY asiento.fecha,asiento.codigo_asiento', (cuenta, fecha_desde, fecha_hasta))

        ro = cursor.fetchall()
        json_resultados = json.dumps(ro)

    else:
        raise Http404

    return HttpResponse(json_resultados, content_type="application/json")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return list


# =========================EjercicioContable============================#

class EjercicioContableListView(ObjectListView):
    model = EjercicioContable
    paginate_by = 100
    template_name = 'ejerciciocontable/index.html'
    table_class = EjercicioContableTable
    filter_class = EjercicioContableFilter

    def get_context_data(self, **kwargs):
        context = super(EjercicioContableListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('ejerciciocontable-delete')
        return context


class EjercicioContableDetailView(ObjectDetailView):
    model = EjercicioContable
    template_name = 'ejerciciocontable/detail.html'


class EjercicioContableCreateView(ObjectCreateView):
    model = EjercicioContable
    form_class = EjercicioContableForm
    template_name = 'ejerciciocontable/create.html'
    url_success = 'ejerciciocontable-list'
    url_success_other = 'ejerciciocontable-create'
    url_cancel = 'ejerciciocontable-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user.get_full_name()
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(EjercicioContableCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo EjercicioContable."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class EjercicioContableUpdateView(ObjectUpdateView):
    model = EjercicioContable
    form_class = EjercicioContableForm
    template_name = 'ejerciciocontable/create.html'
    url_success = 'ejerciciocontable-list'
    url_cancel = 'ejerciciocontable-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Ejercicio Contable actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def ejercicioContableEliminarView(request):
    return eliminarView(request, EjercicioContable, 'ejerciciocontable-list')


# =====================================================#
@login_required()
def ejercicioContableEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, EjercicioContable)


# =========================PlanDeCuentas============================#

@login_required()
def PlanDeCuentasListView(request):
    if request.method == 'POST':

        row = PlanDeCuentas.objects.filter(activo=True).order_by('codigo_plan')
        return render_to_response('plandecuentas/index.html', {'row': row}, RequestContext(request))
    else:
        row = PlanDeCuentas.objects.filter(activo=True).order_by('codigo_plan')
        return render_to_response('plandecuentas/index.html', {'row': row}, RequestContext(request))


class PlanDeCuentasDetailView(ObjectDetailView):
    model = PlanDeCuentas
    template_name = 'plandecuentas/detail.html'


@login_required()
def PlanDeCuentasCreateView(request):
    if request.method == 'POST':
        proforma_form = PlanDeCuentasForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save(commit=False)
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            
            new_orden.save()

            return HttpResponseRedirect('/contabilidad/plandecuentas')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = PlanDeCuentasForm

    return render_to_response('plandecuentas/create.html', {'form': proforma_form,}, RequestContext(request))


class PlanDeCuentasUpdateView(ObjectUpdateView):
    model = PlanDeCuentas
    form_class = PlanDeCuentasForm
    template_name = 'plandecuentas/edit.html'
    url_success = 'plandecuentas-list'
    url_cancel = 'plandecuentas-list'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Plan de Cuentas actualizado con exito')

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def planDeCuentasEliminarView(request):
    return eliminarView(request, PlanDeCuentas, 'plandecuentas-list')


# =====================================================#
@login_required()
def planDeCuentasEliminarByPkView(request, pk):
    obj = PlanDeCuentas.objects.get(plan_id=pk)

    if obj:
        obj.activo = False
        obj.save()

    return HttpResponseRedirect('/contabilidad/plandecuentas')


# =========================TipoCuenta============================#

class TipoCuentaListView(ObjectListView):
    model = TipoCuenta
    paginate_by = 100
    template_name = 'tipocuenta/index.html'
    table_class = TipoCuentaTable
    filter_class = TipoCuentaFilter

    def get_context_data(self, **kwargs):
        context = super(TipoCuentaListView, self).get_context_data(**kwargs)
        context['url_delete'] = reverse_lazy('tipocuenta-delete')
        return context


class TipoCuentaDetailView(ObjectDetailView):
    model = TipoCuenta
    template_name = 'tipocuenta/detail.html'


class TipoCuentaCreateView(ObjectCreateView):
    model = TipoCuenta
    form_class = TipoCuentaForm
    template_name = 'tipocuenta/create.html'
    url_success = 'tipocuenta-list'
    url_success_other = 'tipocuenta-create'
    url_cancel = 'tipocuenta-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user.get_full_name()
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(TipoCuentaCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Tipo de Cuenta."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class TipoCuentaUpdateView(ObjectUpdateView):
    model = TipoCuenta
    form_class = TipoCuentaForm
    template_name = 'tipocuenta/create.html'
    url_success = 'tipocuenta-list'
    url_cancel = 'tipocuenta-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Tipo de Cuenta actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def tipoCuentaEliminarView(request):
    return eliminarView(request, TipoCuenta, 'tipocuenta-list')


# =====================================================#
@login_required()
def tipoCuentaEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, TipoCuenta)


# =========================CentroCosto============================#
@login_required()
def CentroCostoListView(request):
    centro_costo = CentroCosto.objects.all()
    return render_to_response('centrocosto/index.html', {'centro_costo':centro_costo},  RequestContext(request))

class CentroCostoDetailView(ObjectDetailView):
    model = CentroCosto
    template_name = 'centrocosto/detail.html'


class CentroCostoCreateView(ObjectCreateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'centrocosto/create.html'
    url_success = 'centrocosto-list'
    url_success_other = 'centrocosto-create'
    url_cancel = 'centrocosto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user.get_full_name()
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()
        
        if self.object.padre_id:
            padre = CentroCosto.objects.get(centro_id = self.object.padre_id)
            modulo_secuencial_padre = padre.secuencia_subcentro+1
            padre.secuencia_subcentro=modulo_secuencial_padre
            padre.save()
        else:
            objetos = Secuenciales.objects.get(modulo = 'centro_costo')
            modulo_secuencial = objetos.secuencial+100
            objetos.secuencial=modulo_secuencial
            objetos.save()
            
            

        return super(CentroCostoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo Centro de Costo."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


class CentroCostoUpdateView(ObjectUpdateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'centrocosto/create.html'
    url_success = 'centrocosto-list'
    url_cancel = 'centrocosto-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Centro de Costo actualizado con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#
@login_required()
def centroCostoEliminarView(request):
    return eliminarView(request, CentroCosto, 'centrocosto-list')


# =====================================================#
@login_required()
def centroCostoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, CentroCosto)


# =========================Asiento============================#

@login_required()
def AsientoListView(request):
    # asientos = Asiento.objects.all().order_by('-asiento_id')
    # cursor = connection.cursor()
    # sql='select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,a.modulo,m.proveedor_id,m.descripcion,m.paguese_a,m.monto,m.numero_comprobante from contabilidad_asiento a left join movimiento m on m.asiento_id=a.asiento_id order by a.fecha;'
    # cursor.execute(sql)
    # ro = cursor.fetchall()
    ro=''
    asientos=''
    
    return render_to_response('asiento/index.html', {'asientos': asientos,'ro': ro}, RequestContext(request))

class AsientoDetailView(ObjectDetailView):
    model = Asiento
    template_name = 'asiento/detail.html'


@login_required()
@transaction.atomic
def AsientoCreateView(request):
    if request.method == 'POST':
        asiento_form = AsientoForm(request.POST)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.filter(activo=True)

        if asiento_form.is_valid():
            with transaction.atomic():
                new_asiento = asiento_form.save()
                new_asiento.created_by = request.user.get_full_name()
                new_asiento.updated_by = request.user.get_full_name()
                new_asiento.created_at = datetime.now()
                new_asiento.updated_at = datetime.now()
                new_asiento.modulo='Contabilidad-Asiento'

                new_asiento.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='asiento')

                    new_asiento.secuencia_asiento = secuencial.secuencial
                    new_asiento.save()

                    secuencial.secuencial = secuencial.secuencial + 1
                    secuencial.updated_by = request.user.get_full_name()
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

                        if 'id_cuenta_kits' + str(i) in request.POST:

                            asientodetalle = AsientoDetalle()
                            asientodetalle.asiento = new_asiento
                            asientodetalle.cuenta = PlanDeCuentas.objects.get(
                                pk=request.POST["id_cuenta_kits" + str(i)])
                            if request.POST["id_centro_kits" + str(i)] != '0':
                                asientodetalle.centro_costo = CentroCosto.objects.get(
                                    pk=request.POST["id_centro_kits" + str(i)])
                            asientodetalle.debe = request.POST["debe_kits" + str(i)]
                            asientodetalle.haber = request.POST["haber_kits" + str(i)]
                            asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                            asientodetalle.save()

                    print(i)
                    print('contadorsd prueba' + str(contador))

                return HttpResponseRedirect('/contabilidad/asiento')
        else:
            print 'error'
            print asiento_form.errors, len(asiento_form.errors)
    else:
        asiento_form = AsientoForm
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()

    return render_to_response('asiento/create.html',
                              {'asiento_form': asiento_form, 'cuentas': cuentas, 'centros': centros,'centros_defecto':centros_defecto},
                              RequestContext(request))


def AsientoUpdateView(request, pk):
    if request.method == 'POST':
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(request.POST, request.FILES, instance=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        modulo=asiento.modulo

        print asiento_form.is_valid(), asiento_form.errors, type(asiento_form.errors)

        if asiento_form.is_valid():
            asiento = asiento_form.save()
            asiento.modulo=modulo
            asiento.updated_by = request.user.get_full_name()
            asiento.updated_at = datetime.now()
            asiento.save()
            contador = request.POST["columnas_receta"]
            objetos = AsientoDetalle.objects.filter(asiento_id=pk)
            for obj in objetos:
                obj.delete()

            i = 0
            while int(i) < int(contador):
                i += 1
                if 'id_cuenta_kits' + str(i) in request.POST:
                    asientodetalle = AsientoDetalle()
                    asientodetalle.asiento = asiento
                    asientodetalle.cuenta = PlanDeCuentas.objects.get(
                    pk=request.POST["id_cuenta_kits" + str(i)])

                    if request.POST["id_centro_kits" + str(i)] != '0':
                        try:
                            c_cost = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])

                        except CentroCosto.DoesNotExist:
                            c_cost = None
                        if c_cost:
                            asientodetalle.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                    asientodetalle.debe = request.POST["debe_kits" + str(i)]
                    asientodetalle.haber = request.POST["haber_kits" + str(i)]
                    asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                    asientodetalle.save()
                # if 'id_detalle' + str(i) in request.POST:
                #     detalle_id = request.POST["id_detalle" + str(i)]
                #     detalle_asiento = AsientoDetalle.objects.get(detalle_id=detalle_id)
                #     detalle_asiento.cuenta = PlanDeCuentas.objects.get(pk=request.POST["id_cuenta_kits" + str(i)])
                #     if request.POST["id_centro_kits" + str(i)] != '0':
                #         detalle_asiento.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                #     detalle_asiento.debe = request.POST["debe_kits" + str(i)]
                #     detalle_asiento.haber = request.POST["haber_kits" + str(i)]
                #     detalle_asiento.concepto = request.POST["concepto_kits" + str(i)]
                #     detalle_asiento.save()
                #
                # else:
                #     asientodetalle = AsientoDetalle()
                #     asientodetalle.asiento = asiento
                #     asientodetalle.cuenta = PlanDeCuentas.objects.get(
                #         pk=request.POST["id_cuenta_kits" + str(i)])
                #     if request.POST["id_centro_kits" + str(i)] != '0':
                #         asientodetalle.centro_costo = CentroCosto.objects.get(
                #             pk=request.POST["id_centro_kits" + str(i)])
                #     asientodetalle.debe = request.POST["debe_kits" + str(i)]
                #     asientodetalle.haber = request.POST["haber_kits" + str(i)]
                #     asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                #     asientodetalle.save()


            return HttpResponseRedirect('/contabilidad/asiento')
        else:

            asiento_form = AsientoForm(request.POST)
            detalle = AsientoDetalle.objects.filter(asiento=asiento.asiento_id).order_by('detalle_id')

            context = {
                'section_title': 'Actualizar Asiento',
                'button_text': 'Actualizar',
                'asiento_form': asiento_form,
                'cuentas': cuentas, 'centros': centros,
                'detalle': detalle}

        return render_to_response(
            'asiento/update.html',
            context,
            context_instance=RequestContext(request))
    else:
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(instance=asiento)
        detalle = AsientoDetalle.objects.filter(asiento=asiento).order_by('detalle_id')
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()

        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'asiento_form': asiento_form,
            'cuentas': cuentas, 'centros': centros,
            'detalle': detalle}

        return render_to_response(
            'asiento/update.html',
            context,
            context_instance=RequestContext(request))


# =====================================================#
@login_required()
def asientoEliminarView(request):
    return eliminarView(request, Asiento, 'asiento-list')


# =====================================================#
@login_required()
def asientoEliminarByPkView(request, pk):
    return eliminarByPkView(request, pk, Asiento)


@login_required()
def estadoSituacionFinancieraView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True, tipo_cuenta_id__in=[2, 3, 4]).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/balance_general.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))




def asientoRelacionarFacturasView(request, pk):
    if request.method == 'POST':
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(request.POST, request.FILES, instance=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        
        try:
            movimiento=Movimiento.objects.get(asiento_id=pk)
        except Movimiento.DoesNotExist:
                    movimiento = None

        print asiento_form.is_valid(), asiento_form.errors, type(asiento_form.errors)
        if movimiento:
            print 'entro a movimiento'
            movimiento.descripcion=request.POST["descripcion_movimiento"]
            movimiento.updated_by = request.user.get_full_name()
            movimiento.updated_at = datetime.now()
            movimiento.save()
        
        
       
        centros = CentroCosto.objects.all()
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()


        if asiento_form.is_valid():
            asiento = asiento_form.save()
            asiento.modulo='Banco'
            asiento.updated_by = request.user.get_full_name()
            asiento.created_by = request.user.get_full_name()
            asiento.created_at = datetime.now()
            asiento.updated_at = datetime.now()
            asiento.save()
            contador2 = request.POST["columnas_receta"]
            objetos = AsientoDetalle.objects.filter(asiento_id=pk)
            for obj in objetos:
                obj.delete()

            i = 0
            while int(i) < int(contador2):
                i += 1
                if 'id_cuenta_kits' + str(i) in request.POST:
                    asientodetalle = AsientoDetalle()
                    asientodetalle.asiento = asiento
                    asientodetalle.cuenta = PlanDeCuentas.objects.get(
                    pk=request.POST["id_cuenta_kits" + str(i)])

                    if request.POST["id_centro_kits" + str(i)] != '0':
                        try:
                            c_cost = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])

                        except CentroCosto.DoesNotExist:
                            c_cost = None
                        if c_cost:
                            asientodetalle.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                    asientodetalle.debe = request.POST["debe_kits" + str(i)]
                    asientodetalle.haber = request.POST["haber_kits" + str(i)]
                    asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                    asientodetalle.save()
                    
                    

            contador = request.POST["columnas_recetaf"]
            i = 0
            while int(i) < int(contador):
                i += 1
                if 'facturas_kits' + str(i) in request.POST:
                    
                    if 'id_detallef' + str(i) in request.POST:
                        id_detall=request.POST["id_detallef" + str(i)]
                        if id_detall:
                            print "ID detalle"
                            print id_detall
                            asientodetalle=DocumentoAbono.objects.get(id=id_detall)
                            asientodetalle.abono = request.POST["monto_kits" + str(i)]
                            asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                            asientodetalle.activo=True
                            asientodetalle.anulado=False
                            asientodetalle.updated_by = request.user.get_full_name()
                            asientodetalle.updated_at = datetime.now()
                            asientodetalle.save()
                        else:
                            fact=request.POST["facturas_kits" + str(i)]
                            if fact!='0':
                                asientodetalle = DocumentoAbono()
                                asientodetalle.movimiento_id = movimiento.id
                                asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                asientodetalle.activo=True
                                asientodetalle.anulado=False
                                asientodetalle.updated_by = request.user.get_full_name()
                                asientodetalle.created_by = request.user.get_full_name()
                                asientodetalle.created_at = datetime.now()
                                asientodetalle.updated_at = datetime.now()
                                asientodetalle.save()
                            
                        
                    else:
                        fact=request.POST["facturas_kits" + str(i)]
                        if fact!='0':
                            asientodetalle = DocumentoAbono()
                            asientodetalle.movimiento_id = movimiento.id
                            asientodetalle.abono = request.POST["monto_kits" + str(i)]
                            asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                            asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                            asientodetalle.activo=True
                            asientodetalle.anulado=False
                            asientodetalle.updated_by = request.user.get_full_name()
                            asientodetalle.created_by = request.user.get_full_name()
                            asientodetalle.created_at = datetime.now()
                            asientodetalle.updated_at = datetime.now()
                            asientodetalle.save()
                                

              

        return HttpResponseRedirect('/contabilidad/asiento_factura_list')
       

        
    else:
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(instance=asiento)
        detalle = AsientoDetalle.objects.filter(asiento=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        facturas= DocumentoCompra.objects.exclude(nota_credito=True).exclude(anulado=True).order_by('-fecha_emision')
        try:
            movimiento = Movimiento.objects.filter(asiento_id=pk).last()
        except Movimiento.DoesNotExist:
            movimiento = None
        print movimiento
        if movimiento:
            proveedor_id=movimiento.proveedor_id
        else:
            proveedor_id ='0'
       
        
        cursor = connection.cursor()
        #facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,SUM(dr.retenciones) as retenciones,dc.total_pagar ,SUM(m.total) as nc,dc.valor_retenido from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN documento_compra_retenciones dr ON (dr.documento_compra_id = dc.id)  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        # if proveedor_id == '0':
        #     facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        # else:
        #     facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True and dc.proveedor_id='+str(proveedor_id)+' GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        cursor.execute(facturas_sql)
        ro = cursor.fetchall()
        
        
        detalle_sql='select dc.* from documento_abono dc, contabilidad_asiento a,movimiento m where a.asiento_id=m.asiento_id and m.id=dc.movimiento_id and a.asiento_id=' + (pk) +';'
        cursor.execute(detalle_sql)
        detallefactura= cursor.fetchall()
        
        
        facturas2_sql='select f.id,f.establecimiento,f.punto_emision,f.secuencial,f.descripcion from documento_abono dc,documento_compra f, movimiento m where m.id=dc.movimiento_id and f.id=dc.documento_compra_id and m.asiento_id=' + (pk) +';'
        cursor.execute(facturas2_sql)
        ro2 = cursor.fetchall()
        
        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'asiento_form': asiento_form,
            'facturas': facturas,
            'cuentas': cuentas,
            'centros': centros,
            'facturas_sql': ro,
            'detallefactura':detallefactura,
            'movimiento': movimiento,
            'facturas_sql2': ro2,
            'centros_defecto':centros_defecto,
            'detalle': detalle
            }
        
        
        return render_to_response(
            'asiento/asientoFacturas.html',
            context,
            context_instance=RequestContext(request))



@login_required()
def asiento_factura_list(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,m.proveedor_id,m.descripcion,m.paguese_a,td.descripcion,m.monto,periodos from contabilidad_asiento a,movimiento m,tipo_documento td ,(SELECT b.id as periodos,p.asiento_id FROM contabilidad_asiento  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha)) G  where G.asiento_id= a.asiento_id and m.asiento_id=a.asiento_id and m.tipo_anticipo_id=1 and td.id=m.tipo_documento_id and m.activo=true and td.id=1;"
        cursor.execute(query)
        asientos = cursor.fetchall()
        #print asientos
        return render_to_response('asiento/asientoFacturaList.html', {'asientos': asientos},
                                  RequestContext(request))
    else:
        cursor = connection.cursor()
        query = "select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,m.proveedor_id,m.descripcion,m.paguese_a,td.descripcion,m.monto,periodos from contabilidad_asiento a,movimiento m,tipo_documento td ,(SELECT b.id as periodos,p.asiento_id FROM contabilidad_asiento  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha)) G  where G.asiento_id= a.asiento_id and m.asiento_id=a.asiento_id and m.tipo_anticipo_id=1 and td.id=m.tipo_documento_id and m.activo=true and td.id=1;"
        cursor.execute(query)
        asientos = cursor.fetchall()
        #print asientos
        return render_to_response('asiento/asientoFacturaList.html', {'asientos': asientos},
                                  RequestContext(request))



#ASIENTO ASOCIAR AL LIBRO DIARIO
def asientoRelacionarFacturasLibroDiarioView(request, pk):
    if request.method == 'POST':
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(request.POST, request.FILES, instance=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        #print pk
        try:
            movimiento=Movimiento.objects.get(asiento_id=pk)
        except Movimiento.DoesNotExist:
            movimiento = None

        print asiento_form.is_valid(), asiento_form.errors, type(asiento_form.errors)
        
        if movimiento:
            movimiento.updated_by = request.user.get_full_name()
            movimiento.updated_at = datetime.now()
            
            
            movimiento.descripcion=request.POST["descripcion_movimiento"]
            movimiento.save()
        
        
       
        centros = CentroCosto.objects.all()


        if asiento_form.is_valid():
            asiento = asiento_form.save()
            asiento.modulo='Libro Diario'
            asiento.updated_by = request.user.get_full_name()
            asiento.created_by = request.user.get_full_name()
            asiento.created_at = datetime.now()
            asiento.updated_at = datetime.now()
            asiento.save()
            contador2 = request.POST["columnas_receta"]
            objetos = AsientoDetalle.objects.filter(asiento_id=pk)
            for obj in objetos:
                obj.delete()

            i = 0
            while int(i) < int(contador2):
                i += 1
                if 'id_cuenta_kits' + str(i) in request.POST:
                    asientodetalle = AsientoDetalle()
                    asientodetalle.asiento = asiento
                    asientodetalle.cuenta = PlanDeCuentas.objects.get(
                    pk=request.POST["id_cuenta_kits" + str(i)])

                    if request.POST["id_centro_kits" + str(i)] != '0':
                        try:
                            c_cost = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])

                        except CentroCosto.DoesNotExist:
                            c_cost = None
                        if c_cost:
                            asientodetalle.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                    asientodetalle.debe = request.POST["debe_kits" + str(i)]
                    asientodetalle.haber = request.POST["haber_kits" + str(i)]
                    asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                    asientodetalle.save()
                    
                    

            contador = request.POST["columnas_recetaf"]
            i = 0
            while int(i) < int(contador):
                i += 1
                if 'facturas_kits' + str(i) in request.POST:
                    
                    if 'id_detallef' + str(i) in request.POST:
                        id_detall=request.POST["id_detallef" + str(i)]
                        if id_detall:
                            asientodetalle=DocumentoAbono.objects.get(id=id_detall)
                            asientodetalle.abono = request.POST["monto_kits" + str(i)]
                            asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                            asientodetalle.activo=True
                            asientodetalle.anulado=False
                            asientodetalle.updated_by = request.user.get_full_name()
                            asientodetalle.updated_at = datetime.now()
                            asientodetalle.save()
                        else:
                            fact=request.POST["facturas_kits" + str(i)]
                            if fact!='0':
                                asientodetalle = DocumentoAbono()
                                asientodetalle.movimiento_id = movimiento.id
                                asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                asientodetalle.activo=True
                                asientodetalle.anulado=False
                                asientodetalle.updated_by = request.user.get_full_name()
                                asientodetalle.created_by = request.user.get_full_name()
                                asientodetalle.created_at = datetime.now()
                                asientodetalle.updated_at = datetime.now()
                                asientodetalle.save()
                            
                        
                    else:
                        fact=request.POST["facturas_kits" + str(i)]
                        if fact!='0':
                            asientodetalle = DocumentoAbono()
                            asientodetalle.movimiento_id = movimiento.id
                            asientodetalle.abono = request.POST["monto_kits" + str(i)]
                            asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                            asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                            asientodetalle.activo=True
                            asientodetalle.anulado=False
                            asientodetalle.updated_by = request.user.get_full_name()
                            asientodetalle.created_by = request.user.get_full_name()
                            asientodetalle.created_at = datetime.now()
                            asientodetalle.updated_at = datetime.now()
                            asientodetalle.save()
                                

              

        return HttpResponseRedirect('/contabilidad/asiento_factura_libro_list')
       

        
    else:
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(instance=asiento)
        detalle = AsientoDetalle.objects.filter(asiento=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        facturas= DocumentoCompra.objects.exclude(nota_credito=True).exclude(anulado=True).order_by('-fecha_emision')
        try:
            movimiento = Movimiento.objects.filter(asiento_id=pk).last()
        except Movimiento.DoesNotExist:
            movimiento = None
        print movimiento
        if movimiento:
            proveedor_id=movimiento.proveedor_id
        else:
            proveedor_id ='0'
       
        
        cursor = connection.cursor()
        facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        # if proveedor_id == '0':
        #     facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        # else:
        #     facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True and dc.proveedor_id='+str(proveedor_id)+' GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        cursor.execute(facturas_sql)
        ro = cursor.fetchall()
        
        
        detalle_sql='select dc.* from documento_abono dc, contabilidad_asiento a,movimiento m where a.asiento_id=m.asiento_id and m.id=dc.movimiento_id and a.asiento_id=' + (pk) +';'
        cursor.execute(detalle_sql)
        detallefactura= cursor.fetchall()
        
        
        facturas2_sql='select f.id,f.establecimiento,f.punto_emision,f.secuencial,f.descripcion from documento_abono dc,documento_compra f, movimiento m where m.id=dc.movimiento_id and f.id=dc.documento_compra_id and m.asiento_id=' + (pk) +';'
        cursor.execute(facturas2_sql)
        ro2 = cursor.fetchall()
        
        
        
        abono_sql='select f.proveedor_id,f.nombre_proveedor,dc.abono,m.numero_comprobante from documento_abono dc, movimiento m,proveedor f where m.id=dc.movimiento_id and f.proveedor_id=dc.proveedor_id  and dc.activo is not False and dc.anulado is not True and m.asiento_id=' + (pk) +';'
        cursor.execute(abono_sql)
        ro_abono = cursor.fetchall()
        
        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'asiento_form': asiento_form,
            'facturas': facturas,
            'cuentas': cuentas,
            'centros': centros,
            'facturas_sql': ro,
            'detallefactura':detallefactura,
            'movimiento': movimiento,
            'facturas_sql2': ro2,
            'detalle': detalle,
            'abonos': ro_abono,
            'centros_defecto':centros_defecto,
            }
        
        
        return render_to_response(
            'asiento/asientoFaturasLibroDiario.html',
            context,
            context_instance=RequestContext(request))





@login_required()
def asiento_factura_libro_list(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,a.modulo,m.proveedor_id,m.descripcion,m.paguese_a,td.descripcion,m.id,m.activo,m.monto,periodos from contabilidad_asiento a,movimiento m,tipo_documento td, (SELECT b.id as periodos,p.asiento_id FROM contabilidad_asiento  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha)) G  where G.asiento_id= a.asiento_id and m.asiento_id=a.asiento_id and m.tipo_anticipo_id=1 and td.id=m.tipo_documento_id and m.tipo_documento_id=10"
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('asiento/asientoFacturaLibroDiarioList.html', {'asientos': ro},
                                  RequestContext(request))
    else:
        cursor = connection.cursor()
        query = "select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,a.modulo,m.proveedor_id,m.descripcion,m.paguese_a,td.descripcion,m.id,m.activo,m.monto,periodos from contabilidad_asiento a,movimiento m,tipo_documento td, (SELECT b.id as periodos,p.asiento_id FROM contabilidad_asiento  p LEFT JOIN bloqueo_periodo b on  date_part('year',b.fecha)=EXTRACT(YEAR FROM p.fecha) and date_part('month',b.fecha)=EXTRACT(MONTH from p.fecha)) G  where G.asiento_id= a.asiento_id and m.asiento_id=a.asiento_id and m.tipo_anticipo_id=1 and td.id=m.tipo_documento_id and m.tipo_documento_id=10"
        cursor.execute(query)
        ro = cursor.fetchall()
        return render_to_response('asiento/asientoFacturaLibroDiarioList.html', {'asientos': ro},
                                  RequestContext(request))
    
    
def asientoRelacionarFacturasLibroDiarioCreateView(request):
    if request.method == 'POST':
        asiento_form = AsientoForm(request.POST)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.filter(activo=True)
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        now=datetime.now()
        if asiento_form.is_valid():
            with transaction.atomic():
                
                asiento = asiento_form.save()
                asiento.created_by = request.user.get_full_name()
                asiento.updated_by = request.user.get_full_name()
                asiento.created_at = datetime.now()
                asiento.updated_at = datetime.now()

                asiento.save()
                codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                #asiento.codigo_asiento = "LD-DB"+str(now.year)+"000"+str(codigo_asiento)
                #asiento.fecha = now
                asiento.gasto_no_deducible = False
                asiento.secuencia_asiento = codigo_asiento
                total_debe=request.POST['total_debe']
                total_haber=request.POST['total_haber']
                asiento.total_debe = total_debe
                asiento.total_haber = total_haber
                asiento.modulo='Libro Diario'
                asiento.save()
                Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                movimiento= Movimiento()
                movimiento.asiento_id=asiento.asiento_id
                movimiento.proveedor_id=request.POST["persona_id"]
                movimiento.tipo_anticipo_id=1
                movimiento.tipo_documento_id=10
                movimiento.fecha_emision = asiento.fecha
                movimiento.paguese_a = request.POST['paguese_a'] 
                movimiento.descripcion = request.POST['descripcion']
                movimiento.monto =  total_haber
                movimiento.updated_by = request.user.get_full_name()
                movimiento.created_by = request.user.get_full_name()
                movimiento.created_at = datetime.now()
                movimiento.updated_at = datetime.now()
                movimiento.save()
                movimiento.numero_comprobante = 'DB'+str(now.year)+'000'+str(movimiento.id)
                movimiento.save()
                asiento.glosa = 'MOVIMIENTO LIBRO DIARIO-DARBAJA - ' + movimiento.numero_comprobante
                asiento.save()
            
                contador2 = request.POST["columnas_receta"]
                i = 0
                while int(i) < int(contador2):
                    i += 1
                    if 'id_cuenta_kits' + str(i) in request.POST:
                        asientodetalle = AsientoDetalle()
                        asientodetalle.asiento = asiento
                        asientodetalle.cuenta = PlanDeCuentas.objects.get(
                        pk=request.POST["id_cuenta_kits" + str(i)])
    
                        if request.POST["id_centro_kits" + str(i)] != '0':
                            try:
                                c_cost = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
    
                            except CentroCosto.DoesNotExist:
                                c_cost = None
                            if c_cost:
                                asientodetalle.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                        asientodetalle.debe = request.POST["debe_kits" + str(i)]
                        asientodetalle.haber = request.POST["haber_kits" + str(i)]
                        asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                        asientodetalle.save()
                    
                    

                contador = request.POST["columnas_recetaf"]
                i = 0
                while int(i) < int(contador):
                    i += 1
                    if 'facturas_kits' + str(i) in request.POST:
                        
                        if 'id_detallef' + str(i) in request.POST:
                            id_detall=request.POST["id_detallef" + str(i)]
                            if id_detall:
                                print "ID detalle"
                                print id_detall
                                asientodetalle=DocumentoAbono.objects.get(id=id_detall)
                                asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                asientodetalle.activo=True
                                asientodetalle.anulado=False
                                asientodetalle.updated_by = request.user.get_full_name()
                                asientodetalle.updated_at = datetime.now()
                                asientodetalle.save()
                            else:
                                fact=request.POST["facturas_kits" + str(i)]
                                if fact!='0':
                                    asientodetalle = DocumentoAbono()
                                    asientodetalle.movimiento_id = movimiento.id
                                    asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                    asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                    asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                    asientodetalle.activo=True
                                    asientodetalle.anulado=False
                                    asientodetalle.updated_by = request.user.get_full_name()
                                    asientodetalle.created_by = request.user.get_full_name()
                                    asientodetalle.created_at = datetime.now()
                                    asientodetalle.updated_at = datetime.now()
                                    asientodetalle.save()
                                
                            
                        else:
                            fact=request.POST["facturas_kits" + str(i)]
                            if fact!='0':
                                asientodetalle = DocumentoAbono()
                                asientodetalle.movimiento_id = movimiento.id
                                asientodetalle.abono = request.POST["monto_kits" + str(i)]
                                asientodetalle.observacion = request.POST["observacion_kits" + str(i)]
                                asientodetalle.documento_compra_id = request.POST["facturas_kits" + str(i)]
                                asientodetalle.activo=True
                                asientodetalle.anulado=False
                                asientodetalle.updated_by = request.user.get_full_name()
                                asientodetalle.created_by = request.user.get_full_name()
                                asientodetalle.created_at = datetime.now()
                                asientodetalle.updated_at = datetime.now()
                                asientodetalle.save()
                               
        else:
            print 'error'
            print asiento_form.errors, len(asiento_form.errors)
                                        
                    
    

        
            
        
        return HttpResponseRedirect('/contabilidad/asiento_factura_libro_list')
    else:
        asiento_form = AsientoForm
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()
        facturas= DocumentoCompra.objects.exclude(nota_credito=True).exclude(anulado=True).order_by('-fecha_emision')
        proveedores = Proveedor.objects.all()
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        cursor = connection.cursor()
        facturas_sql='select dc.id, to_char(dc.fecha_emision, \'DD/MM/YYYY\') as fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,SUM(da.abono),dc.punto_emision,dc.secuencial,dc.descripcion,dc.valor_retenido,dc.total_pagar ,SUM(m.total) as nc from documento_compra dc LEFT JOIN documento_abono da  ON (da.documento_compra_id = dc.id)  and da.anulado is not True  LEFT JOIN movimiento_nota_credito m  ON (m.documento_compra_id = dc.id) AND m.anulado is not True where  dc.anulado is not True GROUP BY dc.id, dc.fecha_emision, dc.establecimiento, dc.base_iva, dc.valor_iva, dc.total,dc.valor_retenido,dc.total_pagar;'
        cursor.execute(facturas_sql)
        ro = cursor.fetchall()
        
        #detalle_sql='select dc.* from documento_abono dc, contabilidad_asiento a,movimiento m where a.asiento_id=m.asiento_id and m.id=dc.movimiento_id and a.asiento_id=' + (pk) +';'
        #cursor.execute(detalle_sql)
        #detallefactura= cursor.fetchall()
        
        
        
        
        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'asiento_form': asiento_form,
            'facturas': facturas,
            'cuentas': cuentas,
            'centros': centros,
            'facturas_sql': ro,
            'proveedores': proveedores,
            'centros_defecto':centros_defecto,

            }
        
        
        return render_to_response(
            'asiento/asientoFacturaLibroDiarioCreate.html',
            context,
            context_instance=RequestContext(request))

    

@login_required()
def imprimir_asiento_baja(request,pk):
    

    try:
        asientos = Asiento.objects.get(asiento_id=pk)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=pk)
    except AsientoDetalle.DoesNotExist:
        detalle = None
    
    
    try:
        movimiento = Movimiento.objects.filter(asiento_id=pk).last()
    except Movimiento.DoesNotExist:
        movimiento = None
        print movimiento


    #html = render_to_string('movimientos/imprimir_orden_egreso.html', {'pagesize':'A4','movimiento':movimiento,'detalle':detalle,'asiento':asientos}, context_instance=RequestContext(request))
    #return generar_pdf(html)
    html = loader.get_template('asiento/imprimir_asiento_baja.html')
    context = RequestContext(request, {'movimiento':movimiento,'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))



@login_required()
def asientoMovimientoEliminarByPkView(request, pk):
    obj = Movimiento.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()
        try:
            abonos = DocumentoAbono.objects.filter(movimiento_id=obj.id)
        except DocumentoAbono.DoesNotExist:
            abonos = None
        if abonos:
            for a in abonos:
                a.anulado= True
                a.save()
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.updated_by = request.user.get_full_name()
                a.updated_at = datetime.now()
                a.save()

    return HttpResponseRedirect('/contabilidad/asiento_factura_libro_list/')



@login_required()
def MayoresContablesActualView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    centro_costos = CentroCosto.objects.filter(activo=True).order_by('codigo')
    return render_to_response('registrar_libro_diario/mayores_contables_actual.html',
                              RequestContext(request, {'cuentas': plan_ctas,'centro_costos':centro_costos}))


@login_required()
def ConsultaMayorActualView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        cuenta_hasta = request.POST['inputCuentaHasta']
        centroCosto = request.POST['centro_costo']
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        
        cursor.execute('select nombre_plan, codigo_plan,plan_id '
            'from contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta '
            'where cuenta.tipo_cuenta_id = tcuenta.tipo_id '
            'and cuenta.codigo_plan::float>=%s '
            'and  cuenta.codigo_plan::float<=%s '
            'GROUP BY nombre_plan, codigo_plan,plan_id order by codigo_plan ', (float(cuenta_cod_desde.codigo_plan),float(cuenta_cod_hasta.codigo_plan)))
        rop_actual = cursor.fetchall()
        html=''
        html+='<table class="table table-bordered table-asiento" id="estado_cuentas">'
        html+='<thead style="background-color: #EEEEEE"><tr><td colspan="9"><b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</td></tr><tr><th style="text-align: center"><b>Cuenta</b></th><th style="text-align: center"><b>Fecha</b></th><th style="text-align: center"><b>Asiento</b></th><th style="text-align: center"><b>Glosa</b></th><th style="text-align: center"><b>Debe</b></th><th style="text-align: center"><b>Haber</b></th><th style="text-align: center"><b>Saldo</b></th><th style="text-align: center"><b>Concepto</b></th>'
        if centroCosto != "0":
            html+='<th style="text-align: center"><b>Centro de Costo</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        for co in rop_actual:
            
            html+='<tr><td colspan="9"><b>CODIGO: '+str(co[1].encode('utf8'))+' '+str(co[0].encode('utf8'))+'</td><tr>'
            total_debito=0
            total_haber=0
            #date = datetime.strptime(fecha_hasta, "%d/%m/%y").date()
            fec=fecha_hasta.split("/")
            anio_anterior=int(fec[2])-1
            #print 'anio anterior'
            #print anio_anterior
            #print co[1]
            fecha_inicial_consulta=datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
            #print fecha_inicial_consulta
            try:
                pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(co[2]))
                #print "entro2"
            except PeriodoAnterior.DoesNotExist:
                pb = None
                #print "no entro"

            #Aqui nuevo codigo
            fecini = fecha_desde.split("/")
            vdia = fecini[0]
            vmes = fecini[1]
            vano = fecini[2]
            saldo=0
            Cadena = co[1]
            Cadena = Cadena[0:1]
            SecCuenta = int(Cadena)
            # SecCuenta < 4 and
            if (vdia == "01" and vmes == "01") and SecCuenta > 3:
                saldo_inicial = 0
            else:

                sql2="select nombre_plan, codigo_plan,plan_id,sum(ad.debe),sum(ad.haber) from contabilidad_plandecuentas as cuenta,contabilidad_asiento a,contabilidad_asientodetalle ad where a.asiento_id=ad.asiento_id and a.anulado is not True and ad.cuenta_id=cuenta.plan_id"
                sql2+=" and cuenta.plan_id= "+str(co[2])
                if SecCuenta > 3:
                    sql2+=" and a.fecha >= '" + vano + "-01-01' "

                sql2+= " and a.fecha < '"+str(fecha_inicial_consulta)+"'  GROUP BY nombre_plan, codigo_plan,plan_id"
                #print sql2
                x = co[1]
                cursor.execute(sql2)
                rop_saldo_anterior = cursor.fetchall()
                # if pb:
                #     saldo_inicial=pb[0].saldo
                #     saldo = saldo + saldo_inicial
                # else:
                #     saldo_inicial=0
                if rop_saldo_anterior:
                    if rop_saldo_anterior[0][3]:
                        debito_a=float(rop_saldo_anterior[0][3])
                    else:
                        debito_a=0
                
                    if rop_saldo_anterior[0][4]:
                        haber_a=float(rop_saldo_anterior[0][4])
                    else:
                        haber_a=0
                
                    #saldo_inicial=pb[0].saldo
                    saldo_inicial=debito_a-haber_a
                    saldo = saldo + saldo_inicial
                else:
                    saldo_inicial=0

                
            html+='<tr><td>SALDO ANTERIOR</td><td></td><td></td><td></td>'
            #html+='<td align="right">' + str("%2.2f" % saldo_inicial).replace('.', ',') + '</td>'
            html+='<td align="right">0</td>'
            html+='<td align="right">0</td>'
            html+='<td align="right">'+str("%2.2f" % saldo).replace('.', ',')+'</td><td align="right"></td><td align="right"></td> </tr>'
            total_debito=total_debito+float(saldo_inicial)
            if centroCosto != "0":
                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto,nombre_centro '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and cuenta.codigo_plan=%s '            
                    'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
                    'and adetalle.centro_costo_id=%s '  
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (str(co[1]), fecha_desde, fecha_hasta,centroCosto))
            else:
                
                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and cuenta.codigo_plan=%s '            
                    'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (str(co[1]), fecha_desde, fecha_hasta))
    
            ro = cursor.fetchall()
            print ro
                
                
            
            for cuentas in ro:
                saldo = saldo + float(cuentas[5])
                concepto=""
                if cuentas[8]:
                    concepto=cuentas[8]
                if cuentas[3]==0 and cuentas[4]==0:
                    print "cuenta vacia"
                else:
                    html+='<tr><td>' + str(cuentas[7].encode('utf8'))+ '-' + str(cuentas[6].encode('utf8')) + '</td><td>' + str(cuentas[1]) + '</td><td>' + str(cuentas[0]) + '</td><td>' + str(cuentas[2].encode('utf8')) + '</td>'
                    html+='<td align="right">' + str("%2.2f" % cuentas[3]).replace('.', ',')+ '</td>'
                    html+='<td align="right">' +  str("%2.2f" % cuentas[4]).replace('.', ',')+'</td>'
                    html+='<td align="right"><b>' +  str("%2.2f" % saldo).replace('.', ',') + '</b></td><td>' + str(concepto.encode('utf8')) + '</td>'
                    if centroCosto != "0":
                        try:
                            pb = CentroCosto.objects.filter(centro_id=centroCosto).first()
                            #print "entro2"
                        except CentroCosto.DoesNotExist:
                            pb = None
            
                        
                        if pb:
                            html+='<td>' + str(cuentas[9])+ '</td>'
                    else:
                         html+='<td></td>'
                    html+='</tr>'
                    total_debito=total_debito+float(cuentas[3])
                    total_haber=total_haber+float(cuentas[4])
            html+='<tr><td colspan="4"><b>Total</b></td><td><b>'+str("%2.2f" % total_debito).replace('.', ',')+'</b></td><td><b>'+str("%2.2f" % total_haber).replace('.', ',')+'</b></td><td><b>'+str("%2.2f" % saldo).replace('.', ',')+'</b></td><td></td><td></td></tr>'
    
                    
            
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
    
@csrf_exempt
def consultar_balance_diario(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']

        cursor = connection.cursor()
        sql="select distinct cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel, "
        sql+=" case when tcuenta.acreedora = 't' then 'f' else case when tcuenta.deudora = 't' then 't' else 'f' end end naturaleza "
        sql+=" from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=2 or cuenta.tipo_cuenta_id=3 or cuenta.tipo_cuenta_id=4) and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)

        ro = cursor.fetchall()
        print sql
        date = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
        anio_anterior=int(date.year)-1
        html = '<table id="tabla" class="table2 table-striped " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="5" style="text-align:center  !important"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>ESTADO DE SITUACION FINANCIERA  </b><br>'
        #html+='<b>AL 31 DE DICIEMBRE DE '+str(date.year)+' Y '+str(anio_anterior)+'</b> <br>'
        html+='(Expresado en d&oacute;lares de E.U.A.)</td></tr>'
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3">AL '+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th><th>SALDO ANTERIOR</th><th>SALDO PERIODO</th>'
        html+='<th>SALDO ACTUAL</th>'
        if centroCosto != "0":
            html+='<th>CENTRO DE COSTO</th>'
        
        html+='</tr></thead>'
        html+='<tbody>'
        total_pasivo=0
        total_patri=0
        total_pasivo0=0
        total_patri0=0
        
        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left  !important"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right  !important">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left  !important">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'

            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            natcuenta = p[6]
            #print anio_anterior
            try:
                # Obtener saldo anterior mediante SQL similar al saldo actual
                saldo_anterior = 0
                cursor = connection.cursor()
                sql_anterior = "select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "

                if fecha_desde:
                    sql_anterior += " and a.fecha<'" + str(fecha_desde) + "' "

                sql_anterior += "and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '" + str(
                    p[1]) + "%'  and a.anulado is not True"
                if centroCosto != "0":
                    sql_anterior += " and (ad.centro_costo_id=" + str(
                        centroCosto) + " or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id=" + str(
                        centroCosto) + "))"

                # print sqlr3
                cursor.execute(sql_anterior);
                row_anterior = cursor.fetchall()
                t_debe_anterior = 0
                t_habe_anterior = 0
                for row in row_anterior:
                    if row[0]:
                        t_debe_anterior = t_debe_anterior + row[0]
                    if row[1]:
                        t_habe_anterior = t_habe_anterior + row[1]

                    if natcuenta == 't':
                        saldo_anterior = t_debe_anterior - t_habe_anterior
                    else:
                        saldo_anterior = t_habe_anterior - t_debe_anterior

                #pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(p[0]))
                #print "entro2"

                #Obtenemos la Utilidad del periodo anterior
                saldo_utilidad = 0
                if p[1] == '310103002' or p[1] == '310103' or p[1] == '3101' or p[1] == '31' or p[1] == '3':
                    cursor = connection.cursor()
                    sql_utianterior = "select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "

                    if fecha_desde:
                        sql_utianterior += " and a.fecha<'" + str(fecha_desde) + "' "

                        sql_utianterior += "and ad.cuenta_id=cpc.plan_id and (cpc.codigo_plan like '4%' or cpc.codigo_plan like '5%' or cpc.codigo_plan like '6%') and a.anulado is not True"
                    if centroCosto != "0":
                        sql_utianterior += " and (ad.centro_costo_id=" + str(
                            centroCosto) + " or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id=" + str(
                            centroCosto) + "))"
                    cursor.execute(sql_utianterior);
                    row_utianterior = cursor.fetchall()

                    t_debe_utianterior = 0
                    t_habe_utianterior = 0

                    for rowu in row_utianterior:
                        if rowu[0]:
                            t_debe_utianterior = t_debe_utianterior + rowu[0]
                        if rowu[1]:
                            t_habe_utianterior = t_habe_utianterior + rowu[1]

                    #Utilidad del Ejercicio Anterior
                    saldo_utilidad = t_habe_utianterior - t_debe_utianterior

                    #Cuentas de Resultados
                    if p[1] != '310103002':
                        cursor = connection.cursor()

                        sqlrcta = "select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                        if fecha_desde:
                            sqlrcta += " and a.fecha<'" + str(fecha_desde) + "'"

                        sqlrcta += "and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '" + str(p[1]) + "%'  and a.anulado is not True"
                        if centroCosto != "0":
                            sqlrcta += " and (ad.centro_costo_id=" + str(
                                centroCosto) + " or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id=" + str(
                                centroCosto) + "))"

                        cursor.execute(sqlrcta);
                        rowrcta = cursor.fetchall()
                        cta_total_debe = 0
                        cta_total_haber = 0
                        cta_total_saldo = 0
                        for prcta in rowrcta:
                            if prcta[0]:
                                cta_total_debe = cta_total_debe + prcta[0]
                            if prcta[1]:
                                cta_total_haber = cta_total_haber + prcta[1]

                        cta_total_saldo = cta_total_haber - cta_total_debe + saldo_utilidad
                        saldo_anterior = cta_total_saldo
                    else:
                        saldo_anterior = saldo_utilidad

            except PeriodoAnterior.DoesNotExist:
                pb = None

            
            # if pb:
            #     saldo_anterior=pb[0].saldo
            # else:
            #     saldo_anterior=0
            
            html+='<td style="text-align:right  !important">'+str("%0.2f" % saldo_anterior).replace('.', ',') +' </td>'

            
            if p[0]:
                
                saldo_periodo=0
                cursor = connection.cursor()
                sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                if fecha_desde:
                    sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                if fecha_hasta:
                    sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "

                sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                if centroCosto != "0":
                    sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                #print sqlr3
                cursor.execute(sqlr3);
                rowr3 = cursor.fetchall()
                total_debe=0
                total_haber=0
                for pr2 in rowr3:
                    if pr2[0]:
                        total_debe=total_debe+pr2[0]
                    if pr2[1]:
                        total_haber=total_haber+pr2[1]

                if natcuenta == 't':
                    saldo_periodo = total_debe - total_haber
                else:
                    saldo_periodo = total_haber - total_debe

                #Codigo Original
                #saldo_periodo=total_debe-total_haber
                mult=float('-1.0')

                #Nuevo Codigo


                #Codigo Original
                #if p[3]==5 and total_debe>total_haber and saldo_periodo>0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                #if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                #if p[3]==3 and total_debe>total_haber and saldo_periodo>0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                #if p[3]==3 and total_haber>total_debe and saldo_periodo<0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                #if p[3]==4 and total_debe>total_haber and saldo_periodo>0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                #if p[3]==4 and total_haber>total_debe and saldo_periodo<0:
                #    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                if p[1]=='310103002' or p[1]=='310103' or p[1]=='3101' or p[1]=='31' or p[1]=='3' :
                    cursor = connection.cursor()
                    sql="select distinct  cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
                    if cuenta != "Todas":
                        sql+=" and cuenta.nombre_plan='"+cuenta+"'"
                    if inputTipo != "0":
                        sql+=" and cuenta.tipo_cuenta_id="+inputTipo
                    #if nivel != "":
                    #    sql+=" and cuenta.nivel="+nivel
                    sql += " and cuenta.nivel=0" #+ nivel
                    sql+=" ORDER BY codigo_plan"
                    cursor.execute(sql)
                    ro = cursor.fetchall()
                    date = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
                    anio_anterior=int(date.year)-1
                    ingresos=0
                    egresos=0

                    #Saldo Anterior
                    for pr in ro:
                        
                        saldo_anterior1=0
                        saldo_periodo1=0
                        saldo_actual1=0
                        
                        #print anio_anterior
                        #Comentamos
                        #try:
                        #    pb1 = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(pr[0]))
                        #    #print "entro2"
                        #except PeriodoAnterior.DoesNotExist:
                        #    pb1 = None

                        #if pb1:
                        #    saldo_anterior1=pb1[0].saldo
                        #else:
                        #    saldo_anterior1=0

                        saldo_anterior1=0

                        #Saldo Mes Actual
                        if pr[0]:
                            
                            saldo_periodo1=0
                            cursor = connection.cursor()
                            
                            sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                            if fecha_desde:
                                sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                            if fecha_hasta:
                                sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "
                            
                            #sqlr3+=" and ad.cuenta_id="+ str(p[0])+"  and a.anulado is not True group by ad.cuenta_id"
                            sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(pr[1])+"%'  and a.anulado is not True"
                            if centroCosto != "0":
                                sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                            
                            #print sqlr3
                            cursor.execute(sqlr3)
                            rowr3 = cursor.fetchall()
                            total_debe1=0
                            total_haber1=0
                            for prb2 in rowr3:
                                if prb2[0]:
                                    total_debe1=total_debe1+prb2[0]
                                if prb2[1]:
                                    total_haber1=total_haber1+prb2[1]
                            saldo_periodo1=total_debe1-total_haber1
                            mult1=float('-1.0')
                            if pr[3]==5 and saldo_periodo1<0:           #pasa
                                saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)
                                
                            saldo_actual1=float(saldo_periodo1)+float(saldo_anterior1)

                            #if pr[6] == '0' and pr[3] == 5:
                            if pr[3] == 5:
                                ingresos=ingresos+saldo_periodo1

                            #if pr[6] == '0' and pr[3] != 5:
                            if pr[3]!=5:
                                egresos=egresos+saldo_periodo1
                                
                    total_ejercicio=ingresos-egresos
                    saldo_periodo=saldo_periodo+total_ejercicio

                html+='<td style="text-align:right  !important">'+str("%0.2f" % saldo_periodo).replace('.', ',')+'</td>'
                #if anio_anterior == '2016' or anio_anterior == 2016:
                #    saldo_actual=float(saldo_periodo)
                #else:
                saldo_actual=float(saldo_periodo)+float(saldo_anterior)

                html+='<td style="text-align:right  !important">'+str("%0.2f" % saldo_actual).replace('.', ',') +'</td>'
                if p[1]=='2':
                    total_pasivo=saldo_actual
                    total_pasivo0=saldo_periodo
                if p[1]=='3':
                    total_patri=saldo_actual
                    total_patri0=saldo_periodo
                if centroCosto != "0":
                    try:
                        pb = CentroCosto.objects.filter(centro_id=centroCosto).first()
                        #print "entro2"
                    except CentroCosto.DoesNotExist:
                        pb = None
        
                    
                    if pb:
                        html+='<td style="text-align:right  !important">'+str(pb.nombre_centro) +'</td>'
                    
            else:
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                if centroCosto != "0":
                    html += '<td></td>'
            html+='</tr>'
        total_f=total_pasivo+total_patri
        total_f0=total_pasivo0+total_patri0
        html+='<tr style="border:1px solid black  !important" ><td colspan="3"><b>TOTAL PASIVO + PATRIMONIO</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_f0).replace('.', ',') +'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_f).replace('.', ',') +'</b></td>'
        html+='</tr>'
            
            
        return HttpResponse(
            html
        )

    else:
        raise Http404


@login_required()
def estadoResultadoView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True, tipo_cuenta_id__in=[1, 5, 6,8]).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/estados_resultados.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))



@csrf_exempt
def consultar_estados_resultados(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']

        cursor = connection.cursor()
        sql="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)



        
        ro = cursor.fetchall()
        date = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
        anio_anterior=int(date.year)-1
        ingresos=0
        egresos=0
        print sql
        #html = '<table id="tabla" class="table2 table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead>'
        html = '<table id="tabla" class="table2 " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="5" style="text-align:center"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>ESTADOS DEL RESULTADO INTEGRAL </b><br>'
        #html+='<b>AL 31 DE DICIEMBRE DE '+str(date.year)+' Y '+str(anio_anterior)+'</b> <br>'
        html+='(Expresado en d&oacute;lares de E.U.A.)</td></tr>'
        html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3"><b>DESDE</b> '+str(fecha_desde)+'<br /><b>HASTA</b> '+str(fecha_hasta)+'</td></tr>'
        
        
        
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th><th>SALDO ANTERIOR</th><th>SALDO PERIODO</th>'
        html+='<th>SALDO ACTUAL</th>'
        if centroCosto != "0":
            html+='<th>CENTRO DE COSTO</th>'
        
        html+='</tr></thead>'
        html+='<tbody>'
        
        
        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
            
                
            
            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            
            #print anio_anterior
            try:
                pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(p[0]))
                #print "entro2"
            except PeriodoAnterior.DoesNotExist:
                pb = None

            
            if pb:
                saldo_anterior=pb[0].saldo
            else:
                saldo_anterior=0
            
            saldo_anterior=0
            #html+='<td style="text-align:right">'+str("%0.2f" % saldo_anterior).replace('.', ',') +'</td>'
            html+='<td style="text-align:right"></td>'
                
            
                    
            
            if p[0]:
                
                saldo_periodo=0
                cursor = connection.cursor()
                    
                sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                if fecha_desde:
                    sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                if fecha_hasta:
                    sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "
                
                
                sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                if centroCosto != "0":
                    sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                
                #print sqlr3
                cursor.execute(sqlr3);
                rowr3 = cursor.fetchall()
                total_debe=0
                total_haber=0
                for pr2 in rowr3:
                    if pr2[0]:
                        total_debe=total_debe+pr2[0]
                    if pr2[1]:
                        total_haber=total_haber+pr2[1]
                saldo_periodo=total_debe-total_haber
                mult=float('-1.0')
                if p[3]==5 and total_haber<total_debe and saldo_periodo>0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo).replace('.', ',')+'</td>'
                saldo_actual=float(saldo_periodo)+float(saldo_anterior)
                html+='<td style="text-align:right">'+str("%0.2f" % saldo_actual).replace('.', ',') +'</td>'
                #html+='<td>-'+str(p[3])+'</td>'
                if p[6] == '0' and p[3] == 5:
                    ingresos=ingresos+saldo_periodo
                    print "entro a ingresos"
                    print ingresos
                    
                if p[6]=='0' and p[3]!=5:
                    egresos=egresos+saldo_periodo
                    print "entro a egresos"
                    print egresos
                    
                if centroCosto != "0":
                    try:
                        pb = CentroCosto.objects.filter(centro_id=centroCosto).first()
                        #print "entro2"
                    except CentroCosto.DoesNotExist:
                        pb = None
        
                    
                    if pb:
                        html+='<td style="text-align:right  !important">'+str(pb.nombre_centro) +'</td>'
            else:
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                if centroCosto != "0":
                    html+='<td></td>'
            html+='</tr>'
        total_ejercicio=ingresos-egresos
        html+='<tr style="border:1px solid black" ><td colspan="3"><b>RESULTADO DEL EJERCICIO</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_ejercicio).replace('.', ',') +'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_ejercicio).replace('.', ',') +'</b></td>'
        html+='</tr>'
        
        
        
        cursor = connection.cursor()
        sql2="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and  cuenta.codigo_plan like '310104%' and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql2+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql2+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql2+=" and cuenta.nivel<="+nivel
        
        sql2+=" ORDER BY codigo_plan"
        cursor.execute(sql2)
        ro2 = cursor.fetchall()
        saldo_total1=0
        for p1 in ro2:
            html+='<tr>'
            if p1[5]==0 or p1[5]==1 or p1[5]==2 :
                if p1[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p1[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p1[2]:
                    html += '<td style="text-align:left"><b>' + str(p1[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p1[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p1[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p1[2]:
                    html += '<td style="text-align:left">' + str(p1[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
            
                
            
            saldo_anterior1=0
            saldo_periodo1=0
            saldo_actual1=0
            
            #print anio_anterior
            try:
                pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(p1[0]))
                #print "entro2"
            except PeriodoAnterior.DoesNotExist:
                pb = None

            
            if pb:
                saldo_anterior1=pb[0].saldo
            else:
                saldo_anterior1=0
            
            saldo_anterior1=0
            #html+='<td style="text-align:right">'+str("%0.2f" % saldo_anterior).replace('.', ',') +'</td>'
            html+='<td style="text-align:right"></td>'
                
            
                    
            
            if p1[0]:
                
                saldo_periodo1=0
                cursor = connection.cursor()
                    
                sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                if fecha_desde:
                    sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                if fecha_hasta:
                    sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "
                
                
                sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p1[1])+"%'  and a.anulado is not True"
                if centroCosto != "0":
                    sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                
                #print sqlr3
                cursor.execute(sqlr3);
                rowr3 = cursor.fetchall()
                total_debe=0
                total_haber=0
                for pr2 in rowr3:
                    if pr2[0]:
                        total_debe=total_debe+pr2[0]
                    if pr2[1]:
                        total_haber=total_haber+pr2[1]
                saldo_periodo1=total_debe-total_haber
                mult=float('-1.0')
                if p[3]==5 and total_haber<total_debe and saldo_periodo1>0:
                    saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult)
                    
                if p[3]==5 and total_haber>total_debe and saldo_periodo1<0:
                    saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult)
                    
                html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo1).replace('.', ',')+'</td>'
                saldo_actual1=float(saldo_periodo1)+float(saldo_anterior1)
                html+='<td style="text-align:right">'+str("%0.2f" % saldo_actual1).replace('.', ',') +'</td>'
                #html+='<td>-'+str(p[3])+'</td>'
                saldo_total1=Decimal(saldo_total1)+Decimal(saldo_actual1)
                if p[6] == '0' and p[3] == 5:
                    ingresos=ingresos+saldo_periodo1
                    
                    
                if p[6]=='0' and p[3]!=5:
                    egresos=egresos+saldo_periodo1
                
                if centroCosto != "0":
                    try:
                        pb = CentroCosto.objects.filter(centro_id=centroCosto).first()
                        #print "entro2"
                    except CentroCosto.DoesNotExist:
                        pb = None
        
                    
                    if pb:
                        html+='<td style="text-align:right  !important">'+str(pb.nombre_centro) +'</td>'
                    
                    
                    
            else:
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                if centroCosto != "0":
                    html+='<td></td>'
            html+='</tr>'
        
     
        
        total_final1=Decimal(total_ejercicio)+Decimal(saldo_total1)
        html+='<tr style="border:1px solid black" ><td colspan="3"><b>RESULTADO INTEGRAL TOTAL</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_final1).replace('.', ',') +'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_final1).replace('.', ',') +'</b></td>'
        html+='</tr>'    
            
        return HttpResponse(
            html
        )

    else:
        raise Http404



def AsientoConsultarView(request, pk):
    if request.method == 'POST':
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(request.POST, request.FILES, instance=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()

        print asiento_form.is_valid(), asiento_form.errors, type(asiento_form.errors)

        if asiento_form.is_valid():
            asiento = asiento_form.save()
            contador = request.POST["columnas_receta"]
            objetos = AsientoDetalle.objects.filter(asiento_id=pk)
            for obj in objetos:
                obj.delete()

            i = 0
            while int(i) < int(contador):
                i += 1
                if 'id_cuenta_kits' + str(i) in request.POST:
                    asientodetalle = AsientoDetalle()
                    asientodetalle.asiento = asiento
                    asientodetalle.cuenta = PlanDeCuentas.objects.get(
                    pk=request.POST["id_cuenta_kits" + str(i)])

                    if request.POST["id_centro_kits" + str(i)] != '0':
                        try:
                            c_cost = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])

                        except CentroCosto.DoesNotExist:
                            c_cost = None
                        if c_cost:
                            asientodetalle.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                    asientodetalle.debe = request.POST["debe_kits" + str(i)]
                    asientodetalle.haber = request.POST["haber_kits" + str(i)]
                    asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                    asientodetalle.save()
                # if 'id_detalle' + str(i) in request.POST:
                #     detalle_id = request.POST["id_detalle" + str(i)]
                #     detalle_asiento = AsientoDetalle.objects.get(detalle_id=detalle_id)
                #     detalle_asiento.cuenta = PlanDeCuentas.objects.get(pk=request.POST["id_cuenta_kits" + str(i)])
                #     if request.POST["id_centro_kits" + str(i)] != '0':
                #         detalle_asiento.centro_costo = CentroCosto.objects.get(pk=request.POST["id_centro_kits" + str(i)])
                #     detalle_asiento.debe = request.POST["debe_kits" + str(i)]
                #     detalle_asiento.haber = request.POST["haber_kits" + str(i)]
                #     detalle_asiento.concepto = request.POST["concepto_kits" + str(i)]
                #     detalle_asiento.save()
                #
                # else:
                #     asientodetalle = AsientoDetalle()
                #     asientodetalle.asiento = asiento
                #     asientodetalle.cuenta = PlanDeCuentas.objects.get(
                #         pk=request.POST["id_cuenta_kits" + str(i)])
                #     if request.POST["id_centro_kits" + str(i)] != '0':
                #         asientodetalle.centro_costo = CentroCosto.objects.get(
                #             pk=request.POST["id_centro_kits" + str(i)])
                #     asientodetalle.debe = request.POST["debe_kits" + str(i)]
                #     asientodetalle.haber = request.POST["haber_kits" + str(i)]
                #     asientodetalle.concepto = request.POST["concepto_kits" + str(i)]
                #     asientodetalle.save()


            return HttpResponseRedirect('/contabilidad/asiento')
        else:

            asiento_form = AsientoForm(request.POST)
            detalle = AsientoDetalle.objects.filter(asiento=asiento.asiento_id)

            context = {
                'section_title': 'Actualizar Asiento',
                'button_text': 'Actualizar',
                'asiento_form': asiento_form,
                'asiento': asiento,
                'cuentas': cuentas, 'centros': centros,
                'detalle': detalle}

        return render_to_response(
            'asiento/consultar.html',
            context,
            context_instance=RequestContext(request))
    else:
        asiento = Asiento.objects.get(asiento_id=pk)
        asiento_form = AsientoForm(instance=asiento)
        detalle = AsientoDetalle.objects.filter(asiento=asiento)
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        centros = CentroCosto.objects.all()

        context = {
            'section_title': 'Actualizar Asiento',
            'button_text': 'Actualizar',
            'asiento_form': asiento_form,
            'asiento': asiento,
            'cuentas': cuentas, 'centros': centros,
            'detalle': detalle}

        return render_to_response(
            'asiento/consultar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def imprimir_asiento(request,pk):
    

    try:
        asientos = Asiento.objects.get(asiento_id=pk)
    except Asiento.DoesNotExist:
        asientos = None

    try:
        detalle= AsientoDetalle.objects.filter(asiento_id=pk)
    except AsientoDetalle.DoesNotExist:
        detalle = None
    
    
    

    #html = render_to_string('movimientos/imprimir_orden_egreso.html', {'pagesize':'A4','movimiento':movimiento,'detalle':detalle,'asiento':asientos}, context_instance=RequestContext(request))
    #return generar_pdf(html)
    html = loader.get_template('asiento/imprimir_asiento.html')
    context = RequestContext(request, {'detalle':detalle,'asiento':asientos})
    return HttpResponse(html.render(context))

@login_required()
def asiento_eliminarView(request, pk):
    try:
        asiento = Asiento.objects.filter(asiento_id=pk)
    except Asiento.DoesNotExist:
        asiento = None
    if asiento:
        for a in asiento:
            a.anulado= True
            a.save()
    
        

    return HttpResponseRedirect('/contabilidad/asiento/')

@login_required()
def estadoSituacionFinancieraMensualizadoView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True, tipo_cuenta_id__in=[2, 3, 4]).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/balance_general_mensual.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))

@csrf_exempt
def consultar_balance_mensualizado(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']
        fecha_inicial=desde.split('-')
        fecha_final=hasta.split('-')
        mes_inicio=fecha_inicial[1]
        anio_inicio=fecha_inicial[0]
        mes_fin=fecha_final[1]
        anio_fin=fecha_final[0]
        

        cursor = connection.cursor()
        sql="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=2 or cuenta.tipo_cuenta_id=3 or cuenta.tipo_cuenta_id=4) and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)



        
        ro = cursor.fetchall()
        print sql
        date = datetime.strptime(fecha_hasta, "%Y-%m").date()
        anio_anterior=int(date.year)-1
        html = '<table id="tabla" class="table2 table-striped " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="5" style="text-align:center"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>ESTADO DE SITUACION FINANCIERA  </b><br>'
        #html+='<b>AL 31 DE DICIEMBRE DE '+str(date.year)+' Y '+str(anio_anterior)+'</b> <br>'
        html+='(Expresado en d&oacute;lares de E.U.A.)</td></tr>'
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3">DESDE '+str(fecha_desde)+' HASTA  '+str(fecha_hasta)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th>'
        
        indexm=int(mes_inicio)
        
        
        for indexm in range(int(indexm), 13):
                if indexm <= int(mes_fin):
                    x=indexm
                    if x == 1:
                        html+='<th>Enero</th>'
                    if x == 2:
                        html+='<th>Febrero</th>'
                    if x == 3:
                        html+='<th>Marzo</th>'
                    if x == 4:
                        html+='<th>Abril</th>'
                    if x == 5:
                        html+='<th>Mayo</th>'
                    if x == 6:
                        html+='<th>Junio</th>'
                    if x == 7:
                        html+='<th>Julio</th>'
                    if x == 8:
                        html+='<th>Agosto</th>'
                    if x == 9:
                        html+='<th>Septiembre</th>'
                    if x == 10:
                        html+='<th>Octubre</th>'
                    if x == 11:
                        html+='<th>Noviembre</th>'
                    if x == 12:
                        html+='<th>Diciembre</th>'
        
        #html+='<th>SALDO ACTUAL</th>'
        
        html+='</tr></thead>'
        html+='<tbody>'
        total_pasivo=0
        total_patri=0
        total_pasivo0=0
        total_patri0=0
        pasivo=[]
        patrimonio=[]
        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'

            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            index=mes_inicio
                   
            
            if p[0]:
                mes_fin1=int(mes_fin)+1

                sqlr3 = "select * from dbdctasc where codi_cta = '" + str(p[1]) + "' and tipcta = 'B' and anio_cta = " + str(anio_fin)

                dia_consulta = calendar.monthrange(int(anio_fin), int(index))[1]
                fecha_fin_mes = str(anio_fin) + "-" + str(index) + "-" + str(dia_consulta)
                cursor = connection.cursor()
                cursor.execute(sqlr3);
                rowr3 = cursor.fetchall()

                for pr2 in rowr3:
                    saldo_actual=pr2[4]

                for index in range(int(index),int(mes_fin1)):
                    
                    if index <= mes_fin:
                        saldo_periodo=0
                        if (index == 1):
                            saldo_periodo = pr2[7]
                        if (index == 2):
                            saldo_periodo = pr2[10]
                        if (index == 3):
                            saldo_periodo = pr2[13]
                        if (index == 4):
                            saldo_periodo = pr2[16]
                        if (index == 5):
                            saldo_periodo = pr2[19]
                        if (index == 6):
                            saldo_periodo = pr2[22]
                        if (index == 7):
                            saldo_periodo = pr2[25]
                        if (index == 8):
                            saldo_periodo = pr2[28]
                        if (index == 9):
                            saldo_periodo = pr2[31]
                        if (index == 10):
                            saldo_periodo = pr2[34]
                        if (index == 11):
                            saldo_periodo = pr2[37]
                        if (index == 12):
                            saldo_periodo = pr2[40]



                        # #sqlr3="select ad.cuenta_id,sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad where a.asiento_id=ad.asiento_id "
                        # sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                        # #sqlr3+=" and  date_part('year',a.fecha)<='"+str(anio_fin)+"' and date_part('month',a.fecha)<='"+str(index)+"'"
                        # sqlr3+=" and  a.fecha<='"+fecha_fin_mes+"'"
                        #
                        # sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                        # if centroCosto != "0":
                        #     sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                        #print sqlr3
                        # total_debe=0
                        # total_haber=0
                        # for pr2 in rowr3:
                        #     if pr2[0]:
                        #         total_debe=total_debe+pr2[0]
                        #     if pr2[1]:
                        #         total_haber=total_haber+pr2[1]
                        #
                        # saldo_periodo=total_debe-total_haber
                        # mult=float('-1.0')

                        # if p[3]==5 and total_debe>total_haber and saldo_periodo>0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==3 and total_debe>total_haber and saldo_periodo>0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==3 and total_haber>total_debe and saldo_periodo<0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==4 and total_debe>total_haber and saldo_periodo>0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==4 and total_haber>total_debe and saldo_periodo<0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)

                        # if p[1]=='310103002' or p[1]=='310103' or p[1]=='3101' or p[1]=='31' or p[1]=='3' :
                        #     cursor = connection.cursor()
                        #     sql="select distinct  cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
                        #     if cuenta != "Todas":
                        #         sql+=" and cuenta.nombre_plan='"+cuenta+"'"
                        #     if inputTipo != "0":
                        #         sql+=" and cuenta.tipo_cuenta_id="+inputTipo
                        #     if nivel != "":
                        #         sql+=" and cuenta.nivel="+nivel
                        #     sql+=" ORDER BY codigo_plan"
                        #     cursor.execute(sql)
                        #     ro = cursor.fetchall()
                           
                            # ingresos=0
                            # egresos=0

                            # for pr in ro:
                            #     saldo_anterior1=0
                            #     saldo_periodo1=0
                            #     saldo_actual1=0
                            #     saldo_anterior1=0
                            #     if pr[0]:
                            #         saldo_periodo1=0
                            #         cursor = connection.cursor()
                            #         sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                            #         #sqlr3+=" and  date_part('year',a.fecha)<='"+str(anio_fin)+"' and date_part('month',a.fecha)<='"+str(index)+"'"
                            #         sqlr3 += " and  a.fecha<='" + fecha_fin_mes + "'"
                            #         sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(pr[1])+"%'  and a.anulado is not True"
                            #         if centroCosto != "0":
                            #             sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                            #         #print sqlr3
                            #         cursor.execute(sqlr3);
                            #         rowr3 = cursor.fetchall()
                            #         total_debe1=0
                            #         total_haber1=0
                            #         for prb2 in rowr3:
                            #             if prb2[0]:
                            #                 total_debe1=total_debe1+prb2[0]
                            #             if prb2[1]:
                            #                 total_haber1=total_haber1+prb2[1]
                            #         saldo_periodo1=total_debe1-total_haber1
                            #         mult1=float('-1.0')
                            #         if pr[3]==5 and saldo_periodo1<0:
                            #             saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)
                            #
                            #         saldo_actual1=float(saldo_periodo1)+float(saldo_anterior1)
                            #         if pr[6] == '0' and pr[3] == 5:
                            #             ingresos=ingresos+saldo_periodo1
                            #
                            #         if pr[6]=='0' and pr[3]!=5:
                            #             egresos=egresos+saldo_periodo1
                            # total_ejercicio=ingresos-egresos
                            # saldo_periodo=saldo_periodo+total_ejercicio
                       
                        html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo).replace('.', ',')+'</td>'
                        if p[1]=='2':
                            total_pasivo0=saldo_periodo
                            pasivo.append(total_pasivo0)
                        if p[1]=='3':
                            total_patri0=saldo_periodo
                            patrimonio.append(total_patri0)
            
                    
                    
                    
            else:
                while index < 13:
                    if index<=mes_fin:
                        html += '<td>ent</td>'
                        index= index+1  
               
            html+='</tr>'
            
        html+='<tr style="border:1px solid black" ><td colspan="2"><b>TOTAL PASIVO + PATRIMONIO</b></td>'
        i=0
        length_pat=len(pasivo)
        for i in range(i,int(length_pat)):
            total_f=pasivo[i]+patrimonio[i]
            html+='<td style="text-align:right"><b>'+str("%0.2f" % total_f).replace('.', ',') +'</b></td>'
        
        html+='</tr>'
            
            
        return HttpResponse(
            html
        )

    else:
        raise Http404
    
    
@login_required()
def asiento_list_prueba(request):
    #compras = DocumentoCompra.objects.all().order_by('-fecha_emision')
    compras=0
    template = loader.get_template('asiento/index_prueba.html')
    context = RequestContext(request, {'compras': compras})
    return HttpResponse(template.render(context))
@login_required()
@csrf_exempt
def asiento_api_view(request):
    if request.method == "GET" and request.is_ajax:
        _draw = request.GET['draw']
        _start = int(request.GET['start'])
        _end = int(request.GET['length'])
        _search_value = request.GET['search[value]']
        _order=request.GET['order[0][column]']
        _order_dir=request.GET['order[0][dir]']
        cursor = connection.cursor()
        sql="select a.asiento_id,a.codigo_asiento,a.fecha,a.glosa,a.gasto_no_deducible,a.secuencia_asiento,a.total_debe,a.total_haber,a.anulado,a.modulo,m.proveedor_id,m.descripcion,m.paguese_a,m.monto,m.numero_comprobante,a.modulo from contabilidad_asiento a left join movimiento m on m.asiento_id=a.asiento_id where 1=1"
        if _search_value:
            sql+=" and a.codigo_asiento like '%"+_search_value+"%' or UPPER(a.glosa) like '%"+_search_value.upper()+"%' or UPPER(a.modulo) like '%"+_search_value.upper()+"%' or UPPER(m.descripcion) like '%"+_search_value.upper()+"%' or UPPER(m.paguese_a) like '%"+_search_value.upper()+"%' or CAST(a.fecha as VARCHAR)  like '%"+_search_value+"%' or UPPER(m.numero_comprobante) like '%"+_search_value.upper()+"%'"
        
        if _search_value.upper()=='ANULADO'  or _search_value.upper()=='AN' or _search_value.upper()=='ANU' or _search_value.upper()=='ANUL'  or _search_value.upper()=='ANULA' or _search_value.upper()=='ANULAD':
            sql+=" or a.anulado is True"
        
        if _search_value.upper()=='ACTIVO' or _search_value.upper()=='AC' or _search_value.upper()=='ACT' or _search_value.upper()=='ACTI' or _search_value.upper()=='ACTIV':
            sql+=" or a.anulado is not True"
           
    
        #sql +=" order by fecha"
        print _order
        if _order == '0':
            sql +=" order by a.codigo_asiento "+_order_dir
        if _order == '1':
            sql +=" order by a.fecha "+_order_dir
        if _order == '2':
            sql +=" order by a.glosa "+_order_dir
        
        if _order == '3':
            sql +=" order by m.descripcion "+_order_dir
        
        if _order == '4':
            sql +=" order by m.paguese_a "+_order_dir
        if _order == '5':
            sql +=" order by m.numero_comprobante "+_order_dir
        if _order == '6':
            sql +=" order by a.modulo "+_order_dir
        
        if _order == '7':
            sql +=" order by a.anulado "+_order_dir
        print sql
        cursor.execute(sql)
        asientos = cursor.fetchall()
            
        asientos_filtered = asientos[_start:_start + _end]

        asientos_list = []
        for o in asientos_filtered:
            asientos_obj = []
            asientos_obj.append(o[1])
            asientos_obj.append(o[2].strftime('%Y-%m-%d'))
            asientos_obj.append(o[3])
            asientos_obj.append(o[11])
            asientos_obj.append(o[12])
            
            asientos_obj.append(o[14])
            
            html=''
            mes=o[2].month
            anio=o[2].year
            cursor = connection.cursor()
            query="select anio_id,mes_id from bloqueo_periodo  where date_part('year',fecha)='"+str(anio)+"' and date_part('month',fecha)='"+str(mes)+"'"
            cursor.execute(query)
            ro = cursor.fetchall()
            

            if o[8]:
                asientos_obj.append("Anulado")
                asientos_obj.append(o[9])
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/consultar/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/imprimir"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
                

            else:
                asientos_obj.append("Activo")
                asientos_obj.append(o[9])
                if ro:
                    r=1
                else:
                    html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/editar/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-pencil"></i></button></a>'
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/consultar/"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-eye"></i></button></a>'
                html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/imprimir" style="top: 2px; position: relative;"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-print"></i></button></a>'
                if o[9]== 'Contabilidad-Asiento':
                    if ro:
                        r=1
                    else:
                        #html+='<a href="http://'+str( request.META['HTTP_HOST'])+'/contabilidad/asiento/'+str(o[0])+'/eliminarbyPk" style="top: 2px; position: relative;"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'
                        html+='<a href="#" onclick="mostrarAnulacion('+str(o[0])+')" style="top: 2px; position: relative;"><button type="button" class="btn btn-default btn-xs"><i class="fa fa-trash"></i></button></a>'
                        
                    
                else:
                    html+=''
                    
            
           
            
            

            asientos_obj.append(html)

            asientos_list.append(asientos_obj)
        response_data = {}
        response_data['draw'] = _draw
        response_data['recordsTotal'] = len(asientos)
        response_data['recordsFiltered'] = len(asientos)
        response_data['data'] = asientos_list
    else:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")


@login_required()
def estadoResultadoMensualView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True, tipo_cuenta_id__in=[1, 5, 6]).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/estados_resultados_mensual.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))



@csrf_exempt
def consultar_estados_resultados_mensual(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']
        fecha_inicial=desde.split('-')
        fecha_final=hasta.split('-')
        mes_inicio=fecha_inicial[1]
        anio_inicio=fecha_inicial[0]
        mes_fin=fecha_final[1]
        anio_fin=fecha_final[0]
        ingresos_arr=[]
        egresos_arr=[]
        costos_arr=[]
        
        ingresos_arr1=[]
        egresos_arr1=[]
        costos_arr1=[]
        ingresos1_arr=[]
        

        cursor = connection.cursor()
        sql="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)
        ro = cursor.fetchall()
        
        ingresos=0
        egresos=0
        ingresos1=0
        egresos1=0
        print sql
        
        contador=int(mes_fin)-int(mes_inicio)
        cont1=contador+4
        #html = '<table id="tabla" class="table2 table-striped table-bordered" border="1"   aria-describedby="data-table_info"><thead>'
        html = '<table id="tabla" class="table " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="'+str(cont1)+'" style="text-align:center"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>ESTADOS DEL RESULTADO INTEGRAL </b><br>'
        #html+='<b>AL 31 DE DICIEMBRE DE '+str(date.year)+' Y '+str(anio_anterior)+'</b> <br>'
        html+='(Expresado en d&oacute;lares de E.U.A.)</td></tr>'
        html+='<tr><td colspan="'+str(contador)+'">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="4"><b>DESDE</b> '+str(fecha_desde)+'<br /><b>HASTA</b> '+str(fecha_hasta)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th>'
        
        indexm=int(mes_inicio)

        for indexm in range(int(indexm), 13):
                if indexm <= int(mes_fin):
                    x=indexm
                    if x == 1:
                        html+='<th>Enero</th>'
                    if x == 2:
                        html+='<th>Febrero</th>'
                    if x == 3:
                        html+='<th>Marzo</th>'
                    if x == 4:
                        html+='<th>Abril</th>'
                    if x == 5:
                        html+='<th>Mayo</th>'
                    if x == 6:
                        html+='<th>Junio</th>'
                    if x == 7:
                        html+='<th>Julio</th>'
                    if x == 8:
                        html+='<th>Agosto</th>'
                    if x == 9:
                        html+='<th>Septiembre</th>'
                    if x == 10:
                        html+='<th>Octubre</th>'
                    if x == 11:
                        html+='<th>Noviembre</th>'
                    if x == 12:
                        html+='<th>Diciembre</th>'

        html+='<th>Total</th></tr></thead>'
        html+='<tbody>'

        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'

            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            index=mes_inicio
            totalf=0
            if p[0]:
                mes_fin1=int(mes_fin)+1
                
                for index in range(int(index),int(mes_fin1)): 
                    
                    if index <= mes_fin:
                        saldo_periodo=0
                        cursor = connection.cursor()
                        sqlr3 = "select * from dbdctasc where codi_cta = '" + str(p[1]) + "' and tipcta = 'R' and anio_cta = " + str(anio_fin)

                        # sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                        # sqlr3+=" and  date_part('year',a.fecha)='"+str(anio_fin)+"' and date_part('month',a.fecha)='"+str(index)+"'"
                        # sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                        # if centroCosto != "0":
                        #     sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"

                        cursor.execute(sqlr3);
                        rowr3 = cursor.fetchall()
                        total_debe=0
                        total_haber=0

                        for pr2 in rowr3:
                            saldo_actual = pr2[4]
                            # if pr2[0]:
                            #     total_debe=total_debe+pr2[0]
                            # if pr2[1]:
                            #     total_haber=total_haber+pr2[1]
                        # saldo_periodo=total_debe-total_haber
                        mult=float('-1.0')
                        # if p[3]==5 and total_haber<total_debe and saldo_periodo>0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        #
                        # if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                        #     saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)

                        if index <= mes_fin:
                            saldo_periodo = 0
                            if (index == 1):
                                saldo_periodo = pr2[7]
                            if (index == 2):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[8] - pr2[9])
                                else:
                                    saldo_periodo = (pr2[9] - pr2[8])
                            if (index == 3):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[11] - pr2[12])
                                else:
                                    saldo_periodo = (pr2[12] - pr2[11])
                            if (index == 4):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[14] - pr2[15])
                                else:
                                    saldo_periodo = (pr2[15] - pr2[14])
                            if (index == 5):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[17] - pr2[18])
                                else:
                                    saldo_periodo = (pr2[18] - pr2[17])
                            if (index == 6):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[20] - pr2[21])
                                else:
                                    saldo_periodo = (pr2[21] - pr2[20])
                            if (index == 7):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[23] - pr2[24])
                                else:
                                    saldo_periodo = (pr2[24] - pr2[23])
                            if (index == 8):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[26] - pr2[27])
                                else:
                                    saldo_periodo = (pr2[27] - pr2[26])
                            if (index == 9):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[29] - pr2[30])
                                else:
                                    saldo_periodo = (pr2[30] - pr2[29])
                            if (index == 10):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[32] - pr2[33])
                                else:
                                    saldo_periodo = (pr2[33] - pr2[32])
                            if (index == 11):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[35] - pr2[36])
                                else:
                                    saldo_periodo = (pr2[36] - pr2[35])
                            if (index == 12):
                                if (pr2[2]=="DB"):
                                    saldo_periodo = (pr2[38] - pr2[39])
                                else:
                                    saldo_periodo = (pr2[39] - pr2[38])

                        html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo).replace('.', ',')+'</td>'
                        #html+='<td>-'+str(p[3])+'</td>'
                        if p[1]=='4':
                            total_ingre0=saldo_periodo
                            ingresos_arr.append(total_ingre0)
                        if p[1]=='5':
                            total_costos0=saldo_periodo
                            costos_arr.append(total_costos0)
                            
                        if p[1]=='6':
                            total_egre0=saldo_periodo
                            egresos_arr.append(total_egre0)

                        totalf = pr2[40]
                        #totalf=totalf+saldo_periodo
                            
            else:
                for index in range(int(index),int(mes_fin1)): 
                    
                    if index <= mes_fin:
                        html += '<td></td>'
                
            html+='<td style="text-align:right">'+str("%0.2f" % totalf).replace('.', ',')+'</td>'        
            html+='</tr>'
        # total_ejercicio=ingresos-egresos
        html+='<tr style="border:1px solid black" ><td colspan="2"><b>RESULTADO DEL EJERCICIO</b></td>'
        i=0
        length_pat=len(ingresos_arr)
        total_ing_egre=0
        total_suma_ing_eg=0
        
        total_resultado_ejercicio=[]
        for i in range(i,int(length_pat)):
            total_ing_egre=ingresos_arr[i]-egresos_arr[i]-costos_arr[i]
            html+='<td style="text-align:right"><b>'+str("%0.2f" % total_ing_egre).replace('.', ',') +'</b></td>'
            total_resultado_ejercicio.append(total_ing_egre)
            total_suma_ing_eg=total_suma_ing_eg+total_ing_egre
            
            
        html+='<td style="text-align:right"><b>'+str("%0.2f" % total_suma_ing_eg).replace('.', ',') +'</b></td>'
        html+='</tr>'
        
        #Otros Resultados Integrales
        cursor = connection.cursor()
        sql1="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and cuenta.codigo_plan like '310104%' and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql1+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql1+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql1+=" and cuenta.nivel<="+nivel
        
        sql1+=" ORDER BY codigo_plan"
        cursor.execute(sql1)
        ro1 = cursor.fetchall()
        cont_oi=0
        #otros_re=[[]]
        otros_re= {}
        
        for p in ro1:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
            
            saldo_anterior1=0
            saldo_periodo1=0
            saldo_actual1=0
            index1=mes_inicio
            cursor = connection.cursor()
            lcSql = "select cuenta.codigo_plan, cuenta.nivel, det.* from contabilidad_plandecuentas cuenta "
            lcSql += "LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id) "
            lcSql += "LEFT JOIN dbdctasc det ON (cuenta.codigo_plan = det.codi_cta) "
            lcSql += "where cuenta.codigo_plan = '" + p[1]+ "' and cuenta.activo is NOT FALSE and det.anio_cta = " + str(anio_fin)
            cursor.execute(lcSql);
            rowr4 = cursor.fetchall()

            totalf1=0
            if p[0]:
                mes_fin1=int(mes_fin)+1
                total_debe1 = 0
                total_haber1 = 0
                for index1 in range(int(index1),int(mes_fin1)):
                    if index1 <= mes_fin:
                        saldo_periodo1=0
                        cuenta = ''
                        for pr2 in rowr4:
                            cuenta = pr2[0]

                        if (index1 == 1):
                            saldo_periodo1=pr2[7]
                            total_debe1 = saldo_periodo1
                        if (index1 == 2):
                            saldo_periodo1=0
                        if (index1 == 3):
                            saldo_periodo1=0
                        if (index1 == 4):
                            saldo_periodo1=0
                        if (index1 == 5):
                            saldo_periodo1=0
                        if (index1 == 6):
                            saldo_periodo1=0
                        if (index1 == 7):
                            saldo_periodo1=0
                        if (index1 == 8):
                            saldo_periodo1=0
                        if (index1 == 9):
                            saldo_periodo1=0
                        if (index1 == 10):
                            saldo_periodo1=0
                        if (index1 == 11):
                            saldo_periodo1=0
                        if (index1 == 12):
                            #41 - 42
                            saldo_periodo1 = pr2[40] - pr2[41]
                            #saldo_periodo1=total_debe1+saldo_actual

                        # cursor = connection.cursor()
                        # sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                        # sqlr3+=" and  date_part('year',a.fecha)='"+str(anio_fin)+"' and date_part('month',a.fecha)='"+str(index1)+"'"
                        # sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                        # if centroCosto != "0":
                        #     sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                        # cursor.execute(sqlr3);
                        # rowr3 = cursor.fetchall()

                            # if pr2[0]:
                            #     total_debe1=total_debe1+pr2[0]
                            # if pr2[1]:
                            #     total_haber1=total_haber1+pr2[1]
                        # saldo_periodo1=total_debe1-total_haber1
                        # mult1=float('-1.0')
                        # if p[3]==5 and total_haber1<total_debe1 and saldo_periodo1>0:
                        #     saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)
                        #
                        # if p[3]==5 and total_haber1>total_debe1 and saldo_periodo1<0:
                        #     saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)

                        html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo1).replace('.', ',')+'</td>'
                        #html+='<td>-'+str(p[3])+'</td>'
                        total_ingre01=saldo_periodo1
                        otros_re[cont_oi,index1]=total_ingre01
                        #ingresos_arr1.append(total_ingre01)

                        totalf1=totalf1+saldo_periodo1

            else:
                for index1 in range(int(index1),int(mes_fin1)): 
                    
                    if index1 <= mes_fin:
                        html += '<td></td>'
                        #otros_re[cont_oi,index1]=0
                
            html+='<td style="text-align:right">'+str("%0.2f" % totalf1).replace('.', ',')+'</td>'        
            html+='</tr>'
            cont_oi=cont_oi+1
        # total_ejercicio=ingresos-egresos
        print 'inicio cont'
        print cont_oi
        print 'termino'
        total_otros_resultados=[]
        j=1
        length_pat1=0
        total_ing_egre1=0
        total_suma_ing_eg1=0
        #html+='<tr style="border:1px solid black" ><td colspan="2"><b> TOTAL'+str(length_pat1)+'</b></td>'
        print otros_re
        for j in range(j,int(mes_fin1)):
            z=0
            total_ing_egre1=0
            for z in range(z,int(cont_oi)):
                
                if otros_re[z,j]:
                    total_ing_egre1=total_ing_egre1+otros_re[z,j]
                else:
                    total_ing_egre1=total_ing_egre1+0
                    
            #html+='<td style="text-align:right"><b>'+str("%0.2f" % total_ing_egre1).replace('.', ',') +'</b></td>'
            total_otros_resultados.append(total_ing_egre1)
            total_suma_ing_eg1=total_suma_ing_eg1+total_ing_egre1
            

        # html+='<td style="text-align:right"><b>'+str("%0.2f" % total_suma_ing_eg1).replace('.', ',') +'</b></td>'
        # html+='</tr>'
        # print total_otros_resultados
        # print total_resultado_ejercicio
        contf=len(total_otros_resultados)
        print contf
        total_final=0
        
        x=0
        html+='<tr style="border:1px solid black" ><td colspan="2"><b> TOTAL'+str(length_pat1)+'</b></td>'
        for x in range(x,int(contf)):
            total_men=total_resultado_ejercicio[x]+total_otros_resultados[x]
            #total_men=0
            html+='<td style="text-align:right"><b>'+str("%0.2f" % total_men).replace('.', ',') +'</b></td>'
            total_final=total_final+total_men
        
        html+='<td style="text-align:right"><b>'+str("%0.2f" % total_final).replace('.', ',') +'</b></td>'
        html+='</tr>'

            
        
        
        # html+='</tr>'
            
            
        return HttpResponse(
            html
        )

    else:
        raise Http404


@login_required()
@csrf_exempt
def consultarSubCentro(request):
    if request.method == 'POST':
        modulo = request.POST.get('id')
        count_codigo=0
        count_secuencial=0


        objetos = CentroCosto.objects.get(centro_id = modulo)

        modulo_secuencial = objetos.secuencia_subcentro
        codigo = objetos.codigo
        if codigo:
            count_codigo=codigo
        if modulo_secuencial:
            count_secuencial=modulo_secuencial
        
        secuencial=int(count_codigo)+int(count_secuencial)

        return HttpResponse(
                secuencial
            )
    else:
        raise Http404



@login_required()
def balancedeComprobacionView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    anio = Anio.objects.all()
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/balance_comprobacion.html',
                              RequestContext(request, {'cuentas': plan_ctas,'anio': anio,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))



@csrf_exempt
def consultar_balance_comprobacion(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']
        

        cursor = connection.cursor()
        sql="select distinct cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,tcuenta.acreedora,tcuenta.deudora from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
            
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)



        
        ro = cursor.fetchall()
        print sql
        date = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
        anio_anterior=int(date.year)-1
        html = '<table id="tabla" class="table2 table-striped " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="6" style="text-align:center  !important"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>BALANCE DE COMPROBACION  </b><br>'
        html+='<b>DESDE '+str(fecha_desde)+' HASTA '+str(fecha_hasta)+'</b> <br>'
        html+='</td></tr>'
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        #html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3">AL '+str(date.day)+'/'+str(date.month)+'/'+str(date.year)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th><th>SALDO ANTERIOR</th><th>DEBITOS</th><th>CREDITOS</th>'
        html+='<th>SALDO ACTUAL</th>'
        
        html+='</tr></thead>'
        html+='<tbody>'
        total_pasivo=0
        total_patri=0
        total_pasivo0=0
        total_patri0=0
        total_saldo_anterior=0
        total_final_debe=0
        total_final_haber=0
        total_final_saldo_actual=0
        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left  !important"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right  !important">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left  !important">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
            
                
            
            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            
            #print anio_anterior
            try:
                pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(p[0]))
                #print "entro2"
            except PeriodoAnterior.DoesNotExist:
                pb = None

            
            if pb:
                saldo_anterior=pb[0].saldo
            else:
                saldo_anterior=0
            
            html+='<td style="text-align:right  !important">'+str("%0.2f" % saldo_anterior).replace('.', ',') +'</td>'
                
            
                    
            
            if p[0]:
                
                saldo_periodo=0
                cursor = connection.cursor()
                #sqlr3="select ad.cuenta_id,sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad where a.asiento_id=ad.asiento_id "
                sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                 
                if fecha_desde:
                    sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                if fecha_hasta:
                    sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "
                
                #sqlr3+=" and ad.cuenta_id="+ str(p[0])+"  and a.anulado is not True group by ad.cuenta_id"
                sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                if centroCosto != "0":
                    sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                   
                print sqlr3
                cursor.execute(sqlr3);
                rowr3 = cursor.fetchall()
                total_debe=0
                total_haber=0
                for pr2 in rowr3:
                    if pr2[0]:
                        total_debe=total_debe+pr2[0]
                    if pr2[1]:
                        total_haber=total_haber+pr2[1]
                saldo_periodo=total_debe-total_haber
                mult=float('-1.0')
                
                if p[3]==5 and total_debe>total_haber and saldo_periodo>0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                if p[3]==3 and total_debe>total_haber and saldo_periodo>0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                if p[3]==3 and total_haber>total_debe and saldo_periodo<0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                    
                if p[3]==4 and total_debe>total_haber and saldo_periodo>0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                if p[3]==4 and total_haber>total_debe and saldo_periodo<0:
                    saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                
                if p[1]=='310103002' or p[1]=='310103' or p[1]=='310103' or p[1]=='3101' or p[1]=='31' or p[1]=='3' :
                    cursor = connection.cursor()
                    sql="select distinct  cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
                    if cuenta != "Todas":
                        sql+=" and cuenta.nombre_plan='"+cuenta+"'"
                    if inputTipo != "0":
                        sql+=" and cuenta.tipo_cuenta_id="+inputTipo
                    if nivel != "":
                        sql+=" and cuenta.nivel="+nivel
                    sql+=" ORDER BY codigo_plan"
                    cursor.execute(sql)
                    ro = cursor.fetchall()
                    date = datetime.strptime(fecha_hasta, "%Y-%m-%d").date()
                    anio_anterior=int(date.year)-1
                    ingresos=0
                    egresos=0
                    
                    
                    
                    for pr in ro:
                        
                        saldo_anterior1=0
                        saldo_periodo1=0
                        saldo_actual1=0
                        
                        #print anio_anterior
                        try:
                            pb1 = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(pr[0]))
                            #print "entro2"
                        except PeriodoAnterior.DoesNotExist:
                            pb1 = None
            
                        
                        if pb1:
                            saldo_anterior1=pb1[0].saldo
                        else:
                            saldo_anterior1=0
                        
                        saldo_anterior1=0
                            
                        
                                
                        
                        if pr[0]:
                            
                            saldo_periodo1=0
                            cursor = connection.cursor()
                            
                            sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                            if fecha_desde:
                                sqlr3+=" and a.fecha>='"+ str(fecha_desde)+"'"
                            if fecha_hasta:
                                sqlr3+=" and a.fecha<='"+ str(fecha_hasta)+"' "
                            
                            #sqlr3+=" and ad.cuenta_id="+ str(p[0])+"  and a.anulado is not True group by ad.cuenta_id"
                            sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(pr[1])+"%'  and a.anulado is not True"
                            if centroCosto != "0":
                                sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                            
                            #print sqlr3
                            cursor.execute(sqlr3);
                            rowr3 = cursor.fetchall()
                            total_debe1=0
                            total_haber1=0
                            for prb2 in rowr3:
                                if prb2[0]:
                                    total_debe1=total_debe1+prb2[0]
                                if prb2[1]:
                                    total_haber1=total_haber1+prb2[1]
                            saldo_periodo1=total_debe1-total_haber1
                            mult1=float('-1.0')
                            if pr[3]==5 and saldo_periodo1<0:
                                saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)
                                
                            saldo_actual1=float(saldo_periodo1)+float(saldo_anterior1)
                            if pr[6] == '0' and pr[3] == 5:
                                ingresos=ingresos+saldo_periodo1
                                
                            if pr[6]=='0' and pr[3]!=5:
                                egresos=egresos+saldo_periodo1
                                
                                
                        
                    total_ejercicio=ingresos-egresos
                    saldo_periodo=saldo_periodo+total_ejercicio
                    
                
                    
                html+='<td style="text-align:right  !important">'+str("%0.2f" % total_debe).replace('.', ',')+'</td>'
                html+='<td style="text-align:right  !important">'+str("%0.2f" % total_haber).replace('.', ',') +'</td>'
                if anio_anterior == '2016' or anio_anterior == 2016:
                    saldo_actual=float(saldo_periodo)
                else:
                    saldo_actual=float(saldo_periodo)+float(saldo_anterior)
                
                #SUMA Y RESTA E SALDO ACTUAL Y SALDO ANTERIOR
                if p[7]:
                    saldo_actual=float(saldo_anterior)+float(total_debe)-float(total_haber)
                if p[6]:
                    saldo_actual=float(saldo_anterior)+float(total_haber)-float(total_debe)
                
                
                html+='<td style="text-align:right  !important">'+str("%0.2f" % saldo_actual).replace('.', ',') +'</td>'
                total_saldo_anterior=total_saldo_anterior+saldo_anterior
                total_final_debe=total_final_debe+total_debe
                total_final_haber=total_final_haber+total_haber
                total_final_saldo_actual=total_final_saldo_actual+saldo_actual
            else:
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
            html+='</tr>'
       
        #html+='<tr style="border:1px solid black  !important" ><td colspan="3"><b>TOTAL PASIVO + PATRIMONIO</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_f0).replace('.', ',') +'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_f).replace('.', ',') +'</b></td>'
        #html+='</tr>'
        html+='<tr style="border:1px solid black  !important" ><td colspan="2"><b>TOTAL Debitos/Creditos</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_saldo_anterior).replace('.', ',') +'</b></td><td style="text-align:right"><b>'+str("%0.2f" % total_final_debe).replace('.', ',') +'</b></td>'
        html+='<td style="text-align:right"><b>'+str("%0.2f" % total_final_haber).replace('.', ',') +'</b></td>'
        html+='<td style="text-align:right"><b>'+str("%0.2f" % total_final_saldo_actual).replace('.', ',') +'</b></td>'
        html+='</tr>'
    
            
            
        return HttpResponse(
            html
        )

    else:
        raise Http404



@login_required()
def balanceComprobacionMensualizadoView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).order_by('codigo_plan')
    centro_costos = CentroCosto.objects.filter(activo=True)
    tipo_cuenta = TipoCuenta.objects.filter(activo=True)
    return render_to_response('estado_financiero/balance_comprobacion_mensual.html',
                              RequestContext(request, {'cuentas': plan_ctas,
                                                       'centros': centro_costos,
                                                       'tipo_cuenta': tipo_cuenta}))

@csrf_exempt
def consultar_balance_comprobacion_mensualizado(request):
    if request.method == "POST" :
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        centroCosto = request.POST['inputCentroCosto']
        inputTipo = request.POST['inputTipo']
        desde = fecha_desde
        hasta = fecha_hasta
        nivel = request.POST['nivel']
        fecha_inicial=desde.split('-')
        fecha_final=hasta.split('-')
        mes_inicio=fecha_inicial[1]
        anio_inicio=fecha_inicial[0]
        mes_fin=fecha_final[1]
        anio_fin=fecha_final[0]
        

        cursor = connection.cursor()
        sql="select cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,tcuenta.acreedora,tcuenta.deudora from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=2 or cuenta.tipo_cuenta_id=3 or cuenta.tipo_cuenta_id=4) and cuenta.activo is NOT FALSE "
        if cuenta != "Todas":
            sql+=" and cuenta.nombre_plan='"+cuenta+"'"
        if inputTipo != "0":
            sql+=" and cuenta.tipo_cuenta_id="+inputTipo
        if nivel != "":
            sql+=" and cuenta.nivel<="+nivel
        
        sql+=" ORDER BY codigo_plan"
        cursor.execute(sql)

        ro = cursor.fetchall()
        print sql
        date = datetime.strptime(fecha_hasta, "%Y-%m").date()
        anio_anterior=int(date.year)-1
        html = '<table id="tabla" class="table2 table-striped " border="0"   aria-describedby="data-table_info"><thead>'
        html+='<tr><td colspan="5" style="text-align:center"><b>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.</b><br>'
        
        html+='<b>BALANCE DE COMPROBACION  </b><br>'
        html+='<b>DESDE '+str(fecha_desde)+' HASTA '+str(fecha_hasta)+'</b> <br>'
        #html+='<b>AL 31 DE DICIEMBRE DE '+str(date.year)+' Y '+str(anio_anterior)+'</b> <br>'
        #html+='(Expresado en d&oacute;lares de E.U.A.)</td></tr>'
        
        #html+='<tr><td colspan="1"><b>DESDE</b></td><td colspan="1">'+str(fecha_desde)+'</td><td colspan="1"><b>HASTA</b></td><td colspan="2">'+str(fecha_hasta)+'</td></tr>'
        #html+='<tr><td colspan="2">Pertenecientes a una entidad individual<br><b>Grado de redondeo:</b>Sin redondeo</td><td colspan="3">DESDE '+str(fecha_desde)+' HASTA  '+str(fecha_hasta)+'</td></tr>'
        html+='<tr>'
        html+='<th>Codigo</th><th>Nombre</th>'
        
        indexm=int(mes_inicio)
        
        
        for indexm in range(int(indexm), 13):
                if indexm <= int(mes_fin):
                    x=indexm
                    if x == 1:
                        html+='<th>Enero</th>'
                    if x == 2:
                        html+='<th>Febrero</th>'
                    if x == 3:
                        html+='<th>Marzo</th>'
                    if x == 4:
                        html+='<th>Abril</th>'
                    if x == 5:
                        html+='<th>Mayo</th>'
                    if x == 6:
                        html+='<th>Junio</th>'
                    if x == 7:
                        html+='<th>Julio</th>'
                    if x == 8:
                        html+='<th>Agosto</th>'
                    if x == 9:
                        html+='<th>Septiembre</th>'
                    if x == 10:
                        html+='<th>Octubre</th>'
                    if x == 11:
                        html+='<th>Noviembre</th>'
                    if x == 12:
                        html+='<th>Diciembre</th>'

        html+='<th>TOTAL</th>'
        html+='</tr></thead>'
        html+='<tbody>'
        total_pasivo=0
        total_patri=0
        total_pasivo0=0
        total_patri0=0
        pasivo=[]
        patrimonio=[]
        for p in ro:
            html+='<tr>'
            if p[5]==0 or p[5]==1 or p[5]==2 :
                if p[1]:
                    html += '<td style="text-align:right"><b>&nbsp;' + str(p[1].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left"><b>' + str(p[2].encode('utf8')) +'</b></td>'
                else:
                    html += '<td></td>'
            else:
                if p[1]:
                    html += '<td style="text-align:right">&nbsp;' + str(p[1].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
                if p[2]:
                    html += '<td style="text-align:left">' + str(p[2].encode('utf8')) +'</td>'
                else:
                    html += '<td></td>'
            
                
            
            saldo_anterior=0
            saldo_periodo=0
            saldo_actual=0
            index=mes_inicio
           
            if p[0]:
                mes_fin1=int(mes_fin)+1
                saldo_mensual=0
                
                for index in range(int(index),int(mes_fin1)): 
                    
                    if index <= mes_fin:
                        #html+='<td>'+str(index)+'</td>'
                
                        saldo_periodo=0
                        cursor = connection.cursor()
                        #sqlr3="select ad.cuenta_id,sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad where a.asiento_id=ad.asiento_id "
                        sqlr3="select sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                        sqlr3+=" and  date_part('year',a.fecha)='"+str(anio_fin)+"' and date_part('month',a.fecha)='"+str(index)+"'"
                        sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(p[1])+"%'  and a.anulado is not True"
                        if centroCosto != "0":
                            sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                        #print sqlr3
                        cursor.execute(sqlr3);
                        rowr3 = cursor.fetchall()
                        total_debe=0
                        total_haber=0
                        for pr2 in rowr3:
                            if pr2[0]:
                                total_debe=total_debe+pr2[0]
                            if pr2[1]:
                                total_haber=total_haber+pr2[1]
                        
                        saldo_periodo=total_debe-total_haber
                        if p[6]:
                            saldo_periodo=total_haber-total_debe
                        if p[7]:
                            saldo_periodo=total_debe-total_haber
                        mult=float('-1.0')
                        
                        
                        
                        if p[3]==5 and total_debe>total_haber and saldo_periodo>0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        
                        if p[3]==5 and total_haber>total_debe and saldo_periodo<0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                            
                        if p[3]==3 and total_debe>total_haber and saldo_periodo>0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                            
                        if p[3]==3 and total_haber>total_debe and saldo_periodo<0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                            
                        if p[3]==4 and total_debe>total_haber and saldo_periodo>0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        
                        if p[3]==4 and total_haber>total_debe and saldo_periodo<0:
                            saldo_periodo=Decimal(saldo_periodo)*Decimal(mult)
                        
                           
                        
                        if p[1]=='310103002' or p[1]=='310103' or p[1]=='310103' or p[1]=='3101' or p[1]=='31' or p[1]=='3' :
                            cursor = connection.cursor()
                            sql="select distinct  cuenta.plan_id,cuenta.codigo_plan, cuenta.nombre_plan,tcuenta.tipo_id,tcuenta.nombre_tipo,cuenta.nivel,cuenta.nivel_padre from contabilidad_plandecuentas cuenta LEFT JOIN contabilidad_tipocuenta  tcuenta ON (cuenta.tipo_cuenta_id = tcuenta.tipo_id)  where 1=1  and (cuenta.tipo_cuenta_id=1 or cuenta.tipo_cuenta_id=5 or cuenta.tipo_cuenta_id=6) and cuenta.activo is NOT FALSE "
                            if cuenta != "Todas":
                                sql+=" and cuenta.nombre_plan='"+cuenta+"'"
                            if inputTipo != "0":
                                sql+=" and cuenta.tipo_cuenta_id="+inputTipo
                            if nivel != "":
                                sql+=" and cuenta.nivel="+nivel
                            sql+=" ORDER BY codigo_plan"
                            cursor.execute(sql)
                            ro = cursor.fetchall()
                           
                            ingresos=0
                            egresos=0
                    
                    
                    
                            for pr in ro:
                                
                                saldo_anterior1=0
                                saldo_periodo1=0
                                saldo_actual1=0
                                
                                
                                
                                saldo_anterior1=0
                                    
                                
                                        
                                
                                if pr[0]:
                                    
                                    saldo_periodo1=0
                                    cursor = connection.cursor()
                                    
                                    sqlr3="select distinct sum(ad.debe),sum(ad.haber) from contabilidad_asiento a, contabilidad_asientodetalle ad,contabilidad_plandecuentas cpc where a.asiento_id=ad.asiento_id "
                                    sqlr3+=" and  date_part('year',a.fecha)<='"+str(anio_fin)+"' and date_part('month',a.fecha)<='"+str(index)+"'"
                                    sqlr3+="and ad.cuenta_id=cpc.plan_id and cpc.codigo_plan like '"+ str(pr[1])+"%'  and a.anulado is not True"
                                    if centroCosto != "0":
                                        sqlr3+=" and (ad.centro_costo_id="+str(centroCosto)+" or ad.centro_costo_id in (select centro_id from contabilidad_centrocosto where padre_id="+str(centroCosto)+"))"
                 
                                    
                                    #print sqlr3
                                    cursor.execute(sqlr3);
                                    rowr3 = cursor.fetchall()
                                    total_debe1=0
                                    total_haber1=0
                                    for prb2 in rowr3:
                                        if prb2[0]:
                                            total_debe1=total_debe1+prb2[0]
                                        if prb2[1]:
                                            total_haber1=total_haber1+prb2[1]
                                    saldo_periodo1=total_debe1-total_haber1
                                    mult1=float('-1.0')
                                    if pr[3]==5 and saldo_periodo1<0:
                                        saldo_periodo1=Decimal(saldo_periodo1)*Decimal(mult1)
                                        
                                    saldo_actual1=float(saldo_periodo1)+float(saldo_anterior1)
                                    if pr[6] == '0' and pr[3] == 5:
                                        ingresos=ingresos+saldo_periodo1
                                        
                                    if pr[6]=='0' and pr[3]!=5:
                                        egresos=egresos+saldo_periodo1
                                        
                                        
                            if p[6]:
                                total_ejercicio=ingresos-egresos
                            if p[7]:
                                total_ejercicio=egresos-ingresos
                            saldo_periodo=saldo_periodo+total_ejercicio
                       
                        html+='<td style="text-align:right">'+str("%0.2f" % saldo_periodo).replace('.', ',')+'</td>'
                        saldo_mensual=saldo_mensual+saldo_periodo
                        # if p[1]=='2':
                        #     total_pasivo0=saldo_periodo
                        #     pasivo.append(total_pasivo0)
                        # if p[1]=='3':
                        #     total_patri0=saldo_periodo
                        #     patrimonio.append(total_patri0)
            
                html+='<td style="text-align:right">'+str("%0.2f" % saldo_mensual).replace('.', ',')+'</td>'

                    
                    
            else:
                while index < 13:
                    if index<=mes_fin:
                        html += '<td>ent</td>'
                        index= index+1  
               
            html+='</tr>'
            
        #html+='<tr style="border:1px solid black" ><td colspan="2"><b>TOTAL PASIVO + PATRIMONIO</b></td>'
        # i=0
        # length_pat=len(pasivo)
        # for i in range(i,int(length_pat)):
        #     total_f=pasivo[i]+patrimonio[i]
        #     html+='<td style="text-align:right"><b>'+str("%0.2f" % total_f).replace('.', ',') +'</b></td>'
        # 
        # html+='</tr>'
            
            
        return HttpResponse(
            html
        )

    else:
        raise Http404
   

@login_required()
def mostrar_motivo_anulacion(request):
    if request.method == "POST":
        #fila = request.POST['fila']
        fila=0
        id = request.POST['id']
        asiento = Asiento.objects.get(asiento_id=id)
        return render_to_response('asiento/mostrar_motivo_anulacion.html',
                                  {'id': id,'asiento': asiento},RequestContext(request))
    else:
        fila=0
        id = request.POST['id']
        asiento = Asiento.objects.get(asiento_id=id)
        return render_to_response('asiento/mostrar_motivo_anulacion.html',
                                  {'id': id,'asiento': asiento},RequestContext(request))
    
    
@login_required()
def anulacion_asiento_motivo(request):
    if request.method == "POST":
        pk = request.POST['id']
        motivo = request.POST['motivo']
        try:
            asiento = Asiento.objects.filter(asiento_id=pk)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.motivo_anulacion= motivo
                a.anulado_at= datetime.now()
                a.anulado_por= request.user.get_full_name()
                a.save()
    
        

    return HttpResponseRedirect('/contabilidad/asiento/')






@login_required()
def MayoresContablesActualPruebaView(request):
    plan_ctas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
    centro_costos = CentroCosto.objects.filter(activo=True).order_by('codigo')
    return render_to_response('registrar_libro_diario/mayores_contables_prueba.html',
                              RequestContext(request, {'cuentas': plan_ctas,'centro_costos':centro_costos}))

@login_required()
@login_required()
def ConsultaMayorActualPruebaView(request):
    if request.method == "POST" and request.is_ajax:
        cuenta = request.POST['inputCuenta']
        fecha_desde = request.POST['fecha_desde']
        fecha_hasta = request.POST['fecha_hasta']
        cuenta_hasta = request.POST['inputCuentaHasta']
        centroCosto = request.POST['centro_costo']
        try:
            cuenta_cod_desde = PlanDeCuentas.objects.get(plan_id=cuenta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_desde = None
            
        try:
            cuenta_cod_hasta = PlanDeCuentas.objects.get(plan_id=cuenta_hasta)

        except PlanDeCuentas.DoesNotExist:
            cuenta_cod_hasta= None
        
    

        cursor = connection.cursor()
        
        cursor.execute('select nombre_plan, codigo_plan,plan_id '
            'from contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta '
            'where cuenta.tipo_cuenta_id = tcuenta.tipo_id '
            'and cuenta.codigo_plan::float>=%s '
            'and  cuenta.codigo_plan::float<=%s '
            'GROUP BY nombre_plan, codigo_plan,plan_id order by codigo_plan ', (float(cuenta_cod_desde.codigo_plan),float(cuenta_cod_hasta.codigo_plan)))
        rop_actual = cursor.fetchall()
        html=''
        html+='<table class="table table-bordered table-asiento" id="estado_cuentas">'
        html+='<thead style="background-color: #EEEEEE"><tr><td colspan="9"><b>ESTADO DE CUENTA </b>(DESDE '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+'  HASTA '+str(cuenta_cod_desde.codigo_plan)+' '+str(cuenta_cod_desde.nombre_plan.encode('utf8'))+')<br>DESDE:'+str(fecha_desde)+' HASTA: '+str(fecha_hasta)+'</td></tr><tr><th style="text-align: center"><b>Cuenta</b></th><th style="text-align: center"><b>Fecha</b></th><th style="text-align: center"><b>Asiento</b></th><th style="text-align: center"><b>Glosa</b></th><th style="text-align: center"><b>Debe</b></th><th style="text-align: center"><b>Haber</b></th><th style="text-align: center"><b>Saldo</b></th><th style="text-align: center"><b>Concepto</b></th>'
        if centroCosto != "0":
            html+='<th style="text-align: center"><b>Centro de Costo</b></th>'
        html+='</tr></thead>'
        html+='<tbody>'
        for co in rop_actual:
            
            html+='<tr><td colspan="9"><b>CODIGO: '+str(co[1].encode('utf8'))+' '+str(co[0].encode('utf8'))+'</td><tr>'
            total_debito=0
            total_haber=0
            #date = datetime.strptime(fecha_hasta, "%d/%m/%y").date()
            fec=fecha_hasta.split("/")
            anio_anterior=int(fec[2])-1
            #print 'anio anterior'
            #print anio_anterior
            print co[1]
            fecha_inicial_consulta=datetime.strptime(fecha_desde, "%d/%m/%Y").strftime("%Y-%m-%d")
            print fecha_inicial_consulta
            try:
                pb = PeriodoAnterior.objects.filter(anio=anio_anterior).filter(plan_id=str(co[2]))
                #print "entro2"
            except PeriodoAnterior.DoesNotExist:
                pb = None
                #print "no entro"

            saldo=0
            sql2="select nombre_plan, codigo_plan,plan_id,sum(ad.debe),sum(ad.haber) from contabilidad_plandecuentas as cuenta,contabilidad_asiento a,contabilidad_asientodetalle ad where a.asiento_id=ad.asiento_id and a.anulado is not True and ad.cuenta_id=cuenta.plan_id"
            sql2+=" and cuenta.plan_id= "+str(co[2])+" and a.fecha < '"+str(fecha_inicial_consulta)+"'  GROUP BY nombre_plan, codigo_plan,plan_id"
            print sql2
            cursor.execute(sql2)
            rop_saldo_anterior = cursor.fetchall()
            # if pb:
            #     saldo_inicial=pb[0].saldo
            #     saldo = saldo + saldo_inicial
            # else:
            #     saldo_inicial=0
            if rop_saldo_anterior:
                if rop_saldo_anterior[0][3]:
                    debito_a=float(rop_saldo_anterior[0][3])
                else:
                    debito_a=0
                
                if rop_saldo_anterior[0][4]:
                    haber_a=float(rop_saldo_anterior[0][4])
                else:
                    haber_a=0
                
                #saldo_inicial=pb[0].saldo
                saldo_inicial=debito_a-haber_a
                saldo = saldo + saldo_inicial
            else:
                saldo_inicial=0
                
            html+='<tr><td>SALDO ANTERIOR</td><td></td><td></td><td></td>'
            #html+='<td align="right">' + str("%2.2f" % saldo_inicial).replace('.', ',') + '</td>'
            html+='<td align="right">0</td>'
            html+='<td align="right">0</td>'
            html+='<td align="right">'+str("%2.2f" % saldo).replace('.', ',')+'</td><td align="right"></td><td align="right"></td> </tr>'
            total_debito=total_debito+float(saldo_inicial)
            if centroCosto != "0":
                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto,nombre_centro,asiento.asiento_id '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and cuenta.codigo_plan=%s '            
                    'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
                    'and adetalle.centro_costo_id=%s '  
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (str(co[1]), fecha_desde, fecha_hasta,centroCosto))
            else:
                
                cursor.execute(
                    'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto,asiento.asiento_id '
                    'from contabilidad_asiento as asiento,  '
                    'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
                    'LEFT JOIN contabilidad_centrocosto as ccosto '
                    'ON adetalle.centro_costo_id = ccosto.centro_id '
                    'where asiento.asiento_id = adetalle.asiento_id '
                    'and adetalle.cuenta_id = cuenta.plan_id  '
                    'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
                    'and cuenta.codigo_plan=%s '            
                    'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
                    'ORDER BY asiento.fecha,asiento.codigo_asiento', (str(co[1]), fecha_desde, fecha_hasta))
    
            ro = cursor.fetchall()
            print ro
                
                
            
            for cuentas in ro:
                saldo = saldo + float(cuentas[5])
                concepto=""
                if cuentas[8]:
                    concepto=cuentas[8]
                if cuentas[3]==0 and cuentas[4]==0:
                    print "cuenta vacia"
                else:
                    html+='<tr><td>' + str(cuentas[7].encode('utf8'))+ '-' + str(cuentas[6].encode('utf8')) + '</td><td>' + str(cuentas[1]) + '</td><td>' + str(cuentas[0]) + '</td><td>' + str(cuentas[2].encode('utf8')) + '</td>'
                    html+='<td align="right">' + str("%2.2f" % cuentas[3]).replace('.', ',')+ '</td>'
                    html+='<td align="right">' +  str("%2.2f" % cuentas[4]).replace('.', ',')+'</td>'
                    html+='<td align="right"><b>' +  str("%2.2f" % saldo).replace('.', ',') + '</b></td><td>' + str(concepto.encode('utf8')) + '</td>'
                    if centroCosto != "0":
                        try:
                            pb = CentroCosto.objects.filter(centro_id=centroCosto).first()
                            #print "entro2"
                        except CentroCosto.DoesNotExist:
                            pb = None
            
                        
                        if pb:
                            html+='<td>' + str(cuentas[9])+ '</td>'
                    else:
                         html+='<td></td>'
                         
                    cursor = connection.cursor()
                    sql='select a.asiento_id,a.codigo_asiento,m.fecha_emision,m.numero_comprobante,m.proveedor_id,m.activo,m.monto,m.id from contabilidad_asiento a,movimiento m  where m.asiento_id=a.asiento_id and a.asiento_id='+str(cuentas[9])+' order by a.fecha;'
                    cursor.execute(sql)
                    rmovimiento = cursor.fetchall()
                    cadena_mov=''
                    for rc in rmovimiento:
                        cadena_mov+='Mov-'+str(rc[3])+'/'+str(rc[4])+'/'+str(rc[5])+'/'+str(rc[6])+'/'+str(rc[7])
                        sql='select m.id,sum(d.abono) from documento_abono d ,movimiento m  where d.movimiento_id=m.id and m.id='+str(rc[7])+' group by m.id;'
                        cursor.execute(sql)
                        abono = cursor.fetchall()
                        ca=0
                        for a in abono:
                            if a[1]:
                                ca=float(ca)+float(a[1])
                        cadena_mov+="abono/"+str(ca)
                        
                        
                            
                            
                            
                    html+='<td>'+str(cadena_mov)+'</td>'
                        
                    sql1='select a.asiento_id,a.codigo_asiento,dc.fecha_emision,dc.id,dc.secuencial,dc.proveedor_id,dc.anulado,dc.total from contabilidad_asiento a,documento_compra dc where dc.asiento_id=a.asiento_id and a.asiento_id='+str(cuentas[9])+' order by a.fecha;'
                    cursor.execute(sql1)
                    rcompra = cursor.fetchall()
                    cadena_comp=''
                    for c in rcompra:
                        cadena_comp+='Compra-'+str(c[3])+'//'+str(c[4])+'//'+str(c[5])+'//'+str(c[6])+'//'+str(c[7])
                        sql2='select d.retenciones from documento_compra_retenciones d  where d.documento_compra_id='+str(c[3])+' '
                        cursor.execute(sql2)
                        abono2 = cursor.fetchall()
                        ca2=0
                        for a2 in abono2:
                            if a2[0]:
                                ca2=float(ca2)+float(a2[0])
                        total_factura=c[7]-ca2
                        cadena_comp+="total/"+str(total_factura)
                            
                            
                    html+='<td>'+str(cadena_comp)+'</td>'
                    
                
                    html+='</tr>'
                    total_debito=total_debito+float(cuentas[3])
                    total_haber=total_haber+float(cuentas[4])
            html+='<tr><td colspan="4"><b>Total</b></td><td><b>'+str("%2.2f" % total_debito).replace('.', ',')+'</b></td><td><b>'+str("%2.2f" % total_haber).replace('.', ',')+'</b></td><td><b>'+str("%2.2f" % saldo).replace('.', ',')+'</b></td><td></td><td></td></tr>'
    
                    
            
            
        html+='</tbody>'
    else:
        raise Http404

    return HttpResponse(
            html
        )
    #return HttpResponse(json_resultados, content_type="application/json")
  
# def ConsultaMayorActualPruebaView(request):
#     if request.method == "POST" and request.is_ajax:
#         cuenta = 678
#         fecha_desde ='01/01/2017'
#         fecha_hasta = '01/01/2018'
#         
#         
#         html=''
#         html+='<table class="table table-bordered table-asiento" id="estado_cuentas">'
#         html+='<tbody>'
#         total_debito=0
#         total_haber=0
#         saldo=0
#         co='210101001'
#         cursor = connection.cursor()
#         cursor.execute(
#                     'select codigo_asiento, to_char(fecha, \'DD/MM/YYYY\') as fecha, glosa, debe, haber, debe - haber as saldo, nombre_plan, codigo_plan,concepto ,adetalle.asiento_id'
#                     ' from contabilidad_asiento as asiento,  '
#                     'contabilidad_plandecuentas as cuenta,contabilidad_tipocuenta as tcuenta,contabilidad_asientodetalle as adetalle '
#                     'LEFT JOIN contabilidad_centrocosto as ccosto '
#                     'ON adetalle.centro_costo_id = ccosto.centro_id '
#                     'where asiento.asiento_id = adetalle.asiento_id '
#                     'and adetalle.cuenta_id = cuenta.plan_id  '
#                     'and cuenta.tipo_cuenta_id = tcuenta.tipo_id '
#                     'and cuenta.codigo_plan=%s '            
#                     'and fecha between to_date(%s, \'DD/MM/YYYY\') and  to_date(%s, \'DD/MM/YYYY\') and asiento.anulado is not True '
#                     'ORDER BY asiento.fecha,asiento.codigo_asiento', (str(co), fecha_desde, fecha_hasta))
#     
#         ro = cursor.fetchall()
#         print ro
#                 
#                 
#             
#         for cuentas in ro:
#             saldo = saldo + float(cuentas[5])
#             concepto=""
#             html+='<tr><td>' + str(cuentas[7].encode('utf8'))+ '-' + str(cuentas[6].encode('utf8')) + '</td><td>' + str(cuentas[1]) + '</td><td>' + str(cuentas[0]) + '</td><td>' + str(cuentas[2].encode('utf8')) + '</td>'
#             html+='<td align="right">' + str("%2.2f" % cuentas[3]).replace('.', ',')+ '</td>'
#             html+='<td align="right">' +  str("%2.2f" % cuentas[4]).replace('.', ',')+'</td>'
#             html+='<td align="right"><b>' +  str("%2.2f" % saldo).replace('.', ',') + '</b></td><td>' + str(concepto.encode('utf8')) + '</td>'
#             
#             cursor = connection.cursor()
#             sql='select a.asiento_id,a.codigo_asiento,m.fecha_emision,m.numero_comprobante,m.proveedor_id,m.activo,m.monto from contabilidad_asiento a,movimiento m  where m.asiento_id=a.asiento_id and a.asiento_id='+str(cuentas[9])+' order by a.fecha;'
#             cursor.execute(sql)
#             rmovimiento = cursor.fetchall()
#             cadena_mov=''
#             for rc in rmovimiento:
#                 cadena_mov+='Mov'+str(rc[3])+'//'+str(rc[4])+'//'+str(rc[5])+'//'+str(rc[6])
#                     
#                     
#             html+='<td>'+str(cadena_mov)+'</td>'
#                 
#             sql1='select a.asiento_id,a.codigo_asiento,dc.fecha_emision,dc.id,dc.secuencial,dc.proveedor_id,dc.anulado from contabilidad_asiento a,documento_compra dc where dc.asiento_id=a.asiento_id and a.asiento_id='+str(cuentas[9])+' order by a.fecha;'
#             cursor.execute(sql1)
#             rcompra = cursor.fetchall()
#             cadena_comp=''
#             for c in rcompra:
#                 cadena_comp+='Compra'+str(c[3])+'//'+str(c[4])+'//'+str(c[5])+'//'+str(c[6])
#                     
#                     
#             html+='<td>'+str(cadena_comp)+'</td>'
#                 
#             html+='</tr>'
#             total_debito=total_debito+float(cuentas[3])
#             total_haber=total_haber+float(cuentas[4])
#             
#     
#                     
#             
#             
#         html+='</tbody>'
#     else:
#         raise Http404
# 
#     return HttpResponse(
#             html
#         )
#    