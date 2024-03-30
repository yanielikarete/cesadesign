# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
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
from django.contrib.auth import authenticate, login
# from login.lib.tools import Tools


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
# from config.models import Mensajes

from login.lib.tools import Tools
from django.contrib import auth
from contabilidad.models import *
from django.db.models import Sum
from datetime import datetime, date, time, timedelta
import calendar
# from config.models import Mensajes

from django.db import IntegrityError, transaction
from django.conf import settings
# Create your views here.

from django.db import IntegrityError, transaction
from django.db import connection, transaction

@login_required()
def RolesPagoView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.order_by('id')
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado, 'banco': banco,
                                                            'roles_pago': roles_pago,
                                                            'sueldos_unificados': sueldos_unificados, 'plan': plan,
                                                            'clasificacion': clasificacion}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado, 'banco': banco,
                                                            'roles_pago': roles_pago,
                                                            'sueldos_unificados': sueldos_unificados, 'plan': plan,
                                                            'clasificacion': clasificacion}, RequestContext(request))

@login_required()
def RolesPagoCuentasContablesListView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.all()
        return render_to_response('roles_pago/rolPagoCuentasContablesList.html', {'rol_cuentas': rol_cuentas},
                                  RequestContext(request))
    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        return render_to_response('roles_pago/rolPagoCuentasContablesList.html', {'rol_cuentas': rol_cuentas},
                                  RequestContext(request))

class RolesPagoCuentasContablesCreateView(ObjectCreateView):
    model = RolPagoCuentaContable
    form_class = RolPagoCuentaContableForm
    template_name = 'roles_pago/rolPagoCuentasContablecreate.html'
    url_success = 'roles-pago-cuentas-contables-list'
    url_success_other = 'roles-pago-cuentas-contables-create'
    url_cancel = 'roles-pago-cuentas-contables-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(RolesPagoCuentasContablesCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva cuenta."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def guardarCargoView(request):
    if request.method == 'POST':

        id_cargo = request.POST["id_cargo"]
        if id_cargo:
            nombre = request.POST["nombre"]
            sueldo = request.POST["salario_min_sectorial"]
            depart = request.POST["padre_id_cargo"]
            cargo = TipoEmpleado.objects.get(tipo_empleado_id=id_cargo)
            cargo.cargo_empleado = nombre
            cargo.sueldo = float(sueldo)
            cargo.departamento_id = depart
            cargo.updated_at = datetime.now()
            cargo.updated_by = request.user.get_full_name()
            cargo.save()

        else:
            nombre = request.POST["nombre"]
            sueldo = request.POST["salario_min_sectorial"]
            depart = request.POST["padre_id_cargo"]

            cargo = TipoEmpleado()
            cargo.cargo_empleado = nombre
            cargo.sueldo = float(sueldo)
            cargo.departamento_id = depart
            cargo.created_by = request.user.get_full_name()
            cargo.updated_by = request.user.get_full_name()
            cargo.created_at = datetime.now()
            cargo.updated_at = datetime.now()
            cargo.save()

        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/')


    else:
        id_cargo = request.POST["id_cargo"]
        nombre = request.POST["nombre"]
        sueldo = request.POST["salario_min_sectorial"]

        cargo = TipoEmpleado.objects.get(tipo_empleado_id=id_cargo)
        cargo.cargo_empleado = nombre
        cargo.sueldo = float(sueldo)
        cargo.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado}, RequestContext(request))

@login_required()
def guardarRolesView(request):
    if request.method == 'POST':
        mensual = request.POST.get("mensual", False)
        quincenal = request.POST.get("quincenal", False)
        dia_pago = request.POST["dia_pago"]
        porcentaje_primera_quincena = request.POST["porcentaje_primera_quincena"]
        porcentaje_iess = request.POST["porcentaje_iess"]
        porcentaje_ext_conyugal = request.POST["porcentaje_ext_conyugal"]
        cuenta_bancaria_rrhh = request.POST["cuenta_bancaria_rrhh"]

        rol = RolPagoConfiguraciones()
        rol.dia_pago = dia_pago
        rol.porcentaje_primera_quincena = porcentaje_primera_quincena
        rol.mensual = mensual
        rol.quincenal = quincenal
        rol.porcentaje_iess = porcentaje_iess
        rol.extension_conyugal_iess = porcentaje_ext_conyugal
        rol.banco_id = cuenta_bancaria_rrhh
        rol.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/')


    else:
        id_cargo = request.POST["id_cargo"]
        nombre = request.POST["nombre"]
        sueldo = request.POST["salario_min_sectorial"]

        cargo = TipoEmpleado.objects.get(tipo_empleado_id=id_cargo)
        cargo.cargo_empleado = nombre
        cargo.sueldo = float(sueldo)
        cargo.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado}, RequestContext(request))

@login_required()
def guardarDepartamentoView(request):
    if request.method == 'POST':

        id_departamento = request.POST["id_departamento"]
        if id_departamento:
            print('departamento1')
            nombre = request.POST["nombre_departamento"]
            cargo = Departamento.objects.get(id=id_departamento)
            cargo.nombre = nombre
            cargo.updated_at = datetime.now()
            cargo.updated_by = request.user.get_full_name()
            cargo.save()

        else:
            nombre = request.POST["nombre_departamento"]
            print('departamento2')
            cargo = Departamento()
            cargo.nombre = nombre
            cargo.created_by = request.user.get_full_name()
            cargo.updated_by = request.user.get_full_name()
            cargo.created_at = datetime.now()
            cargo.updated_at = datetime.now()
            cargo.save()

        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/')


    else:
        id_departamento = request.POST["id_departamento"]
        nombre = request.POST["nombre_departamento"]
        print('departamento3')
        cargo = Departamento.objects.get(id=id_departamento)
        cargo.nombre = nombre
        cargo.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado}, RequestContext(request))

@login_required()
def GenerarRolesPagoView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        contador = request.POST["columnas_receta_roles"]
        dc_id = SueldosUnificados.objects.last()

        rol = RolPago()
        rol.anio = anio
        rol.quincena = quincena
        rol.mes = mes
        rol.salario_base = dc_id.sueldo
        rol.created_by = request.user.get_full_name()
        rol.created_at = datetime.now()
        rol.updated_at = datetime.now()
        rol.salario_base = dc_id.sueldo
        rol.save()
        i = 0
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_empleado' + str(i) in request.POST:
                    detallecompra = RolPagoDetalle()
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.created_by = request.user.get_full_name()
                    detallecompra.empleado_id = request.POST["id_empleado" + str(i)]
                    detallecompra.ingresos = request.POST["pago_" + str(i) + "_total"]
                    detallecompra.egresos = request.POST["pago_" + str(i) + "_total_egresos"]
                    detallecompra.otros_ingresos = request.POST["pago_" + str(i) + "_otros_ingresos"]
                    detallecompra.otros_egresos = 0
                    detallecompra.dias = request.POST["pago_" + str(i) + "_dias"]

                    detallecompra.tipo_pago_id = request.POST["pago_" + str(i) + "_tipo_pago"]
                    detallecompra.numero_comprobante = request.POST["pago_" + str(i) + "_numero_comprobante"]
                    detallecompra.tipo_pago_id = request.POST["pago_" + str(i) + "_tipo_pago"]
                    detallecompra.banco_id = request.POST["pago_" + str(i) + "_cuenta_bancaria"]
                    detallecompra.descuento_dias = request.POST["pago_valor_" + str(i) + "_dias"]
                    detallecompra.total = request.POST["pago_" + str(i) + "_valor_a_recibir"]
                    detallecompra.rol_pago_id = rol.id
                    empleado_id=request.POST["id_empleado" + str(i)]
                    try:
                        empleado = Empleado.objects.get(empleado_id=empleado_id)
                    except Empleado.DoesNotExist:
                        empleado = None
            
                    if empleado:
                        if empleado.acumular_fondo_reserva:
                            detallecompra.pagar_fondo_reserva=True
                            
                        if empleado.acumular_decimo_tercero:
                            detallecompra.pagar_decimo_tercero=True
                            
                        if empleado.acumular_decimo_cuarto:
                            detallecompra.pagar_decimo_cuarto=True
                            
                        if empleado.acumular_iess_asumido:
                            detallecompra.pagar_iess_asumido=True
                            
                        if empleado.extension_conyugal:
                            detallecompra.pagar_extension_conyugal=True
                        
                        if empleado.asumir_impuesto_renta:
                            detallecompra.pagar_impuesto_renta=True
                        
                        
                        detallecompra.fecha_ini_reconocida=empleado.fecha_ini_reconocida

                    detallecompra.save()
                else:
                    print('entrosd')

        anio = Anio.objects.all()
        return render_to_response('roles_pago/roles.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,
                                   'empleados': empleados, 'anio': anio}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        anio=Anio.objects.all()
        return render_to_response('roles_pago/roles.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,
                                   'empleados': empleados, 'anio': anio}, RequestContext(request))

@login_required()
@csrf_exempt
def obtenerEmpleados(request):
    if request.method == 'POST':
        empleados = Empleado.objects.filter(activo=True).order_by('nombre_empleado')
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        print('post entro')
        try:
            rol = RolPago.objects.get(anio=anio, mes=mes)
        except RolPago.DoesNotExist:
            rol = None

        # if rol:
        #     html += '<tr><td colspan="8">Ya se genero ese rol</td></tr>'
        # else:
        #     for detal in empleados:
        #         i += 1
        #         ingresosPro = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
        #         if ingresosPro:
        #             for detali in ingresosPro:
        #                 try:
        #                     existe = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
        #                                                              empleado_id=detal.empleado_id,
        #                                                              tipo_ingreso_egreso_empleado_id=detali.tipo_ingreso_egreso_empleado_id,
        #                                                              ingresos_proyectados=True)
        #                 except IngresosRolEmpleado.DoesNotExist:
        #                     existe = None
        # 
        #                 if existe:
        #                     existe.valor = round(float(detali.valor_mensual), 2)
        #                     existe.valor_diario = round(float(detali.valor_diario), 2)
        #                     existe.valor_mensual = round(float(detali.valor_mensual), 2)
        #                     existe.nombre = detali.tipo_ingreso_egreso_empleado.nombre
        #                     existe.updated_by = request.user.get_full_name()
        #                     existe.updated_at = datetime.now()
        #                     existe.save()
        #                 else:
        #                     existeNew = IngresosRolEmpleado()
        #                     existeNew.quincena = quincena
        #                     existeNew.anio = anio
        #                     existeNew.mes = mes
        #                     existeNew.empleado_id = detal.empleado_id
        #                     existeNew.nombre = detali.tipo_ingreso_egreso_empleado
        #                     existeNew.tipo_ingreso_egreso_empleado_id = detali.tipo_ingreso_egreso_empleado_id
        #                     existeNew.valor = round(float(detali.valor_mensual), 2)
        #                     existeNew.valor_diario = round(float(detali.valor_diario), 2)
        #                     existeNew.valor_mensual = round(float(detali.valor_mensual), 2)
        #                     existeNew.ingresos_proyectados = True
        #                     existeNew.created_by = request.user.get_full_name()
        #                     existeNew.updated_by = request.user.get_full_name()
        #                     existeNew.created_at = datetime.now()
        #                     existeNew.updated_at = datetime.now()
        #                     existeNew.pagar = True
        #                     existeNew.save()
        # 
        #         egresosPro = EgresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
        #         if egresosPro:
        #             for detale in egresosPro:
        #                 try:
        #                     existeE = EgresosRolEmpleado.objects.get(anio=anio, mes=mes,
        #                                                              empleado_id=detal.empleado_id,
        #                                                              tipo_ingreso_egreso_empleado_id=detale.tipo_ingreso_egreso_empleado_id,
        #                                                              egresos_proyectados=True)
        #                 except EgresosRolEmpleado.DoesNotExist:
        #                     existeE = None
        # 
        #                 if existeE:
        #                     existeE.valor = round(float(detale.valor), 2)
        #                     existeE.updated_by = request.user.get_full_name()
        #                     existeE.updated_at = datetime.now()
        #                     existeE.nombre = detale.tipo_ingreso_egreso_empleado.nombre
        #                     existeE.save()
        #                 else:
        #                     existeENew = EgresosRolEmpleado()
        #                     #existeENew.quincena = quincena
        #                     existeENew.anio = anio
        #                     existeENew.mes = mes
        #                     existeENew.empleado_id = detal.empleado_id
        #                     existeENew.tipo_ingreso_egreso_empleado_id = detale.tipo_ingreso_egreso_empleado_id
        #                     existeENew.valor = round(float(detale.valor), 2)
        #                     existeENew.egresos_proyectados = True
        #                     existeENew.nombre = detale.tipo_ingreso_egreso_empleado.nombre
        #                     existeENew.created_by = request.user.get_full_name()
        #                     existeENew.updated_by = request.user.get_full_name()
        #                     existeENew.created_at = datetime.now()
        #                     existeENew.updated_at = datetime.now()
        #                     existeENew.save()
        # 
        #         try:
        #             sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
        #                                                      empleado_id=detal.empleado_id,
        #                                                      tipo_ingreso_egreso_empleado_id=24)
        #         except IngresosRolEmpleado.DoesNotExist:
        #             sueldo = 0
        #         
        #         
        #         
        #         
        # 
        #         ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
        # 
        #         if detal.acumular_fondo_reserva:
        #             otros_ingresos_fr = OtrosIngresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=7)
        #             if otros_ingresos_fr:
        #                 print('hola1')
        #             else:
        #                 comprasdetalle = OtrosIngresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 7
        #                 if ingresos['valor__sum']:
        #                     comprasdetalle.valor = round(float((ingresos['valor__sum'])/12),2)
        #                     #comprasdetalle.valor = float((ingresos['valor__sum'] ) * 0.0833)
        #                     #comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
        # 
        # 
        #                 comprasdetalle.nombre = 'FONDOS DE RESERVA'
        #                 comprasdetalle.anio = anio
        #                 comprasdetalle.mes = mes
        #                 #comprasdetalle.quincena = quincena
        #                 comprasdetalle.empleado_id = detal.empleado_id
        #                 comprasdetalle.save()
        # 
        #         if detal.acumular_decimo_tercero:
        #             otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=8)
        #             if otros_ingresos_dt:
        #                 print('hola2')
        #             else:
        #                 comprasdetalle = OtrosIngresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 8
        #                 if ingresos['valor__sum']:
        #                     comprasdetalle.valor = round(float(ingresos['valor__sum'] / 24),2)
        #                 comprasdetalle.nombre = ' DECIMO 3ER SUELDO'
        #                 comprasdetalle.anio = anio
        #                 comprasdetalle.mes = mes
        #                 #comprasdetalle.quincena = quincena
        #                 comprasdetalle.empleado_id = detal.empleado_id
        #                 comprasdetalle.save()
        # 
        #         if detal.acumular_decimo_cuarto:
        #             dc_id = SueldosUnificados.objects.last()
        #             print('sueldo unificado' + str(dc_id.sueldo))
        #             otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=9)
        #             if otros_ingresos_dc:
        #                 print('hola3')
        #             else:
        #                 comprasdetalle = OtrosIngresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 9
        #                 comprasdetalle.valor = round(float(dc_id.sueldo / 24),2)
        #                 comprasdetalle.nombre = ' DECIMO 4TO SUELDO'
        #                 comprasdetalle.anio = anio
        #                 comprasdetalle.mes = mes
        #                 #comprasdetalle.quincena = quincena
        #                 comprasdetalle.empleado_id = detal.empleado_id
        #                 comprasdetalle.save()
        #         if detal.acumular_iess_asumido:
        #             otros_ingresos_ia = OtrosIngresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=27)
        #             if otros_ingresos_ia:
        #                 print('hola4')
        #             else:
        #                 comprasdetalle = OtrosIngresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 27
        #                 if ingresos['valor__sum']:
        #                     #comprasdetalle.valor = float((ingresos['valor__sum'] / 10.5816) / 2)
        #                     comprasdetalle.valor = round(float((ingresos['valor__sum'] / 10.5816) ),2)
        #                 comprasdetalle.nombre = 'IESS ASUMIDO'
        #                 comprasdetalle.anio = anio
        #                 comprasdetalle.mes = mes
        #                 #comprasdetalle.quincena = quincena
        #                 comprasdetalle.empleado_id = detal.empleado_id
        #                 comprasdetalle.save()
        #         if detal.asumir_impuesto_renta:
        #             otros_ingresos_ir = OtrosIngresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=28)
        #             if otros_ingresos_ir:
        #                 print('hola5')
        #             else:
        #                 comprasdetalle = OtrosIngresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 28
        #                 comprasdetalle.valor = 0
        #                 comprasdetalle.nombre = 'IR ASUMIDO'
        #                 comprasdetalle.anio = anio
        #                 comprasdetalle.mes = mes
        #                 #comprasdetalle.quincena = quincena
        #                 comprasdetalle.empleado_id = detal.empleado_id
        #                 comprasdetalle.save()
        # 
        #         if detal.aportacion_conyugal:
        #             otros_egresos_esposa = EgresosRolEmpleado.objects.filter(
        #                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #                 tipo_ingreso_egreso_empleado_id=30)
        #             if otros_egresos_esposa:
        #                 print('hola7')
        #             else:
        #                 comprasdetalle = EgresosRolEmpleado()
        #                 comprasdetalle.updated_by = request.user.get_full_name()
        #                 comprasdetalle.tipo_ingreso_egreso_empleado_id = 30
        #                 if ingresos['valor__sum']:
        #                     #comprasdetalle.valor = float((ingresos['valor__sum'] * 0.0341) / 2)
        #                     comprasdetalle.valor = round(float((ingresos['valor__sum'] * 0.0341) ),2)
        #                     comprasdetalle.nombre = 'DESCUENTO 3.41%'
        #                     comprasdetalle.anio = anio
        #                     comprasdetalle.mes = mes
        #                     #comprasdetalle.quincena = quincena
        #                     comprasdetalle.empleado_id = detal.empleado_id
        #                     comprasdetalle.save()
        # 
        #         otros_egresos_nueve = EgresosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
        #             tipo_ingreso_egreso_empleado_id=29)
        #         if otros_egresos_nueve:
        #             print('hola6')
        #         else:
        # 
        #             comprasdetalle = EgresosRolEmpleado()
        #             comprasdetalle.updated_by = request.user.get_full_name()
        #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 29
        #             if ingresos['valor__sum']:
        #                 print('sueldoa' + str(ingresos['valor__sum']))
        #                 comprasdetalle.valor = round(float((ingresos['valor__sum'] * 0.0945)),2)
        #                 calc = float((ingresos['valor__sum'] * 0.0945))
        #                 print('egresos' + str(calc)+'VALOR DEL SUELDO'+str(ingresos['valor__sum']))
        #             comprasdetalle.nombre = 'DESCUENTO 9.45%'
        #             comprasdetalle.anio = anio
        #             comprasdetalle.mes = mes
        #             #comprasdetalle.quincena = quincena
        #             comprasdetalle.empleado_id = detal.empleado_id
        #             comprasdetalle.save()
        # 
        #         otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
        # 
        #         egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
        #         otros_egresos = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
        #         dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             tipo_ausencia_id=3).aggregate(Sum('dias'))
        #         valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
        #             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))
        #         faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             tipo_ausencia_id=3).aggregate(Sum('valor'))
        #         faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
        #         atrasos_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             tipo_ausencia_id=5).aggregate(Sum('valor'))
        #         atrasos_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             cargar_vacaciones=False).filter(tipo_ausencia_id=4).aggregate(Sum('valor'))
        #         vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
        #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
        #             cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
        # 
        #         total_otros_ingresos = 0
        #         total_otros_egresos = 0
        #         total_egresos = 0
        #         total_dias = 0
        #         total_desc = 0
        #         dias_trabajados = 15
        #         total_valor_dias = 0
        # 
        #         if ingresos['valor__sum']:
        #             total_ingresos = float(ingresos['valor__sum'])
        #         else:
        #             total_ingresos = 0
        # 
        #         if otros_ingresos['valor__sum']:
        #             total_otros_ingresos = float(otros_ingresos['valor__sum'])
        #             print('ENTRO A OTROS INGRESOS'+str(detal.empleado_id))
        #         else:
        #             total_otros_ingresos = 0
        # 
        #         if egresos['valor__sum']:
        #             total_egresos = float(egresos['valor__sum'])
        # 
        # 
        #         else:
        #             total_egresos = 0
        # 
        #         total_egreso_neto = float(total_egresos)
        #         mensaj=''
        #         mensaj+='Egresos' + str(total_egresos)
        #         if faltas_justificadas_valor['valor__sum']:
        #             total_egresos = float(faltas_justificadas_valor['valor__sum'] + total_egresos)
        #             mensaj+='Faltas justificadas'+ str(faltas_justificadas_valor['valor__sum'])
        #         if atrasos_justificadas_valor['valor__sum']:
        #             total_egresos = float(atrasos_justificadas_valor['valor__sum'] + total_egresos)
        #             mensaj += 'Atrasos justificadas' + str( atrasos_justificadas_valor['valor__sum'])
        #         if atrasos_injustificadas_valor['valor__sum']:
        #             total_egresos = float(atrasos_injustificadas_valor['valor__sum'] + total_egresos)
        #             mensaj += 'Atrasos injustificadas' + str(atrasos_injustificadas_valor['valor__sum'])
        # 
        #         if vacaciones_justificadas_valor['valor__sum']:
        # 
        #             total_egresos = float(vacaciones_justificadas_valor['valor__sum'] + total_egresos)
        #             mensaj += 'Vacaciones justificadas' + str(vacaciones_justificadas_valor['valor__sum'])
        # 
        # 
        #         if otros_egresos['valor__sum']:
        #             print('otros_egresos' + str(otros_egresos['valor__sum']))
        #             total_otros_egresos = float(otros_egresos['valor__sum'])
        #             mensaj += 'Otros Egresos' + str(total_otros_egresos)
        # 
        #         else:
        #             total_otros_egresos = 0
        #         total_ingreso_neto = float(total_ingresos)
        # 
        #         if dias['dias__sum']:
        #             total_dias = float(dias['dias__sum'])
        #             dias_trabajados = float((dias_trabajados * 8) - total_dias) / 8
        # 
        #             if faltas_injustificadas_valor['valor__sum']:
        #                 total_desc = float(faltas_injustificadas_valor['valor__sum'])
        #             else:
        #                 total_desc = 0
        #             total_ingresos = float(total_ingresos - (total_desc))
        #         if valor_dias['valor__sum']:
        #             total_valor_dias = float(valor_dias['valor__sum'])
        #             # total_ingresos=float(total_ingresos-(valor_diario['valor_diario__sum']*total_dias))
        # 
        #         total = float(total_ingresos + total_otros_ingresos - total_egresos - total_otros_egresos)
        #         html += ' <tr><td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
        #             i) + '" id="id_empleado' + str(i) + '" value="' + str(detal.empleado_id) + '"/></td>'
        #         # html+='<td class="text-center"><div class="checkbox custom-checkbox custom-checkbox-primary"><input class="seleccionar" data-contextual="info" data-target="tr" data-toggle="selectrow" id="id_pago_'+str(i)+'_seleccionado" name="pago_'+str(i)+'_seleccionado" type="checkbox"><label for="id_pago_'+str(i)+'_seleccionado"></label></div></td>'
        #         html += '<td><input class="form-control input-sm" id="id_cedula_' + str(
        #             i) + '" maxlength="10" name="cedula_' + str(i) + '" readonly="readonly" size="10" value="' + str(
        #             detal.cedula_empleado) + '" type="text"></td>'
        #         html += '<td><input class="form-control input-sm" id="id_pago_' + str(
        #             i) + '_razon_social" maxlength="300" name="pago_' + str(
        #             i) + '_razon_social" readonly="readonly" size="31" value="' + str(
        #             detal.nombre_empleado.encode('utf8')) + '" type="text"><input id="id_pago_' + str(
        #             i) + '_idpersona" name="pago_' + str(i) + '_idpersona" value="893721" type="hidden"></td>'
        #         html += '<td><input class="form-control input-sm" id="id_area_' + str(
        #             i) + '" maxlength="10" name="area_' + str(i) + '" readonly="readonly" size="10" value="' + str(
        #             detal.departamento) + '" type="text"></td>'
        #         html += '<td><input class="form-control input-sm" id="id_cargo_' + str(
        #             i) + '" maxlength="10" name="cargo_' + str(i) + '" readonly="readonly" size="10" value="' + str(
        #             detal.tipo_empleado) + '" type="text"></td>'
        #         if sueldo:
        #             html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
        #                 i) + '" maxlength="10" name="sueldo_' + str(
        #                 i) + '" readonly="readonly" size="10" value="' + str(
        #                 sueldo.valor_mensual) + '" type="text"></td>'
        #         else:
        #             html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
        #                 i) + '" maxlength="10" name="sueldo_' + str(
        #                 i) + '" readonly="readonly" size="10" value="' + str(sueldo) + '" type="text"></td>'
        # 
        #         html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_diasagregados_ad()"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_dias" name="pago_' + str(i) + '_dias" readonly="readonly" size="5" value="' + str(
        #             dias_trabajados) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_dias_valor" name="pago_valor_' + str(i) + '_dias" readonly="readonly" value="' + str(
        #             total_valor_dias) + '" type="hidden"></a><span class="input-group-btn input"><a href="javascript: dias_ad(' + str(
        #             i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
        #         html += '<td><a href="javascript: ingresos(' + str(
        #             i) + ')" data-toggle="modal"><input class="form-control input-sm" id="id_pago_' + str(
        #             i) + '_total" name="pago_' + str(
        #             i) + '_total" readonly="readonly" size="7" style="text-align:right;" value="' + str(
        #             total_ingresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
        #             i) + '_ingreso" name="pago_' + str(
        #             i) + '_ingreso" readonly="readonly" size="7" style="text-align:right;" value="' + str(
        #             total_ingreso_neto) + '" type="hidden"></td>'
        #         html += '<td><div class="input-group input-group-sm"><a href="#"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_otros_ingresos" maxlength="15" name="pago_' + str(
        #             i) + '_otros_ingresos" readonly="readonly" size="6" value="' + str(
        #             total_otros_ingresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: ingresos_ad(' + str(
        #             i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
        #         html += '<td><a href="javascript: egresos(' + str(
        #             i) + ')" data-toggle="modal"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_total_egresos" maxlength="15" name="pago_' + str(
        #             i) + '_total_egresos" readonly="readonly" size="6" value="' + str(
        #             total_egresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
        #             i) + 'egreso_neto" name="pago_' + str(
        #             i) + 'egreso_neto" readonly="readonly" size="7" style="text-align:right;" value="' + str(
        #             total_egreso_neto) + '" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_otros_egresos" maxlength="10" name="pago_' + str(
        #             i) + '_otros_egresos" readonly="readonly" size="6" value="0" type="hidden"></td>'
        #         # #html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_descuentos()"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #         #     i) + '_otros_egresos" maxlength="10" name="pago_' + str(
        #         #     i) + '_otros_egresos" readonly="readonly" size="6" value="' + str(
        #         #     total_otros_egresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: egresos_ad(' + str(
        #         #     i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
        # 
        #         html += '<td><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_valor_a_recibir" name="pago_' + str(
        #             i) + '_valor_a_recibir" readonly="readonly" size="10" value="' + str(
        #             total) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
        #             i) + '_valor_a_recibir_hidden" name="pago_' + str(
        #             i) + '_valor_a_recibir_hidden" readonly="readonly" size="10" value="231.00" type="hidden"></td>'
        #         html += '<td><select class="tipopago form-control input-sm" id="id_pago_' + str(
        #             i) + '_tipo_pago" maxlength="15" name="pago_' + str(
        #             i) + '_tipo_pago" onchange="mostrarComprobante(this);">'
        #         for am in tipopago:
        #             html += '<option value="' + str(am.id) + '"'
        #             if am.id == detal.forma_pago_empleado_id:
        #                 html += ' selected="selected"'
        #             html += ' >' + str(am.nombre) + '</option>'
        #         html += '</select><div class="num_comprobante"><div class="pull-right"><input placeholder="# Cheque" class="form-control input-sm" id="id_pago_' + str(
        #             i) + '_numero_comprobante" maxlength="40" name="pago_' + str(
        #             i) + '_numero_comprobante" size="12" type="text"></div></div></td>'
        #         html += '<td><select class="select-input form-control input-sm" id="id_pago_' + str(
        #             i) + '_cuenta_bancaria" name="pago_' + str(i) + '_cuenta_bancaria">'
        #         for b in banco:
        #             bnombre = (b.nombre).encode('ascii', 'ignore').decode('ascii')
        #             html += '<option value="' + str(b.id) + '"'
        #             if b.id == detal.banco_id:
        #                 html += ' selected="selected"'
        #             html += ' >' + str(bnombre) + '</option>'
        #         html += '</select></td></tr>'
        #         final_ingresos = final_ingresos + total_ingresos
        #         final_otros_ingresos = final_otros_ingresos + total_otros_ingresos
        #         final_egresos = final_egresos + total_egresos
        #         final_otros_egresos = final_otros_egresos + total_otros_egresos
        #         final_total = final_total + total
        # 
        #     html += '<tr><td></td><td></td><td></td><td style="text-align:right">' + str(
        #         final_ingresos) + '</td><td >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
        #         final_otros_ingresos) + '</td><td style="text-align:right">' + str(
        #         final_egresos) + '</td><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
        #         final_otros_egresos) + '</td><td></td><td style="text-align:right">' + str(
        #         final_total) + '</td><td></td><td></td></tr>'
        #     html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
        #         i) + '" />'
        return HttpResponse(
            html
        )
    else:
        print('get entro')
        empleados = Empleado.objects.filter(activo=True).order_by('nombre_empleado')
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        mes = 7
        anio = "2016"
        quincena = "1Q"
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        print('post entro')
        try:
            rol = RolPago.objects.get(anio=anio, mes=mes)
        except RolPago.DoesNotExist:
            rol = None

        # if rol:
        #     html += '<tr><td colspan="8">Ya se genero ese rol</td></tr>'
        # else:
            # for detal in empleados:
            #     i += 1
            #     ingresosPro = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
            #     if ingresosPro:
            #         for detali in ingresosPro:
            #             try:
            #                 existe = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
            #                                                          empleado_id=detal.empleado_id,
            #                                                          tipo_ingreso_egreso_empleado_id=detali.tipo_ingreso_egreso_empleado_id,
            #                                                          ingresos_proyectados=True)
            #             except IngresosRolEmpleado.DoesNotExist:
            #                 existe = None
            # 
            #             if existe:
            #                 existe.valor = round(float(detali.valor_mensual), 2)
            #                 existe.valor_diario = round(float(detali.valor_diario), 2)
            #                 existe.valor_mensual = round(float(detali.valor_mensual), 2)
            #                 existe.nombre = detali.tipo_ingreso_egreso_empleado.nombre
            #                 existe.updated_by = request.user.get_full_name()
            #                 existe.updated_at = datetime.now()
            #                 existe.save()
            #             else:
            #                 existeNew = IngresosRolEmpleado()
            #                 existeNew.quincena = quincena
            #                 existeNew.anio = anio
            #                 existeNew.mes = mes
            #                 existeNew.empleado_id = detal.empleado_id
            #                 existeNew.nombre = detali.tipo_ingreso_egreso_empleado
            #                 existeNew.tipo_ingreso_egreso_empleado_id = detali.tipo_ingreso_egreso_empleado_id
            #                 existeNew.valor = round(float(detali.valor_mensual), 2)
            #                 existeNew.valor_diario = round(float(detali.valor_diario), 2)
            #                 existeNew.valor_mensual = round(float(detali.valor_mensual), 2)
            #                 existeNew.ingresos_proyectados = True
            #                 existeNew.created_by = request.user.get_full_name()
            #                 existeNew.updated_by = request.user.get_full_name()
            #                 existeNew.created_at = datetime.now()
            #                 existeNew.updated_at = datetime.now()
            #                 existeNew.pagar = True
            #                 existeNew.save()
            # 
            #     egresosPro = EgresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
            #     if egresosPro:
            #         for detale in egresosPro:
            #             try:
            #                 existeE = EgresosRolEmpleado.objects.get(anio=anio, mes=mes,
            #                                                          empleado_id=detal.empleado_id,
            #                                                          tipo_ingreso_egreso_empleado_id=detale.tipo_ingreso_egreso_empleado_id,
            #                                                          egresos_proyectados=True)
            #             except EgresosRolEmpleado.DoesNotExist:
            #                 existeE = None
            # 
            #             if existeE:
            #                 existeE.valor = round(float(detale.valor), 2)
            #                 existeE.updated_by = request.user.get_full_name()
            #                 existeE.updated_at = datetime.now()
            #                 existeE.nombre = detale.tipo_ingreso_egreso_empleado.nombre
            #                 existeE.save()
            #             else:
            #                 existeENew = EgresosRolEmpleado()
            #                 # existeENew.quincena = quincena
            #                 existeENew.anio = anio
            #                 existeENew.mes = mes
            #                 existeENew.empleado_id = detal.empleado_id
            #                 existeENew.tipo_ingreso_egreso_empleado_id = detale.tipo_ingreso_egreso_empleado_id
            #                 existeENew.valor = round(float(detale.valor), 2)
            #                 existeENew.egresos_proyectados = True
            #                 existeENew.nombre = detale.tipo_ingreso_egreso_empleado.nombre
            #                 existeENew.created_by = request.user.get_full_name()
            #                 existeENew.updated_by = request.user.get_full_name()
            #                 existeENew.created_at = datetime.now()
            #                 existeENew.updated_at = datetime.now()
            #                 existeENew.save()
            # 
            #     try:
            #         sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
            #                                                  empleado_id=detal.empleado_id,
            #                                                  tipo_ingreso_egreso_empleado_id=24)
            #     except IngresosRolEmpleado.DoesNotExist:
            #         sueldo = 0
            # 
            #     ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # 
            #     if detal.acumular_fondo_reserva:
            #         otros_ingresos_fr = OtrosIngresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=7)
            #         if otros_ingresos_fr:
            #             print('hola1')
            #         else:
            #             comprasdetalle = OtrosIngresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 7
            #             if ingresos['valor__sum']:
            #                 comprasdetalle.valor = round(float((ingresos['valor__sum']) / 12), 2)
            #                 # comprasdetalle.valor = float((ingresos['valor__sum'] ) * 0.0833)
            #                 # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
            # 
            #             comprasdetalle.nombre = 'FONDOS DE RESERVA'
            #             comprasdetalle.anio = anio
            #             comprasdetalle.mes = mes
            #             # comprasdetalle.quincena = quincena
            #             comprasdetalle.empleado_id = detal.empleado_id
            #             comprasdetalle.save()
            # 
            #     if detal.acumular_decimo_tercero:
            #         otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=8)
            #         if otros_ingresos_dt:
            #             print('hola2')
            #         else:
            #             comprasdetalle = OtrosIngresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 8
            #             if ingresos['valor__sum']:
            #                 comprasdetalle.valor = round(float(ingresos['valor__sum'] / 24), 2)
            #             comprasdetalle.nombre = ' DECIMO 3ER SUELDO'
            #             comprasdetalle.anio = anio
            #             comprasdetalle.mes = mes
            #             # comprasdetalle.quincena = quincena
            #             comprasdetalle.empleado_id = detal.empleado_id
            #             comprasdetalle.save()
            # 
            #     if detal.acumular_decimo_cuarto:
            #         dc_id = SueldosUnificados.objects.last()
            #         print('sueldo unificado' + str(dc_id.sueldo))
            #         otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=9)
            #         if otros_ingresos_dc:
            #             print('hola3')
            #         else:
            #             comprasdetalle = OtrosIngresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 9
            #             comprasdetalle.valor = round(float(dc_id.sueldo / 24), 2)
            #             comprasdetalle.nombre = ' DECIMO 4TO SUELDO'
            #             comprasdetalle.anio = anio
            #             comprasdetalle.mes = mes
            #             # comprasdetalle.quincena = quincena
            #             comprasdetalle.empleado_id = detal.empleado_id
            #             comprasdetalle.save()
            #     if detal.acumular_iess_asumido:
            #         otros_ingresos_ia = OtrosIngresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=27)
            #         if otros_ingresos_ia:
            #             print('hola4')
            #         else:
            #             comprasdetalle = OtrosIngresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 27
            #             if ingresos['valor__sum']:
            #                 # comprasdetalle.valor = float((ingresos['valor__sum'] / 10.5816) / 2)
            #                 comprasdetalle.valor = float((ingresos['valor__sum'] / 10.5816))
            #             comprasdetalle.nombre = 'IESS ASUMIDO'
            #             comprasdetalle.anio = anio
            #             comprasdetalle.mes = mes
            #             # comprasdetalle.quincena = quincena
            #             comprasdetalle.empleado_id = detal.empleado_id
            #             comprasdetalle.save()
            #     if detal.asumir_impuesto_renta:
            #         otros_ingresos_ir = OtrosIngresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=28)
            #         if otros_ingresos_ir:
            #             print('hola5')
            #         else:
            #             comprasdetalle = OtrosIngresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 28
            #             comprasdetalle.valor = 0
            #             comprasdetalle.nombre = 'IR ASUMIDO'
            #             comprasdetalle.anio = anio
            #             comprasdetalle.mes = mes
            #             # comprasdetalle.quincena = quincena
            #             comprasdetalle.empleado_id = detal.empleado_id
            #             comprasdetalle.save()
            # 
            #     if detal.aportacion_conyugal:
            #         otros_egresos_esposa = EgresosRolEmpleado.objects.filter(
            #             anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #             tipo_ingreso_egreso_empleado_id=30)
            #         if otros_egresos_esposa:
            #             print('hola7')
            #         else:
            #             comprasdetalle = EgresosRolEmpleado()
            #             comprasdetalle.updated_by = request.user.get_full_name()
            #             comprasdetalle.tipo_ingreso_egreso_empleado_id = 30
            #             if ingresos['valor__sum']:
            #                 # comprasdetalle.valor = float((ingresos['valor__sum'] * 0.0341) / 2)
            #                 comprasdetalle.valor = round(float((ingresos['valor__sum'] * 0.0341)), 2)
            #                 comprasdetalle.nombre = 'DESCUENTO 3.41%'
            #                 comprasdetalle.anio = anio
            #                 comprasdetalle.mes = mes
            #                 # comprasdetalle.quincena = quincena
            #                 comprasdetalle.empleado_id = detal.empleado_id
            #                 comprasdetalle.save()
            # 
            #     otros_egresos_nueve = EgresosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
            #         tipo_ingreso_egreso_empleado_id=29)
            #     if otros_egresos_nueve:
            #         print('hola6')
            #     else:
            # 
            #         comprasdetalle = EgresosRolEmpleado()
            #         comprasdetalle.updated_by = request.user.get_full_name()
            #         comprasdetalle.tipo_ingreso_egreso_empleado_id = 29
            #         if ingresos['valor__sum']:
            #             print('sueldoa' + str(ingresos['valor__sum']))
            #             comprasdetalle.valor = round(float((ingresos['valor__sum'] * 0.0945)), 2)
            #             calc = float((ingresos['valor__sum'] * 0.0945))
            #             print('egresos' + str(calc) + 'VALOR DEL SUELDO' + str(ingresos['valor__sum']))
            #         comprasdetalle.nombre = 'DESCUENTO 9.45%'
            #         comprasdetalle.anio = anio
            #         comprasdetalle.mes = mes
            #         # comprasdetalle.quincena = quincena
            #         comprasdetalle.empleado_id = detal.empleado_id
            #         comprasdetalle.save()
            # 
            #     otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # 
            #     egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
            #     otros_egresos = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
            #     dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         tipo_ausencia_id=3).aggregate(Sum('dias'))
            #     valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #         mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))
            #     faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         tipo_ausencia_id=3).aggregate(Sum('valor'))
            #     faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
            #     atrasos_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         tipo_ausencia_id=5).aggregate(Sum('valor'))
            #     atrasos_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         cargar_vacaciones=False).filter(tipo_ausencia_id=4).aggregate(Sum('valor'))
            #     vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
            #         anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #         cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
            # 
            #     total_otros_ingresos = 0
            #     total_otros_egresos = 0
            #     total_egresos = 0
            #     total_dias = 0
            #     total_desc = 0
            #     dias_trabajados = 15
            #     total_valor_dias = 0
            # 
            #     if ingresos['valor__sum']:
            #         total_ingresos = float(ingresos['valor__sum'])
            #     else:
            #         total_ingresos = 0
            # 
            #     if otros_ingresos['valor__sum']:
            #         total_otros_ingresos = float(otros_ingresos['valor__sum'])
            #     else:
            #         total_otros_ingresos = 0
            # 
            #     if egresos['valor__sum']:
            #         total_egresos = float(egresos['valor__sum'])
            # 
            # 
            #     else:
            #         total_egresos = 0
            # 
            #     total_egreso_neto = float(total_egresos)
            #     mensaj = ''
            #     mensaj += 'Egresos' + str(total_egresos)
            #     if faltas_justificadas_valor['valor__sum']:
            #         total_egresos = float(faltas_justificadas_valor['valor__sum'] + total_egresos)
            #         mensaj += 'Faltas justificadas' + str(faltas_justificadas_valor['valor__sum'])
            #     if atrasos_justificadas_valor['valor__sum']:
            #         total_egresos = float(atrasos_justificadas_valor['valor__sum'] + total_egresos)
            #         mensaj += 'Atrasos justificadas' + str(atrasos_justificadas_valor['valor__sum'])
            #     if atrasos_injustificadas_valor['valor__sum']:
            #         total_egresos = float(atrasos_injustificadas_valor['valor__sum'] + total_egresos)
            #         mensaj += 'Atrasos injustificadas' + str(atrasos_injustificadas_valor['valor__sum'])
            # 
            #     if vacaciones_justificadas_valor['valor__sum']:
            #         total_egresos = float(vacaciones_justificadas_valor['valor__sum'] + total_egresos)
            #         mensaj += 'Vacaciones justificadas' + str(vacaciones_justificadas_valor['valor__sum'])
            # 
            #     if otros_egresos['valor__sum']:
            #         print('otros_egresos' + str(otros_egresos['valor__sum']))
            #         total_otros_egresos = float(otros_egresos['valor__sum'])
            #         mensaj += 'Otros Egresos' + str(total_otros_egresos)
            # 
            #     else:
            #         total_otros_egresos = 0
            #     total_ingreso_neto = float(total_ingresos)
            # 
            #     if dias['dias__sum']:
            #         total_dias = float(dias['dias__sum'])
            #         dias_trabajados = float((dias_trabajados * 8) - total_dias) / 8
            # 
            #         if faltas_injustificadas_valor['valor__sum']:
            #             total_desc = float(faltas_injustificadas_valor['valor__sum'])
            #         else:
            #             total_desc = 0
            #         total_ingresos = float(total_ingresos - (total_desc))
            #     if valor_dias['valor__sum']:
            #         total_valor_dias = float(valor_dias['valor__sum'])
            #         # total_ingresos=float(total_ingresos-(valor_diario['valor_diario__sum']*total_dias))
            # 
            #     total = float(total_ingresos + total_otros_ingresos - total_egresos - total_otros_egresos)
            #     html += ' <tr><td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
            #         i) + '" id="id_empleado' + str(i) + '" value="' + str(detal.empleado_id) + '"/></td>'
            #     # html+='<td class="text-center"><div class="checkbox custom-checkbox custom-checkbox-primary"><input class="seleccionar" data-contextual="info" data-target="tr" data-toggle="selectrow" id="id_pago_'+str(i)+'_seleccionado" name="pago_'+str(i)+'_seleccionado" type="checkbox"><label for="id_pago_'+str(i)+'_seleccionado"></label></div></td>'
            #     html += '<td><input class="form-control input-sm" id="id_cedula_' + str(
            #         i) + '" maxlength="10" name="cedula_' + str(i) + '" readonly="readonly" size="10" value="' + str(
            #         detal.cedula_empleado) + '" type="text"></td>'
            #     html += '<td><input class="form-control input-sm" id="id_pago_' + str(
            #         i) + '_razon_social" maxlength="300" name="pago_' + str(
            #         i) + '_razon_social" readonly="readonly" size="31" value="' + str(
            #         detal.nombre_empleado.encode('utf8')) + '" type="text"><input id="id_pago_' + str(
            #         i) + '_idpersona" name="pago_' + str(i) + '_idpersona" value="893721" type="hidden"></td>'
            #     html += '<td><input class="form-control input-sm" id="id_area_' + str(
            #         i) + '" maxlength="10" name="area_' + str(i) + '" readonly="readonly" size="10" value="' + str(
            #         detal.departamento) + '" type="text"></td>'
            #     html += '<td><input class="form-control input-sm" id="id_cargo_' + str(
            #         i) + '" maxlength="10" name="cargo_' + str(i) + '" readonly="readonly" size="10" value="' + str(
            #         detal.tipo_empleado) + '" type="text"></td>'
            #     if sueldo:
            #         html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
            #             i) + '" maxlength="10" name="sueldo_' + str(
            #             i) + '" readonly="readonly" size="10" value="' + str(
            #             sueldo.valor_mensual) + '" type="text"></td>'
            #     else:
            #         html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
            #             i) + '" maxlength="10" name="sueldo_' + str(
            #             i) + '" readonly="readonly" size="10" value="' + str(sueldo) + '" type="text"></td>'
            # 
            #     html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_diasagregados_ad()"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_dias" name="pago_' + str(i) + '_dias" readonly="readonly" size="5" value="' + str(
            #         dias_trabajados) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_dias_valor" name="pago_valor_' + str(i) + '_dias" readonly="readonly" value="' + str(
            #         total_valor_dias) + '" type="hidden"></a><span class="input-group-btn input"><a href="javascript: dias_ad(' + str(
            #         i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
            #     html += '<td><a href="javascript: ingresos(' + str(
            #         i) + ')" data-toggle="modal"><input class="form-control input-sm" id="id_pago_' + str(
            #         i) + '_total" name="pago_' + str(
            #         i) + '_total" readonly="readonly" size="7" style="text-align:right;" value="' + str(
            #         total_ingresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
            #         i) + '_ingreso" name="pago_' + str(
            #         i) + '_ingreso" readonly="readonly" size="7" style="text-align:right;" value="' + str(
            #         total_ingreso_neto) + '" type="hidden"></td>'
            #     html += '<td><div class="input-group input-group-sm"><a href="#"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_otros_ingresos" maxlength="15" name="pago_' + str(
            #         i) + '_otros_ingresos" readonly="readonly" size="6" value="' + str(
            #         total_otros_ingresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: ingresos_ad(' + str(
            #         i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
            #     html += '<td><a href="javascript: egresos(' + str(
            #         i) + ')" data-toggle="modal"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_total_egresos" maxlength="15" name="pago_' + str(
            #         i) + '_total_egresos" readonly="readonly" size="6" value="' + str(
            #         total_egresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
            #         i) + 'egreso_neto" name="pago_' + str(
            #         i) + 'egreso_neto" readonly="readonly" size="7" style="text-align:right;" value="' + str(
            #         total_egreso_neto) + '" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_otros_egresos" maxlength="10" name="pago_' + str(
            #         i) + '_otros_egresos" readonly="readonly" size="6" value="0" type="hidden"></td>'
            #     # #html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_descuentos()"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #     #     i) + '_otros_egresos" maxlength="10" name="pago_' + str(
            #     #     i) + '_otros_egresos" readonly="readonly" size="6" value="' + str(
            #     #     total_otros_egresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: egresos_ad(' + str(
            #     #     i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
            # 
            #     html += '<td><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_valor_a_recibir" name="pago_' + str(
            #         i) + '_valor_a_recibir" readonly="readonly" size="10" value="' + str(
            #         total) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
            #         i) + '_valor_a_recibir_hidden" name="pago_' + str(
            #         i) + '_valor_a_recibir_hidden" readonly="readonly" size="10" value="231.00" type="hidden"></td>'
            #     html += '<td><select class="tipopago form-control input-sm" id="id_pago_' + str(
            #         i) + '_tipo_pago" maxlength="15" name="pago_' + str(
            #         i) + '_tipo_pago" onchange="mostrarComprobante(this);">'
            #     for am in tipopago:
            #         html += '<option value="' + str(am.id) + '"'
            #         if am.id == detal.forma_pago_empleado_id:
            #             html += ' selected="selected"'
            #         html += ' >' + str(am.nombre) + '</option>'
            #     html += '</select><div class="num_comprobante"><div class="pull-right"><input placeholder="# Cheque" class="form-control input-sm" id="id_pago_' + str(
            #         i) + '_numero_comprobante" maxlength="40" name="pago_' + str(
            #         i) + '_numero_comprobante" size="12" type="text"></div></div></td>'
            #     html += '<td><select class="select-input form-control input-sm" id="id_pago_' + str(
            #         i) + '_cuenta_bancaria" name="pago_' + str(i) + '_cuenta_bancaria">'
            #     for b in banco:
            #         bnombre = (b.nombre).encode('ascii', 'ignore').decode('ascii')
            #         html += '<option value="' + str(b.id) + '"'
            #         if b.id == detal.banco_id:
            #             html += ' selected="selected"'
            #         html += ' >' + str(bnombre) + '</option>'
            #     html += '</select></td></tr>'
            #     final_ingresos = final_ingresos + total_ingresos
            #     final_otros_ingresos = final_otros_ingresos + total_otros_ingresos
            #     final_egresos = final_egresos + total_egresos
            #     final_otros_egresos = final_otros_egresos + total_otros_egresos
            #     final_total = final_total + total
            # 
            # html += '<tr><td></td><td></td><td></td><td style="text-align:right">' + str(
            #     final_ingresos) + '</td><td >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
            #     final_otros_ingresos) + '</td><td style="text-align:right">' + str(
            #     final_egresos) + '</td><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
            #     final_otros_egresos) + '</td><td></td><td style="text-align:right">' + str(
            #     final_total) + '</td><td></td><td></td></tr>'
            # html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
            #     i) + '" />'


        return HttpResponse(
            html
        )

@login_required()
def MostrarOtrosIngresosView(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_ingresos = request.POST["id_txt_otros_ingresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_ingresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(otros_ingresos=True).order_by('nombre')
        if quincena== 'M':
            detalle = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_ingresos)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,tipo_ingreso_egreso_empleado_id=24)
        else:
            detalle = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=id_txt_otros_ingresos)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,
                                                     quincena=quincena,
                                                     tipo_ingreso_egreso_empleado_id=24)

        return render_to_response('roles_pago/mostrar_otros_ingresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'sueldo': sueldo}, RequestContext(request))


    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_ingresos = request.POST["id_txt_otros_ingresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_ingresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(otros_ingresos=True).order_by('nombre')
        detalle = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_ingresos)
        sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,
                                                 quincena=quincena, tipo_ingreso_egreso_empleado_id=24)
        return render_to_response('roles_pago/mostrar_otros_ingresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'sueldo': sueldo}, RequestContext(request))

@login_required()
@csrf_exempt
def guardarOtrosIngresosView(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta_otros_ingresos"]
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        sueldo = request.POST["sueldo"]
        print('sueldo' + str(sueldo))
        sueldo_quincenal = float(sueldo) / 2
        print('sueldo_quincenal' + str(sueldo_quincenal))
        tipo_contrato_persona = request.POST["tipo_contrato_persona"]
        i = 0
        html = "Guardado con exito"
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_detalle' + str(i) in request.POST:
                    detalle_id = request.POST["id_detalle" + str(i)]
                    detallecompra = OtrosIngresosRolEmpleado.objects.get(id=detalle_id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                    detallecompra.valor = request.POST["valor_kits" + str(i)]
                    detallecompra.nombre = request.POST["nombre_kits" + str(i)]
                    detallecompra.deducible = request.POST.get('deducible_kits' + str(i), False)
                    detallecompra.aportaciones = request.POST.get('aportaciones' + str(i), False)
                    detallecompra.anio = request.POST["anio"]
                    detallecompra.mes = request.POST["mes"]
                    #detallecompra.quincena = request.POST["quincena"]
                    detallecompra.empleado_id = request.POST["empleado_otro_ingreso"]
                    detallecompra.pagar = True
                    if 'horas_kits' + str(i) in request.POST:
                        hr = request.POST["horas_kits" + str(i)]
                        if len(hr) != 0:
                            detallecompra.horas = request.POST["horas_kits" + str(i)]
                    detallecompra.save()
                    print('guardar1')

                else:
                    if 'tipos_kits' + str(i) in request.POST:
                        comprasdetalle = OtrosIngresosRolEmpleado()
                        # comprasdetalle.proforma_id = new_orden.id
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                        comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                        comprasdetalle.nombre = request.POST["nombre_kits" + str(i)]
                        comprasdetalle.deducible = request.POST.get('deducible_kits' + str(i), False)
                        comprasdetalle.aportaciones = request.POST.get('aportaciones_kits' + str(i), False)
                        comprasdetalle.anio = request.POST["anio"]
                        comprasdetalle.mes = request.POST["mes"]
                        #comprasdetalle.quincena = request.POST["quincena"]
                        comprasdetalle.empleado_id = request.POST["empleado_otro_ingreso"]
                        comprasdetalle.pagar = True
                        if 'horas_kits' + str(i) in request.POST:
                            hr = request.POST["horas_kits" + str(i)]
                            if len(hr) != 0:
                                comprasdetalle.horas = request.POST["horas_kits" + str(i)]
                        comprasdetalle.save()
                        print('guardar2')

                tip_id = request.POST["tipos_kits" + str(i)]
                print(tip_id)

                emp = request.POST["empleado_otro_ingreso"]
                try:
                    tip = TipoIngresoEgresoEmpleado.objects.get(id=tip_id, parte_ingreso=True)
                except TipoIngresoEgresoEmpleado.DoesNotExist:
                    tip = None
                if tip:
                    cursor = connection.cursor();
                    cursor.execute(
                        "SELECT  distinct sum(oi.valor)from otros_ingresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.parte_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes  + "'");
                    row = cursor.fetchall();
                    if row:
                        cursor1 = connection.cursor();
                        cursor1.execute(
                            "SELECT  distinct oi.id,oi.tipo_ingreso_egreso_empleado_id,oi.valor from otros_ingresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.calcular_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes + "'");
                        row1 = cursor1.fetchall();
                        t_ing_sueldo = row[0][0] + sueldo_quincenal
                        print('horas_extras' + str(row[0][0]))
                        print('total ingreso' + str(t_ing_sueldo))
                        if row1:
                            for p in row1:
                                if p[1] == 7:
                                    ing1 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                    if ing1:
                                        print('tip1')
                                        ing1.updated_by = request.user.get_full_name()
                                        ing1.updated_at = datetime.now()
                                        ing1.valor = float((t_ing_sueldo) * 0.0833)
                                        ing1.save()
                                if p[1] == 8:
                                    print('entro')
                                    ing2 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                    ing2.updated_by = request.user.get_full_name()
                                    ing2.updated_at = datetime.now()
                                    total_guardar = float(t_ing_sueldo) / 24
                                    ing2.valor = total_guardar
                                    ing2.save()
                                    print('tardar' + str(ing2.valor))
                                    print('total guardar' + str(total_guardar))
                                if p[1] == 27:
                                    ing3 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                    if ing3:
                                        ing3.updated_by = request.user.get_full_name()
                                        ing3.updated_at = datetime.now()
                                        ing3.valor = float((t_ing_sueldo / 10.58) / 2)
                                        ing3.save()
                        cursor2 = connection.cursor();
                        cursor2.execute(
                            "SELECT  distinct oi.id,oi.tipo_ingreso_egreso_empleado_id,oi.valor from otros_egresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.calcular_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes + "'");
                        row2 = cursor1.fetchall();
                        if row2:
                            t_ing_sueldo = row[0][0] + sueldo_quincenal
                            for p2 in row2:
                                eg = OtrosEgresosRolEmpleado.objects.get(id=p2[0])
                                if eg:
                                    if p2[1] == 29:
                                        eg.updated_by = request.user.get_full_name()
                                        eg.updated_at = datetime.now()
                                        eg.valor = float((t_ing_sueldo) * 0.0945)
                                        eg.save()
                                    if p2[1] == 30:
                                        eg.updated_by = request.user.get_full_name()
                                        eg.updated_at = datetime.now()
                                        eg.valor = float(((t_ing_sueldo) * 0.0341) / 2)
                                        eg.save()

        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def MostrarOtrosEgresosView(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_egresos = request.POST["id_txt_otros_egresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_egresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(otros_egresos=True).order_by('nombre')
        detalle = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_egresos)
        return render_to_response('roles_pago/mostrar_otros_egresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena}, RequestContext(request))


    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_egresos = request.POST["id_txt_otros_egresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_egresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(otros_egresos=True).order_by('nombre')
        detalle = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_egresos)
        return render_to_response('roles_pago/mostrar_otros_egresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena}, RequestContext(request))

@login_required()
@csrf_exempt
def guardarOtrosEgresosView(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta_otros_egresos"]
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        tipo_contrato_persona = request.POST["tipo_contrato_persona"]
        i = 0
        html = "Guardado con exito"
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_detalle' + str(i) in request.POST:
                    detalle_id = request.POST["id_detalle" + str(i)]
                    detallecompra = OtrosEgresosRolEmpleado.objects.get(id=detalle_id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                    detallecompra.valor = request.POST["valor_kits" + str(i)]
                    detallecompra.nombre = request.POST["nombre_kits" + str(i)]
                    detallecompra.memo = request.POST.get('memo_kits' + str(i), False)
                    detallecompra.anio = request.POST["anio"]
                    detallecompra.mes = request.POST["mes"]
                    detallecompra.quincena = request.POST["quincena"]
                    detallecompra.empleado_id = request.POST["empleado_otro_egreso"]
                    detallecompra.save()
                else:
                    if 'tipos_kits' + str(i) in request.POST:
                        comprasdetalle = OtrosEgresosRolEmpleado()
                        # comprasdetalle.proforma_id = new_orden.id
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                        comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                        comprasdetalle.nombre = request.POST["nombre_kits" + str(i)]
                        comprasdetalle.memo = request.POST.get('memo_kits' + str(i), False)
                        comprasdetalle.anio = request.POST["anio"]
                        comprasdetalle.mes = request.POST["mes"]
                        comprasdetalle.quincena = request.POST["quincena"]
                        comprasdetalle.empleado_id = request.POST["empleado_otro_egreso"]
                        comprasdetalle.save()
        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def MostrarOtrosDiasNoLaboradosView(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_dias = request.POST["id_txt_otros_dias"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_dias)
        tipos = TipoAusencia.objects.all().order_by('nombre')
        detalle = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_dias).filter(descontar=True)
        sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,
                                                 tipo_ingreso_egreso_empleado_id=24)
        if quincena=='M':
            detalle = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=id_txt_otros_dias).filter(descontar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,
                                                 tipo_ingreso_egreso_empleado_id=24)
        else:
            detalle = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=id_txt_otros_dias).filter(descontar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,
                                                     tipo_ingreso_egreso_empleado_id=24)
        return render_to_response('roles_pago/mostrar_dias_no_laborados.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena, 'sueldo': sueldo},
                                  RequestContext(request))


    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_dias = request.POST["id_txt_otros_dias"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_dias)
        tipos = TipoAusencia.objects.all().order_by('nombre')
        detalle = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=id_txt_otros_dias).filter(descontar=True)
        sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,tipo_ingreso_egreso_empleado_id=24)
        # if quincena=='M':
        #     detalle = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
        #     empleado_id=id_txt_otros_dias).filter(descontar=True)
        #     sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,
        #                                          tipo_ingreso_egreso_empleado_id=24)
        # else:
        #     detalle = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
        #         mes=mes).filter(
        #         empleado_id=id_txt_otros_dias).filter(descontar=True)
        #     sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_dias, anio=anio, mes=mes,
        #                                              quincena=quincena,
        #                                              tipo_ingreso_egreso_empleado_id=24)
        return render_to_response('roles_pago/mostrar_dias_no_laborados.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena, 'sueldo': sueldo},
                                  RequestContext(request))

@login_required()
@csrf_exempt
def guardarDiasNoLaboradosView(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta_dias"]
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        tipo_contrato_persona = request.POST["tipo_contrato_persona"]
        i = 0
        temp=0
        html = "Guardado con exito"
        print('entro a guardar dias no laborados')
        
        while int(i) <= int(contador):

            i += 1

            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                tipo = request.POST["tipos_kits" + str(i)]
                empleado_id = request.POST["empleado_otro_dia"]
                valor=request.POST["valor_kits" + str(i)]
                print ('tipo' + str(tipo))
                print ('valores ' + str(valor))
                if tipo == 1 or tipo == 3 or tipo == '1' or tipo == '3' or tipo == 7 or tipo == '7':
                    sueldo = IngresosRolEmpleado.objects.get(empleado_id=empleado_id, anio=anio, mes=mes,
                                                             tipo_ingreso_egreso_empleado_id=24)
                    sueldo_cal=sueldo.valor
                    if valor:
                        temp=valor
                    else:
                        temp=0
                    sueldo.valor=float(sueldo_cal)-float(temp)
                    sueldo.save()
                    print ('Sueldo calculo ' + str(sueldo.valor))

                if 'id_detalle' + str(i) in request.POST:
                    detalle_id = request.POST["id_detalle" + str(i)]
                    detallecompra = DiasNoLaboradosRolEmpleado.objects.get(id=detalle_id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.tipo_ausencia_id = request.POST["tipos_kits" + str(i)]
                    if request.POST["dias_kits" + str(i)]:
                        detallecompra.dias = request.POST["dias_kits" + str(i)]
                    else:
                        detallecompra.dias =0
                    detallecompra.valor = request.POST["valor_kits" + str(i)]
                    # if request.POST["fecha_salida_kits"+str(i)]:
                    #   detallecompra.fecha_salida= request.POST["fecha_salida_kits"+str(i)]
                    detallecompra.anio = request.POST["anio"]
                    detallecompra.mes = request.POST["mes"]
                    #detallecompra.quincena = request.POST["quincena"]
                    detallecompra.tipo_ausencia_id = request.POST["tipos_kits" + str(i)]
                    detallecompra.empleado_id = request.POST["empleado_otro_dia"]
                    detallecompra.descontar = True
                    detallecompra.cargar_vacaciones = request.POST.get('vacaciones' + str(i), False)
                    detallecompra.motivo = request.POST["motivo" + str(i)]
                    detallecompra.save()
                else:
                    if 'tipos_kits' + str(i) in request.POST:
                        print 'entro'
                        comprasdetalle = DiasNoLaboradosRolEmpleado()
                        # comprasdetalle.proforma_id = new_orden.id
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ausencia_id = request.POST["tipos_kits" + str(i)]
                        #comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                        comprasdetalle.cargar_vacaciones = request.POST.get('vacaciones' + str(i), False)
                        if request.POST["dias_kits" + str(i)]:
                            comprasdetalle.dias = request.POST["dias_kits" + str(i)]
                        else:
                            detallecompra.dias = 0

                        comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                        # if request.POST["fecha_salida_kits"+str(i)]:
                        #   comprasdetalle.fecha_salida=request.POST["fecha_salida_kits"+str(i)]
                        comprasdetalle.anio = request.POST["anio"]
                        comprasdetalle.mes = request.POST["mes"]
                        #comprasdetalle.quincena = request.POST["quincena"]
                        comprasdetalle.empleado_id = request.POST["empleado_otro_dia"]
                        comprasdetalle.motivo = request.POST["motivo" + str(i)]
                        comprasdetalle.descontar = True
                        comprasdetalle.save()
        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def ConsultarRolesPagoView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        contador = request.POST["columnas_receta_roles"]
        try:
            detalles = RolPago.objects.get(mes=mes, quincena=quincena, anio=anio)
        except RolPago.DoesNotExist:
            detalles = None

        if detalles:
            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_detalle' + str(i) in request.POST:
                        id_detalle = request.POST["id_detalle" + str(i)]
                        detallecompra = RolPagoDetalle.objects.get(id=id_detalle)
                        detallecompra.updated_by = request.user.get_full_name()
                        detallecompra.updated_at = datetime.now()
                        detallecompra.empleado_id = request.POST["id_empleado" + str(i)]
                        detallecompra.ingresos = request.POST["pago_" + str(i) + "_total"]
                        detallecompra.egresos = request.POST["pago_" + str(i) + "_total_egresos"]
                        detallecompra.otros_ingresos = request.POST["pago_" + str(i) + "_otros_ingresos"]
                        detallecompra.otros_egresos = request.POST["pago_" + str(i) + "_otros_egresos"]
                        detallecompra.dias = request.POST["pago_" + str(i) + "_dias"]
                        detallecompra.total = request.POST["pago_" + str(i) + "_valor_a_recibir"]
                        detallecompra.tipo_pago_id = request.POST["pago_" + str(i) + "_tipo_pago"]
                        detallecompra.numero_comprobante = request.POST["pago_" + str(i) + "_numero_comprobante"]
                        detallecompra.tipo_pago_id = request.POST["pago_" + str(i) + "_tipo_pago"]
                        detallecompra.banco_id = request.POST["pago_" + str(i) + "_cuenta_bancaria"]
                        detallecompra.rol_pago_id = detalles.id
                        detallecompra.descuento_dias = request.POST["pago_valor_" + str(i) + "_dias"]

                        detallecompra.save()
                    else:
                        print('entrosd')

            anio = Anio.objects.all()
            return render_to_response('roles_pago/consultar_roles.html',
                                      {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio':anio,
                                       'empleados': empleados}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoPago.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        departamentos = Departamento.objects.all()
        anio = Anio.objects.all()
        return render_to_response('roles_pago/consultar_roles.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio':anio,
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))

@login_required()
@csrf_exempt
def obtenerRolView(request):
    if request.method == 'POST':
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        empleado = request.POST["empleado"]
        departamento = request.POST["departamento"]

        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        tipopago = TipoPago.objects.all()
        print('EMPLEADO')
        print(str(empleado))
        try:
            detalles = RolPago.objects.get(mes=mes, anio=anio)
        except RolPago.DoesNotExist:
            detalles = None

        if detalles:

            if empleado == '0':
                roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id)
                print('entroRolNofILTRADOempleado')
            else:

                roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).filter(empleado_id=empleado)
                print('entro2')

            cursor = connection.cursor()
            sql = 'select d.id,d.rol_pago_id from rol_pago_detalle d,departamento de,empleados_empleado e,rol_pago r  where d.empleado_id=e.empleado_id and d.rol_pago_id=r.id and d.rol_pago_id=' + str(
                detalles.id) + ' and e.departamento_id=de.id and 1=1 '
            if mes != '':
                sql += ' and r.mes=' + mes
            if anio != '':
                sql += " and r.anio='" + anio + "' "
            # if quincena != '':
            #     sql += " and r.quincena='" + quincena + "' "
            if empleado != '0':
                sql += ' and d.empleado_id=' + empleado
            if departamento != '0':
                sql += ' and de.id=' + departamento

            sql += ' order by d.id;'
            cursor.execute(sql)
            roles_detalle = cursor.fetchall()
            id = detalles.id
            for det in roles_detalle:
                detal = RolPagoDetalle.objects.get(id=det[0])

                i += 1
                try:
                    sueldo = IngresosRolEmpleado.objects.get( anio=anio, mes=mes,
                                                             empleado_id=detal.empleado_id,
                                                             tipo_ingreso_egreso_empleado_id=24)
                except IngresosRolEmpleado.DoesNotExist:
                    print('NOquerySueldo')
                    sueldo = 0

                #ingresosPro = IngresosRolEmpleado.objects.filter(empleado_id=detal.empleado_id)
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
                
                faltas_ingresos_egresos_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('valor'))

                vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
                
                dias_no_trabajados_por_ingreso_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('valor'))
                dias_parciales_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=8).aggregate(Sum('valor'))

                descont_dias = 0
                if faltas_injustificadas_valor['valor__sum']:
                    descont_dias = faltas_injustificadas_valor['valor__sum']
                    

                if vacaciones_justificadas_valor['valor__sum']:
                    descont_dias = descont_dias + vacaciones_justificadas_valor['valor__sum']
                
                if dias_no_trabajados_por_ingreso_valor['valor__sum']:
                    descont_dias = descont_dias + dias_no_trabajados_por_ingreso_valor['valor__sum']
                
                if dias_parciales_valor['valor__sum']:
                    print 'valor dde dias parciales'+str(dias_parciales_valor['valor__sum'])
                    descont_dias = descont_dias + dias_parciales_valor['valor__sum']
                

                ingresosRecorrer = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True)

                for ir in ingresosRecorrer:
                    if ir.tipo_ingreso_egreso_empleado_id ==24:
                        ir.valor = round(float(ir.valor_mensual - descont_dias), 2)
                        ir.updated_by = request.user.get_full_name()
                        ir.updated_at = datetime.now()
                        ir.save()


                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

                otrosingresosRecorrer = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id)
                if otrosingresosRecorrer:
                    for oiR in otrosingresosRecorrer:
                        if oiR.tipo_ingreso_egreso_empleado_id == 7:
                            #ACUMULACION DE FONDO DE RESERVA
                            if detal.pagar_fondo_reserva:
                                fecha_comparar_modif=date(int(anio), int(mes), 30)
                    
                                if detal.empleado.fecha_ini_reconocida:
                                    hoyfr=date(int(anio),int(mes), 30)
                                    diferencia_entrada=hoyfr-detal.fecha_ini_reconocida
            
                                    dias_comp= str(diferencia_entrada).split('days')
                                    dias_c=dias_comp[0]
                                    if int(dias_c)>=  364:
                                        oiR.updated_by = request.user.get_full_name()
                                        if float(dias_c)>=394:
                                            fr_provision=ingresos['valor__sum']/12
                                            acumular_fondo=float((ingresos['valor__sum']) / 12)
                                            oiR.valor = round(acumular_fondo, 2)
                                        else:
                                                        
                                            proporcional=float(dias_c)-364
                                            fr_provision=float((ingresos['valor__sum']) / 12)
                                            proporcionaf=float((fr_provision*proporcional)/30)
                                            oiR.valor = round(proporcionaf, 2)
                                        oiR.save()
                                            
 
                                # oiR.updated_by = request.user.get_full_name()
                                # if ingresos['valor__sum']:
                                #     oiR.valor = round(float((ingresos['valor__sum']) / 12), 2)
                                #     # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
                                # 
                                # oiR.save()
                        if oiR.tipo_ingreso_egreso_empleado_id == 8:
                            oiR.updated_by = request.user.get_full_name()
                            dtercero=float(ingresos['valor__sum'] / 12)
                            oiR.valor = round(dtercero, 2)
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
                            oiR.save()
                        #Decimo cuarto
                        if oiR.tipo_ingreso_egreso_empleado_id == 9:
                            oiR.updated_by = request.user.get_full_name()
                            if detalles.salario_base:
                                if detal.empleado.tipo_remuneracion_id == 2:
                                    mes_t=dias_trabajados/30
                                    total_anios=mes_t*12
                                    dcuarto=float(detalles.salario_base/ 12)
                                    dcuarto=(dcuarto*total_anios)/12
                                
                                else:
                                    dcuarto=float(detalles.salario_base/ 12)
                                #dcuarto=float(detalles.salario_base / 12)
                                oiR.valor = round(dcuarto, 2)
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
                            oiR.save()

                        if oiR.tipo_ingreso_egreso_empleado_id == 27:
                            oiR.updated_by = request.user.get_full_name()
                            if detal.pagar_iess_asumido:
                                #acumulado_iess=float(ingresos['valor__sum'] / 10.5816)
                                acumulado_iess=float(ingresos['valor__sum'] * 0.0945)
                                oiR.valor = round(acumulado_iess,2)
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
                            oiR.save()

                egresosRecorrer = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id)
                if egresosRecorrer:
                    for eR in egresosRecorrer:
                        if eR.tipo_ingreso_egreso_empleado_id == 30:
                            eR.updated_by = request.user.get_full_name()
                            if detal.pagar_extension_conyugal:
                                if ingresos['valor__sum']:
                                    ext=float(ingresos['valor__sum'] * 0.0341)
                                    eR.valor = round(ext, 2)
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)

                            eR.save()
                        if eR.tipo_ingreso_egreso_empleado_id == 29:
                            eR.updated_by = request.user.get_full_name()
                            if ingresos['valor__sum']:
                                nueve=float(ingresos['valor__sum'] * 0.0945)
                                eR.valor = round(nueve, 2)
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)

                            eR.save()

                egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).aggregate(Sum('valor'))

                otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

                if ingresos['valor__sum']:
                    total_ingresos = float(ingresos['valor__sum'])
                    print('entro comoqw' + str(total_ingresos))
                    print('entro')
                else:
                    print('entroNO')
                    total_ingresos = 0

                if egresos['valor__sum']:
                    total_egresos = float(egresos['valor__sum'])
                    print('entro comoEgesor' + str(total_egresos))
                    print('entroEgreso')
                else:

                    total_egresos = 0
                    print('entroEgresoNO')

                if otros_ingresos['valor__sum']:
                    total_otros_ingresos = float(otros_ingresos['valor__sum'])
                    print('entro comoEgesor' + str(total_otros_ingresos))
                    print('entroEgreso')
                else:

                    total_otros_ingresos = 0
                    print('entroEgresoNO')

                if detal.ingresos!=total_ingresos:
                    detal.ingresos=total_ingresos

                if detal.egresos!=total_egresos:
                    detal.egresos=total_egresos

                if detal.otros_ingresos!=total_otros_ingresos:
                    detal.otros_ingresos=total_otros_ingresos

                faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
                atrasos_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=4).aggregate(Sum('valor'))
                descuentos_dias_no=0
                if faltas_justificadas_valor['valor__sum']:
                    descuentos_dias_no = float(faltas_justificadas_valor['valor__sum'] + descuentos_dias_no)

                if atrasos_justificadas_valor['valor__sum']:
                    descuentos_dias_no = float(atrasos_justificadas_valor['valor__sum'] + descuentos_dias_no)
                print ('entro descuento Dias afect base' + str(descont_dias))

                detal.descuento_dias=descuentos_dias_no
                total_emp= total_ingresos+total_otros_ingresos-total_egresos-descuentos_dias_no
                if detal.total!=total_emp:
                    detal.total=total_emp
                detal.save()
                
                faltas_injustificadas_dias= DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('dias'))
                dias_no_trabajados_por_ingreso_dias= DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('dias'))
                dias_p= DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=8).aggregate(Sum('dias'))
                
                vacaciones_p= DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=1).aggregate(Sum('dias'))
                
            

                
                descont_dias = 0
                if faltas_injustificadas_dias['dias__sum']:
                    descont_dias_rol = faltas_injustificadas_dias['dias__sum']
                else:
                    descont_dias_rol=0
                print ('entro  Dias a descontar1:' + str(descont_dias_rol))
                
                if dias_no_trabajados_por_ingreso_dias['dias__sum']:
                    descont_dias_rol =descont_dias_rol+ dias_no_trabajados_por_ingreso_dias['dias__sum']
                
                if dias_p['dias__sum']:
                    descont_dias_rol =descont_dias_rol+ dias_p['dias__sum']
                    
                if vacaciones_p['dias__sum']:
                    descont_dias_rol =descont_dias_rol+ vacaciones_p['dias__sum']
                
                print ('entro  Dias a descontar2:' + str(descont_dias_rol))


                total_ingreso_neto = total_ingresos
                total_egreso_neto = total_egresos
                total_otros_ingresos_neto = total_otros_ingresos
                html += ' <tr><td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
                    i) + '" id="id_empleado' + str(i) + '" value="' + str(
                    detal.empleado_id) + '"/><input type="hidden" name="id_detalle' + str(
                    i) + '" id="id_detalle' + str(i) + '" value="' + str(detal.id) + '"/></td>'
                # html+='<td class="text-center"><div class="checkbox custom-checkbox custom-checkbox-primary"><input class="seleccionar" data-contextual="info" data-target="tr" data-toggle="selectrow" id="id_pago_'+str(i)+'_seleccionado" name="pago_'+str(i)+'_seleccionado" type="checkbox"><label for="id_pago_'+str(i)+'_seleccionado"></label></div></td>'
                html += '<td><input class="form-control input-sm" id="id_cedula_' + str(
                    i) + '" maxlength="10" name="cedula_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.empleado.cedula_empleado) + '" type="text"></td>'
                html += '<td><a class="text-primary" href="#" target="_blank"><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_razon_social" maxlength="300" name="pago_' + str(
                    i) + '_razon_social" readonly="readonly" size="31" value="' + str(
                    detal.empleado.nombre_empleado.encode('utf8')) + '" type="text"></a><input id="id_pago_' + str(
                    i) + '_idpersona" name="pago_' + str(i) + '_idpersona" value="893721" type="hidden"></td>'
                html += '<td><input class="form-control input-sm" id="id_area_' + str(
                    i) + '" maxlength="10" name="area_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.empleado.departamento) + '" type="text"></td>'
                html += '<td><input class="form-control input-sm" id="id_cargo_' + str(
                    i) + '" maxlength="10" name="cargo_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.empleado.tipo_empleado) + '" type="text"></td>'
                if sueldo:
                    html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
                        i) + '" maxlength="10" name="sueldo_' + str(
                        i) + '" readonly="readonly" size="10" value="' + str(
                        sueldo.valor_mensual) + '" type="text"></td>'
                else:
                    html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
                        i) + '" maxlength="10" name="sueldo_' + str(
                        i) + '" readonly="readonly" size="10" value="' + str(sueldo) + '" type="text"></td>'
                #dias_trabajados=float(detal.dias)-float(descont_dias_rol/8)
                dias_trabajados=30-float(descont_dias_rol/8)
                html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_diasagregados_ad()"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_dias" name="pago_' + str(i) + '_dias" readonly="readonly" size="5" value="' + str(
                    dias_trabajados) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_dias_valor" name="pago_valor_' + str(i) + '_dias" readonly="readonly" value="' + str(
                    detal.descuento_dias) + '" type="hidden"></a><span class="input-group-btn input"><a href="javascript: dias_ad(' + str(
                    i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
                html += '<td><a href="javascript: ingresos(' + str(
                    i) + ')" data-toggle="modal"><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_total" name="pago_' + str(
                    i) + '_total" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    detal.ingresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_ingreso" name="pago_' + str(
                    i) + '_ingreso" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    total_ingreso_neto) + '" type="hidden"></td>'
                html += '<td><div class="input-group input-group-sm"><a href="#"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_otros_ingresos" maxlength="15" name="pago_' + str(
                    i) + '_otros_ingresos" readonly="readonly" size="6" value="' + str(
                    detal.otros_ingresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: ingresos_ad(' + str(
                    i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
                html += '<td><a href="javascript: egresos(' + str(
                    i) + ')"  data-toggle="modal"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_total_egresos" maxlength="15" name="pago_' + str(
                    i) + '_total_egresos" readonly="readonly" size="6" value="' + str(
                    detal.egresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
                    i) + 'egreso_neto" name="pago_' + str(
                    i) + 'egreso_neto" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    total_egreso_neto) + '" type="hidden"></td>'
                # html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_descuentos()"><input class="form-control input-sm text-right" id="id_pago_' + str(
                #     i) + '_otros_egresos" maxlength="10" name="pago_' + str(
                #     i) + '_otros_egresos" readonly="readonly" size="6" value="' + str(
                #     detal.otros_egresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: egresos_ad(' + str(
                #     i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'

                html += '<td><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_a_recibir" name="pago_' + str(
                    i) + '_valor_a_recibir" readonly="readonly" size="10" value="' + str(
                    detal.total) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_a_recibir_hidden" name="pago_' + str(
                    i) + '_valor_a_recibir_hidden" readonly="readonly" size="10" value="231.00" type="hidden"></td>'
                html += '<td><select class="tipopago form-control input-sm" id="id_pago_' + str(
                    i) + '_tipo_pago" maxlength="15" name="pago_' + str(
                    i) + '_tipo_pago" onchange="mostrarComprobante(this);">'
                for am in tipopago:
                    html += '<option value="' + str(am.id) + '"'
                    if am.id == detal.tipo_pago_id:
                        html += ' selected="selected"'
                    html += ' >' + str(am.nombre) + '</option>'
                html += '</select><div class="num_comprobante"><div class="pull-right"><input placeholder="# Cheque" class="form-control input-sm" id="id_pago_' + str(
                    i) + '_numero_comprobante" maxlength="40" name="pago_' + str(
                    i) + '_numero_comprobante" size="12" type="text"></div></div></td>'
                html += '<td><select class="select-input form-control input-sm" id="id_pago_' + str(
                    i) + '_cuenta_bancaria" name="pago_' + str(i) + '_cuenta_bancaria">'
                for b in banco:
                    bnombre = (b.nombre).encode('ascii', 'ignore').decode('ascii')
                    html += '<option value="' + str(b.id) + '"'
                    if b.id == detal.banco_id:
                        html += ' selected="selected"'
                    html += ' >' + str(bnombre) + '</option>'
                html += '</select></tr>'
                final_ingresos = final_ingresos + detal.ingresos
                final_otros_ingresos = final_otros_ingresos + detal.otros_ingresos
                final_egresos = final_egresos + detal.egresos
                final_otros_egresos = final_otros_egresos + detal.otros_egresos
                final_total = final_total + detal.total

            html += '<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="text-align:right">' + str(
                final_ingresos) + '</td><td >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
                final_otros_ingresos) + '</td><td style="text-align:right">' + str(
                final_egresos) + '</td><td style="text-align:right">' + str(
                final_total) + '</td><td></td><td></td></tr>'
            html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
                i) + '" />'
            item = {
                'html': html,
                'id': id,

            }
            return HttpResponse(json.dumps(item), content_type='application/json')
        else:
            html += '<tr><td colspan="8">No se ha genero ese rol</td></tr>'
            item = {
                'html': html,

            }
            return HttpResponse(json.dumps(item), content_type='application/json')
    else:
        html += '<tr><td colspan="8">No se ha genero ese rol</td></tr>'
        item = {
            'html': html,

        }
        return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
def PrestamosListView(request):
    if request.method == 'POST':

        row = Prestamo.objects.all().order_by('codigo')
        return render_to_response('prestamo/index.html', {'row': row}, RequestContext(request))
    else:
        row = Prestamo.objects.all().order_by('codigo')
        return render_to_response('prestamo/index.html', {'row': row}, RequestContext(request))

@login_required()
@transaction.atomic
def PrestamoCreateView(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                new_orden = form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.plazos = request.POST["plazo"]
                new_orden.total = request.POST["total_real"]
                if 'saldo_deuda_anterior' in request.POST:
                    new_orden.saldo_deuda_anterior = request.POST["saldo_deuda_anterior"]
                if 'total_pagar_detalle' in request.POST:
                    new_orden.total_pagar = request.POST["total_pagar_detalle"]

                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='prestamo')
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
                        if 'fecha_kits' + str(i) in request.POST:
                            proformadetalle = PrestamoDetalle()
                            proformadetalle.prestamo_id = new_orden.id
                            proformadetalle.fecha = request.POST["fecha_kits" + str(i)]
                            proformadetalle.abono = request.POST["abono_kits" + str(i)]
                            proformadetalle.cuota = request.POST["cuota_kits" + str(i)]
                            proformadetalle.saldo = request.POST["saldo_kits" + str(i)]
                            proformadetalle.descuento = request.POST["descuento_kits" + str(i)]
                            proformadetalle.save()

                return HttpResponseRedirect('/recursos_humanos/prestamo')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = PrestamoForm

    return render_to_response('prestamo/nuevo.html', {'form': form}, RequestContext(request))


@login_required()
def PrestamoUpdateView(request, pk):
    if request.method == 'POST':
        prestamo = Prestamo.objects.get(id=pk)
        form = PrestamoForm(request.POST, request.FILES, instance=prestamo)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            new_orden = form.save()
            new_orden.save()
            context = {
                'section_title': 'Actualizar Orden Egreso',
                'button_text': 'Actualizar',
                'form': form}
            return render_to_response(
                'prestamo/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:
            form = PrestamoForm(request.POST)
            context = {
                'section_title': 'Actualizar',
                'button_text': 'Actualizar',
                'form': form}

            return render_to_response(
                'prestamo/actualizar.html',
                context,
                context_instance=RequestContext(request))
    else:
        prestamo = Prestamo.objects.get(id=pk)
        form = PrestamoForm(instance=prestamo)
        context = {
            'section_title': 'Actualizar',
            'button_text': 'Actualizar',
            'form': form}

        return render_to_response(
            'prestamo/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def guardarCuentasContablesView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.all()
        for r in rol_cuentas:
            if 'cuentas' + str(r.id) in request.POST:
                id_cuenta = request.POST['cuentas' + str(r.id)]
                cuent = RolPagoCuentaContable.objects.get(id=r.id)
                cuent.plandecuentas_id = id_cuenta
                cuent.updated_at = datetime.now()
                cuent.updated_by = request.user.get_full_name()
                cuent.save()

        plan = PlanDeCuentas.objects.all()

        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/')


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        for r in rol_cuentas:
            if 'cuentas' + r.id in request.POST:
                id_cuenta = request.POST['cuentas' + r.id]
                cuent = RolPagoCuentaContable.objects.get(id=r.id)
                cuent.plandecuentas_id = id_cuenta
                cuent.updated_at = datetime.now()
                cuent.updated_by = request.user.get_full_name()
                cuent.save()

        plan = PlanDeCuentas.objects.all()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return render_to_response('roles_pago/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado, 'plan': plan},
                                  RequestContext(request))

@login_required()
def RolCuentaContableListView(request):
    if request.method == 'POST':

        row = RolPagoCuentaContable.objects.all().order_by('clave')
        return render_to_response('cuentas_contable/index.html', {'row': row}, RequestContext(request))
    else:
        row = RolPagoCuentaContable.objects.all().order_by('clave')
        return render_to_response('cuentas_contable/index.html', {'row': row}, RequestContext(request))

@login_required()
def RolCuentaContableCreateView(request):
    if request.method == 'POST':
        form = RolPagoCuentaContableForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            return HttpResponseRedirect('/recursos_humanos/rol_cuenta_contable')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = RolPagoCuentaContableForm

    return render_to_response('cuentas_contable/nuevo.html', {'form': form}, RequestContext(request))


# =====================================================#
@login_required()
def RolCuentaContableUpdateView(request, pk):
    if request.method == 'POST':
        prestamo = RolPagoCuentaContable.objects.get(id=pk)
        form = RolPagoCuentaContableForm(request.POST, request.FILES, instance=prestamo)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            new_orden = form.save()
            new_orden.save()
            context = {
                'section_title': 'Actualizar Orden Egreso',
                'button_text': 'Actualizar',
                'form': form}
            return render_to_response(
                'cuentas_contable/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:
            form = RolPagoCuentaContableForm(request.POST)
            context = {
                'section_title': 'Actualizar',
                'button_text': 'Actualizar',
                'form': form}

            return render_to_response(
                'cuentas_contable/actualizar.html',
                context,
                context_instance=RequestContext(request))
    else:
        prestamo = RolPagoCuentaContable.objects.get(id=pk)
        form = RolPagoCuentaContableForm(instance=prestamo)
        context = {
            'section_title': 'Actualizar',
            'button_text': 'Actualizar',
            'form': form}

        return render_to_response(
            'cuentas_contable/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def ConsultarPagosView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.order_by('id')
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('pagos/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                       'tipoempleado': tipoempleado, 'banco': banco,
                                                       'roles_pago': roles_pago,
                                                       'sueldos_unificados': sueldos_unificados, 'plan': plan,
                                                       'clasificacion': clasificacion}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('pagos/index.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                       'tipoempleado': tipoempleado, 'banco': banco,
                                                       'roles_pago': roles_pago,
                                                       'sueldos_unificados': sueldos_unificados, 'plan': plan,
                                                       'clasificacion': clasificacion}, RequestContext(request))

@login_required()
def MostrarEmpleadosView(request):
    if request.method == 'POST':
        detalle = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado',
                                          'apellido')
        return render_to_response('roles_pago/mostrar_empleados.html', {'detalle': detalle,}, RequestContext(request))
    else:
        detalle = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado',
                                          'apellido')
        return render_to_response('roles_pago/mostrar_empleados.html', {'detalle': detalle,}, RequestContext(request))

@login_required()
def MostrarEgresosView(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_egresos = request.POST["id_txt_otros_egresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_egresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')
        if quincena == 'M':
            detalle = EgresosRolEmpleado.objects.filter(empleado_id=id_txt_otros_egresos).filter(
            anio=anio).filter(mes=mes)
        else:
            detalle = EgresosRolEmpleado.objects.filter(empleado_id=id_txt_otros_egresos).filter(
                quincena=quincena).filter(
                anio=anio).filter(mes=mes)
        return render_to_response('roles_pago/mostrar_egresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio,
                                   'mes': mes, 'quincena': quincena}, RequestContext(request))


    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_egresos = request.POST["id_txt_otros_egresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_egresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('nombre')
        if quincena == 'M':
            detalle = EgresosRolEmpleado.objects.filter(empleado_id=id_txt_otros_egresos).filter(
            anio=anio).filter(mes=mes)
        else:
            detalle = EgresosRolEmpleado.objects.filter(empleado_id=id_txt_otros_egresos).filter(
                quincena=quincena).filter(
                anio=anio).filter(mes=mes)
        return render_to_response('roles_pago/mostrar_egresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio,
                                   'mes': mes, 'quincena': quincena}, RequestContext(request))

@login_required()
def MostrarIngresosView(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_ingresos = request.POST["id_txt_otros_ingresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_ingresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')

        # detalle = IngresosProyectadosEmpleado.objects.filter(empleado_id=id_txt_otros_egresos)
        if quincena == 'M':
            detalle = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                empleado_id=id_txt_otros_ingresos).filter(pagar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,
                                                     tipo_ingreso_egreso_empleado_id=24)
        else:
            detalle = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
                empleado_id=id_txt_otros_ingresos).filter(pagar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,
                                                     quincena=quincena,
                                                     tipo_ingreso_egreso_empleado_id=24)
        return render_to_response('roles_pago/mostrar_ingresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'detalle': detalle,
                                   'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena, 'sueldo': sueldo},
                                  RequestContext(request))


    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        id_txt_otros_ingresos = request.POST["id_txt_otros_ingresos"]
        fila = request.POST["fila"]

        empleados = Empleado.objects.get(empleado_id=id_txt_otros_ingresos)
        tipos = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('nombre')
        # detalle = IngresosProyectadosEmpleado.objects.filter(empleado_id=id_txt_otros_ingresos)
        # sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=id_txt_otros_ingresos,tipo_ingreso_egreso_empleado_id=24)
        if quincena=='M':
            detalle = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                empleado_id=id_txt_otros_ingresos).filter(pagar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,tipo_ingreso_egreso_empleado_id=24)
        else:
            detalle = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
                empleado_id=id_txt_otros_ingresos).filter(pagar=True)
            sueldo = IngresosRolEmpleado.objects.get(empleado_id=id_txt_otros_ingresos, anio=anio, mes=mes,
                                                     quincena=quincena,
                                                     tipo_ingreso_egreso_empleado_id=24)
        return render_to_response('roles_pago/mostrar_ingresos.html',
                                  {'empleados': empleados, 'tipos': tipos, 'detalle': detalle, 'fila': fila,
                                   'anio': anio, 'mes': mes, 'quincena': quincena, 'sueldo': sueldo},
                                  RequestContext(request))

# def index(request, pk):
#     # vista de ejemplo con un hipot?tico modelo Libro
#
#     detalles = RolPago.objects.get(id=pk)
#     mes = detalles.mes
#     anio = detalles.anio
#     quincena = detalles.quincena
#     i = 0
#     html = ''
#     final_ingresos = 0
#     final_otros_ingresos = 0
#     final_egresos = 0
#     final_otros_egresos = 0
#     final_total = 0
#     tipopago = TipoPago.objects.all()
#     if mes == 1:
#         mes_string = 'ENERO'
#     if mes == 2:
#         mes_string = 'FEBRERO'
#     if mes == 3:
#         mes_string = 'MARZO'
#     if mes == 4:
#         mes_string = 'ABRIL'
#     if mes == 5:
#         mes_string = 'Mayo'
#     if mes == 6:
#         mes_string = 'JUNIO'
#     if mes == 7:
#         mes_string = 'JULIO'
#     if mes == 8:
#         mes_string = 'AGOSTO'
#     if mes == 9:
#         mes_string = 'SEPTIEMBRE'
#     if mes == 10:
#         mes_string = 'OCTUBRE'
#     if mes == 11:
#         mes_string = 'NOVIEMBRE'
#     if mes == 12:
#         mes_string = 'DICIEMBRE'
#
#     if detalles:
#         roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')
#
#     for detal in roles:
#         i += 1
#
#         html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center">'
#         html += 'MUEBLES Y DIVERSIDADES<br />MUEDIRSA S.A. <br />RUC: 0992128372001<br />KM.11.5 VIA A DAULE, GUAYAQUIL-ECUADOR '
#         html += '</td></tr>'
#         html += '<tr><td colspan="2" style="text-align:center"><b>ROL DE PAGO MUEDIRSA DE '
#
#         if quincena == '1Q':
#             html += ' PRIMERA QUINCENA '
#         else:
#             html += ' SEGUNDA QUINCENA '
#
#         html += 'DE ' + str(mes_string) + ' ' + str(anio) + '</td></tr></table>'
#
#         dia = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
#             tipo_ausencia_id=3).aggregate(Sum('dias'))
#         valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))
#
#         if dia['dias__sum']:
#             t_dias = (120 - dia['dias__sum']) / 8
#         else:
#             t_dias = 15
#
#         ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
#             empleado_id=detal.empleado_id).filter(pagar=True)
#         total_ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
#             empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
#
#         html += '<table border="1"><tr><td colspan="2"><table border="0"><tr><td colspan="2"><b>Codigo:</b>' + str(
#             detal.empleado.codigo_empleado.encode('utf8')) + '</td></tr>'
#
#         html += '<tr><td colspan="2"><b>Nombre:</b>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td></tr>'
#         html += ''
#         html += '<tr><td colspan="2"><b>Cargo:</b>' + str(
#             detal.empleado.tipo_empleado) + '&nbsp;&nbsp;&nbsp;<b>Area:</b>' + str(
#             detal.empleado.departamento) + '</td></tr>'
#         try:
#             sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
#                                                      empleado_id=detal.empleado_id,
#                                                      tipo_ingreso_egreso_empleado_id=24)
#         except IngresosRolEmpleado.DoesNotExist:
#             sueldo = 0
#
#         html += ''
#         html += '<tr><td colspan="2"><b>Sueldo Basico Mensual:</b>'
#         if sueldo:
#             html += str(round(sueldo.valor_mensual, 2))
#         else:
#             html += '0'
#         html += '</td></tr></table></td>'
#
#         today = datetime.now()  # fecha actual
#         dateFormat = today.strftime("%Y/%m/%d")
#         html += '</td><td colspan="2"><table border="0"><tr><td><b>Cedula:</b>' + str(
#             detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>'
#         if detal.empleado.fecha_ini_reconocida:
#             html += '<tr><td colspan="2"><b>Fecha de Ingreso:</b>' + str(
#                 detal.empleado.fecha_ini_reconocida.strftime("%d/%m/%Y")) + '</td></tr>'
#         else:
#             html += '<tr><td colspan="2"><b>Fecha de Ingreso:</b></td></tr>'
#         html += '<tr><td colspan="2"><b>Fecha Calculo Rol:</b>' + str(
#             detalles.created_at.strftime("%d/%m/%Y")) + '</td></tr>'
#         html += '<tr><td colspan="2"><b>Fecha Calculo Sobre tiempo:</b>' + str(
#             detalles.created_at.strftime("%d/%m/%Y")) + '</td></tr></table></td></tr>'
#         html += '<tr><td colspan="2"><b>D&iacute;as trabajados</b>' + str(t_dias) + '</td><td colspan="2"></td></tr>'
#
#         # if quincena=='1Q':
#         #   html+='<tr><td colspan="4" style="text-align:center"><b>ROL DE 1era QUINCENA</b></td></tr>'
#         # else:
#         #   html+='<tr><td colspan="4" style="text-align:center"><b>ROL DE 2da QUINCENA</b></td></tr>'
#
#         html += '</table>'
#         html += '<table border="1">'
#         html += '<tr><td colspan="2"><b>INGRESOS:</b></td><td colspan="2"><b>EGRESOS:</b></td></tr>'
#         html += '<tr><td colspan="2">'
#         html += '<table>'
#         t_otros_ingresos = 0
#         t_ingresos = 0
#         t_egresos = 0
#         t_otros_egresos = 0
#         tipo_ingreso = TipoIngresoEgresoEmpleado.objects.filter(ingreso=True).order_by('orden')
#         for tip in tipo_ingreso:
#             ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
#                 pagar=True)
#             total_ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
#                 pagar=True).aggregate(Sum('valor'))
#             faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
#                 anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
#                 tipo_ausencia_id=3).aggregate(Sum('valor'))
#
#             if faltas_injustificadas_valor['valor__sum']:
#                 total_desc = float(faltas_injustificadas_valor['valor__sum'])
#                 # html += '<tr><td>AUSENCIAS INSJUSTIFICADAS</td><td style="text-align:right">' + str(round(total_desc, 2)) + '</td></tr>'
#             else:
#                 total_desc = 0
#
#             if ingresos:
#                 if tip.id==5 or tip.id==25 or tip.id==26:
#                     total_horas = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(pagar=True).aggregate(Sum('horas'))
#                     html += '<tr><td>' + str(tip.nombre) + '&nbsp;&nbsp;&nbsp;' +str(round(total_horas['horas__sum'], 2))+'</td><td style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
#                 else:
#                     if tip.id==24 and  faltas_injustificadas_valor['valor__sum']:
#                         s_descontado=total_ingresos['valor__sum']-faltas_injustificadas_valor['valor__sum']
#                         html += '<tr><td>' + str(tip.nombre) + '</td><td style="text-align:right">' + str(round(s_descontado, 2)) + '</td></tr>'
#
#                     else:
#                         html += '<tr><td>' + str(tip.nombre) + '</td><td style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
#
#             if total_ingresos['valor__sum']:
#                 t_ingresos += total_ingresos['valor__sum']
#             else:
#                 t_ingresos += 0
#
#         tipo_otros_ingreso = TipoIngresoEgresoEmpleado.objects.filter(otros_ingresos=True).order_by('orden')
#         for tipoi in tipo_otros_ingreso:
#             otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoi.id).filter(
#                 pagar=True)
#             total_otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoi.id).filter(
#                 pagar=True).aggregate(Sum('valor'))
#             if otros_ingresos:
#                 html += '<tr><td>' + str(tipoi.nombre) + '</td><td style="text-align:right">' + str(
#                     round(total_otros_ingresos['valor__sum'], 2)) + '</td></tr>'
#
#             if total_otros_ingresos['valor__sum']:
#                 t_otros_ingresos += total_otros_ingresos['valor__sum']
#             else:
#                 t_otros_ingresos += 0
#
#
#
#         t_ingresos = float(t_ingresos - (total_desc))
#         total_i = t_ingresos + t_otros_ingresos
#
#         html += '<tr><td><b>TOTAL</b></td><td style="text-align:right">' + str(round(total_i, 2)) + '</td></tr>'
#         html += '</table></td>'
#         html += '<td colspan="2">'
#         html += '<table>'
#         tipo_egreso = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('orden')
#         for tipe in tipo_egreso:
#             egresos = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id)
#             total_egresos = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id).aggregate(
#                 Sum('valor'))
#             if egresos:
#                 html += '<tr><td>' + str(tipe.nombre) + '</td><td style="text-align:right">' + str(
#                     total_egresos['valor__sum']) + '</td></tr>'
#
#             if total_egresos['valor__sum']:
#                 t_egresos += total_egresos['valor__sum']
#             else:
#                 t_egresos += 0
#
#         tipo_otros_egreso = TipoIngresoEgresoEmpleado.objects.filter(otros_egresos=True)
#         for tipoe in tipo_otros_egreso:
#             otros_egresos = OtrosEgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id)
#             total_otros_egresos = OtrosEgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#                 mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id).aggregate(
#                 Sum('valor'))
#             if otros_egresos:
#                 html += '<tr><td>' + str(tipoe.nombre) + '</td><td style="text-align:right">' + str(
#                     round(float(total_otros_egresos['valor__sum']), 2)) + '</td></tr>'
#
#             if total_otros_egresos['valor__sum']:
#                 t_otros_egresos += total_otros_egresos['valor__sum']
#             else:
#                 t_otros_egresos += 0
#
#         dias_j = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
#             empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
#             tipo_ausencia_id=1)
#         total_dias_je = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
#             cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
#         if dias_j:
#
#             html += '<tr><td>PERMISOS</td><td style="text-align:right">' + str(
#                 round(float(total_dias_je['valor__sum']), 2)) + '</td></tr>'
#             total_dias_j = total_dias_je['valor__sum']
#
#         else:
#             total_dias_j = 0
#
#         dias_p = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
#             empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
#             tipo_ausencia_id=2)
#         total_dias_pe = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#             mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
#             cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
#         if dias_p:
#
#             html += '<tr><td>VACACIONES</td><td style="text-align:right">' + str(
#                 round(float(total_dias_pe['valor__sum']), 2)) + '</td></tr>'
#             total_dias_p = total_dias_pe['valor__sum']
#         else:
#             total_dias_p = 0
#
#         total_e = float(t_egresos) + float(t_otros_egresos) + float(total_dias_j) + float(total_dias_p)
#
#         total_dias_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
#             mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
#         if total_dias_valor['valor__sum']:
#             t_dias_valor = total_dias_valor['valor__sum']
#         else:
#             t_dias_valor = 0
#
#         html += '<tr><td><b>TOTAL:&nbsp;&nbsp;&nbsp</b></td><td style="text-align:right">' + str(
#             round(float(total_e), 2)) + '</td><td colspan="2"></td></tr>';
#         # total_cobrar=total_i-total_e-t_dias_valor
#         if detal.ingresos:
#             ingresos_total = detal.ingresos
#         else:
#             ingresos_total = 0
#         if detal.otros_ingresos:
#             oingresos_total = detal.otros_ingresos
#         else:
#             oingresos_total = 0
#         if detal.egresos:
#             egresos_total = detal.egresos
#         else:
#             egresos_total = 0
#         if detal.otros_egresos:
#             oegresos_total = detal.otros_egresos
#         else:
#             oegresos_total = 0
#         if detal.descuento_dias:
#             dias = detal.descuento_dias
#         else:
#             dias = 0
#         total_cobrar = float(ingresos_total) + float(oingresos_total) - float(egresos_total)
#         html += '</table></td>'
#         html += '<tr><td colspan="2" style="text-align:right;vertical-align:middle"></td><td  style="text-align:right;vertical-align:middle"><b>NETO A RECIBIR:</b></td><td>' + str(
#             round(total_cobrar, 2)) + '</td></tr>';
#         html += '<tr><td colspan="4"><table border="0"><tr><td colspan="2">&nbsp;</td><td colspan="2">&nbsp;</td></tr>';
#         html += '<tr><td colspan="2">&nbsp;</td><td colspan="2">&nbsp;</td></tr>';
#         #html += '<tr><td  style="text-align:center;" ><img src="media/imagenes/general/firma_nomina.jpg"  width="100" height="50"><br />-------------------<br />ELABORADO</td><td style="text-align:center">-------------------<br />AUTORIZADO</td><td colspan="2" style="text-align:center">-------------------<br />Recibi Conforme: EMPLEADO</td></tr>';
#         html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>' + str(
#             detal.empleado.nombre_empleado.encode('utf8')) + '</td><td >' + str(
#             detal.empleado.tipo_empleado) + '</td></tr>';
#         html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>C.C.NO</td><td >' + str(
#             detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>';
#
#         html += '<tr><td colspan="4">Nota: Declaro haber recibido conforme el importe del Rol de Pago, sin derecho a reclamo por ning&uacute;n concepto en lo posterior.</td></tr>'
#         html += '</table></td></tr></table>'
#         html += ' <pdf:nextpage />'
#     html1 = render_to_string('roles_pago/imprimir.html', {'pagesize': 'A4', 'html': html,},
#                              context_instance=RequestContext(request))
#     return generar_pdf(html1)
#
#     #         'ordenproduccion':ordenproduccion,
#     #         }
#
#     # return render_to_response(
#     #         'ordenproduccion/imprimir.html',
#     #         context,
#     #         context_instance=RequestContext(request))

def index(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro

    detalles = RolPago.objects.get(id=pk)
    mes = detalles.mes
    anio = detalles.anio
    quincena = detalles.quincena
    i = 0
    html_final= ''
    final_ingresos = 0
    final_otros_ingresos = 0
    final_egresos = 0
    final_otros_egresos = 0
    final_total = 0
    tipopago = TipoPago.objects.all()
    if mes == 1:
        mes_string = 'ENERO'
    if mes == 2:
        mes_string = 'FEBRERO'
    if mes == 3:
        mes_string = 'MARZO'
    if mes == 4:
        mes_string = 'ABRIL'
    if mes == 5:
        mes_string = 'Mayo'
    if mes == 6:
        mes_string = 'JUNIO'
    if mes == 7:
        mes_string = 'JULIO'
    if mes == 8:
        mes_string = 'AGOSTO'
    if mes == 9:
        mes_string = 'SEPTIEMBRE'
    if mes == 10:
        mes_string = 'OCTUBRE'
    if mes == 11:
        mes_string = 'NOVIEMBRE'
    if mes == 12:
        mes_string = 'DICIEMBRE'

    if detalles:
        roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')

    for detal in roles:
        i += 1
        html=''

        html += '<table border="1"><tr><td style="text-align:left">'
        html += 'MUEBLES Y DIVERSIDADES MUEDIRSA S.A. <br />RUC: 0992128372001<br /><b>ROL DE PAGO MUEDIRSA DE '

        if quincena == '1Q':
            html += ' PRIMERA QUINCENA '
        else:
            html += ' SEGUNDA QUINCENA '

        html += 'DE ' + str(mes_string) + ' ' + str(anio)
        html += '</td><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td></tr>'
        html += '</table>'


        dia = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            tipo_ausencia_id=3).aggregate(Sum('dias'))
        valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))

        if dia['dias__sum']:
            t_dias = (120 - dia['dias__sum']) / 8
        else:
            t_dias = 30

        ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(pagar=True)
        total_ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

        html += '<table border="1"><tr><td ><b>Trabajador:</b></td><td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td></tr>'
        html += ''
        html += '<tr><td ><b>Cargo:</b></td><td>' + str(
            detal.empleado.tipo_empleado) + '&nbsp;&nbsp;&nbsp;<b>Area:</b>' + str(
            detal.empleado.departamento) + '</td></tr><tr><td><b>D&iacute;as trabajados</b>' + str(t_dias) + '</td></tr>'
        try:
            sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
                                                     empleado_id=detal.empleado_id,
                                                     tipo_ingreso_egreso_empleado_id=24)
        except IngresosRolEmpleado.DoesNotExist:
            sueldo = 0

        html += ''

        html += '<table border="1">'
        # html += '<tr><td colspan="2"><b>INGRESOS:</b></td><td colspan="2"><b>EGRESOS:</b></td></tr>'
        html += '<tr><td colspan="2">'
        html += '<table>'
        t_otros_ingresos = 0
        t_ingresos = 0
        t_egresos = 0
        t_otros_egresos = 0
        tipo_ingreso = TipoIngresoEgresoEmpleado.objects.exclude(egreso=True).order_by('orden')
        for tip in tipo_ingreso:
            if tip:
                if tip.ingreso== True :
                    ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True)
                    total_ingresos = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True).aggregate(Sum('valor'))
                    faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                        tipo_ausencia_id=3).aggregate(Sum('valor'))

                    if faltas_injustificadas_valor['valor__sum']:
                        total_desc = float(faltas_injustificadas_valor['valor__sum'])
                        # html += '<tr><td>AUSENCIAS INSJUSTIFICADAS</td><td style="text-align:right">' + str(round(total_desc, 2)) + '</td></tr>'
                    else:
                        total_desc = 0


                    if ingresos:
                        if tip.id==5 or tip.id==25 or tip.id==26:
                            total_horas = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(pagar=True).aggregate(Sum('horas'))
                            html += '<tr><td  width="220">' + str(tip.nombre) + '&nbsp;&nbsp;&nbsp;' +str(round(total_horas['horas__sum'], 2))+'</td><td style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
                        else:
                            if tip.id==24 and  faltas_injustificadas_valor['valor__sum']:
                                s_descontado=total_ingresos['valor__sum']-faltas_injustificadas_valor['valor__sum']
                                html += '<tr><td>' + str(tip.nombre) + '</td><td style="text-align:right">' + str(round(s_descontado, 2)) + '</td></tr>'

                            else:
                                html += '<tr><td>' + str(tip.nombre) + '</td><td style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
                    else:
                        html += '<tr><td width="220">' + str(tip.nombre) + '</td><td style="text-align:right">0</td></tr>'


                    if total_ingresos['valor__sum']:
                        t_ingresos += total_ingresos['valor__sum']
                    else:
                        t_ingresos += 0

                if tip.otros_ingresos == True:
                    otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True)
                    total_otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True).aggregate(Sum('valor'))
                    if otros_ingresos:
                        valor_otros_ingresos=total_otros_ingresos['valor__sum']
                    else:
                        valor_otros_ingresos=0
                    html += '<tr><td width="220">' + str(tip.nombre) + '</td><td style="text-align:right">' + str(
                            round(valor_otros_ingresos, 2)) + '</td></tr>'

                    if total_otros_ingresos['valor__sum']:
                        t_otros_ingresos += total_otros_ingresos['valor__sum']
                    else:
                        t_otros_ingresos += 0



        t_ingresos = float(t_ingresos - (total_desc))
        total_i = t_ingresos + t_otros_ingresos


        html += '</table></td>'
        html += '<td colspan="2">'
        html += '<table>'
        tipo_egreso = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('orden')
        for tipe in tipo_egreso:
            egresos = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id)
            total_egresos = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id).aggregate(
                Sum('valor'))
            if egresos:
                valor_egresos=total_egresos['valor__sum']
            else:
                valor_egresos=0
            html += '<tr><td width="300">' + str(tipe.nombre) + '</td><td style="text-align:right">' + str(valor_egresos) + '</td></tr>'

            if total_egresos['valor__sum']:
                t_egresos += total_egresos['valor__sum']
            else:
                t_egresos += 0

        tipo_otros_egreso = TipoIngresoEgresoEmpleado.objects.filter(otros_egresos=True)
        for tipoe in tipo_otros_egreso:
            otros_egresos = OtrosEgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id)
            total_otros_egresos = OtrosEgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id).aggregate(
                Sum('valor'))
            if otros_egresos:
                valor_otros_egresos=total_otros_egresos['valor__sum']
            else:
                valor_otros_egresos =0





            html += '<tr><td>' + str(tipoe.nombre) + '</td><td style="text-align:right">' + str(round(float(valor_otros_egresos), 2)) + '</td></tr>'

            if total_otros_egresos['valor__sum']:
                t_otros_egresos += total_otros_egresos['valor__sum']
            else:
                t_otros_egresos += 0

        dias_j = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
            tipo_ausencia_id=1)
        total_dias_je = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
        if dias_j:


            total_dias_j = total_dias_je['valor__sum']

        else:
            total_dias_j = 0

        html += '<tr><td>PERMISOS</td><td style="text-align:right">' + str(round(float(total_dias_j), 2)) + '</td></tr>'
        dias_p = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
            tipo_ausencia_id=2)
        total_dias_pe = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
        if dias_p:


            total_dias_p = total_dias_pe['valor__sum']
        else:
            total_dias_p = 0

        html += '<tr><td>VACACIONES</td><td style="text-align:right">' + str(round(float(total_dias_p), 2)) + '</td></tr>'
        total_e = float(t_egresos) + float(t_otros_egresos) + float(total_dias_j) + float(total_dias_p)

        total_dias_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
        if total_dias_valor['valor__sum']:
            t_dias_valor = total_dias_valor['valor__sum']
        else:
            t_dias_valor = 0


        # total_cobrar=total_i-total_e-t_dias_valor
        if detal.ingresos:
            ingresos_total = detal.ingresos
        else:
            ingresos_total = 0
        if detal.otros_ingresos:
            oingresos_total = detal.otros_ingresos
        else:
            oingresos_total = 0
        if detal.egresos:
            egresos_total = detal.egresos
        else:
            egresos_total = 0
        if detal.otros_egresos:
            oegresos_total = detal.otros_egresos
        else:
            oegresos_total = 0
        if detal.descuento_dias:
            dias = detal.descuento_dias
        else:
            dias = 0
        total_cobrar = float(ingresos_total) + float(oingresos_total) - float(egresos_total)
        html += '</table></td></tr>'
        html += '<tr><td><b>**TOTAL INGRESOS**</b></td><td style="text-align:right">' + str(
            round(total_i, 2)) + '</td>'
        html += '<td><b>**TOTAL EGRESOS **&nbsp;&nbsp;&nbsp</b></td><td style="text-align:right">' + str(
            round(float(total_e), 2)) + '</td></tr>';
        html += '<tr><td colspan="2" style="text-align:right;vertical-align:middle"></td><td  style="text-align:right;vertical-align:middle"><b>** A RECIBIR **</b></td><td>' + str(
            round(total_cobrar, 2)) + '</td></tr>';
        html += '<tr><td colspan="4"><table border="0"><tr><td colspan="2">ENTREGA</td><td colspan="2">RECIBI CONFORME</td></tr>';
        html += '<tr><td colspan="2">&nbsp;</td><td colspan="2">NOMBRE:' + str(
            detal.empleado.nombre_empleado.encode('utf8')) + '<br />NUM. CEDULA: 0' + str(
            detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>';
        html += '<tr><td colspan="2" style="text-align:center;">_______________________________________<br /> FIRMA</td><td colspan="2"  style="text-align:center;">_______________________________________<br /> FIRMA</td></tr>';
        #html += '<tr><td  style="text-align:center;" ><img src="media/imagenes/general/firma_nomina.jpg"  width="100" height="50"><br />-------------------<br />ELABORADO</td><td style="text-align:center">-------------------<br />AUTORIZADO</td><td colspan="2" style="text-align:center">-------------------<br />Recibi Conforme: EMPLEADO</td></tr>';
        # html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>' + str(
        #     detal.empleado.nombre_empleado.encode('utf8')) + '</td><td >' + str(
        #     detal.empleado.tipo_empleado) + '</td></tr>';
        # html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>C.C.NO</td><td >' + str(
        #     detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>';
        #
        # html += '<tr><td colspan="4">***Nota: Declaro haber recibido conforme el importe del Rol de Pago, sin derecho a reclamo por ning&uacute;n concepto en lo posterior.</td></tr>'
        html += '</table></td></tr></table>'
        html_final+=html
        html_final += html
        #COPIA DEL ROL DE PAGO


        html_final += ' <pdf:nextpage />'
    html1 = render_to_string('roles_pago/imprimir.html', {'pagesize': 'A4', 'html': html_final,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

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

@login_required()
def PlantillaListView(request):
    if request.method == 'POST':
        plantillas = PlantillaRrhh.objects.order_by('id')

        return render_to_response('plantillas/index.html', {'plantillas': plantillas,}, RequestContext(request))


    else:
        plantillas = PlantillaRrhh.objects.order_by('id')

        return render_to_response('plantillas/index.html', {'plantillas': plantillas,}, RequestContext(request))

@login_required()
@transaction.atomic
def PlantillaCreateView(request):
    if request.method == 'POST':
        form = PlantillaRrhhForm(request.POST)
        empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
        tipos = TipoIngresoEgresoEmpleado.objects.all()

        if form.is_valid():
            with transaction.atomic():
                new_orden = form.save()
                new_orden.created_by = request.user.get_full_name()
                new_orden.updated_by = request.user.get_full_name()
                new_orden.created_at = datetime.now()
                new_orden.updated_at = datetime.now()
                new_orden.save()
                try:
                    secuencial = Secuenciales.objects.get(modulo='plantillas')
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
                                proformadetalle = PlantillaRrhhDetalle()
                                proformadetalle.plantilla_rrhh_id = new_orden.id
                                proformadetalle.empleado_id = request.POST["id_kits" + str(i)]
                                proformadetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                                proformadetalle.valor = request.POST["valor_kits" + str(i)]
                                proformadetalle.save()

                    print(i)
                    #print('contadorsd prueba' + str(contador))

                return HttpResponseRedirect('/recursos_humanos/plantilla_rrhh')
        else:
            print 'error'
            print form.errors, len(form.errors)
    else:
        form = PlantillaRrhhForm
        empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
        tipos = TipoIngresoEgresoEmpleado.objects.all()

    return render_to_response('plantillas/create.html', {'form': form, 'empleados': empleados, 'tipos': tipos},
                              RequestContext(request))

class PlantillaUpdateView(ObjectUpdateView):
    def get(self, request, *args, **kwargs):

        plantilla_rrhh = PlantillaRrhh.objects.get(id=kwargs['pk'])
        empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
        tipos = TipoIngresoEgresoEmpleado.objects.all()
        suma = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=plantilla_rrhh.id).aggregate(Sum('valor'))
        total= suma['valor__sum']

        form = PlantillaRrhhForm(instance=plantilla_rrhh)
        detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=plantilla_rrhh.id).order_by('id')

        context = {
            'section_title': 'Actualizar Presupuesto',
            'button_text': 'Actualizar',
            'form': form,
            'empleados': empleados,
            'detalle': detalle,
            'total':total,
            'tipos': tipos
        }

        return render_to_response(
            'plantillas/actualizar.html', context, context_instance=RequestContext(request))

    def post(sel, request, *args, **kwargs):
        plantilla_rrhh = PlantillaRrhh.objects.get(id=kwargs['pk'])
        form = PlantillaRrhhForm(request.POST, request.FILES, instance=plantilla_rrhh)
        p_id = kwargs['pk']
        print(p_id)
        print form.is_valid(), form.errors, type(form.errors)
        empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
        tipos = TipoIngresoEgresoEmpleado.objects.all()

        if form.is_valid():

            new_orden = form.save()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            contador = request.POST["columnas_receta"]

            i = 0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kits' + str(i) in request.POST:
                        product = Empleado.objects.get(empleado_id=request.POST["id_kits" + str(i)])

                        cont = request.POST["id_kits" + str(i)]
                        if cont:
                            if 'id_detalle' + str(i) in request.POST:
                                detalle_id = request.POST["id_detalle" + str(i)]
                                detallecompra = PlantillaRrhhDetalle.objects.get(id=detalle_id)
                                detallecompra.updated_by = request.user.get_full_name()
                                detallecompra.empleado = product
                                detallecompra.plantilla_rrhh_id = new_orden.id
                                detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                                detallecompra.valor = request.POST["valor_kits" + str(i)]
                                detallecompra.save()

                                print('Tiene detalle' + str(i))
                            else:
                                comprasdetalle = PlantillaRrhhDetalle()
                                comprasdetalle.plantilla_rrhh_id = new_orden.id
                                comprasdetalle.empleado = product
                                comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                                comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                                comprasdetalle.save()
                                i += 1
                                print('No Tiene detalle' + str(i))
                                #print('contadorsd prueba' + str(contador))
            # ordencompra_form=OrdenCompraForm(request.POST)
            detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=p_id)
            empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
            tipos = TipoIngresoEgresoEmpleado.objects.all()

            context = {
                'section_title': 'Actualizar Proforma',
                'button_text': 'Actualizar',
                'form': form,
                'detalle': detalle,
                'empleados': empleados,
                'tipos': tipos,
                'mensaje': 'Proforma actualizada con exito'}

            return render_to_response(
                'plantillas/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:

            form = PlantillarRrhhForm(request.POST)
            detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=plantilla_rrhh.id)
            empleados = Empleado.objects.values('empleado_id', 'codigo_empleado', 'cedula_empleado', 'nombre_empleado')
            tipos = TipoIngresoEgresoEmpleado.objects.all()

            context = {
                'section_title': 'Actualizar Proforma',
                'button_text': 'Actualizar',
                'form': form,
                'detalle': detalle,
                'empleados': empleados,
                'tipos': tipos,
                'mensaje': 'Proforma actualizada con exito'}

        return render_to_response(
            'plantillas/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@csrf_exempt
def obtenerRolPlantillas(request):
    if request.method == 'POST':

        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        plantillas = PlantillaRrhh.objects.all()
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        try:
            rol = RolPagoPlantilla.objects.filter(quincena=quincena, anio=anio, mes=mes)
        except RolPagoPlantilla.DoesNotExist:
            rol = None

        if rol:
            html += '<form id="formid">'
            for am in plantillas:
                html += '<input type="checkbox" id="' + str(am.id) + '" value="' + str(am.id) + '" name="plantillas[]"'
                for r in rol:
                    if r.plantilla_rrhh_id == am.id:
                        html += ' checked="checked" '
                    else:
                        h1=0
                        #print('contadorsd prueba')

                html += ' >   ' + str(am.nombre) + '<br />'
            html += '</form>'
        else:
            html += '<form id="formid">'
            for am in plantillas:
                html += '<input type="checkbox" id="' + str(am.id) + '" value="' + str(
                    am.id) + '" name="plantillas[]" >   ' + str(am.nombre) + '<br />'
            html += '</form>'

        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def agregarPlantillas(request):
    if request.method == 'POST':
        plantillas = request.POST["selected"]
        my_list = plantillas.split(",")
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        for r in my_list:
            print('valoor' + str(r))
            if int(r) > 0:
                print('entro' + str(r))
                try:
                    plantillas_detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=r)
                except PlantillaRrhhDetalle.DoesNotExist:
                    plantillas_detalle = None

                if plantillas_detalle:
                    try:
                        rol_pago = RolPagoPlantilla.objects.filter(plantilla_rrhh_id=r).filter(mes=mes).filter(anio=anio).filter(quincena=quincena)
                    except RolPagoPlantilla.DoesNotExist:
                        rol_pago = None
                    if rol_pago:
                        print('existe')
                    else:


                        pl = RolPagoPlantilla()
                        pl.plantilla_rrhh_id = r
                        pl.created_by = request.user.get_full_name()
                        pl.updated_by = request.user.get_full_name()
                        pl.created_at = datetime.now()
                        pl.updated_at = datetime.now()
                        pl.anio = anio
                        pl.mes = mes
                        pl.quincena = quincena
                        pl.save()

                        for pd in plantillas_detalle:
                            if pd.tipo_ingreso_egreso_empleado.ingreso:
                                cuent = IngresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.pagar = True
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.otros_ingresos:
                                cuent = OtrosIngresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.pagar = True
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.egreso:
                                cuent = EgresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.otros_egresos:
                                cuent = OtrosEgresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()

                    html = 'Se agrego satisfactoriamente'
                else:
                    html = 'Error durante la ejecucion'

        return HttpResponse(
                html
            )    
    else:
        plantillas = request.POST["selected"]
        my_list = plantillas.split(",")
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        for r in my_list:
            print('vaalor' + str(r))
            if r > 0:
                try:
                    plantillas_detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=r)
                except PlantillaRrhhDetalle.DoesNotExist:
                    plantillas_detalle = None
                if plantillas_detalle:
                    try:
                        rol_pago = RolPagoPlantilla.objects.filter(plantilla_rrhh_id=r).filter(mes=mes).filter(anio=anio).filter(quincena=quincena)
                    except RolPagoPlantilla.DoesNotExist:
                        rol_pago = None
                    if rol_pago:
                        print('existe')
                    else:
                        pl = RolPagoPlantilla()
                        pl.plantilla_rrhh_id = r
                        pl.created_by = request.user.get_full_name()
                        pl.updated_by = request.user.get_full_name()
                        pl.created_at = datetime.now()
                        pl.updated_at = datetime.now()
                        pl.anio = anio
                        pl.mes = mes
                        pl.quincena = quincena
                        pl.save()
                        for pd in plantillas_detalle:
                            if pd.tipo_ingreso_egreso_empleado.ingreso:
                                cuent = IngresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.otros_ingresos:
                                cuent = OtrosIngresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.egreso:
                                cuent = EgresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()
                            if pd.tipo_ingreso_egreso_empleado.otros_egresos:
                                cuent = OtrosEgresosRolEmpleado()
                                cuent.tipo_ingreso_egreso_empleado_id = pd.tipo_ingreso_egreso_empleado_id
                                cuent.anio = anio
                                cuent.mes = mes
                                cuent.quincena = quincena
                                cuent.empleado_id = pd.empleado_id
                                cuent.valor = pd.valor
                                cuent.plantilla_rrhh_id = r
                                cuent.nombre = pd.tipo_ingreso_egreso_empleado.nombre
                                cuent.created_by = request.user.get_full_name()
                                cuent.updated_by = request.user.get_full_name()
                                cuent.created_at = datetime.now()
                                cuent.updated_at = datetime.now()
                                cuent.save()

                    html = 'Se agrego satisfactoriamente'
                else:
                    html = 'Error durante la ejecucion'

        return HttpResponse(
            html
        )

@login_required()
def obtenerOtrosIngresos(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        empleado_id = request.POST["empleado_id"]

        fila = request.POST["fila"]
        if quincena =='M':
            detalle = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=empleado_id).aggregate(Sum('valor'))
        else:
            detalle = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=empleado_id).aggregate(Sum('valor'))
        html = detalle['valor__sum']
        print('HTML' + str(html))
        return HttpResponse(
            html
        )

    else:
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        empleado_id = request.POST["empleado_id"]

        fila = request.POST["fila"]

        if quincena =='M':
            detalle = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=empleado_id).aggregate(Sum('valor'))
        else:
            detalle = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=empleado_id).aggregate(Sum('valor'))
        html = detalle['valor__sum']
        print('HTML' + str(html))
        return HttpResponse(
            html
        )

@login_required()
@csrf_exempt
def verRolGlobal(request, pk):
    if request.method == 'POST':
        html = ''

    else:
        detalles = RolPago.objects.get(id=pk)
        mes = detalles.mes
        anio = detalles.anio
        quincena = detalles.quincena
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        if detalles:
            roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')
            id = detalles.id
        for detal in roles:
            i += 1
            try:
                sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
                                                         empleado_id=detal.empleado_id,
                                                         tipo_ingreso_egreso_empleado_id=24)
            except IngresosRolEmpleado.DoesNotExist:
                sueldo = 0
            html += '<tr>'
            html += '<td>' + str(detal.empleado.cedula_empleado) + '</td>'
            html += '<td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.empleado.departamento) + '</td>'
            html += '<td>' + str(detal.empleado.tipo_empleado) + '</td>'
            if sueldo:
                html += '<td style="text-align:right">' + str("%0.2f" % sueldo.valor_mensual).replace('.', ',') + '</td>'

            else:
                html += '<td style="text-align:right">0</td>'

            ingresos_total = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if ingresos_total['valor__sum']:
                t_ingresoT = ingresos_total['valor__sum']
            else:
                t_ingresoT = 0

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                total_desc = float(faltas_injustificadas_valor['valor__sum'])
            else:
                total_desc = 0

            # total_ingresos = float(t_ingresoT - (total_desc))
            total_ingresos = float(t_ingresoT)
            dias_trabajados = 0
            dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('dias'))
            if dias['dias__sum']:
                total_dias = float(dias['dias__sum'])
                dias_trabajados = float((dias_trabajados * 8) - total_dias) / 8
            else:
                dias_trabajados = 15

            html += '<td>' + str(dias_trabajados) + '</td>'

            sueldo_valor = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).aggregate(
                Sum('valor'))

            if sueldo_valor['valor__sum']:
                html += '<td style="text-align:right">' +str("%0.2f" % sueldo_valor['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            otros_ingresos_total = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

            otros_ingresos_horas_feriados = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('valor'))

            cantidad_horas_feriados = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('horas'))

            otros_ingresos_horas_normal = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('valor'))

            cantidad_horas_normal = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('horas'))

            otros_ingresos_horas_fines = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('valor'))

            cantidad_horas_fines = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('horas'))

            otros_ingresos_comisiones = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=4).aggregate(Sum('valor'))

            otros_ingresos_bonificaciones = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=3).aggregate(Sum('valor'))

            otros_ingresos_movilizacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=31).aggregate(Sum('valor'))

            otros_ingresos_freserva = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7).aggregate(Sum('valor'))

            otros_ingresos_alimentacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=1).aggregate(Sum('valor'))

            otros_ingresos_dtercero = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))

            otros_ingresos_dcuarto = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(
                tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))

            otros_ingresos_iasumido = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=27).aggregate(Sum('valor'))

            otros_ingresos_irenta = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            if cantidad_horas_feriados['horas__sum']:
                html += '<td >' + str(cantidad_horas_feriados['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_feriados['valor__sum']:
                html += '<td style="text-align:right">' + str(otros_ingresos_horas_feriados['valor__sum']) + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if cantidad_horas_normal['horas__sum']:
                html += '<td>' + str(cantidad_horas_normal['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_normal['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_horas_normal['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if cantidad_horas_fines['horas__sum']:
                html += '<td>' + str(cantidad_horas_fines['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_fines['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_horas_fines['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_comisiones['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_comisiones['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_bonificaciones['valor__sum']:
                html += '<td style="text-align:right">' +  str("%0.2f" % otros_ingresos_bonificaciones['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_alimentacion['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_alimentacion['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_movilizacion['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_movilizacion['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_freserva['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_freserva['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_dtercero['valor__sum']:
                html += '<td style="text-align:right">' +str("%0.2f" % otros_ingresos_dtercero['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_ingresos_dcuarto['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_dcuarto['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_ingresos_iasumido['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_iasumido['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_irenta['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_irenta['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_total['valor__sum']:
                suma_ingresos_otros_ingresos = total_ingresos + float(
                    otros_ingresos_total['valor__sum'])
            else:
                suma_ingresos_otros_ingresos = total_ingresos

            html += '<td style="text-align:right">' + str("%0.2f" % suma_ingresos_otros_ingresos).replace('.', ',') + '</td>'

            egresos_total = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_total = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_nueve = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))
            otros_egresos_tres = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=30).aggregate(Sum('valor'))

            otros_egresos_atraso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_descir = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=20).aggregate(Sum('valor'))

            otros_egresos_falta = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_multa = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=21).aggregate(Sum('valor'))

            otros_egresos_hipotecario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=13).aggregate(Sum('valor'))

            otros_egresos_permiso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=40).aggregate(Sum('valor'))

            otros_egresos_quirografario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

            otros_egresos_anticipo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))

            otros_egresos_movistar = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

            otros_egresos_ptmo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

            otros_egresos_contribucion = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=32).aggregate(Sum('valor'))

            otros_egresos_otros = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                faltas = float(faltas_injustificadas_valor['valor__sum'])
            else:
                faltas = 0

            if otros_egresos_nueve['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_nueve['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_egresos_tres['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_tres['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            atrasos = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).exclude(tipo_ausencia_id=2).exclude(tipo_ausencia_id=3).exclude(
                tipo_ausencia_id=1).aggregate(Sum('valor'))
            if atrasos['valor__sum']:
                atras = float(atrasos['valor__sum'])
            else:
                atras = 0

            html += '<td>' + str(atras) + '</td>'

            # if otros_egresos_atraso['valor__sum']:
            #     html += '<td>' + str(otros_egresos_atraso['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'


            html += '<td>' + str(faltas) + '</td>'

            faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
            if faltas_justificadas_valor['valor__sum']:
                permisos = float(faltas_justificadas_valor['valor__sum'])
            else:
                permisos = 0
            
            if otros_egresos_permiso['valor__sum']:
                permisos = float(permisos+otros_egresos_permiso['valor__sum'])
                

            html += '<td>' + str(permisos) + '</td>'

            if otros_egresos_anticipo['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_anticipo['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_ptmo['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_ptmo['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_movistar['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_movistar['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_quirografario['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_quirografario['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_hipotecario['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_hipotecario['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_descir['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_descir['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_contribucion['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_contribucion['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_otros['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_otros['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            # if otros_egresos_falta['valor__sum']:
            #     html += '<td>' + str(otros_egresos_falta['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'
            if otros_egresos_multa['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_multa['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            # html+='<td>'+str(total_desc)+'</td>'

            if egresos_total['valor__sum']:
                egres_t = egresos_total['valor__sum']
            else:
                egres_t = 0

            if otros_egresos_total['valor__sum']:

                # html += '<td>' + str(otros_egresos_total['valor__sum']) + '</td>'
                otros_egre_t = otros_egresos_total['valor__sum']
            else:
                # html += '<td>0</td>'
                otros_egre_t = 0

            suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos + total_desc
            html += '<td style="text-align:right">' +  str("%0.2f" % suma_egresos_otros_egresos).replace('.', ',')+ '</td>'
            # html+='<td>'+str(detal.otros_egresos)+'</td>'
            if suma_ingresos_otros_ingresos:
                suma_ingresos_otros_ingresos = suma_ingresos_otros_ingresos

            else:
                suma_ingresos_otros_ingresos = 0

            total_recibir_mensual = suma_ingresos_otros_ingresos - suma_egresos_otros_egresos
            html += '<td style="text-align:right">' +  str("%0.2f" % total_recibir_mensual).replace('.', ',') + '</td>'
        context = {
            'html': html,
            'anio': anio,
            'mes': mes,
            'id': pk,

        }
        return render_to_response('roles_pago/verRolGlobal.html', context, context_instance=RequestContext(request))

@login_required()
def verRolBanco(request, pk):
    if request.method == 'POST':
        html = ''
    else:
        html = ''
        detalles = RolPago.objects.get(id=pk)
        quincena = detalles.quincena
        anio = detalles.anio
        mes = detalles.mes
        if detalles:
            roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id)
            for detal in roles:
                html += ' <tr>'
                if detal.empleado.tipo_documento == 'Cedula':
                    html += '<td>C</td>'
                else:
                    html += '<td>P</td>'
                html += '<td>' + str(detal.empleado.cedula_empleado.encode('utf8')) + '</td>'
                html += '<td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
                html += '<td> PAGO' + str(quincena) + '</td>'
                if detal.empleado.banco_id == 2:
                    html += '<td>CUE</td>'
                    html += '<td>34</td>'
                else:
                    html += '<td>COB</td>'
                    html += '<td>'+ str(detal.empleado.banco.macro_rrhh) + '</td>'
                if detal.empleado.tipo_cuenta_id == 5:
                    html += '<td>04</td>'
                else:
                    html += '<td>03</td>'
                if detal.empleado.cuenta_contable:
                    html += '<td>' + str(detal.empleado.cuenta_contable) + '</td>'
                else:
                    html += '<td>0</td>'
                if detal.ingresos:
                    ingresos_total = detal.ingresos
                else:
                    ingresos_total = 0
                if detal.otros_ingresos:
                    oingresos_total = detal.otros_ingresos
                else:
                    oingresos_total = 0
                if detal.egresos:
                    egresos_total = detal.egresos
                else:
                    egresos_total = 0
                if detal.otros_egresos:
                    oegresos_total = detal.otros_egresos
                else:
                    oegresos_total = 0

                if detal.descuento_dias:
                    dias = detal.descuento_dias
                else:
                    dias = 0
                total = ingresos_total + oingresos_total - egresos_total - oegresos_total
                html += '<td>' + str(round(float(total), 2)) + '</td></tr>'
        context = {
            'anio': anio,
            'mes': mes,
            'quincena': quincena,
            'html': html
        }
        return render_to_response('roles_pago/verRolBanco.html', context, context_instance=RequestContext(request))


@login_required()
def eliminarDetalleOtrosIngresoView(request):
    pk = request.POST["id"]
    objetos = OtrosIngresosRolEmpleado.objects.get(id=pk)

    objetos.delete()
    return HttpResponse(

    )


@login_required()
def eliminarDetalleOtrosEgresoView(request):
    pk = request.POST["id"]
    objetos = OtrosEgresosRolEmpleado.objects.get(id=pk)

    objetos.delete()
    return HttpResponse(

    )


@login_required()
def eliminarDetalleDiasView(request):
    pk = request.POST["id"]
    objetos = DiasNoLaboradosRolEmpleado.objects.get(id=pk)

    objetos.delete()
    return HttpResponse(

    )

@login_required()
@csrf_exempt
def obtenerEmpleadosDias(request):
    if request.method == 'POST':
        empleados = Empleado.objects.all().order_by('nombre_empleado')
        tipopago = TipoAusencia.objects.all()
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        departamento = request.POST["departamento"]
        empleado = request.POST["empleado"]
        #fecha = request.POST["fecha"]
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        cursor = connection.cursor()
        sql = 'select d.id,d.empleado_id from dias_no_laborados_rol_empleado d,departamento de,empleados_empleado e  where d.empleado_id=e.empleado_id and e.departamento_id=de.id and 1=1 '
        if mes != '':
            sql += ' and d.mes=' + mes
        if anio != '':
            sql += " and d.anio='" + anio + "' "
        # if quincena != '':
        #     sql += " and d.quincena='" + quincena + "' "
        if empleado != '0':
            sql += ' and d.empleado_id=' + empleado
        if departamento != '0':
            sql += ' and de.id=' + departamento
        # if fecha != '':
        #     sql += " and d.fecha='" + fecha + "' "

        sql += ';'
        cursor.execute(sql)
        rol = cursor.fetchall()

        # try:
        #   rol = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena,anio=anio,mes=mes)
        # except DiasNoLaboradosRolEmpleado.DoesNotExist:
        #   rol = None

        if rol:

            for r in rol:
                detal = DiasNoLaboradosRolEmpleado.objects.get(id=r[0])
                i += 1
                ingresos = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor_mensual'))
                egresos = EgresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor_mensual'))
                valor_diario = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor_diario'))
                try:
                    sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                     tipo_ingreso_egreso_empleado_id=24)
                except IngresosProyectadosEmpleado.DoesNotExist:
                    sueldo = 0

                html += '<tr>'
                html += '<td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
                    i) + '" id="id_empleado' + str(i) + '" value="' + str(
                    detal.empleado_id) + '"/><input type="hidden" name="id' + str(i) + '" id="id' + str(
                    i) + '" value="' + str(detal.id) + '"/></td><td>' + str(
                    detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
                html += '<td><select class=" form-control input-sm" id="tipo' + str(
                    i) + '" maxlength="15" name="tipo' + str(i) + '" onchange="calcular(' + str(i) + ',' + str(
                    sueldo.valor_mensual) + ');">'
                html += '<option value="0">Seleccione</option>'
                for am in tipopago:
                    html += '<option value="' + str(am.id) + '"'
                    if am.id == detal.tipo_ausencia_id:
                        html += ' selected="selected"'
                    html += '>' + str(am.nombre) + '</option>'

                html += '</select>'
                # html += '<td class="text-center"><input type="text" name="fecha' + str(i) + '" id="fecha' + str(
                #     i) + '" value="' + str(detal.fecha) + '"/></td>'
                html += '<td class="text-center"><input type="text" name="hora' + str(i) + '" id="hora' + str(
                    i) + '" value="' + str(detal.dias) + '" onKeyUp="calcular(' + str(i) + ',' + str(
                    sueldo.valor_mensual) + ');"/></td>'
                html += '<td class="text-center"><input type="text" name="valor' + str(i) + '" id="valor' + str(
                    i) + '" value="' + str(detal.valor) + '"/></td>'
                html += '<td class="text-center"><input type="checkbox" id="descontar' + str(
                    i) + '" name="descontar' + str(i) + '" '
                if detal.descontar:
                    html += 'checked="checked"'
                html += '/></td>'
                html += '<td class="text-center"><input type="checkbox" id="vacaciones' + str(
                    i) + '" name="vacaciones' + str(i) + '" '
                if detal.cargar_vacaciones:
                    html += 'checked="checked"'
                html += '/></td>'
                html += '</tr>'

            html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
                i) + '" />'
        else:
            html += '<tr><td colspan="8">No existen datos</td></tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def DiasTrabajadosView(request):
    if request.method == 'POST':

        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        contador = request.POST["columnas_receta_roles"]

        i = 0
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_empleado' + str(i) in request.POST:
                    id = request.POST["id" + str(i)]
                    detallecompra = DiasNoLaboradosRolEmpleado.objects.get(id=id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.created_by = request.user.get_full_name()
                    detallecompra.dias = request.POST["hora" + str(i)]
                    tipo = request.POST["tipo" + str(i)]
                    if tipo == '0':
                        print 'hola'
                    else:
                        detallecompra.tipo_ausencia_id = request.POST["tipo" + str(i)]
                    detallecompra.valor = request.POST["valor" + str(i)]
                    #detallecompra.fecha = request.POST["fecha" + str(i)]
                    detallecompra.descontar = request.POST.get('descontar' + str(i), False)
                    detallecompra.cargar_vacaciones = request.POST.get('vacaciones' + str(i), False)

                    detallecompra.save()
                else:
                    print('entrosd')

        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoAusencia.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        departamentos = Departamento.objects.all()
        anio= Anio.objects.all()

        return render_to_response('dias_no_trabajados/index.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio': anio, 
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoAusencia.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        departamentos = Departamento.objects.all()
        anio= Anio.objects.all()
        return render_to_response('dias_no_trabajados/index.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio': anio,
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))

@login_required()
def HorasExtrasView(request):
    if request.method == 'POST':

        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        contador = request.POST["columnas_receta_roles"]

        i = 0
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_empleado' + str(i) in request.POST:
                    id = request.POST["id" + str(i)]
                    detallecompra = IngresosRolEmpleado.objects.get(id=id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.created_by = request.user.get_full_name()
                    detallecompra.horas = request.POST["hora" + str(i)]
                    tipo = request.POST["tipo" + str(i)]
                    if tipo == '0':
                        print 'hola'
                    else:
                        detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipo" + str(i)]
                    detallecompra.valor = request.POST["valor" + str(i)]
                    detallecompra.pagar = request.POST.get('pagar' + str(i), False)
                    #detallecompra.fecha = request.POST["fecha" + str(i)]

                    detallecompra.save()
                else:
                    print('entrosd')

        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoAusencia.objects.all()
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        departamentos = Departamento.objects.all()
        anio= Anio.objects.all()

        return render_to_response('horas_extras/index.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio': anio,
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        tipopago = TipoIngresoEgresoEmpleado.objects.filter(id__in=[5, 25, 26])
        banco = Banco.objects.all()
        empleados = Empleado.objects.all()
        departamentos = Departamento.objects.all()
        anio= Anio.objects.all()
        return render_to_response('horas_extras/index.html',
                                  {'rol_cuentas': rol_cuentas, 'banco': banco, 'tipopago': tipopago,'anio': anio,
                                   'empleados': empleados, 'departamentos': departamentos}, RequestContext(request))

@login_required()
def obtenerEmpleadosHorasExtras(request):
    if request.method == 'POST':
        empleados = Empleado.objects.all().order_by('nombre_empleado')
        tipopago = TipoIngresoEgresoEmpleado.objects.filter(id__in=[5, 25, 26])
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        departamento = request.POST["departamento"]
        empleado = request.POST["empleado"]
        #fecha = request.POST["fecha"]
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        cursor = connection.cursor()
        sql = 'select d.id,d.empleado_id from ingresos_rol_empleado d,departamento de,empleados_empleado e  where d.empleado_id=e.empleado_id and e.departamento_id=de.id and 1=1 and d.tipo_ingreso_egreso_empleado_id IN (5,25,26) '
        if mes != '':
            sql += ' and d.mes=' + mes
        if anio != '':
            sql += " and d.anio='" + anio + "' "
        # if quincena != '':
        #     sql += " and d.quincena='" + quincena + "' "
        if empleado != '0':
            sql += ' and d.empleado_id=' + empleado
        if departamento != '0':
            sql += ' and de.id=' + departamento
        # if fecha != '':
        #     sql += " and d.fecha='" + fecha + "' "

        sql += ' order by d.empleado_id;'
        cursor.execute(sql)
        rol = cursor.fetchall()

        if rol:

            for det in rol:
                detal = IngresosRolEmpleado.objects.get(id=det[0])

                i += 1
                ingresos = IngresosRolEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor'))
                egresos = EgresosRolEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor'))
                valor_diario = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id).aggregate(
                    Sum('valor_diario'))
                try:
                    sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                     tipo_ingreso_egreso_empleado_id=24)
                except IngresosProyectadosEmpleado.DoesNotExist:
                    sueldo = 0

                html += '<tr>'
                html += '<td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
                    i) + '" id="id_empleado' + str(i) + '" value="' + str(
                    detal.empleado_id) + '"/><input type="hidden" name="id' + str(i) + '" id="id' + str(
                    i) + '" value="' + str(detal.id) + '"/></td><td>' + str(
                    detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
                html += '<td><select class=" form-control input-sm" id="tipo' + str(
                    i) + '" maxlength="15" name="tipo' + str(i) + '" onchange="calcular(' + str(i) + ',' + str(
                    sueldo.valor_mensual) + ');">'
                html += '<option value="0">Seleccione</option>'
                for am in tipopago:
                    html += '<option value="' + str(am.id) + '"'
                    if am.id == detal.tipo_ingreso_egreso_empleado_id:
                        html += ' selected="selected"'
                    html += '>' + str(am.nombre) + '</option>'

                html += '</select>'
                # html += '<td class="text-center"><input type="text" name="fecha' + str(i) + '" id="fecha' + str(
                #     i) + '" value="' + str(detal.fecha) + '"/></td>'
                html += '<td class="text-center"><input type="text" name="hora' + str(i) + '" id="hora' + str(
                    i) + '" value="' + str(detal.horas) + '" onKeyUp="calcular(' + str(i) + ',' + str(
                    sueldo.valor_mensual) + ');"/></td>'
                html += '<td class="text-center"><input type="text" name="valor' + str(i) + '" id="valor' + str(
                    i) + '" value="' + str(detal.valor) + '" readonly="readonly"/></td>'
                html += '<td class="text-center"><input type="checkbox" name="pagar' + str(i) + '" id="pagar' + str(
                    i) + '"'
                if detal.pagar:
                    html += ' checked="checked" '


                html += '/></td>'
                html += '</tr>'

            html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
                i) + '" />'
        else:
            html += '<tr><td colspan="8">No existen datos</td></tr>'
        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
def tipoSolicitudView(request):
    tipos = TipoSolicitud.objects.all()
    new = TipoSolicitudForm
    return render_to_response('solicitud/index.html', {'tipos': tipos, 'new': new}, RequestContext(request))

@login_required()
@csrf_exempt
def createTipoSolicitud(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        response_data = {}

        tipo = TipoSolicitud(codigo=codigo, descripcion=descripcion)
        tipo.save()

        response_data['result'] = 'Create TIPO successful!'
        response_data['postpk'] = tipo.pk
        response_data['codigo'] = tipo.codigo
        tipos = TipoSolicitud.objects.all()

        # html = render_to_string('solicitud/tipo.html', {'tipos': tipos})
        # return HttpResponse(html)
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required
def solicitudLisView(request):
    list = Permiso.objects.all().order_by('-fecha_solicitud')
    new = PermisoForm
    return render_to_response('solicitud/solicitud-list.html', {'list': list, 'new': new}, RequestContext(request))

@login_required()
@csrf_exempt
def createSolicitud(request):
    if request.method == 'POST':
        #fecha_desde_hasta = request.POST.get('fecha_desde_hasta')
        total_dias_ausencia = request.POST.get('total_dias_ausencia')

        total_horas_ausencia = request.POST.get('total_horas_ausencia')
        optradio = request.POST.get('optradio')
        tipo_permiso = request.POST.get('tipo_permiso')
        cargo_vacaciones = request.POST.get('cargo_vacaciones')
        observacion = request.POST.get('observacion')
        motivo_trabajo=False
        motivo_personal= False
        motivo_calamidad=False
        motivo_enfermedad=False
        permisos_dias=False
        permisos_horas = False
        licencia_dias = False
        descanso_iess_dias = False
        cita_iess_horas = False
        total_dias_gozados = request.POST.get('total_dias_gozados')
        total_dias_pendientes = request.POST.get('total_dias_pendientes')
        periodo_dias_pendiente = request.POST.get('periodo_dias_pendiente')
        vacaciones_radio = request.POST.get('vacaciones_radio')
        vacaciones=False
        periodo=False
        hora_desde='00:00:00'
        hora_hasta='00:00:00'
        if vacaciones_radio == '1':
            vacaciones=True

        if vacaciones_radio == '2':
            periodo=True



        print('MOTIVO' + str(optradio))
        print('entrosd')
        if optradio == '1':
            motivo_trabajo=True
            print('ENTRO1')
        if optradio == '2':
            motivo_personal=True
            print('ENTRO2')
        if optradio == '3':
            motivo_calamidad=True
            print('ENTRO3')
        if optradio == '4':
            motivo_enfermedad=True
            print('ENTRO4')


        if tipo_permiso == '1':
            permisos_dias=True
            print('EN1')
        if tipo_permiso == '2':
            permisos_horas=True
            hora_desde = request.POST.get('hora_desde')
            hora_hasta = request.POST.get('hora_hasta')
            print('EN2')
        if tipo_permiso == '3':
            licencia_dias=True
            print('EN3')
        if tipo_permiso == '4':
            descanso_iess_dias=True
            print('EN4')
        if tipo_permiso == '5':
            cita_iess_horas=True
            print('EN5')

        desde = request.POST.get('fecha_desde')
        hasta = request.POST.get('fecha_hasta')
        total_horas_laboradas = 0



        id_tipo = request.POST.get('tipo')
        if id_tipo== '3':
            hora_desde = request.POST.get('hora_desde')
            hora_hasta = request.POST.get('hora_hasta')
            total_horas_ausencia =0
            total_dias_ausencia=0
            desde = None
            hasta = None
            total_dias_pendientes = 0
            periodo_dias_pendiente = 0
            total_dias_gozados = 0
            total_horas_laboradas = request.POST.get('total_horas_laboradas')
        else:
            if id_tipo == '1':
                total_horas_ausencia = 0

            if total_horas_ausencia.isdigit():
                print('Si hay numero')
            else:
                total_horas_ausencia = 0
                total_horas_laboradas= 0


        fecha = request.POST.get('fecha')
        id_empleado = request.POST.get('empleado')
        tipo = TipoSolicitud.objects.get(pk=id_tipo)
        empleado = Empleado.objects.get(empleado_id=id_empleado)

        created_by = request.user.get_full_name()
        created_at = datetime.now()
        response_data = {}



        p = Permiso(tipo_solicitud=tipo, fecha_solicitud=fecha, empleados_empleado=empleado,
                    nombre_empleado=empleado.nombre_empleado,
                    fecha_desde=desde,fecha_hasta=hasta,hora_desde=hora_desde,permisos_dias=permisos_dias,permisos_horas=permisos_horas,
                    licencia_dias=licencia_dias,descanso_iess_dias=descanso_iess_dias,cita_iess_horas=cita_iess_horas,hora_hasta=hora_hasta,total_dias_ausencia=total_dias_ausencia,total_horas_ausencia=total_horas_ausencia,
                    cargo_vacaciones=cargo_vacaciones,observacion=observacion,motivo_trabajo=motivo_trabajo,motivo_personal=motivo_personal,motivo_calamidad=motivo_calamidad,motivo_enfermedad=motivo_enfermedad,
                    cargo_empleado=empleado.departamento,created_by=created_by, created_at=created_at,periodo_dias_pendiente=periodo_dias_pendiente,
                    total_dias_gozados=total_dias_gozados,total_dias_pendientes=total_dias_pendientes,vacaciones=vacaciones,periodo=periodo,total_horas_laboradas=total_horas_laboradas)
        p.save()

        response_data['result'] = 'Una nueva solicitud ha sido creada!'
        response_data['postpk'] = p.pk

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required()
@csrf_exempt
def updateSolicitud(request):
    if request.method == 'POST':

        id_solicitud = request.POST.get('id')
        estado = request.POST.get('estado')

        p = Permiso.objects.get(pk=id_solicitud)

        if estado == '2':
            p.activo = 1
        if estado == '3':
            p.activo = 0

        p.save()
        response_data = {}

        response_data['result'] = 'Solicitud modificada!'
        response_data['postpk'] = id_solicitud

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required()
@csrf_exempt
def verProvision(request, pk):
    if request.method == 'POST':
        html = ''

    else:
        detalles = RolPago.objects.get(id=pk)
        mes = detalles.mes
        anio = detalles.anio
        quincena = detalles.quincena
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        t_otros_ingresos = 0
        if detalles:
            roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')
            id = detalles.id
        for detal in roles:
            i += 1
            html += '<tr>'
            html += '<td>' + str(detal.empleado.cedula_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.empleado.departamento) + '</td>'
            html += '<td>' + str(detal.empleado.tipo_empleado) + '</td>'
            ingresos_total = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # otros_ingresos_total = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            #     empleado_id=detal.empleado_id)
            # for ot in otros_ingresos_total:
            #     if ot.tipo_ingreso_egreso_empleado.parte_ingreso == True:
            #         t_otros_ingresos += ot.valor

            if ingresos_total['valor__sum']:
                total_ingresos = round(float(ingresos_total['valor__sum']), 2)
            else:
                total_ingresos = 0
            total = round(float(total_ingresos), 2)
            html += '<td>' + str(total_ingresos) + '</td>'
            tercero = round(float(total / 12), 2)
            if detal.empleado.tipo_remuneracion_id == 2:
                mes_t=dias_trabajados/30
                total_anios=mes_t*12
                cuarto = round(float(detalles.salario_base / 12), 2)
                cuarto=(cuarto*total_anios)/12
            else:
                cuarto = round(float(detalles.salario_base / 12), 2)
            
            vaca = round(float(total / 24), 2)
            iess = round(float(total * 12.15 / 100), 2)
            if detal.empleado.acumular_decimo_tercero:
                html += '<td>-</td>'
            else:
                html += '<td>' + str(tercero) + '</td>'

            if detal.empleado.acumular_decimo_cuarto:
                html += '<td>-</td>'
            else:
                html += '<td>' + str(cuarto) + '</td>'
            html += '<td>' + str(vaca) + '</td>'
            html += '<td>' + str(iess) + '</td>'

        context = {
            'anio': anio,
            'mes': mes,
            'html': html
        }
        return render_to_response('roles_pago/verProvision.html', context, context_instance=RequestContext(request))

@login_required()
def DiasFeriadosNuevoView(request):
    if request.method == 'POST':
        proforma_form = DiasFeriadosForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            return HttpResponseRedirect('/recursos_humanos/diasFeriados')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = DiasFeriadosForm

    return render_to_response('dias_feriados/nuevo.html', {'form': proforma_form,}, RequestContext(request))

@login_required()
def DiasFeriadosListView(request):
    if request.method == 'POST':

        row = DiasFeriados.objects.all().order_by('id')
        return render_to_response('dias_feriados/index.html', {'row': row}, RequestContext(request))
    else:
        row = DiasFeriados.objects.all().order_by('id')
        return render_to_response('dias_feriados/index.html', {'row': row}, RequestContext(request))

class DiasFeriadosUpdateView(ObjectUpdateView):
    model = DiasFeriados
    form_class = DiasFeriadosForm
    template_name = 'dias_feriados/nuevo.html'
    url_success = 'dias-feriados-list'
    url_cancel = 'dias-feriados-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)

@login_required()
def obtenerIngresos(request):
    if request.method == 'POST':
        mes = request.POST["mes"]
        anio = request.POST["anio"]

        empleado_id = request.POST["empleado_id"]

        fila = request.POST["fila"]

        detalle = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=empleado_id).filter(pagar=True).aggregate(Sum('valor'))
        html = detalle['valor__sum']
        return HttpResponse(
            html
        )

    else:
        mes = request.POST["mes"]

        anio = request.POST["anio"]

        empleado_id = request.POST["empleado_id"]

        fila = request.POST["fila"]

        detalle = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=empleado_id).filter(pagar=True).aggregate(Sum('valor'))
        html = detalle['valor__sum']
        return HttpResponse(
            html
        )

@login_required()
@csrf_exempt
def guardarIngresosView(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta_otros_ingresos"]
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        sueldo = request.POST["sueldo"]
        print('sueldo' + str(sueldo))
        sueldo_quincenal = float(sueldo) / 2
        print('sueldo_quincenal' + str(sueldo_quincenal))
        i = 0
        html = "Guardado con exito"
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_detalle' + str(i) in request.POST:
                    detalle_id = request.POST["id_detalle" + str(i)]
                    detallecompra = IngresosRolEmpleado.objects.get(id=detalle_id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                    detallecompra.valor = request.POST["valor_kits" + str(i)]
                    detallecompra.nombre = request.POST["nombre_kits" + str(i)]
                    detallecompra.deducible = request.POST.get('deducible_kits' + str(i), False)
                    detallecompra.aportaciones = request.POST.get('aportaciones' + str(i), False)
                    detallecompra.anio = request.POST["anio"]
                    detallecompra.mes = request.POST["mes"]
                    #detallecompra.quincena = request.POST["quincena"]
                    detallecompra.empleado_id = request.POST["empleado_otro_ingreso"]
                    detallecompra.updated_at = datetime.now()
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.pagar = True
                    if 'horas_kits' + str(i) in request.POST:
                        hr = request.POST["horas_kits" + str(i)]
                        if len(hr) != 0:
                            detallecompra.horas = request.POST["horas_kits" + str(i)]
                    detallecompra.save()
                    print('guardar1')

                else:
                    if 'tipos_kits' + str(i) in request.POST:
                        comprasdetalle = IngresosRolEmpleado()
                        # comprasdetalle.proforma_id = new_orden.id
                        comprasdetalle.created_by = request.user.get_full_name()
                        comprasdetalle.created_at = datetime.now()
                        comprasdetalle.updated_at = datetime.now()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                        comprasdetalle.valor = request.POST["valor_kits" + str(i)]
                        comprasdetalle.nombre = request.POST["nombre_kits" + str(i)]
                        comprasdetalle.deducible = request.POST.get('deducible_kits' + str(i), False)
                        comprasdetalle.aportaciones = request.POST.get('aportaciones_kits' + str(i), False)
                        comprasdetalle.anio = request.POST["anio"]
                        comprasdetalle.mes = request.POST["mes"]
                        #comprasdetalle.quincena = request.POST["quincena"]
                        comprasdetalle.empleado_id = request.POST["empleado_otro_ingreso"]
                        comprasdetalle.pagar = True
                        if 'horas_kits' + str(i) in request.POST:
                            hr = request.POST["horas_kits" + str(i)]
                            if len(hr) != 0:
                                comprasdetalle.horas = request.POST["horas_kits" + str(i)]
                        comprasdetalle.save()
                        print('guardar2')

                tip_id = request.POST["tipos_kits" + str(i)]
                print(tip_id)

                emp = request.POST["empleado_otro_ingreso"]
                try:
                    tip = TipoIngresoEgresoEmpleado.objects.get(id=tip_id, parte_ingreso=True)
                except TipoIngresoEgresoEmpleado.DoesNotExist:
                    tip = None
                if tip:
                    cursor = connection.cursor();
                    sql="SELECT  distinct sum(oi.valor)from ingresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.parte_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes
                    print('sql' + str(sql))
                    cursor.execute(sql)
                    row = cursor.fetchall()
                    print('ROW'+str(row))
                    if row[0][0]:
                        t_ing_sueldo = row[0][0]

                        print('ENTRO row' + str(row[0][0]))

                    sql2 = "SELECT  distinct oi.id,oi.tipo_ingreso_egreso_empleado_id,oi.valor from otros_ingresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.calcular_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes
                    cursor1 = connection.cursor();
                    cursor1.execute(sql2);
                    row1 = cursor1.fetchall();

                    print('sql2' + str(sql2))
                    print('horas_extras' + str(row[0][0]))
                    print('total ingreso' + str(t_ing_sueldo))
                    if row1:
                        for p in row1:
                            if p[1] == 7:
                                ing1 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                if ing1:
                                    print('tip1')
                                    ing1.updated_by = request.user.get_full_name()
                                    ing1.updated_at = datetime.now()
                                    ing1.valor = round(float((t_ing_sueldo)/12),2)
                                    ing1.save()
                            if p[1] == 8:
                                print('entro')
                                ing2 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                ing2.updated_by = request.user.get_full_name()
                                ing2.updated_at = datetime.now()
                                total_guardar = round(float(t_ing_sueldo) / 24,2)
                                ing2.valor = total_guardar
                                ing2.save()
                                print('tardar' + str(ing2.valor))
                                print('total guardar' + str(total_guardar))
                            if p[1] == 27:
                                ing3 = OtrosIngresosRolEmpleado.objects.get(id=p[0],
                                                                                tipo_ingreso_egreso_empleado_id=p[1])
                                if ing3:
                                    ing3.updated_by = request.user.get_full_name()
                                    ing3.updated_at = datetime.now()
                                    ing3.valor = float((t_ing_sueldo / 10.58) / 2)
                                    ing3.save()

                    sql3="SELECT  distinct oi.id,oi.tipo_ingreso_egreso_empleado_id,oi.valor from egresos_rol_empleado oi, tipo_ingreso_egreso_empleado t where oi.tipo_ingreso_egreso_empleado_id=t.id and t.calcular_ingreso=true and oi.empleado_id=" + emp + " and anio='" + anio + "' and mes=" + mes
                    print('sql3' + str(sql3))
                    cursor2 = connection.cursor()
                    cursor2.execute(sql3)
                    row2 = cursor2.fetchall()
                    if row2:
                        print('entroEgreso00000')
                        for p2 in row2:
                            eg = EgresosRolEmpleado.objects.get(id=p2[0])
                            print('entroEgreso1:' + str(p2[0]))
                            if eg:
                                print('entroEgreso2:' + str(eg.id))
                                if p2[1] == 29:
                                    print('entroEgreso3' + str(t_ing_sueldo))
                                    eg.updated_by = request.user.get_full_name()
                                    eg.updated_at = datetime.now()
                                    eg.valor = round(float((t_ing_sueldo) * 0.0945),2)
                                    eg.save()
                                if p2[1] == 30:
                                    eg.updated_by = request.user.get_full_name()
                                    eg.updated_at = datetime.now()
                                    eg.valor = round(float(((t_ing_sueldo) * 0.0341) / 2),2)
                                    eg.save()

        return HttpResponse(
            html
        )
    else:
        raise Http404

@login_required()
@csrf_exempt
def guardarEgresosView(request):
    if request.method == 'POST':
        contador = request.POST["columnas_receta_otros_egresos"]
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        #quincena = request.POST["quincena"]
        tipo_contrato_persona = request.POST["tipo_contrato_persona"]
        i = 0
        html = "Guardado con exito"
        while int(i) <= int(contador):
            i += 1
            if int(i) > int(contador):
                print('entrosd')
                break
            else:
                if 'id_detalle' + str(i) in request.POST:
                    detalle_id = request.POST["id_detalle" + str(i)]
                    detallecompra = EgresosRolEmpleado.objects.get(id=detalle_id)
                    detallecompra.updated_by = request.user.get_full_name()
                    detallecompra.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                    detallecompra.valor = request.POST["valor_kits_egresos" + str(i)]
                    detallecompra.nombre = request.POST["nombre_kits" + str(i)]
                    detallecompra.memo = request.POST.get('memo_kits' + str(i), False)
                    detallecompra.anio = request.POST["anio"]
                    detallecompra.mes = request.POST["mes"]
                    #detallecompra.quincena = request.POST["quincena"]
                    detallecompra.empleado_id = request.POST["empleado_otro_egreso"]
                    detallecompra.save()
                else:
                    if 'tipos_kits' + str(i) in request.POST:
                        comprasdetalle = EgresosRolEmpleado()
                        # comprasdetalle.proforma_id = new_orden.id
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = request.POST["tipos_kits" + str(i)]
                        comprasdetalle.valor = request.POST["valor_kits_egresos" + str(i)]
                        comprasdetalle.nombre = request.POST["nombre_kits" + str(i)]
                        comprasdetalle.memo = request.POST.get('memo_kits' + str(i), False)
                        comprasdetalle.anio = request.POST["anio"]
                        comprasdetalle.mes = request.POST["mes"]
                        #comprasdetalle.quincena = request.POST["quincena"]
                        comprasdetalle.empleado_id = request.POST["empleado_otro_egreso"]
                        comprasdetalle.save()
        return HttpResponse(
            html
        )
    else:
        raise Http404


@login_required()
def eliminarDetalleIngresoView(request):
    pk = request.POST["id"]
    objetos = IngresosRolEmpleado.objects.get(id=pk)

    objetos.delete()
    return HttpResponse(

    )


@login_required()
def eliminarDetalleEgresoView(request):
    pk = request.POST["id"]
    objetos = EgresosRolEmpleado.objects.get(id=pk)

    objetos.delete()
    return HttpResponse(

    )

@login_required()
@csrf_exempt
def verRolGlobalQuincenal(request, pk):
    if request.method == 'POST':
        html = ''

    else:
        detalles = RolPago.objects.get(id=pk)
        mes = detalles.mes
        anio = detalles.anio
        quincena = detalles.quincena
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        if detalles:
            roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')
            id = detalles.id
        for detal in roles:
            i += 1
            try:
                sueldo = IngresosRolEmpleado.objects.get(quincena=quincena, anio=anio, mes=mes,
                                                         empleado_id=detal.empleado_id,
                                                         tipo_ingreso_egreso_empleado_id=24)
            except IngresosRolEmpleado.DoesNotExist:
                sueldo = 0
            html += '<tr>'
            html += '<td>' + str(detal.empleado.cedula_empleado) + '</td>'
            html += '<td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.empleado.departamento) + '</td>'
            html += '<td>' + str(detal.empleado.tipo_empleado) + '</td>'
            if sueldo:
                html += '<td>' + str(sueldo.valor_mensual) + '</td>'

            else:
                html += '<td>0</td>'

            ingresos_total = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if ingresos_total['valor__sum']:
                t_ingresoT = ingresos_total['valor__sum']
            else:
                t_ingresoT = 0

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                total_desc = float(faltas_injustificadas_valor['valor__sum'])
            else:
                total_desc = 0

            # total_ingresos = float(t_ingresoT - (total_desc))
            total_ingresos = float(t_ingresoT)
            dias_trabajados = 0
            dias = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('dias'))
            if dias['dias__sum']:
                total_dias = float(dias['dias__sum'])
                dias_trabajados = 15 -float(total_dias / 8)
            else:
                dias_trabajados = 15

            html += '<td>' + str(dias_trabajados) + '</td>'
            if sueldo:
                html += '<td>' + str(sueldo.valor) + '</td>'
            else:
                html += '<td>0</td>'

            otros_ingresos_total = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

            otros_ingresos_horas_feriados = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('valor'))

            cantidad_horas_feriados = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('horas'))

            otros_ingresos_horas_normal = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('valor'))

            cantidad_horas_normal = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('horas'))

            otros_ingresos_horas_fines = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('valor'))

            cantidad_horas_fines = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('horas'))

            otros_ingresos_comisiones = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=4).aggregate(Sum('valor'))

            otros_ingresos_bonificaciones = IngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=3).aggregate(Sum('valor'))

            otros_ingresos_movilizacion = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=31).aggregate(Sum('valor'))

            otros_ingresos_freserva = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7).aggregate(Sum('valor'))
            otros_ingresos_alimentacion = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=1).aggregate(Sum('valor'))
            otros_ingresos_dtercero = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))
            otros_ingresos_dcuarto = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(quincena=quincena).filter(
                tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))
            otros_ingresos_iasumido = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=27).aggregate(Sum('valor'))
            otros_ingresos_irenta = OtrosIngresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            if cantidad_horas_feriados['horas__sum']:
                html += '<td>' + str(cantidad_horas_feriados['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_feriados['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_feriados['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if cantidad_horas_normal['horas__sum']:
                html += '<td>' + str(cantidad_horas_normal['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_normal['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_normal['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if cantidad_horas_fines['horas__sum']:
                html += '<td>' + str(cantidad_horas_fines['horas__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_fines['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_fines['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_comisiones['valor__sum']:
                html += '<td>' + str(otros_ingresos_comisiones['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_bonificaciones['valor__sum']:
                html += '<td>' + str(otros_ingresos_bonificaciones['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_alimentacion['valor__sum']:
                html += '<td>' + str(otros_ingresos_alimentacion['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_movilizacion['valor__sum']:
                html += '<td>' + str(otros_ingresos_movilizacion['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_freserva['valor__sum']:
                html += '<td>' + str(otros_ingresos_freserva['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_dtercero['valor__sum']:
                html += '<td>' + str(otros_ingresos_dtercero['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_ingresos_dcuarto['valor__sum']:
                html += '<td>' + str(otros_ingresos_dcuarto['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_ingresos_iasumido['valor__sum']:
                html += '<td>' + str(otros_ingresos_iasumido['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_irenta['valor__sum']:
                html += '<td>' + str(otros_ingresos_irenta['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_total['valor__sum']:
                suma_ingresos_otros_ingresos = total_ingresos + float(
                    otros_ingresos_total['valor__sum'])
            else:
                suma_ingresos_otros_ingresos = total_ingresos

            html += '<td>' + str(suma_ingresos_otros_ingresos) + '</td>'

            egresos_total = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_total = OtrosEgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_nueve = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))
            otros_egresos_tres = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=30).aggregate(Sum('valor'))

            otros_egresos_atraso = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_descir = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=20).aggregate(Sum('valor'))
            otros_egresos_falta = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_multa = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=21).aggregate(Sum('valor'))

            otros_egresos_hipotecario = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=13).aggregate(Sum('valor'))

            otros_egresos_permiso = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_quirografario = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

            otros_egresos_anticipo = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))

            otros_egresos_movistar = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

            otros_egresos_ptmo = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

            otros_egresos_contribucion = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=32).aggregate(Sum('valor'))

            otros_egresos_otros = EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                faltas = float(faltas_injustificadas_valor['valor__sum'])
            else:
                faltas = 0

            if otros_egresos_nueve['valor__sum']:
                html += '<td>' + str(otros_egresos_nueve['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_egresos_tres['valor__sum']:
                html += '<td>' + str(otros_egresos_tres['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            atrasos = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).exclude(tipo_ausencia_id=2).exclude(tipo_ausencia_id=3).exclude(
                tipo_ausencia_id=1).aggregate(Sum('valor'))
            if atrasos['valor__sum']:
                atras = float(atrasos['valor__sum'])
            else:
                atras = 0

            html += '<td>' + str(atras) + '</td>'

            # if otros_egresos_atraso['valor__sum']:
            #     html += '<td>' + str(otros_egresos_atraso['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'


            html += '<td>' + str(faltas) + '</td>'

            faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena).filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
            if faltas_justificadas_valor['valor__sum']:
                permisos = float(faltas_justificadas_valor['valor__sum'])
            else:
                permisos = 0

            html += '<td>' + str(permisos) + '</td>'

            if otros_egresos_anticipo['valor__sum']:
                html += '<td>' + str(otros_egresos_anticipo['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_ptmo['valor__sum']:
                html += '<td>' + str(otros_egresos_ptmo['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_movistar['valor__sum']:
                html += '<td>' + str(otros_egresos_movistar['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_quirografario['valor__sum']:
                html += '<td>' + str(otros_egresos_quirografario['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_hipotecario['valor__sum']:
                html += '<td>' + str(otros_egresos_hipotecario['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_descir['valor__sum']:
                html += '<td>' + str(otros_egresos_descir['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_contribucion['valor__sum']:
                html += '<td>' + str(otros_egresos_contribucion['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_otros['valor__sum']:
                html += '<td>' + str(otros_egresos_otros['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            # if otros_egresos_falta['valor__sum']:
            #     html += '<td>' + str(otros_egresos_falta['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'
            if otros_egresos_multa['valor__sum']:
                html += '<td>' + str(otros_egresos_multa['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            # html+='<td>'+str(total_desc)+'</td>'







            # if otros_egresos_permiso['valor__sum']:
            #     html += '<td>' + str(otros_egresos_permiso['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'









            if egresos_total['valor__sum']:
                egres_t = egresos_total['valor__sum']
            else:
                egres_t = 0

            if otros_egresos_total['valor__sum']:

                # html += '<td>' + str(otros_egresos_total['valor__sum']) + '</td>'
                otros_egre_t = otros_egresos_total['valor__sum']
            else:
                # html += '<td>0</td>'
                otros_egre_t = 0

            suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos + total_desc
            html += '<td>' + str(suma_egresos_otros_egresos) + '</td>'
            # html+='<td>'+str(detal.otros_egresos)+'</td>'
            if suma_ingresos_otros_ingresos:
                suma_ingresos_otros_ingresos = suma_ingresos_otros_ingresos

            else:
                suma_ingresos_otros_ingresos = 0

            total_recibir_mensual = suma_ingresos_otros_ingresos - suma_egresos_otros_egresos
            html += '<td>' + str(detal.total) + '</td>'

            #html += '<td>' + str(total_recibir_mensual) + '</td>'

        context = {
            'html': html,
            'anio': anio,
            'mes': mes,
            'id': pk,
            'quincena': quincena,
        }
        return render_to_response('roles_pago/verRolGlobalQuincenal.html', context,
                                  context_instance=RequestContext(request))

@login_required()
def AnalisisPrestamosListView(request):
    if request.method == 'POST':
        analisis = AnalisisPrestamo.objects.order_by('id')

        return render_to_response('prestamo/analisis_index.html', {'analisis': analisis}, RequestContext(request))


    else:
        analisis = AnalisisPrestamo.objects.order_by('id')
        return render_to_response('prestamo/analisis_index.html', {'analisis': analisis}, RequestContext(request))

@login_required()
def AnalisisPrestamoCreateView(request):
    if request.method == 'POST':
        form = AnalisisPrestamoForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.monto_neto_promedio = request.POST.get('neto_promedio')
            new_orden.monto_promedio_fin_mes = request.POST.get('neto_promedio_30')
            new_orden.monto_disponible_descuento = request.POST.get('neto_promedio_70')
            new_orden.save()

            analisis_prestamo_des1 = AnalisisPrestamoDescuentos()
            analisis_prestamo_des1.anio = 2016
            analisis_prestamo_des1.mes = 1
            analisis_prestamo_des1.analisis_prestamo_id = new_orden.id
            analisis_prestamo_des1.iess1 = request.POST.get('iess_1')
            analisis_prestamo_des1.iess2 = request.POST.get('iess_2')
            analisis_prestamo_des1.iess3 = request.POST.get('iess_3')
            analisis_prestamo_des1.salud1 = request.POST.get('seguro_1')
            analisis_prestamo_des1.salud2 = request.POST.get('seguro_2')
            analisis_prestamo_des1.salud3 = request.POST.get('seguro_3')
            analisis_prestamo_des1.telefonia1 = request.POST.get('celular_1')
            analisis_prestamo_des1.telefonia2 = request.POST.get('celular_2')
            analisis_prestamo_des1.telefonia3 = request.POST.get('celular_3')
            analisis_prestamo_des1.ptmo1 = request.POST.get('prestamo_1')
            analisis_prestamo_des1.ptmo2 = request.POST.get('prestamo_2')
            analisis_prestamo_des1.ptmo3 = request.POST.get('prestamo_3')
            analisis_prestamo_des1.donaciones1 = request.POST.get('donaciones_1')
            analisis_prestamo_des1.donaciones2 = request.POST.get('donaciones_2')
            analisis_prestamo_des1.donaciones3 = request.POST.get('donaciones_3')
            analisis_prestamo_des1.otros1 = request.POST.get('otros_1')
            analisis_prestamo_des1.otros2 = request.POST.get('otros_2')
            analisis_prestamo_des1.otros3 = request.POST.get('otros_3')
            analisis_prestamo_des1.quirografario1 = request.POST.get('quirografario_1')
            analisis_prestamo_des1.quirografario2 = request.POST.get('quirografario_2')
            analisis_prestamo_des1.quirografario3 = request.POST.get('quirografario_3')
            analisis_prestamo_des1.total_descuento1 = request.POST.get('descuento_1')
            analisis_prestamo_des1.total_descuento2 = request.POST.get('descuento_2')
            analisis_prestamo_des1.total_descuento3 = request.POST.get('descuento_3')
            analisis_prestamo_des1.total_ingresos1 = request.POST.get('ingreso_1')
            analisis_prestamo_des1.total_ingresos2 = request.POST.get('ingreso_2')
            analisis_prestamo_des1.total_ingresos3 = request.POST.get('ingreso_3')
            analisis_prestamo_des1.anticipo1 = request.POST.get('anticipo_1')
            analisis_prestamo_des1.anticipo2 = request.POST.get('anticipo_2')
            analisis_prestamo_des1.anticipo3 = request.POST.get('anticipo_3')
            analisis_prestamo_des1.sueldo_mensual1 = request.POST.get('sueldo_1')
            analisis_prestamo_des1.sueldo_mensual2 = request.POST.get('sueldo_2')
            analisis_prestamo_des1.sueldo_mensual3 = request.POST.get('sueldo_3')
            analisis_prestamo_des1.neto_recibir1 = request.POST.get('neto_recibir_1')
            analisis_prestamo_des1.neto_recibir2 = request.POST.get('neto_recibir_2')
            analisis_prestamo_des1.neto_recibir3 = request.POST.get('neto_recibir_3')

            analisis_prestamo_des1.tipo_ingreso_egreso_empleado_id = 29
            analisis_prestamo_des1.save()

            try:
                secuencial = Secuenciales.objects.get(modulo='analisis_prestamo')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/recursos_humanos/analisisprestamo')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = AnalisisPrestamoForm

    return render_to_response('prestamo/analisis_prestamo_nuevo.html', {'form': form}, RequestContext(request))

@login_required()
def AnalisisPrestamoImprimir(request, pk):
    if request.method == 'POST':
        return HttpResponseRedirect('/recursos_humanos/analisisprestamo')

    else:
        form = AnalisisPrestamo.objects.get(id=pk)
        detalle = AnalisisPrestamoDescuentos.objects.get(analisis_prestamo_id=pk)
        html = ''
        html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="4" >'
        html += 'MUEBLES Y DIVERSIDADES<br />INFORMACION ECONOMICA <br />ANALISIS DE DESCUENTO</td><td>No de Solicitud</td><td>' + str(
            form.codigo) + '</td></tr>'

        html += '<tr><td colspan="8">DATOS PERSONALES</td></tr>'
        html += '<tr><td colspan="2">Fecha de solicitud:</td><td colspan="3">' + str(
            form.fecha) + '</td><td colspan="2">Sueldo Fijo:</td><td colspan="2">' + str(
            form.sueldo_fijo) + '</td></tr>'
        html += '<tr><td colspan="2">Nombre del colaborador:</td><td colspan="3">' + str(
            form.empleado.nombre_empleado) + '</td><td colspan="2">Fecha de Ingreso:</td><td colspan="2">' + str(
            form.empleado.fecha_ini_reconocida) + '</td></tr>'
        html += '<tr><td colspan="2">Cargo/Area:</td><td colspan="3">' + str(
            form.tipoempleado) + '</td><td colspan="2">Tiempo en la empresa</td><td colspan="2"></td></tr>'
        html += '<tr><td colspan="8">MOTIVO DEL ANTICIPO</td></tr>'
        html += '<tr><td colspan="8">' + str(form.motivo_anticipo) + '</td></tr>'
        html += '<tr><td colspan="2">' + str(form.monto_solicitado) + '</td><td colspan="2">' + str(
            form.plazo_solicitar) + '</td><td colspan="4"></td></tr>'

        html += '<tr><td colspan="2">Monto a Solicitar</td><td colspan="2">Plazo a Solicitar</td><td colspan="4"></td></tr>'

        html += '<tr><td colspan="8">INFORMACION ECONOMICA/ANALISIS DE DESCUENTO</td></tr></table>'
        html += '<table><tr><td><h5>Guia descuentos de 3 ultimos mes</h5>'
        html += '<table border="1"><thead><tr><td></td><td>MES 1</td><td>MES 2</td><td>MES 3</td></tr></thead><tbody>'
        html += '<tr><td>IESS</td><td>' + str(detalle.iess1) + '</td><td>' + str(detalle.iess2) + '</td><td>' + str(
            detalle.iess3) + '</td></tr>'
        html += '<tr><td>Seguro Salud</td><td>' + str(detalle.salud1) + '</td><td>' + str(
            detalle.salud2) + '</td><td>' + str(detalle.salud3) + '</td></tr>'
        html += '<tr><td>Ptmo Empresa</td><td>' + str(detalle.ptmo1) + '</td><td>' + str(
            detalle.ptmo2) + '</td><td>' + str(detalle.ptmo3) + '</td></tr>'
        html += '<tr><td>Donaciones</td><td>' + str(detalle.donaciones1) + '</td><td>' + str(
            detalle.donaciones2) + '</td><td>' + str(detalle.donaciones3) + '</td></tr>'
        html += '<tr><td>Telefonia</td><td>' + str(detalle.telefonia1) + '</td><td>' + str(
            detalle.telefonia2) + '</td><td>' + str(detalle.telefonia3) + '</td></tr>'
        html += '<tr><td>Quirografario</td><td>' + str(detalle.quirografario1) + '</td><td>' + str(
            detalle.quirografario2) + '</td><td>' + str(detalle.quirografario3) + '</td></tr>'
        html += '<tr><td>Total Descuentos</td><td>' + str(detalle.total_descuento1) + '</td><td>' + str(
            detalle.total_descuento2) + '</td><td>' + str(detalle.total_descuento3) + '</td></tr>'

        html += '</tbody></table>'
        html += '</td><td>'

        html += '<h5>Tabla de promedio de 3 &uacute;ltimos meses disponibles</h5>'
        html += '<table border="1"><thead><tr><td></td><td>MES 1</td><td>MES 2</td><td>MES 3</td></tr></thead><tbody>'
        html += '<tr><td>Total Ingresos sueldo</td><td>' + str(detalle.total_ingresos1) + '</td><td>' + str(
            detalle.total_ingresos2) + '</td><td>' + str(detalle.total_ingresos3) + '</td></tr>'
        html += '<tr><td>Anticipo sueldo</td><td>' + str(detalle.anticipo1) + '</td><td>' + str(
            detalle.anticipo2) + '</td><td>' + str(detalle.anticipo3) + '</td></tr>'
        html += '<tr><td>Sueldo fin de mes</td><td>' + str(detalle.sueldo_mensual1) + '</td><td>' + str(
            detalle.sueldo_mensual2) + '</td><td>' + str(detalle.sueldo_mensual3) + '</td></tr>'
        html += '<tr><td>Total Descuentos</td><td>' + str(detalle.total_descuento1) + '</td><td>' + str(
            detalle.total_descuento2) + '</td><td>' + str(detalle.total_descuento3) + '</td></tr>'
        html += '<tr><td><b>Neto a Recibir</b></td><td>' + str(detalle.neto_recibir1) + '</td><td>' + str(
            detalle.neto_recibir2) + '</td><td>' + str(detalle.neto_recibir3) + '</td></tr>'
        html += '<tr><td colspan="3"><b>Monto Neto Promedio</b></td><td>' + str(form.monto_neto_promedio) + '</td></tr>'
        html += '<tr><td colspan="3"><b>Monto  Promedio a recibir el fin de mes(30 %)</b></td><td>' + str(
            form.monto_promedio_fin_mes) + '</td></tr>'
        html += '<tr><td colspan="3"><b>Monto disponible para Descuento (70 %)</b></td><td>' + str(
            form.monto_disponible_descuento) + '</td></tr>'
        html += '</tbody></table>'
        html += '</td></tr></table>'

    html1 = render_to_string('prestamo/analisis_prestam_imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)


# =====================================================#
@login_required()
def AnalisisPrestamoUpdateView(request, pk):
    if request.method == 'POST':
        prestamo = Prestamo.objects.get(id=pk)
        form = PrestamoForm(request.POST, request.FILES, instance=prestamo)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            new_orden = form.save()
            new_orden.save()
            context = {
                'section_title': 'Actualizar Orden Egreso',
                'button_text': 'Actualizar',
                'form': form}
            return render_to_response(
                'prestamo/actualizar.html',
                context,
                context_instance=RequestContext(request))
        else:
            form = PrestamoForm(request.POST)
            context = {
                'section_title': 'Actualizar',
                'button_text': 'Actualizar',
                'form': form}

            return render_to_response(
                'prestamo/actualizar.html',
                context,
                context_instance=RequestContext(request))
    else:
        prestamo = Prestamo.objects.get(id=pk)
        form = PrestamoForm(instance=prestamo)
        context = {
            'section_title': 'Actualizar',
            'button_text': 'Actualizar',
            'form': form}

        return render_to_response(
            'prestamo/actualizar.html',
            context,
            context_instance=RequestContext(request))

@login_required()
@csrf_exempt
def obtenerEmpleadoAnalisis(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        fecha = request.POST.get('fecha')
        formato_fecha = "%Y-%m-%d"

        fecha_inicial = datetime.strptime(fecha, formato_fecha)
        mes = fecha_inicial.month
        anio = fecha_inicial.year
        if mes == 1:
            mes_1 = 12
            anio_1 = anio - 1
            anio_2 = anio - 1
            anio_3 = anio - 1
            mes_2 = 11
            mes_3 = 10
        if mes == 2:
            mes_1 = 1
            anio_1 = anio
            mes_2 = 12
            anio_2 = anio - 1
            mes_3 = 11
            anio_3 = anio - 1
        if mes == 3:
            mes_1 = 2
            anio_1 = anio
            mes_2 = 1
            anio_2 = anio
            mes_3 = 12
            anio_3 = anio - 1

        if mes != 1 and mes != 2 and mes != 3:
            mes_1 = mes - 1
            mes_2 = mes - 2
            mes_3 = mes - 3
            anio_1 = anio
            anio_2 = anio
            anio_3 = anio

        detal = Empleado.objects.get(empleado_id=id)

        iess1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))

        quirografario1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

        salud1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=16).aggregate(Sum('valor'))
        movistar1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

        ptmo1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

        otros_egresos1 = OtrosEgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

        anticipo1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))
        donaciones1 = EgresosRolEmpleado.objects.filter(anio=anio_1).filter(mes=mes_1).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=31).aggregate(Sum('valor'))

        if iess1['valor__sum']:
            iess1_valor = iess1['valor__sum']
        else:
            iess1_valor = 0

        if quirografario1['valor__sum']:
            quirografario1_valor = quirografario1['valor__sum']
        else:
            quirografario1_valor = 0

        if salud1['valor__sum']:
            salud1_valor = salud1['valor__sum']
        else:
            salud1_valor = 0

        if movistar1['valor__sum']:
            movistar1_valor = movistar1['valor__sum']
        else:
            movistar1_valor = 0

        if ptmo1['valor__sum']:
            ptmo1_valor = ptmo1['valor__sum']
        else:
            ptmo1_valor = 0

        if otros_egresos1['valor__sum']:
            otros_egresos1_valor = otros_egresos1['valor__sum']
        else:
            otros_egresos1_valor = 0

        if anticipo1['valor__sum']:
            anticipo1_valor = anticipo1['valor__sum']
        else:
            anticipo1_valor = 0

        if donaciones1['valor__sum']:
            donaciones1_valor = donaciones1['valor__sum']
        else:
            donaciones1_valor = 0
        total_descuento1 = iess1_valor + quirografario1_valor + salud1_valor + movistar1_valor + ptmo1_valor + otros_egresos1_valor + donaciones1_valor

        # 2Anio
        iess2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))

        quirografario2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

        salud2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=16).aggregate(Sum('valor'))
        movistar2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

        ptmo2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

        otros_egresos2 = OtrosEgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

        anticipo2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))
        donaciones2 = EgresosRolEmpleado.objects.filter(anio=anio_2).filter(mes=mes_2).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=31).aggregate(Sum('valor'))

        if iess2['valor__sum']:
            iess2_valor = iess2['valor__sum']
        else:
            iess2_valor = 0

        if quirografario2['valor__sum']:
            quirografario2_valor = quirografario2['valor__sum']
        else:
            quirografario2_valor = 0

        if salud2['valor__sum']:
            salud2_valor = salud2['valor__sum']
        else:
            salud2_valor = 0

        if movistar2['valor__sum']:
            movistar2_valor = movistar2['valor__sum']
        else:
            movistar2_valor = 0

        if ptmo2['valor__sum']:
            ptmo2_valor = ptmo2['valor__sum']
        else:
            ptmo2_valor = 0

        if otros_egresos2['valor__sum']:
            otros_egresos2_valor = otros_egresos2['valor__sum']
        else:
            otros_egresos2_valor = 0

        if anticipo2['valor__sum']:
            anticipo2_valor = anticipo2['valor__sum']
        else:
            anticipo2_valor = 0

        if donaciones2['valor__sum']:
            donaciones2_valor = donaciones2['valor__sum']
        else:
            donaciones2_valor = 0
        total_descuento2 = iess2_valor + quirografario2_valor + salud2_valor + movistar2_valor + ptmo2_valor + otros_egresos2_valor + donaciones2_valor

        # 3Anio
        iess3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))

        quirografario3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

        salud3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=16).aggregate(Sum('valor'))
        movistar3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

        ptmo3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

        otros_egresos3 = OtrosEgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

        anticipo3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))
        donaciones3 = EgresosRolEmpleado.objects.filter(anio=anio_3).filter(mes=mes_3).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=31).aggregate(Sum('valor'))

        if iess3['valor__sum']:
            iess3_valor = iess3['valor__sum']
        else:
            iess3_valor = 0

        if quirografario3['valor__sum']:
            quirografario3_valor = quirografario3['valor__sum']
        else:
            quirografario3_valor = 0

        if salud3['valor__sum']:
            salud3_valor = salud3['valor__sum']
        else:
            salud3_valor = 0

        if movistar3['valor__sum']:
            movistar3_valor = movistar3['valor__sum']
        else:
            movistar3_valor = 0

        if ptmo3['valor__sum']:
            ptmo3_valor = ptmo3['valor__sum']
        else:
            ptmo3_valor = 0

        if otros_egresos3['valor__sum']:
            otros_egresos3_valor = otros_egresos3['valor__sum']
        else:
            otros_egresos3_valor = 0

        if anticipo3['valor__sum']:
            anticipo3_valor = anticipo3['valor__sum']
        else:
            anticipo3_valor = 0

        if donaciones3['valor__sum']:
            donaciones3_valor = donaciones3['valor__sum']
        else:
            donaciones3_valor = 0
        total_descuento3 = iess3_valor + quirografario3_valor + salud3_valor + movistar3_valor + ptmo3_valor + otros_egresos3_valor + donaciones3_valor
        sueldo1 = IngresosRolEmpleado.objects.filter(anio=anio_1, mes=mes_1, empleado_id=detal.empleado_id,
                                                     tipo_ingreso_egreso_empleado_id=24).aggregate(Sum('valor'))

        if sueldo1['valor__sum']:
            sueldo1_valor = sueldo1['valor__sum']
        else:
            sueldo1_valor = 0

        sueldo2 = IngresosRolEmpleado.objects.filter(anio=anio_2, mes=mes_2, empleado_id=detal.empleado_id,
                                                     tipo_ingreso_egreso_empleado_id=24).aggregate(Sum('valor'))

        if sueldo2['valor__sum']:
            sueldo2_valor = sueldo2['valor__sum']
        else:
            sueldo2_valor = 0

        sueldo3 = IngresosRolEmpleado.objects.filter(anio=anio_3, mes=mes_3, empleado_id=detal.empleado_id,
                                                     tipo_ingreso_egreso_empleado_id=24).aggregate(Sum('valor'))

        if sueldo3['valor__sum']:
            sueldo3_valor = sueldo3['valor__sum']
        else:
            sueldo3_valor = 0

        sueldo1_mensual = sueldo1_valor - anticipo1_valor
        sueldo2_mensual = sueldo2_valor - anticipo2_valor
        sueldo3_mensual = sueldo3_valor - anticipo3_valor

        neto_recibir1 = sueldo1_mensual - total_descuento1
        neto_recibir2 = sueldo2_mensual - total_descuento2
        neto_recibir3 = sueldo3_mensual - total_descuento3

        neto_promedio = (neto_recibir1 + neto_recibir2 + neto_recibir3) / 3
        neto_promedio_treinta = neto_promedio * 0.3
        neto_promedio_setenta = neto_promedio * 0.7

        item = {
            'quirografario1': quirografario1_valor,
            'iess1': iess1_valor,
            'salud1': salud1_valor,
            'telefonia1': movistar1_valor,
            'prestamo1': ptmo1_valor,
            'donaciones1': donaciones1_valor,
            'otros1': otros_egresos1_valor,
            'total_descuento1': total_descuento1,
            'anticipo1': anticipo1_valor,
            'ingreso1': sueldo1_valor,
            'sueldo_mensual1': sueldo1_mensual,
            'neto_recibir1': neto_recibir1,
            'quirografario2': quirografario2_valor,
            'iess2': iess2_valor,
            'salud2': salud2_valor,
            'telefonia2': movistar2_valor,
            'prestamo2': ptmo2_valor,
            'donaciones2': donaciones2_valor,
            'otros2': otros_egresos2_valor,
            'total_descuento2': total_descuento2,
            'anticipo2': anticipo2_valor,
            'ingreso2': sueldo2_valor,
            'sueldo_mensual2': sueldo2_mensual,
            'neto_recibir2': neto_recibir2,
            'quirografario3': quirografario3_valor,
            'iess3': iess3_valor,
            'salud3': salud3_valor,
            'telefonia3': movistar3_valor,
            'prestamo3': ptmo3_valor,
            'donaciones3': donaciones3_valor,
            'otros3': otros_egresos3_valor,
            'total_descuento3': total_descuento3,
            'anticipo3': anticipo3_valor,
            'ingreso3': sueldo3_valor,
            'sueldo_mensual3': sueldo3_mensual,
            'neto_recibir3': neto_recibir3,
            'neto_promedio': neto_promedio,
            'neto_promedio_treinta': neto_promedio_treinta,
            'neto_promedio_setenta': neto_promedio_setenta,
            'cargo': detal.tipo_empleado_id,
            'departamento': detal.departamento_id,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')


@login_required()
def SolicitudPrestamoImprimir(request, pk):
    if request.method == 'POST':
        return HttpResponseRedirect('/recursos_humanos/prestamo')

    else:
        form = Prestamo.objects.get(id=pk)

        html = ''
        html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="4" >'
        html += 'MUEBLES Y DIVERSIDADES<br />INFORMACION ECONOMICA <br />ANALISIS DE DESCUENTO</td><td>No de Solicitud</td><td>' + str(
            form.codigo) + '</td></tr>'
        html += '</table>'
        html += '<br> Se&ntilde;ora:'
        html += '<br> MIREYA LUCRECIA DALMAU YEPEZ'
        html += '<br> Gerente General <br>MUEBLES Y DIVERSIDADES MUEDIRSA S.A.'
        html += '<br> De mis consideraciones:'
        html += '<p >Por medio de la presente solicito a usted, que se me conceda un prestamo, por el valor de $' + str(
            form.total) + ' valores que pido y autorizo que me sean descontados de mis sueldos mensuales, y de los beneficios sociales, que me correspondan en cada, periodo, de la siguiente forma:'

        html += '<table border="1"><thead><tr><td>FECHA</td><td>ABONO CAPITAL</td><td>CUOTA</td><td>SALDO CAP</td><td>DESCUENTO</td></tr></thead><tbody>'
        saldo_deuda_anterior=0
        if form.saldo_deuda_anterior:
            saldo_deuda_anterior=form.saldo_deuda_anterior
        html += '<tr><td colspan="2">SALDO DEUDA ANTERIOR</td><td>' + str(
            saldo_deuda_anterior) + '</td><td></td><td></td></tr>'
        total_pagar=0
        total1=0
        if form.total:
            total1=form.total
        if form.total_pagar:
            total_pagar=form.total_pagar
        html += '<tr><td colspan="2"></td><td>' + str(total1) + '</td><td>' + str(
            total_pagar) + '</td><td></td></tr>'
        detalle = PrestamoDetalle.objects.filter(prestamo_id=pk)
        if detalle:
            for d in detalle:
                html += '<tr>'
                html += '<td>' + str(d.fecha) + '</td>'
                html += '<td>' + str(d.abono) + '</td>'
                html += '<td>' + str(d.cuota) + '</td>'
                html += '<td>' + str(d.saldo) + '</td>'
                html += '<td>' + str(d.descuento) + '</td>'
                html += '</tr>'

        html += '</tbody></table>'
        html += '<br> Agradeciendo de antemano, quedo de usted.'
        html += '<br>Observacion:'
        html += '<br>' + str(form.concepto) + ''
        html += '<br>Atentamente<br><br>'
        html += '<br>-----------'
        html += '<br>' + str(form.empleado.nombre_empleado) + ''
        html += '<br>C.I#' + str(form.empleado.cedula_empleado) + ''
        html += '<br><br><table><tr><td>-----------------<br>Elaborado por</td><td>-----------------<br>Visto Bueno</td><td>-----------------<br>Aprobado por</td></tr></table>'

    html1 = render_to_string('prestamo/prestamo_imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

@login_required()
def TipoIngresoEgresoListView(request):
    if request.method == 'POST':

        tipos = TipoIngresoEgresoEmpleado.objects.all().order_by('nombre')
        return render_to_response('tipo_ingreso_egreso/index.html', {'tipos': tipos}, RequestContext(request))
    else:
        tipos = TipoIngresoEgresoEmpleado.objects.all().order_by('nombre')
        return render_to_response('tipo_ingreso_egreso/index.html', {'tipos': tipos}, RequestContext(request))


# =====================================================#
@login_required()
def TipoIngresoEgresoCreateView(request):
    if request.method == 'POST':
        form = TipoIngresoEgresoForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='tipo_ingreso_egreso')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/recursos_humanos/tipo_ingreso_egreso')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = TipoIngresoEgresoForm
        return render_to_response('tipo_ingreso_egreso/create.html', {'form': form}, RequestContext(request))


# =====================================================#
@login_required()
def TipoIngresoEgresoUpdateView(request, pk):
    if request.method == 'POST':
        tipos = TipoIngresoEgresoEmpleado.objects.get(id=pk)
        form = TipoIngresoEgresoForm(request.POST, request.FILES, instance=tipos)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            new_orden = form.save()
            new_orden.save()
            context = {
                'section_title': 'Actualizar Tipo Ingreso ',
                'button_text': 'Actualizar',
                'form': form}
            return render_to_response(
                'tipo_ingreso_egreso/create.html',
                context,
                context_instance=RequestContext(request))
        else:
            form = TipoIngresoEgresoForm(request.POST)
            context = {
                'section_title': 'Actualizar',
                'button_text': 'Actualizar',
                'form': form}

            return render_to_response(
                'tipo_ingreso_egreso/create.html',
                context,
                context_instance=RequestContext(request))
    else:
        tipos = TipoIngresoEgresoEmpleado.objects.get(id=pk)
        form = TipoIngresoEgresoForm(instance=tipos)
        context = {
            'section_title': 'Actualizar',
            'button_text': 'Actualizar',
            'form': form}

        return render_to_response(
            'tipo_ingreso_egreso/create.html',
            context,
            context_instance=RequestContext(request))

@login_required()
def MostrarAnalisisPrestamoView(request):
    if request.method == 'POST':
        id = request.POST.get('id_empleado')
        detalle = AnalisisPrestamo.objects.filter(empleado_id=id)
        empleados = Empleado.objects.get(empleado_id=id)
        return render_to_response('prestamo/mostrar_analisis.html', {'detalle': detalle, 'empleados': empleados},
                                  RequestContext(request))
    else:
        id = request.POST.get('id_empleado')
        detalle = AnalisisPrestamo.objects.filter(empleado_id=id)
        empleados = Empleado.objects.get(empleado_id=id)
        return render_to_response('prestamo/mostrar_analisis.html', {'detalle': detalle, 'empleados': empleados},
                                  RequestContext(request))

@login_required()
def liquidacionLaboralListView(request):
    if request.method == 'POST':
        analisis = LiquidacionLaboral.objects.order_by('fecha')

        return render_to_response('liquidacionfinal/index.html', {'analisis': analisis}, RequestContext(request))


    else:
        analisis = LiquidacionLaboral.objects.order_by('id')
        return render_to_response('liquidacionfinal/index.html', {'analisis': analisis}, RequestContext(request))

@login_required()
def liquidacionLaboralCreateView(request):
    if request.method == 'POST':
        form = LiquidacionLaboralForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.sueldo_pendiente_cantidad = request.POST.get('sueldo_pendiente_cantidad')
            new_orden.sueldo_pendiente_total = request.POST.get('sueldo_pendiente')
            new_orden.antiguedad_cantidad = request.POST.get('antiguedad_vacaciones_cantidad')
            new_orden.total_antiguedad = request.POST.get('antiguedad_vacaciones')
            new_orden.total_beneficio = request.POST.get('total_beneficios')
            new_orden.desahucio = request.POST.get('desahucio_cant')
            new_orden.total_desahucio = request.POST.get('desahucio')
            new_orden.bonificacion_in = request.POST.get('bonificacion_in')
            new_orden.bonificacion = request.POST.get('bonificacion')
            new_orden.total_otros_ingresos = request.POST.get('total_bonificacion')
            new_orden.total_vacaciones = request.POST.get('total_vacaciones')
            new_orden.iess = request.POST.get('iess')
            new_orden.ptmo = request.POST.get('prestamo')
            new_orden.quirografario = request.POST.get('quirografario')
            new_orden.adendum_telefonia = request.POST.get('adendum_movistar')
            new_orden.consumo_telefonia = request.POST.get('consumo_movistar')
            new_orden.total_descuentos = request.POST.get('total_descuento')
            new_orden.total = request.POST.get('recibir')
            new_orden.save()

            try:
                secuencial = Secuenciales.objects.get(modulo='liquidacion_laboral')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/recursos_humanos/liquidacionLaboral')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = LiquidacionLaboralForm

    return render_to_response('liquidacionfinal/create.html', {'form': form}, RequestContext(request))

@login_required()
@csrf_exempt
def obtenerEmpleadoLiquidacion(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        fecha = request.POST.get('fecha')
        formato_fecha = "%Y-%m-%d"

        fecha_inicial = datetime.strptime(fecha, formato_fecha)
        mes = fecha_inicial.month
        anio = fecha_inicial.year
        fecha_calculo = fecha_inicial - timedelta(days=330)

        mes_calculo = fecha_calculo.month
        anio_calculo = fecha_calculo.year
        detal = Empleado.objects.get(empleado_id=id)
        total_ingresos = 0
        total_vacaciones = 0
        total_dt = 0
        total_dc = 0
        sueldo_valor = 0
        bonificacion = 0
        sueldo_mensual = 0

        i = 0
        j = 10
        html = '<table border="1"><tr><td>PERIODO</td><td>DIAS LABORADOS</td><td>SUELDO</td><td>VACACIONES</td><td>XIII</td><td>XIV</td></tr>'
        fecha_buscar = fecha_calculo
        while int(i) <= int(j):
            i = i + 1
            print(str(i))
            fecha_buscar = fecha_buscar + timedelta(days=30)
            mes = fecha_buscar.month
            anio = fecha_buscar.year
            print(str(anio))
            print(str(mes))
            try:
                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
                print('VALIDAR1')
                ingresos_v = ingresos['valor__sum']
            except IngresosRolEmpleado.DoesNotExist:
                ingresos = None
                print('VALIDAR1nonw')
                ingresos_v = 0

            try:
                # sueldo = IngresosRolEmpleado.objects.get(anio=anio,mes=8,quincena=1,empleado_id=detal.empleado_id,pagar=True,tipo_ingreso_egreso_empleado_id=24)
                # print('SUELDO'+str(sueldo.valor_mensual)+'')
                sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)

            except IngresosProyectadosEmpleado.DoesNotExist:
                sueldo = None

            if sueldo:
                if sueldo_mensual < sueldo.valor_mensual:
                    sueldo_mensual = sueldo.valor_mensual
            else:
                sueldo = 0

            try:
                dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('dias'))
                dias_f = dias['dias__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                dias = None
                dias_f = 0

            try:
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
                if ingresos_v != None:
                    if faltas_injustificadas_valor['valor__sum'] != None:
                        ingresos_v = ingresos_v - faltas_injustificadas_valor['valor__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                faltas_injustificadas_valor = None
            print('VALIDAR')

            vacaciones = 0
            ing_dt = 0
            ing_dc = 0

            try:
                otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))
                ing_dc = otros_ingresos_dc['valor__sum']
            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dc = None
                ing_dc = 0

            try:
                otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))
                ing_dt = otros_ingresos_dt['valor__sum']

            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dt = None
                ing_dt = 0

            html += '<tr>'
            html += '<td>' + str(anio) + '-' + str(mes) + '</td>'
            if ingresos_v == None:
                ingresos_v = 0

            vacaciones = float(ingresos_v) / 24
            if dias_f == None:
                dias_f = 0
            html += '<td>' + str(dias_f) + '</td>'
            html += '<td>' + str(ingresos_v) + '</td>'
            html += '<td>' + str(vacaciones) + '</td>'
            if ing_dt == None:
                ing_dt = 0
            html += '<td>' + str(ing_dt) + '</td>'
            if ing_dc == None:
                ing_dc = 0
            html += '<td>' + str(ing_dc) + '</td></tr>'
            if ingresos_v != None:
                total_ingresos = total_ingresos + ingresos_v
            total_vacaciones = total_vacaciones + vacaciones
            total_dt = total_dt + ing_dt
            total_dc = total_dc + ing_dc

        cant = 12
        html += '<tr><td></td><td></td><td>' + str(
            total_ingresos) + '<input type="hidden" name="total_ingresos" id="total_ingresos" value="' + str(
            total_ingresos) + '" /></td><td>' + str(total_vacaciones) + '</td><td>' + str(total_dt) + '</td><td>' + str(
            total_dc) + '</td></tr>'
        html += '</table>'
        html += '<table><tr><td><h5><b>Beneficios Sociales</b></h5></td><td></td><td></td><td></td></tr>'
        html += '<tr><td>Sueldo Pendiente</td><td><input type="text" id="sueldo_pendiente_cantidad"  name="sueldo_pendiente_cantidad" onkeup="calcularSueldo()" value="' + str(
            cant) + '"/></td>'
        sueldo_pendiente = sueldo_mensual / 30 * cant
        html += '<td><input type="text" id="sueldo_pendiente"  name="sueldo_pendiente" onkeup="calcularSueldo()" value="' + str(
            sueldo_pendiente) + '"/></td>'

        horas_extras = 0
        html += '<tr><td>Horas Extras</td><td></td><td><inpu type="text" name="horas_extras" id="horas_extras" value="' + str(
            horas_extras) + '" /></td></tr>'
        cant_v = 1
        html += '<tr><td>Antiguedad por Vacaciones</td><td><input type="text" id="antiguedad_vacaciones_cantidad"  name="antiguedad_vacaciones_cantidad" onkeup="calcularSueldo()" value="' + str(
            cant_v) + '"/></td>'
        antiguedad_vacaciones = total_ingresos / 15 * cant_v

        html += '<td><input type="text" id="antiguedad_vacaciones"  name="antiguedad_vacaciones" onkeup="calcularSueldo()" value="' + str(
            antiguedad_vacaciones) + '"/></td>'

        html += '<tr><td>Vacaciones no Gozadas</td><td style="width:220px"></td><td><input type="text" name="total_vacaciones" id="total_vacaciones" value="' + str(
            total_vacaciones) + '"/></td></tr>'
        html += '<tr><td>XIII SUELDO</td><td></td><td><input type="text" name="total_dt" id="total_dt" value="' + str(
            total_dt) + '"/></td></tr>'
        html += '<tr><td>XIV SUELDO</td><td></td><td><input type="text" name="total_dc" id="total_dc" value="' + str(
            total_dc) + '"/></td></tr>'
        total_beneficios = total_ingresos + horas_extras + total_vacaciones + total_dt + total_dc

        html += '<tr><td>TOTAL DE BENEFICIOS SOCIALES</td><td></td><td><input type="text" name="total_beneficios" id="total_beneficios" value="' + str(
            round(total_beneficios, 2)) + '"/></td></tr>'
        html += '</table>'
        html += '<table>'
        quirografario3 = EgresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))

        ptmo3 = EgresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))

        if quirografario3['valor__sum']:
            quirografario3_valor = quirografario3['valor__sum']
        else:
            quirografario3_valor = 0

        if ptmo3['valor__sum']:
            ptmo3_valor = ptmo3['valor__sum']
        else:
            ptmo3_valor = 0

        html += '<tr><td><h5><b>OTROS INGRESOS</b></h5></td><td></td><td></td></tr>'
        desahucio_cant = 10
        html += '<tr><td>ART.185 C.T. 25% DESAHUCIO</td><td><input type="text" id="desahucio_cant"  name="desahucio_cant" onkeup="calcularSueldo()" value="' + str(
            desahucio_cant) + '"/></td>'
        desahucio = total_ingresos / 10 * 0.25 * desahucio_cant
        html += '<td><input type="text" id="desahucio"  name="desahucio" onkeup="calcularSueldo()" value="' + str(
            desahucio) + '"/></td></tr>'
        html += '<tr><td>BONIFICACION</td><td></td><td><input type="text" id="bonificacion"  name="bonificacion" onkeup="calcularSueldo()" value="' + str(
            bonificacion) + '"/></td></tr>'
        bonificacion_in = 0
        html += '<tr><td>BONIFICACION DESP. INTEMPESTIVO</td><td style="width:220px"></td><td><input type="text" id="bonificacion_in"  name="bonificacion_in" onkeup="calcularSueldo()" value="' + str(
            bonificacion_in) + '"/></td></tr>'
        total_bonificacion = desahucio + bonificacion + bonificacion_in
        html += '<tr><td>BONIFICACION</td><td></td><td><input type="text" id="total_bonificacion"  name="total_bonificacion" onkeup="calcularSueldo()" value="' + str(
            round(total_bonificacion, 2)) + '"/></td></tr>'
        html += '</table>'

        html += '<table><tr><td><h5><b>(-)DESCUENTOS</b></h5></td><td></td><td></td></tr>'
        iess = sueldo_pendiente * 9.45 / 100

        html += '<tr><td>APORTE IESS.</td><td></td><td><input type="text" id="iess"  name="iess" onkeup="calcularSueldo()" value="' + str(
            iess) + '"/></td>'
        html += '</tr>'
        prestamo = 0
        html += '<tr><td>PRESTAMO EMPRESA</td><td style="width:220px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td><td><input type="text" id="prestamo"  name="prestamo" onkeup="calcularSueldo()" value="' + str(
            prestamo) + '"/></td></tr>'
        quirografario = 0
        html += '<tr><td>PRESTAMO QUIROGRAFARIO</td><td></td><td><input type="text" id="quirografario"  name="quirografario" onkeup="calcularSueldo()" value="' + str(
            quirografario) + '"/></td></tr>'
        adendum_movistar = 0
        html += '<tr><td>Adendum Movistar</td><td></td><td><input type="text" id="adendum_movistar"  name="adendum_movistar" onkeup="calcularSueldo()" value="' + str(
            adendum_movistar) + '"/></td></tr>'
        consumo_movistar = 0
        html += '<tr><td>Consumo Movistar</td><td></td><td><input type="text" id="consumo_movistar"  name="consumo_movistar" onkeup="calcularSueldo()" value="' + str(
            consumo_movistar) + '"/></td></tr>'

        total_descuentos = iess + prestamo + quirografario + consumo_movistar + adendum_movistar
        html += '<tr><td></td><td></td><td><input type="text" id="total_descuento"  name="total_descuento" onkeup="calcularSueldo()" value="' + str(
            round(total_descuentos, 2)) + '"/></td></tr>'
        recibir = total_beneficios + total_bonificacion - total_descuentos

        html += '<tr><td></td><td>NETO A RECIBIR</td><td><input type="text" id="recibir"  name="recibir" onkeup="calcularSueldo()" value="' + str(
            round(recibir, 2)) + '"/></td></tr>'
        html += '</table>'

        item = {
            'html': html,
            'sueldo_mensual': sueldo_mensual,
            'cargo': detal.tipo_empleado_id,
            'departamento': detal.departamento_id,
        }
    return HttpResponse(json.dumps(item), content_type='application/json')

@login_required()
def LiquidacionLaboralImprimir(request, pk):
    if request.method == 'POST':
        return HttpResponseRedirect('/recursos_humanos/liquidacionlaboral')

    else:
        form = LiquidacionLaboral.objects.get(id=pk)

        html = ''
        html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="4" >'
        html += 'MUEBLES Y DIVERSIDADES<br />INFORMACION ECONOMICA <br />LIQUIDACION LABORAL</td><td>No de Solicitud</td><td>' + str(
            form.codigo) + '</td></tr>'
        html += '</table>'
        html += '<table><tr><td colspan="8">DATOS PERSONALES</td></tr>'
        html += '<tr><td colspan="2">Fecha de solicitud:</td><td colspan="3">' + str(
            form.fecha) + '</td><td colspan="2">Sueldo Fijo:</td><td colspan="2">' + str(
            form.sueldo_fijo) + '</td></tr>'
        html += '<tr><td colspan="2">Nombre del colaborador:</td><td colspan="3">' + str(
            form.empleado.nombre_empleado) + '</td><td colspan="2">Fecha de Ingreso:</td><td colspan="2">' + str(
            form.empleado.fecha_ini_reconocida) + '</td></tr>'
        html += '<tr><td colspan="2">Cargo/Area:</td><td colspan="3">' + str(
            form.tipoempleado) + '</td><td colspan="2">Fecha de Salida:</td><td colspan="2">' + str(
            form.fecha_salida) + '</td></tr>'
        html += '</table>'

        fecha_inicial = form.fecha
        formato_fecha = "%Y-%m-%d"

        # fecha_inicial = datetime.strptime(fecha, formato_fecha)
        mes = fecha_inicial.month
        anio = fecha_inicial.year
        fecha_calculo = fecha_inicial - timedelta(days=330)

        mes_calculo = fecha_calculo.month
        anio_calculo = fecha_calculo.year
        detal = Empleado.objects.get(empleado_id=form.empleado_id)
        total_ingresos = 0
        total_vacaciones = 0
        total_dt = 0
        total_dc = 0
        sueldo_valor = 0
        bonificacion = 0
        sueldo_mensual = 0

        i = 0
        j = 10

        html += '<br><br/><table border="1"><tr><td>PERIODO</td><td>DIAS LABORADOS</td><td>SUELDO</td><td>VACACIONES</td><td>XIII</td><td>XIV</td></tr>'
        fecha_buscar = fecha_calculo
        while int(i) <= int(j):
            i = i + 1
            fecha_buscar = fecha_buscar + timedelta(days=30)
            mes = fecha_buscar.month
            anio = fecha_buscar.year

            try:
                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
                ingresos_v = ingresos['valor__sum']
            except IngresosRolEmpleado.DoesNotExist:
                ingresos = None
                print('VALIDAR1nonw')
                ingresos_v = 0

            try:

                sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)

            except IngresosProyectadosEmpleado.DoesNotExist:
                sueldo = None

            if sueldo:
                if sueldo_mensual < sueldo.valor_mensual:
                    sueldo_mensual = sueldo.valor_mensual
            else:
                sueldo = 0

            try:
                dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('dias'))
                dias_f = dias['dias__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                dias = None
                dias_f = 0

            try:
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('valor'))
                if ingresos_v != None:
                    if faltas_injustificadas_valor['valor__sum'] != None:
                        ingresos_v = ingresos_v - faltas_injustificadas_valor['valor__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                faltas_injustificadas_valor = None
            print('VALIDAR')

            vacaciones = 0
            ing_dt = 0
            ing_dc = 0

            try:
                otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))
                ing_dc = otros_ingresos_dc['valor__sum']
            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dc = None
                ing_dc = 0

            try:
                otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))
                ing_dt = otros_ingresos_dt['valor__sum']

            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dt = None
                ing_dt = 0

            html += '<tr>'
            html += '<td>' + str(anio) + '-' + str(mes) + '</td>'
            if ingresos_v == None:
                ingresos_v = 0

            vacaciones = float(ingresos_v) / 24
            if dias_f == None:
                dias_f = 0
            html += '<td>' + str(dias_f) + '</td>'
            html += '<td>' + str(ingresos_v) + '</td>'
            html += '<td>' + str(vacaciones) + '</td>'
            if ing_dt == None:
                ing_dt = 0
            html += '<td>' + str(ing_dt) + '</td>'
            if ing_dc == None:
                ing_dc = 0
            html += '<td>' + str(ing_dc) + '</td></tr>'
            if ingresos_v != None:
                total_ingresos = total_ingresos + ingresos_v
            total_vacaciones = total_vacaciones + vacaciones
            total_dt = total_dt + ing_dt
            total_dc = total_dc + ing_dc

        cant = 12
        html += '<tr><td></td><td></td><td>' + str(total_ingresos) + '</td><td>' + str(
            total_vacaciones) + '</td><td>' + str(total_dt) + '</td><td>' + str(total_dc) + '</td></tr>'
        html += '</table>'
        html += '<table><tr><td><h5><b>Beneficios Sociales</b></h5></td><td></td><td></td><td></td></tr>'
        html += '<tr><td>Sueldo Pendiente</td><td>' + str(form.sueldo_pendiente_cantidad) + '</td>'

        html += '<td>' + str(form.sueldo_pendiente_total) + '</td>'

        horas_extras = 0
        html += '<tr><td>Horas Extras</td><td></td><td><inpu type="text" name="horas_extras" id="horas_extras" value="' + str(
            horas_extras) + '" /></td></tr>'
        cant_v = 1
        html += '<tr><td>Antiguedad por Vacaciones</td><td>' + str(form.antiguedad_cantidad) + '</td>'

        html += '<td>' + str(form.total_antiguedad) + '</td>'

        html += '<tr><td>Vacaciones no Gozadas</td><td style="width:220px"></td><td>' + str(
            form.total_vacaciones) + '</td></tr>'
        html += '<tr><td>XIII SUELDO</td><td></td><td>' + str(total_dt) + '</td></tr>'
        html += '<tr><td>XIV SUELDO</td><td></td><td>' + str(total_dc) + '</td></tr>'

        html += '<tr><td>TOTAL DE BENEFICIOS SOCIALES</td><td></td><td>' + str(form.total_beneficio) + '"/></td></tr>'
        html += '</table>'
        html += '<table>'

        html += '<tr><td><h5><b>OTROS INGRESOS</b></h5></td><td></td><td></td></tr>'
        desahucio_cant = 10
        html += '<tr><td>ART.185 C.T. 25% DESAHUCIO</td><td>' + str(form.desahucio) + '</td>'
        html += '<td>' + str(form.total_desahucio) + '</td></tr>'
        html += '<tr><td>BONIFICACION</td><td></td><td>' + str(form.bonificacion) + '</td></tr>'
        html += '<tr><td>BONIFICACION DESP. INTEMPESTIVO</td><td style="width:220px"></td><td>' + str(
            form.bonificacion_in) + '"/></td></tr>'
        html += '<tr><td>BONIFICACION</td><td></td><td>' + str(form.total_otros_ingresos) + '</td></tr>'
        html += '</table>'

        html += '<table><tr><td><h5><b>(-)DESCUENTOS</b></h5></td><td></td><td></td></tr>'

        html += '<tr><td>APORTE IESS.</td><td></td><td>' + str(form.iess) + '</td>'
        html += '</tr>'
        prestamo = 0
        html += '<tr><td>PRESTAMO EMPRESA</td><td style="width:220px">&nbsp;&nbsp;</td><td>' + str(
            form.ptmo) + '</td></tr>'
        html += '<tr><td>PRESTAMO QUIROGRAFARIO</td><td></td><td>' + str(form.quirografario) + '</td></tr>'
        adendum_movistar = 0
        html += '<tr><td>Adendum Movistar</td><td></td><td>' + str(form.adendum_telefonia) + '</td></tr>'
        consumo_movistar = 0
        html += '<tr><td>Consumo Movistar</td><td></td><td>' + str(form.consumo_telefonia) + '</td></tr>'

        html += '<tr><td></td><td></td><td>' + str(form.total_descuentos) + '</td></tr>'

        html += '<tr><td></td><td>NETO A RECIBIR</td><td>' + str(form.total) + '</td></tr>'
        html += '</table>'
        html += '<br><br><table><tr><td>-----------------<br>Elaborado por:<br>Asistente de Nomina</td>'
        html += '<td>-----------------<br>Revisado por<br>Contador</td>'
        html += '<td>-----------------<br>Visto Bueno<br>G. Administrativa</td>'
        html += '<td>-----------------<br>Aprobado por<br>Gerencia</td>'
        html += '</tr></table>'

    html1 = render_to_string('liquidacionfinal/imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

@login_required()
def liquidacionVacacionesListView(request):
    if request.method == 'POST':
        analisis = LiquidacionVacaciones.objects.order_by('fecha')

        return render_to_response('liquidacion_vacaciones/index.html', {'analisis': analisis}, RequestContext(request))


    else:
        analisis = LiquidacionVacaciones.objects.order_by('id')
        return render_to_response('liquidacion_vacaciones/index.html', {'analisis': analisis}, RequestContext(request))

@login_required()
def liquidacionVacacionesCreateView(request):
    if request.method == 'POST':
        form = LiquidacionVacacionesForm(request.POST)

        if form.is_valid():
            new_orden = form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.vacaciones = request.POST.get('vacaciones')
            new_orden.antiguedad_cantidad = request.POST.get('antiguedad')
            new_orden.antiguedad = request.POST.get('total_antiguedad')
            new_orden.total_ingresos = request.POST.get('total_ingresos')
            new_orden.iess = request.POST.get('iess')
            new_orden.anticipo_vacaciones = request.POST.get('anticipo')
            new_orden.total_egresos = request.POST.get('total_egresos')
            new_orden.total = request.POST.get('total_recibir')
            new_orden.sueldo_fijo=request.POST.get('sueldo')

            new_orden.save()

            try:
                secuencial = Secuenciales.objects.get(modulo='liquidacion_vacaciones')
                secuencial.secuencial = secuencial.secuencial + 1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None

            return HttpResponseRedirect('/recursos_humanos/LiquidacionVacaciones')
        else:
            print 'error'
        print form.errors, len(form.errors)
    else:
        form = LiquidacionVacacionesForm

    return render_to_response('liquidacion_vacaciones/create.html', {'form': form}, RequestContext(request))

@login_required()
def LiquidacionVacacionesImprimir(request, pk):
    if request.method == 'POST':
        return HttpResponseRedirect('/recursos_humanos/LiquidacionVacaciones')

    else:
        form = LiquidacionVacaciones.objects.get(id=pk)

        html = ''
        html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="4" >'
        html += 'MUEBLES Y DIVERSIDADES<br />INFORMACION ECONOMICA <br />LIQUIDACION DE VACACIONES</td><td>No de Solicitud</td><td>' + str(
            form.codigo) + '</td></tr>'
        html += '</table>'

        fecha_inicial = form.fecha
        formato_fecha = "%Y-%m-%d"

        # fecha_inicial = datetime.strptime(fecha, formato_fecha)
        mes = fecha_inicial.month
        anio = fecha_inicial.year
        fecha_calculo = fecha_inicial - timedelta(days=370)

        mes_calculo = fecha_calculo.month
        anio_calculo = fecha_calculo.year
        detal = Empleado.objects.get(empleado_id=form.empleado_id)
        total_ingresos = 0
        total_vacaciones = 0
        total_dt = 0
        total_dc = 0
        sueldo_valor = 0
        bonificacion = 0
        sueldo_mensual = 0
        mes_real_calculo = ''
        mes_real = ''

        i = 0
        j = 12
        if mes == 8:
            mes_real = 'Agosto'
        if mes_calculo == 8:
            mes_real_calculo = 'Agosto'

        html += '<table><tr><td colspan="8">DATOS PERSONALES</td></tr>'
        html += '<tr><td colspan="2">Fecha de solicitud:</td><td colspan="3">' + str(
            form.fecha) + '</td><td colspan="2">Sueldo Fijo:</td><td colspan="2">' + str(
            form.sueldo_fijo) + '</td></tr>'
        html += '<tr><td colspan="2">Nombre del colaborador:</td><td colspan="3">' + str(
            form.empleado.nombre_empleado) + '</td><td colspan="2">Fecha de Ingreso:</td><td colspan="2">' + str(
            form.empleado.fecha_ini_reconocida) + '</td></tr>'
        html += '<tr><td colspan="2">Cargo/Area:</td><td colspan="3">' + str(
            form.tipoempleado) + '</td><td colspan="2">Perido de Goce:</td><td colspan="2">Desde:' + str(
            form.fecha_salida) + '<br/> Hasta:' + str(form.fecha_entrada) + '</td></tr>'
        html += '<tr><td colspan="9">Liquidado desde el 1 de ' + str(mes_real) + ' del ' + str(
            anio) + ' hasta el 31 de ' + str(mes_real_calculo) + ' del' + str(anio_calculo) + '</td></tr>'
        html += '</table>'

        html += '<br><br/><table border="1"><thead><tr><td style="width: 400px">DETALLE</td><td>INGRESOS</td><td>EGRESOS</td></tr></thead>'
        html += '<tbody><tr><td colspan="3"><h5>INGRESOS</h5></td></tr>'
        html += '<tr><td>VACACIONES</td><td>' + str(form.vacaciones) + '</td><td></td></tr>'
        html += '<tr><td>Antiguedad' + str(form.antiguedad_cantidad) + 'A&Ntilde;OS</td> <td>' + str(
            form.antiguedad) + '</td><td></td></tr>'
        html += ' <tr><td>TOTAL DE INGRESOS US$</td><td>' + str(form.total_ingresos) + ' </td><td></td></tr>'
        html += ' <tr><td colspan="3"><h5>EGRESOS</h5></td></tr>'
        html += '<tr><td>APORTE IESS 9.45%</td><td></td><td>' + str(form.iess) + '</td></tr>'
        html += '<tr><td>ANTICIPO VACACIONES</td><td></td><td>' + str(form.anticipo_vacaciones) + '</td></tr>'
        html += ' <tr><td>TOTAL DE EGRESOS US$</td><td></td><td>' + str(form.total_egresos) + '</td></tr>'
        html += ' <tr><td colspan=2 style="">INGRESOS MENOS EGRESOS TOTAL A COBRAR</td><td>' + str(
            form.total) + '</td></tr>'
        html += '</tbody></table><br><br/>'

        html += '<br><br/><table border="1"><tr><td>PERIODO</td><td>DIAS LABORADOS</td><td>SUELDO</td><td>VACACIONES</td><td>XIII</td><td>XIV</td></tr>'
        fecha_buscar = fecha_calculo
        while int(i) <= int(j):
            i = i + 1
            fecha_buscar = fecha_buscar + timedelta(days=30)
            mes = fecha_buscar.month
            anio = fecha_buscar.year

            try:
                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
                ingresos_v = ingresos['valor__sum']
            except IngresosRolEmpleado.DoesNotExist:
                ingresos = None
                print('VALIDAR1nonw')
                ingresos_v = 0

            try:

                sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)

            except IngresosProyectadosEmpleado.DoesNotExist:
                sueldo = None

            if sueldo:
                if sueldo_mensual < sueldo.valor_mensual:
                    sueldo_mensual = sueldo.valor_mensual
            else:
                sueldo = 0

            try:
                dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('dias'))
                dias_f = dias['dias__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                dias = None
                dias_f = 0

            try:
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('valor'))
                if ingresos_v != None:
                    if faltas_injustificadas_valor['valor__sum'] != None:
                        ingresos_v = ingresos_v - faltas_injustificadas_valor['valor__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                faltas_injustificadas_valor = None
            print('VALIDAR')

            vacaciones = 0
            ing_dt = 0
            ing_dc = 0

            try:
                otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))
                ing_dc = otros_ingresos_dc['valor__sum']
            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dc = None
                ing_dc = 0

            try:
                otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))
                ing_dt = otros_ingresos_dt['valor__sum']

            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dt = None
                ing_dt = 0

            html += '<tr>'
            html += '<td>' + str(anio) + '-' + str(mes) + '</td>'
            if ingresos_v == None:
                ingresos_v = 0

            vacaciones = float(ingresos_v) / 24
            if dias_f == None:
                dias_f = 0
            html += '<td>' + str(dias_f) + '</td>'
            html += '<td>' + str(ingresos_v) + '</td>'
            html += '<td>' + str(vacaciones) + '</td>'
            if ing_dt == None:
                ing_dt = 0
            html += '<td>' + str(ing_dt) + '</td>'
            if ing_dc == None:
                ing_dc = 0
            html += '<td>' + str(ing_dc) + '</td></tr>'
            if ingresos_v != None:
                total_ingresos = total_ingresos + ingresos_v
            total_vacaciones = total_vacaciones + vacaciones
            total_dt = total_dt + ing_dt
            total_dc = total_dc + ing_dc

        cant = 12
        html += '<tr><td></td><td></td><td>' + str(total_ingresos) + '</td><td>' + str(
            total_vacaciones) + '</td><td>' + str(total_dt) + '</td><td>' + str(total_dc) + '</td></tr>'
        html += '</table>'

        html += '<br><br><table><tr><td>-----------------<br>Elaborado por:<br>Asistente de Nomina</td>'
        html += '<td>-----------------<br>Visto Bueno<br>Gerente de Produccion</td>'
        html += '<td>-----------------<br>Revisador por<br>G. Administrativa</td>'
        html += '<td>-----------------<br>Aprobado por<br>Contador</td>'
        html += '<td>-----------------<br>Recibi Conforme<br>Contador</td>'
        html += '</tr></table>'

    html1 = render_to_string('liquidacion_vacaciones/imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

@login_required()
@csrf_exempt
def obtenerEmpleadoLiquidacionVacaciones(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        fecha = request.POST.get('fecha')
        formato_fecha = "%Y-%m-%d"

        fecha_inicial = datetime.strptime(fecha, formato_fecha)
        mes = fecha_inicial.month
        anio = fecha_inicial.year
        fecha_calculo = fecha_inicial - timedelta(days=370)

        mes_calculo = fecha_calculo.month
        anio_calculo = fecha_calculo.year
        detal = Empleado.objects.get(empleado_id=id)
        total_ingresos = 0
        total_vacaciones = 0
        total_dt = 0
        total_dc = 0
        sueldo_valor = 0
        bonificacion = 0
        sueldo_mensual = 0

        i = 0
        j = 12
        html = '<table border="1"><tr><td>PERIODO</td><td>DIAS LABORADOS</td><td>SUELDO</td><td>VACACIONES</td><td>XIII</td><td>XIV</td></tr>'
        fecha_buscar = fecha_calculo
        while int(i) <= int(j):
            i = i + 1
            print(str(i))
            fecha_buscar = fecha_buscar + timedelta(days=30)
            mes = fecha_buscar.month
            anio = fecha_buscar.year
            print(str(anio))
            print(str(mes))
            try:
                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
                print('VALIDAR1')
                ingresos_v = ingresos['valor__sum']
            except IngresosRolEmpleado.DoesNotExist:
                ingresos = None
                print('VALIDAR1nonw')
                ingresos_v = 0

            try:
                # sueldo = IngresosRolEmpleado.objects.get(anio=anio,mes=8,quincena=1,empleado_id=detal.empleado_id,pagar=True,tipo_ingreso_egreso_empleado_id=24)
                # print('SUELDO'+str(sueldo.valor_mensual)+'')
                sueldo = IngresosProyectadosEmpleado.objects.get(empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)

            except IngresosProyectadosEmpleado.DoesNotExist:
                sueldo = None

            if sueldo:
                if sueldo_mensual < sueldo.valor_mensual:
                    sueldo_mensual = sueldo.valor_mensual
            else:
                sueldo = 0

            try:
                dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(
                    Sum('dias'))
                dias_f = dias['dias__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                dias = None
                dias_f = 0

            try:
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
                if ingresos_v != None:
                    if faltas_injustificadas_valor['valor__sum'] != None:
                        ingresos_v = ingresos_v - faltas_injustificadas_valor['valor__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                faltas_injustificadas_valor = None
            print('VALIDAR')

            try:
                dias_v = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(cargar_vacaciones=True).aggregate(Sum('valor'))
                dias_v_valor = dias_v['valor__sum']
            except DiasNoLaboradosRolEmpleado.DoesNotExist:
                dias_v = None
                dias_v_valor = 0

            vacaciones = 0
            ing_dt = 0
            ing_dc = 0

            try:
                otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))
                ing_dc = otros_ingresos_dc['valor__sum']
            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dc = None
                ing_dc = 0

            try:
                otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
                    empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))
                ing_dt = otros_ingresos_dt['valor__sum']

            except OtrosIngresosRolEmpleado.DoesNotExist:
                otros_ingresos_dt = None
                ing_dt = 0

            html += '<tr>'
            html += '<td>' + str(anio) + '-' + str(mes) + '</td>'
            if ingresos_v == None:
                ingresos_v = 0

            vacaciones = float(ingresos_v) / 24
            if dias_f == None:
                dias_f = 0
            html += '<td>' + str(dias_f) + '</td>'
            html += '<td>' + str(ingresos_v) + '</td>'
            html += '<td>' + str(vacaciones) + '</td>'
            if ing_dt == None:
                ing_dt = 0
            html += '<td>' + str(ing_dt) + '</td>'
            if ing_dc == None:
                ing_dc = 0
            html += '<td>' + str(ing_dc) + '</td></tr>'
            if ingresos_v != None:
                total_ingresos = total_ingresos + ingresos_v
            total_vacaciones = total_vacaciones + vacaciones
            total_dt = total_dt + ing_dt
            total_dc = total_dc + ing_dc

        cant = 12
        html += '<tr><td></td><td></td><td>' + str(
            total_ingresos) + '<input type="hidden" name="total_ingresos" id="total_ingresos" value="' + str(
            total_ingresos) + '" /></td><td>' + str(total_vacaciones) + '</td><td>' + str(total_dt) + '</td><td>' + str(
            total_dc) + '</td></tr>'
        html += '</table>'
        total_ingresos_sueldo = total_ingresos / 24
        antiguedad = 0
        valor_antiguedad = total_ingresos_sueldo / 15 * antiguedad
        total_ingresos_final = total_ingresos_sueldo + valor_antiguedad
        iess = total_ingresos_final * 9.45 / 100
        if dias_v_valor != None:
            anticipo_vacaciones = dias_v_valor
        else:
            anticipo_vacaciones = 0
        total_egresos_final = iess + anticipo_vacaciones
        recibir = total_ingresos_final - total_egresos_final

        item = {
            'html': html,
            'sueldo_mensual': sueldo_mensual,
            'cargo': detal.tipo_empleado_id,
            'departamento': detal.departamento_id,
            'total_vacaciones': total_vacaciones,
            'total_ingresos_sueldo': total_ingresos_sueldo,
            'antiguedad': antiguedad,
            'valor_antiguedad': valor_antiguedad,
            'total_ingresos_final': total_ingresos_final,
            'iess': iess,
            'anticipo_vacaciones': anticipo_vacaciones,
            'total_egresos_final': total_egresos_final,
            'recibir': recibir
        }
    return HttpResponse(json.dumps(item), content_type='application/json')


@login_required()
def SolicitudImprimir(request, pk):
    if request.method == 'POST':
        return HttpResponseRedirect('/recursos_humanos/LiquidacionVacaciones')

    else:
        form = Permiso.objects.get(id=pk)

        html = ''
        html += '<table border="1"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="4" >'
        html += 'MUEBLES Y DIVERSIDADES<br />SOLICITUDES VARIAS DE AUSENCIA DEL PERSONAL</td></tr>'
        html += '</table>'

        html += '<table><tr><td colspan="8">DATOS PERSONALES</td></tr>'
        html += '<tr><td colspan="2">Fecha de solicitud:</td><td colspan="3">' + str(
            form.fecha_solicitud.strftime('%Y-%m-%d')) + '</td></tr>'
        html += '<tr><td colspan="4">Nombre del colaborador:</td><td colspan="3">' + str(
            form.nombre_empleado) + '</td></tr>'
        html += '<tr><td colspan="2">Cargo/Area:</td><td colspan="2">' + str(
            form.cargo_empleado) + '</td><td colspan="2">Area:</td><td colspan="2">' + str(
            form.area_empleado) + '</td></tr>'
        html += '<tr><td colspan="9">' + str(form.tipo_solicitud.descripcion) + '</td></tr>'
        html += '</table>'
        if form.tipo_solicitud_id == 1:

            html += '<br><br/><table border="0">'
            html += '<tbody><tr><td width="30px">'
            if form.permisos_dias:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                html += '</td><td>PERMISO POR DIAS</td>'
                html += '<td>DESDE:'
                if form.fecha_desde:
                    html += str(form.fecha_desde.strftime('%Y-%m-%d'))
                html += '</td>'
                html += '<td>HASTA:'
                if form.fecha_hasta:
                    html += str(form.fecha_hasta.strftime('%Y-%m-%d'))
                html += '</td>'
                html += '<td>TOTAL DIAS AUSENCIA:'
                if form.total_dias_ausencia:
                    html += str(form.total_dias_ausencia)
                html += '</td>'
                html += '<td >'
                if form.motivo_trabajo:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                if form.motivo_personal:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                if form.motivo_calamidad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO CALAMIDAD</td>'
                html += '<td>'
                if form.motivo_enfermedad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'

            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '</td><td>PERMISO POR DIAS</td>'
                html += '<td>DESDE:</td>'
                html += '<td>HASTA:</td>'
                html += '<td>TOTAL DIAS AUSENCIA:</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;MOTIVO CALAMIDAD'
                html += '</td><td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'

            html +='</tr>'
            html+='<tr><td> '
            if form.permisos_horas:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>PERMISO POR HORAS</td>'
                html += '<td>DESDE:'
                if form.fecha_desde:
                    html += str(form.hora_desde)
                html += '</td>'
                html += '<td>HASTA:'
                if form.fecha_hasta:
                    html += str(form.hora_hasta)
                html += '</td>'

                html += '<td>TOTAL HORAS AUSENCIA:'
                if form.total_dias_ausencia:
                    html += str(form.total_horas_ausencia)
                html += '</td>'
                html += '<td>'
                if form.motivo_trabajo:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                if form.motivo_personal:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += 'nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                if form.motivo_calamidad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO CALAMIDAD</td>'
                html += '<td>'
                if form.motivo_enfermedad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>PERMISO POR HORAS</td>'
                html += '<td>DESDE:</td>'
                html += '<td>HASTA:</td>'

                html += '<td>TOTAL HORAS AUSENCIA:</td>'
                html += '<td><img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;MOTIVO CALAMIDAD'
                html += '</td><td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'



            html +='</tr>'

            html += '<tr><td>'
            if form.licencia_dias:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>LICENCIA DIAS</td>'
                html += '<td>DESDE:'
                if form.fecha_desde:
                    html += str(form.fecha_desde)
                html += '</td>'
                html += '<td>HASTA:'
                if form.fecha_hasta:
                    html += str(form.fecha_hasta)
                html += '</td>'
                html += '<td>TOTAL DIAS AUSENCIA:'
                if form.total_dias_ausencia:
                    html += str(form.total_dias_ausencia)
                html += '</td>'
                html += '<td>'
                if form.motivo_trabajo:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                if form.motivo_personal:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                if form.motivo_calamidad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO CALAMIDAD</td>'
                html += '<td>'
                if form.motivo_enfermedad:
                    html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                else:
                    html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>LICENCIA DIAS</td>'
                html += '<td>DESDE:</td>'
                html += '<td>HASTA:</td>'
                html += '<td>TOTAL DIAS AUSENCIA:</td>'
                html += '<td><img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO TRABAJO</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO PERSONAL</td>'
                html += '<td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;MOTIVO CALAMIDAD'
                html += '</td><td>'
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

                html += '&nbsp;MOTIVO ENFERMEDAD</td>'



            html += '</tr>'

            html += '<tr><td>'
            if form.descanso_iess_dias:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>DESCANSO IESS/DIAS</td>'
                html += '<td>DESDE:'
                if form.fecha_desde:
                    html += str(form.fecha_desde)
                html += '</td>'
                html += '<td>HASTA:'
                if form.fecha_hasta:
                    html += str(form.fecha_hasta)
                html += '</td>'
                html += '<td>TOTAL DIAS AUSENCIA:'
                if form.total_dias_ausencia:
                    html += str(form.total_dias_ausencia)
                html += '</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>DESCANSO IESS/DIAS</td>'
                html += '<td>DESDE:</td>'
                html += '<td>HASTA:</td>'
                html += '<td>TOTAL DIAS AUSENCIA:</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'



            html += '</tr>'

            html += '<tr><td>'
            if form.cita_iess_horas:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>CITAS IESS/HORAS</td>'
                html += '<td>DESDE:'
                if form.fecha_desde:
                    html += str(form.fecha_desde)
                html += '</td>'
                html += '<td>HASTA:'
                if form.fecha_hasta:
                    html += str(form.fecha_hasta)
                html += '</td>'
                html += '<td>TOTAL DIAS AUSENCIA:'
                if form.total_dias_ausencia:
                    html += str(form.total_dias_ausencia)
                html += '</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'
                html += '&nbsp;</td><td>CITAS IESS/HORAS</td>'
                html += '<td>DESDE:</td>'
                html += '<td>HASTA:</td>'
                html += '<td>TOTAL DIAS AUSENCIA:</td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'
                html += '<td></td>'



            html += '</tr>'

            html += '<tr><td colspan="2">OBSERVACION MOTIVO</td><td colspan="5">&nbsp;&nbsp;&nbsp;' + str(form.observacion) + '</td></tr>'

            html += '</tbody></table><br><br/>'
        if form.tipo_solicitud_id == 2:

            html += '<br><br/><table border="0">'
            html += '<tbody><tr><td width="30px">'
            if form.vacaciones:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

            html += '&nbsp;</td><td>VACACIONES</td>'
            html += '<td>DESDE:'
            if form.fecha_desde:
                html += str(form.fecha_desde.strftime('%Y-%m-%d'))
            html += '<br>'
            html += 'HASTA:'
            if form.fecha_hasta:
                html += str(form.fecha_hasta.strftime('%Y-%m-%d'))
            html += '</td><td width="30px">'
            if form.periodo:
                html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'
            else:
                html += '<img src="media/imagenes/pedido_detalle/Checkbox.jpg"  alt="logo producto" width="10" height="10">'

            html += '&nbsp;</td><td>PERIODO</td>'
            html += '<td>DESDE:'
            if form.fecha_desde:
                html += str(form.fecha_desde.strftime('%Y-%m-%d'))
            html += '<br>'
            html += 'HASTA:'
            if form.fecha_hasta:
                html += str(form.fecha_hasta.strftime('%Y-%m-%d'))
            html += '</td>'
            html += '<td>TOTAL DIAS GOZADOS:'
            if form.total_dias_ausencia:
                html += str(form.total_dias_ausencia)

            html += '</td>'
            html += '<td>TOTAL DIAS PENDIENTES:'
            if form.total_dias_pendientes:
                html += str(form.total_dias_pendientes)

            html += '</td>'
            html += '<td>PERIODO DIAS PENDIENTES:'
            if form.periodo_dias_pendiente:
                html += str(form.periodo_dias_pendiente)
            html += '</td>'

            html += '<tr><td colspan="2">OBSERVACION MOTIVO</td><td colspan="5">&nbsp;&nbsp;&nbsp;' + str(form.observacion) + '</td></tr>'

            html += '</tbody></table><br><br/>'
        if form.tipo_solicitud_id == 3:

            html += '<br><br/><table border="0" >'
            html += '<tbody><tr><td>'
            html += '<img src="media/imagenes/pedido_detalle/rsz_check.jpg"  alt="logo producto" width="10" height="10">'

            html += '&nbsp;AUTORIZACION PARA LABORAR DIA</td>'
            html += '<td >DESDE:'
            if form.hora_desde:
                html += str(form.hora_desde)
            html += '&nbsp;&nbsp;&nbsp;HASTA:'
            if form.hora_hasta:
                html += str(form.hora_hasta)
            html += '</td>'

            html += '<td >TOTAL HORAS LABORADAS:'
            if form.total_horas_laboradas:
                html += str(form.total_horas_laboradas)

            html += '</td></tr>'


            html += '<tr></tr><tr><td>OBSERVACION MOTIVO</td><td colspan="2">&nbsp;&nbsp;&nbsp;' + str(form.observacion) + '</td></tr>'

            html += '</tbody></table><br><br/>'


        html += '<br><br><table><tr><td>NOMBRE Y FIRMA-----------------<br>'+str(
            form.nombre_empleado)+'</td>'
        html += '<td>-----------------<br>AUTORIZADO POR</td>'
        html += '<td>-----------------<br>AUTORIZADO POR</td>'
        html += '<td>-----------------<br>REVISADO POR</td>'
        html += '<tr><td>CARGO:'+str(form.cargo_empleado)+'</td>'
        html += '<td>JEFE AREA</td>'
        html += '<td>GERENTE/SUPERVISOR</td>'
        html += '<td>RRHH</td>'
        html += '</tr>'
        html += '<tr><td>AREA:' + str(form.area_empleado) + '</td>'
        html += '<td></td>'
        html += '<td></td>'
        html += '<td></td>'
        html += '</tr>'
        html += '</table>'

    html1 = render_to_string('liquidacion_vacaciones/imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)



@login_required()
def VacacionesNuevoView(request):
    if request.method == 'POST':
        proforma_form = VacacionesForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()

            return HttpResponseRedirect('/recursos_humanos/vacaciones')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = VacacionesForm

    return render_to_response('vacaciones/nuevo.html', {'form': proforma_form,}, RequestContext(request))

@login_required()
def VacacionesListView(request):
    if request.method == 'POST':

        row = Vacaciones.objects.all().order_by('id')
        return render_to_response('vacaciones/index.html', {'row': row}, RequestContext(request))
    else:
        row = Vacaciones.objects.all().order_by('id')
        return render_to_response('vacaciones/index.html', {'row': row}, RequestContext(request))

class VacacionesUpdateView(ObjectUpdateView):
    model = Vacaciones
    form_class = VacacionesForm
    template_name = 'vacaciones/nuevo.html'
    url_success = 'vacaciones-list'
    url_cancel = 'vacaciones-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)




@login_required()
@transaction.atomic

def ContabilizacionRolView(request,pk):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.order_by('id')
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        rol= RolPago.objects.get(id=pk)
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        contador = request.POST["contador"]
        print contador
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        with transaction.atomic():

            asiento = Asiento()
            asiento.codigo_asiento = "RRHH " + str(datetime.now().year) + "000" + str(codigo_asiento)
            asiento.fecha = datetime.now()
            asiento.glosa = 'ROL DE PAGO DEL ' + str(rol.anio) + ' mes ' + str(rol.mes)
            asiento.gasto_no_deducible = False
            asiento.save()

            i = 0
            total_debe=0
            total_haber=0
            while int(i) <= int(contador):
                i += 1
                if int(i) > int(contador):
                    print('entrosd')
                    break
                else:
                    if 'id_kitsc' + str(i) in request.POST:
                        cuenta_id=request.POST["id_kitsc"+str(i)]
                        debe=request.POST["debe_kitsc"+str(i)]
                        haber=request.POST["haber_kitsc"+str(i)]
                        concepto = request.POST["concepto_kitsc" + str(i)]
                        asiento_detalle = AsientoDetalle()
                        asiento_detalle.asiento_id = int(asiento.asiento_id)
                        asiento_detalle.cuenta_id = cuenta_id
                        asiento_detalle.debe = debe
                        asiento_detalle.haber = haber
                        asiento_detalle.concepto = concepto
                        asiento_detalle.save()
                        if debe.isdigit():
                            total_debe=total_debe+ float(debe)
                        if haber.isdigit():
                            total_haber=total_haber+ float(haber)

            asiento.total_debe=total_debe
            asiento.total_haber = total_haber
            asiento.save()
            rol.asiento=asiento
            rol.save()

        return HttpResponseRedirect('/contabilidad/asiento')

    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        rol = RolPago.objects.get(id=pk)
        mes=rol.mes
        quincena=rol.quincena
        anio=rol.anio
        print anio
        print 'entro'
        print mes

        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        clasificacion = ClasificacionCuenta.objects.order_by('orden')
        c=1

        cursor = connection.cursor();
        cursor.execute("select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=1 order by p.tipo_cuenta_id");
        row = cursor.fetchall();
        html=''
        #GRUPO 1 ADMINISTRATIVO

        if row:
            i=0
            grupo_pago=GrupoPago.objects.get(id=1)
            for p in row:
                cursor.execute("select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id="+str(p[0])+" and rpc.grupo_pago_id=1  and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                row2 = cursor.fetchall()
               


                if row2:
                   for d in row2:
                    debe=0
                    haber = 0
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    if d[2]:
                        
                        cursor.execute(
                            "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='"+str(mes)+"' and i.anio='"+str(anio)+"' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id="+ str(
                                d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=1");

                        ingresos = cursor.fetchall();
                        if p[3]< 3:
                            if ingresos[0][0]:

                                debe=debe+ingresos[0][0]
                        else:
                            if ingresos[0][0]:

                                haber=haber+ingresos[0][0]
                    if d[3]:
                        cursor.execute(
                            "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(mes) + "' and i.anio='" + str(
                                anio) + "'  and i.tipo_ingreso_egreso_empleado_id=" + str(
                                d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=1");
                        otrosingresos = cursor.fetchall();
                        if p[3]< 3:
                            if otrosingresos[0][0]:
                                debe=debe+otrosingresos[0][0]
                        else:
                            if otrosingresos[0][0]:
                                haber=haber+otrosingresos[0][0]



                    if d[4]:
                        cursor.execute(
                            "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(mes) + "' and i.anio='" + str(
                                anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=1");
                        egresos = cursor.fetchall();
                        # if p[3]< 3:
                        #     if egresos[0][0]:
                        #         debe = debe + egresos[0][0]
                        # else:
                        #     if egresos[0][0]:
                        #         haber = haber + egresos[0][0]
                        if egresos[0][0]:
                            haber = haber + egresos[0][0]



                    #     egresos= EgresosRolEmpleado.objects.filter(quincena=quincena).filter(anio=anio).filter(
                    # mes=mes).filter(tipo_ingreso_egreso_empleado_id=d[0]).aggregate(Sum('valor'))
                    #     if egresos['valor__sum']:
                    #         haber =haber+egresos['valor__sum']



                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(d[1].encode('utf8'))
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(debe)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(haber)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                    c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '" ></td>'
                    html+='</tr>'
                    c=c+1
                    i=i+1
                    
                if p[4]==32:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    #debe= ap
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(ap)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '" ></td>'
                    html+='</tr>'
                    c=c+1
                    i=i+1
                
                if p[4]==33:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    #debe= ap
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(ap)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '" ></td>'
                    html+='</tr>'
                    c=c+1
                    i=i+1
                    
                
                
                    
                
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    c=c+1
                    i=i+1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(fr)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'

                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(haber)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    i = i + 1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(dt)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'

                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(haber)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=1  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31c = cursor.fetchall()
                    decimo_cuarto=0
                    if row31c:
                        for d31c in row31c:
                            if d31c[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31c[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                        print 'Valor del decimo cuarto'
                        print decimo_cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    print dc
                    c=c+1
                    i = i + 1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(dc)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'

                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(haber)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    i = i + 1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="'+str(dt)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'

                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(haber)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                
                
                #PASIVO de administracion
                #SUELDO
                if p[4]==22:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    ingresos_total=0
                    if row31:
                        for d31 in row31:
                            ingresos_total=ingresos_total+d31[0]
                            
                            
                            
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row32 = cursor.fetchall()
                    egresos_total=0
                    if row32:
                        for d31 in row32:
                            egresos_total=egresos_total+d31[0]
                            
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row33 = cursor.fetchall()
                    otros_ingresos_total=0
                    if row31:
                        for d31 in row33:
                            otros_ingresos_total=otros_ingresos_total+d31[0]
                            
                    total=ingresos_total+otros_ingresos_total-egresos_total
                    total=round(float(total),2)
                    c=c+1
                    i=i+1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(total)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    c=c+1
                    i=i+1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(fr)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                
                
                
                
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    i = i + 1
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(dt)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html+= '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                if p[4]==28:
                    salario_base=rol.salario_base
                    
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=1  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31c = cursor.fetchall()
                    decimo_cuarto=0
                    if row31c:
                        for d31c in row31c:
                            if d31c[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31c[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                        
                            
                    dc=round(float(decimo_cuarto),2)
                    print dc
                    c=c+1
                    i = i + 1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(dc)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                    
                 #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=1 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    i = i + 1
                    html+='<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>'+str(p[1])+' '+ str(p[2])+'</td>'
                    html+='<td><input type="hidden" class="form-control" id="id_kitsc'+str(c)+'" name="id_kitsc'+str(c)+'" value="'+str(p[0])+'"/>'
                    concepto=''+str(grupo_pago.nombre)+' Cuenta '+str(p[1])+' '+str(p[5].encode('utf8'))
                
                    html+='<input type="text" class="form-control debe" id="debe_kitsc'+str(c)+'" name="debe_kitsc'+str(c)+'" value="0" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'

                    html+='<td><input type="text" class="form-control haber" id="haber_kitsc'+str(c)+'" name="haber_kitsc'+str(c)+'" value="'+str(dt)+'" onkeyup="actualizarValorCuenta('+str(i)+')" ></td>'
                    html += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto) + '/ACUMULADO" ></td>'
                    html+='</tr>'
                
                
                
                i=i+1
                c=c+1

        #GRUPO2 VENTAS
        cursor = connection.cursor();
        cursor.execute(
            "select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=2 order by p.tipo_cuenta_id");
        rowventas = cursor.fetchall();
        html2 = ''
        if rowventas:
            grupo_pago2 = GrupoPago.objects.get(id=2)
            j = 0
            for p in rowventas:
                
                cursor.execute(
                    "select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id=" + str(
                        p[0]) + " and rpc.grupo_pago_id=2 and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                rowventas2 = cursor.fetchall();
               


                if rowventas2:
                    for d in rowventas2:
                        debe_ventas = 0
                        haber_ventas = 0
                        html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                        html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                        if d[2]:
                            cursor.execute(
                                "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(mes) + "' and i.anio='" + str(
                                    anio) + "' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=2");
                            ingresos = cursor.fetchall();
                            if p[3] < 3:
                                if ingresos[0][0]:
                                    debe_ventas = debe_ventas + ingresos[0][0]
                            else:
                                if ingresos[0][0]:
                                    haber_ventas = haber_ventas + ingresos[0][0]


                        if d[3]:
                            cursor.execute(
                                "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=2");
                            otrosingresos = cursor.fetchall();
                            if p[3] < 3:
                                if otrosingresos[0][0]:
                                    debe_ventas = debe_ventas + otrosingresos[0][0]

                            else:
                                if otrosingresos[0][0]:
                                    haber_ventas = haber_ventas + otrosingresos[0][0]


                        if d[4]:
                            cursor.execute(
                                "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=2");
                            egresos = cursor.fetchall();
                            # if p[3] < 3:
                            #     if egresos[0][0]:
                            #         debe_ventas = debe_ventas + egresos[0][0]
                            # 
                            # else:
                            #     if egresos[0][0]:
                            #         haber_ventas = haber_ventas + egresos[0][0]
                            if egresos[0][0]:
                                haber_ventas = haber_ventas + egresos[0][0]

                    
                        html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(debe_ventas) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
        
                        html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                            haber_ventas) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                        concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(d[1].encode('utf8'))
                        html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                        html2 += '</tr>'
                        c=c+1
                        j = j + 1
                if p[4]==32:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                                    
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
        
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                    c=c+1
                    j = j + 1
                
                if p[4]==33:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                                    
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
        
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str( c) + '" name="haber_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                    c=c+1
                    j = j + 1
                    
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    debe=debe+ fr
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))

                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_ventas) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '/ACUMULADO" ></td>'
                    html2 += '</tr>'
                
                
                
                 #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_ventas) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=2  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_ventas) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                    
                
                 #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_ventas) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                 
                 
                 
                 
                #PASIVO
                
                if p[4]==22:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    ingresos_v=0
                    if row31:
                        for d31 in row31:
                            ingresos_v=ingresos_v+d31[0]
                            
                        
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row32 = cursor.fetchall()
                    egresos_v=0
                    if row32:
                        for d31 in row32:
                            egresos_v=egresos_v+d31[0]
                            
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row33 = cursor.fetchall()
                    oingresos_v=0
                    if row33:
                        for d31 in row33:
                            oingresos_v=oingresos_v+d31[0]
                            
                   
                    total_v=ingresos_v-egresos_v+oingresos_v
                    total_v=round(float(total_v),2)
                    
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'

                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(total_v) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '/ACUMULADO" ></td>'
                    html2 += '</tr>'
                
                
                
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    debe=debe+ fr
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'

                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '/ACUMULADO" ></td>'
                    html2 += '</tr>'
                
                
                
                 #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '/ACUMULADO" ></td>'
                    html2 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==28:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=2  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '" ></td>'
                    html2 += '</tr>'
                
                 #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=2 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html2 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html2 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    concepto2 = '' + str(grupo_pago2.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html2 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(j) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html2 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto2) + '/ACUMULADO" ></td>'
                    html2 += '</tr>'
                 
                 
                 
                   
                j = j + 1
                c=c+1

        #GRUPO 3 
        cursor = connection.cursor();
        cursor.execute(
            "select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=3 order by p.tipo_cuenta_id");
        rowotros_costos = cursor.fetchall();
        html3 = ''
        if rowotros_costos:
            grupo_pago3 = GrupoPago.objects.get(id=3)
            j = 0
            for p in rowotros_costos:
               
                cursor.execute(
                    "select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id=" + str(
                        p[0]) + " and rpc.grupo_pago_id=3 and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                row3 = cursor.fetchall();
                

                if row3:
                    for d in row3:
                        debe_otros_produc = 0
                        haber_otros_produc = 0
                        html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                        html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                        if d[2]:
                            cursor.execute(
                                "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=3");
                            ingresos = cursor.fetchall();
                            if p[3] < 3:
                                if ingresos[0][0]:
                                    debe_otros_produc = debe_otros_produc + ingresos[0][0]
                            else:
                                if ingresos[0][0]:
                                    haber_otros_produc = haber_otros_produc + ingresos[0][0]

                        if d[3]:
                            cursor.execute(
                                "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=3");
                            otrosingresos = cursor.fetchall();
                            if p[3] < 3:
                                if otrosingresos[0][0]:
                                    debe_otros_produc = debe_otros_produc + otrosingresos[0][0]

                            else:
                                if otrosingresos[0][0]:
                                    haber_otros_produc = haber_otros_produc + otrosingresos[0][0]

                        if d[4]:
                            cursor.execute(
                                "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=3");
                            egresos = cursor.fetchall();
                            # if p[3] < 3:
                            #     if egresos[0][0]:
                            #         debe_otros_produc = debe_otros_produc + egresos[0][0]
                            # 
                            # else:
                            #     if egresos[0][0]:
                            #         haber_otros_produc = haber_otros_produc + egresos[0][0]
                            if egresos[0][0]:
                                haber_otros_produc = haber_otros_produc + egresos[0][0]

                        html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(debe_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
        
                        html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                            haber_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                        concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(d[1].encode('utf8'))
                        html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '" ></td>'
                        html3 += '</tr>'
                        c=c+1
                        j = j + 1
                        
                if p[4]==32:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            if d3[0]:
                                aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_otros_produc=debe_otros_produc+ ap
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                        c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
    
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                        c) + '" name="haber_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '" ></td>'
                    html3 += '</tr>'
                    c=c+1
                    j = j + 1
                
                if p[4]==33:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            if d3[0]:
                                aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_otros_produc=debe_otros_produc+ ap
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                        c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
    
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                        c) + '" name="haber_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                        c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '" ></td>'
                    html3 += '</tr>'
                    c=c+1
                    j = j + 1
                    
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                    c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                decimo_tercero=decimo_tercero+d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                    c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=3  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                if d31[3]:
                                    dcuarto = round(float(salario_base / 12), 2)
                                    dias_trabajados=d31[3]/8
                                    
                                    dias_trabajados=30-dias_trabajados
                                    
                                    mes_t=dias_trabajados/30
                                    total_anios=mes_t*12
                                    cuarto=(cuarto*total_anios)/12
                                    decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                    
                
                
                #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                    c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_otros_produc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                
                
                
                #PASIVO
                if p[4]==22:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    ingresos_ot=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                ingresos_ot=ingresos_ot+d31[0]
                    
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row32 = cursor.fetchall()
                    egresos_ot=0
                    if row32:
                        for d31 in row32:
                            if d31[0]:
                                egresos_ot=egresos_ot+d31[0]
                            
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row33 = cursor.fetchall()
                    oingresos_ot=0
                    
                    if row33:
                        for d31 in row33:
                            if d31[0]:
                                oingresos_ot=oingresos_ot+d31[0]
                            
                    total_ot=ingresos_ot+oingresos_ot-egresos_ot
                    total_ot=round(float(total_ot),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(total_ot) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                decimo_tercero=decimo_tercero+d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==28:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=3  and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                if d31[3]:
                                    dcuarto = round(float(salario_base / 12), 2)
                                    dias_trabajados=d31[3]/8
                                    
                                    dias_trabajados=30-dias_trabajados
                                    
                                    mes_t=dias_trabajados/30
                                    total_anios=mes_t*12
                                    cuarto=(cuarto*total_anios)/12
                                    decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                    
                
                
                
                
                
                #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=3 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            if d31[0]:
                                vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html3 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html3 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html3 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto3 = '' + str(grupo_pago3.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html3 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html3 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto3) + '/ACUMULADO" ></td>'
                    html3 += '</tr>'
                    
                j = j + 1
                c=c+1

        cursor = connection.cursor();
        cursor.execute(
            "select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=4 order by p.tipo_cuenta_id");
        rowotros = cursor.fetchall();
        html4 = ''
        if rowotros:
            j = 0
            grupo_pago4 = GrupoPago.objects.get(id=4)
            for p in rowotros:
                
                cursor.execute(
                    "select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id=" + str(
                        p[0]) + " and rpc.grupo_pago_id=4  and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                row4 = cursor.fetchall();
                

                if row4:
                    for d in row4:
                        debe_otros= 0
                        haber_otros = 0
                        html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                        html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                        if d[2]:
                            cursor.execute(
                                "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=4");
                            ingresos = cursor.fetchall();
                            if p[3] < 3:
                                if ingresos[0][0]:
                                    debe_otros = debe_otros + ingresos[0][0]
                            else:
                                if ingresos[0][0]:
                                    haber_otros = haber_otros + ingresos[0][0]

                        if d[3]:
                            cursor.execute(
                                "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "'  and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=4");
                            otrosingresos = cursor.fetchall();
                            if p[3] < 3:
                                if otrosingresos[0][0]:
                                    debe_otros = debe_otros + otrosingresos[0][0]

                            else:
                                if otrosingresos[0][0]:
                                    haber_otros= haber_otros + otrosingresos[0][0]

                        if d[4]:
                            cursor.execute(
                                "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=4");
                            egresos = cursor.fetchall();
                            # if p[3] < 3:
                            #     if egresos[0][0]:
                            #         debe_otros = debe_otros + egresos[0][0]
                            # 
                            # else:
                            #     if egresos[0][0]:
                            #         haber_otros = haber_otros + egresos[0][0]
                            if egresos[0][0]:
                                haber_otros = haber_otros + egresos[0][0]

                        html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(debe_otros) + '" onkeyup="actualizarValorCuenta(' + str(
                            c) + ')" ></td>'
        
                        html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                            haber_otros) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                        concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(d[1].encode('utf8'))
                        html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '" ></td>'
                        html4 += '</tr>'
        
        
                if p[4]==32:
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_otros=debe_otros+ ap
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
    
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
    
    
    
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '" ></td>'
                    html4 += '</tr>'
                
                if p[4]==33:
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_otros=debe_otros+ ap
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))

                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '" ></td>'
                    html4 += '</tr>'
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(
                    c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_otros) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                
                
                 #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_otros) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    
                    html4 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=4 and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_otros) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                    
                
                 #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_otros) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                
                
                
                #PASIVO
                if p[4]==22:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    ingresos_u=0
                    if row31:
                        for d31 in row31:
                            ingresos_u=ingresos_u+d31[0]
                            
                    
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row32 = cursor.fetchall()
                    egresos_u=0
                    if row32:
                        for d31 in row32:
                            egresos_u=egresos_u+d31[0]
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row31 = cursor.fetchall()
                    oingresos_u=0
                    if row31:
                        for d31 in row31:
                            oingresos_u=oingresos_u+d31[0]
                            
                    total_u=ingresos_u+oingresos_u-egresos_u
                    total_u=round(float(total_u),2)
                    
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(
                    c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(total_u) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                
                
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(
                    p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                    c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(
                    c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                    c) + '" name="haber_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                
                
                 #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                if p[4]==28:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=4 and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                    
                
                  
                
                 #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=4 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html4 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html4 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html4 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html4 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto4 = '' + str(grupo_pago4.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html4 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto4) + '/ACUMULADO" ></td>'
                    html4 += '</tr>'
                
                j = j + 1
                
                c=c+1

        cursor = connection.cursor();
        cursor.execute(
            "select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=5 order by p.tipo_cuenta_id");
        row_mano_directa = cursor.fetchall();
        html5 = ''
        if row_mano_directa:
            j = 0
            grupo_pago5 = GrupoPago.objects.get(id=5)
            for p in row_mano_directa:
                
                cursor.execute(
                    "select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id=" + str(
                        p[0]) + " and rpc.grupo_pago_id=5 and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                row5 = cursor.fetchall();
                

                if row5:
                    for d in row5:
                        debe_mano_directa = 0
                        haber_mano_directa = 0
                        html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                        html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                        if d[2]:
                            cursor.execute(
                                "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=5");
                            ingresos = cursor.fetchall();
                            if p[3] < 3:
                                if ingresos[0][0]:
                                    debe_mano_directa = debe_mano_directa + ingresos[0][0]
                            else:
                                if ingresos[0][0]:
                                    haber_mano_directa = haber_mano_directa + ingresos[0][0]

                        if d[3]:
                            cursor.execute(
                                "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "'  and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=5");
                            otrosingresos = cursor.fetchall();
                            if p[3] < 3:
                                if otrosingresos[0][0]:
                                    debe_mano_directa = debe_mano_directa + otrosingresos[0][0]

                            else:
                                if otrosingresos[0][0]:
                                    haber_mano_directa = haber_mano_directa + otrosingresos[0][0]

                        if d[4]:
                            cursor.execute(
                                "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=5");
                            egresos = cursor.fetchall();
                            # if p[3] < 3:
                            #     if egresos[0][0]:
                            #         debe_mano_directa = debe_mano_directa + egresos[0][0]
                            # 
                            # else:
                            #     if egresos[0][0]:
                            #         haber_mano_directa = haber_mano_directa + egresos[0][0]
                            if egresos[0][0]:
                                haber_mano_directa = haber_mano_directa + egresos[0][0]
                        html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(debe_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(
                            c) + ')" ></td>'
        
                        html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                            haber_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                        
        
                        concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(d[1].encode('utf8'))
                        html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '" ></td>'
                        html5 += '</tr>'
                        c=c+1
                        j = j + 1
                        
                if p[4]==32:
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_mano_directa=debe_mano_directa+ ap
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                        c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(
                        c) + ')" ></td>'
    
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                        c) + '" name="haber_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
    
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '" ></td>'
                    html5 += '</tr>'
                    c=c+1
                    j = j + 1
                
                if p[4]==33:
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    #debe_mano_directa=debe_mano_directa+ ap
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '" ></td>'
                    html5 += '</tr>'
                    c=c+1
                    j = j + 1
                    
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=5 and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    haber_mano_directa) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                #PASIVO
                
                if p[4]==22:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    ingresosx=0
                    if row31:
                        for d31 in row31:
                            ingresosx=ingresosx+d31[0]
                    
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    egresosx=0
                    if row31:
                        for d31 in row31:
                            egresosx=egresosx+d31[0]
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row32 = cursor.fetchall()
                    oingresosx=0
                    if row32:
                        for d31 in row32:
                            oingresosx=oingresosx+d31[0]
                            
                    totalx=ingresosx+oingresosx-egresosx
                    totalx=round(float(totalx),2)
                    
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    totalx) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==28:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=5 and e.acumular_decimo_cuarto is not True and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                
                
                #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=5 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html5 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html5 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html5 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html5 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                    dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto5 = '' + str(grupo_pago5.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html5 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto5) + '/ACUMULADO" ></td>'
                    html5 += '</tr>'
                
                
                
                
                
                j = j + 1
                c=c+1

        #MANO DE OBRA INDIRECTA

        cursor = connection.cursor();
        cursor.execute(
            "select distinct rpc.plandecuentas_id,p.codigo_plan,p.nombre_plan,p.tipo_cuenta_id,rpc.rol_cuentacontable_items_id,rpc.clave from  rol_pago_cuenta_contable rpc,contabilidad_plandecuentas p where rpc.plandecuentas_id=p.plan_id and  rpc.grupo_pago_id=6 order by p.tipo_cuenta_id");
        row_mano_indirecta = cursor.fetchall();
        html6 = ''
        if row_mano_indirecta:
            grupo_pago6 = GrupoPago.objects.get(id=6)
            j = 0
            for p in row_mano_indirecta:
                
                cursor.execute(
                    "select tie.id,tie.nombre,tie.ingreso,tie.otros_ingresos,tie.egreso  from rol_pago_cuenta_contable rpc,rol_cuentacontable_tipoingresoegreso t, tipo_ingreso_egreso_empleado tie where rpc.rol_cuentacontable_items_id=t.rol_cuentacontable_items_id and t.tipo_ingreso_egreso_empleado_id=tie.id and rpc.plandecuentas_id=" + str(
                        p[0]) + " and rpc.grupo_pago_id=6 and rpc.rol_cuentacontable_items_id="+str(p[4])+"");
                row6 = cursor.fetchall();
                

                if row6:
                    for d in row6:
                        debe_mano_indirecta = 0
                        haber_mano_indirecta = 0
                        html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                        html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                        if d[2]:
                            cursor.execute(
                                "select  sum(i.valor) from ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.pagar=True and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + " and e.empleado_id=i.empleado_id and e.grupo_pago_id=6");
                            ingresos = cursor.fetchall();
                            if p[3] <3 :
                                if ingresos[0][0]:
                                    debe_mano_indirecta = debe_mano_indirecta + ingresos[0][0]
                            else:
                                if ingresos[0][0]:
                                    haber_mano_indirecta = haber_mano_indirecta + ingresos[0][0]

                        if d[3]:
                            cursor.execute(
                                "select  sum(i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "'  and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=6");
                            otrosingresos = cursor.fetchall();
                            if otrosingresos[0][0]:
                                debe_mano_indirecta = debe_mano_indirecta + otrosingresos[0][0]
                                

                            
                        if d[4]:
                            cursor.execute(
                                "select  sum(i.valor) from egresos_rol_empleado i,empleados_empleado e where i.mes='" + str(
                                    mes) + "' and i.anio='" + str(
                                    anio) + "' and i.tipo_ingreso_egreso_empleado_id=" + str(
                                    d[0]) + "and e.empleado_id=i.empleado_id and e.grupo_pago_id=6");
                            egresos = cursor.fetchall();
                            # if p[3] < 3:
                            #     if egresos[0][0]:
                            #         debe_mano_indirecta = debe_mano_indirecta + egresos[0][0]
                            # 
                            # else:
                            #     if egresos[0][0]:
                            #         haber_mano_indirecta = haber_mano_indirecta + egresos[0][0]
                            if egresos[0][0]:
                                haber_mano_indirecta = haber_mano_indirecta + egresos[0][0]

                #html6+= 'tipo:'+str(p[3])
                        html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(
                            c) + '" value="' + str(debe_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(
                            c) + ')" ></td>'
        
                        html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(
                            c) + '" name="haber_kitsc' + str(c) + '" value="' + str(
                            haber_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                        concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(d[1].encode('utf8'))
                        html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '" ></td>'
                        html6 += '</tr>'
                        c=c+1
                        j = j + 1
                if p[4]==32:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
        
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '" ></td>'
                    html6 += '</tr>'
                        
                    c=c+1
                    j = j + 1
                
                if p[4]==33:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"")
                    row3 = cursor.fetchall()
                    aporte_iess=0
                    if row3:
                        for d3 in row3:
                            aporte_iess=aporte_iess+d3[0]
                            
                    ap=aporte_iess*0.1215
                    ap=round(float(ap),2)
                    
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
        
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(ap) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(
                            c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '" ></td>'
                    html6 += '</tr>'
                        
                    c=c+1
                    j = j + 1
                    
                if p[4]==25:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==23:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                    
                #PROVISION DE DECIMO CUARTO
                
                if p[4]==24:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=6 and e.acumular_decimo_cuarto is not True  and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                #PROVISION DE VACACIONES
                if p[4]==26:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(haber_mano_indirecta) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                #PASIVO MI
                #PASIVO
                
                if p[4]==22:
                    
                    
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    ingresosx=0
                    if row31:
                        for d31 in row31:
                            ingresosx=ingresosx+d31[0]
                    
                    cursor.execute("select  sum (i.valor) from egresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    egresosx=0
                    if row31:
                        for d31 in row31:
                            egresosx=egresosx+d31[0]
                            
                    cursor.execute("select  sum (i.valor) from otros_ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row32 = cursor.fetchall()
                    oingresosx=0
                    if row32:
                        for d31 in row32:
                            oingresosx=oingresosx+d31[0]
                            
                    totalx=ingresosx+oingresosx-egresosx
                    totalx=round(float(totalx),2)
                    
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(totalx) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                    
                   
                
                
                
                if p[4]==29:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_fondo_reserva is not True")
                    
                    row31 = cursor.fetchall()
                    fondo_reserva=0
                    if row31:
                        for d31 in row31:
                            fondo_reserva=fondo_reserva+d31[0]
                            
                    fr=fondo_reserva/12
                    fr=round(float(fr),2)
                    
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(fr) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                
                
                #PROVISION DE DECIMO TERCERO
                if p[4]==27:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" and e.acumular_decimo_tercero is not True")
                    
                    row31 = cursor.fetchall()
                    decimo_tercero=0
                    if row31:
                        for d31 in row31:
                            decimo_tercero=d31[0]
                            
                    dt=decimo_tercero/12
                    dt=round(float(dt),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                    
                #PROVISION DE DECIMO CUARTO
                if p[4]==28:
                    salario_base=rol.salario_base
                    cuarto = round(float(salario_base / 12), 2)
                    cursor.execute(" select  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida, sum(i.dias) from empleados_empleado e left join dias_no_laborados_rol_empleado i on e.empleado_id=i.empleado_id and i.anio='"+str(anio)+"' and i.mes="+str(mes)+"  where e.grupo_pago_id=6 and e.acumular_decimo_cuarto is not True  and e.empleado_id in (select df.empleado_id from rol_pago_detalle df where df.rol_pago_id="+str(pk)+") group by  e.empleado_id,e.tipo_remuneracion_id,e.fecha_ini_reconocida")
                    row31 = cursor.fetchall()
                    decimo_cuarto=0
                    if row31:
                        for d31 in row31:
                            if d31[1] == 2:
                                cuarto = round(float(salario_base / 12), 2)
                                dias_trabajados=d31[3]/8
                                
                                dias_trabajados=30-dias_trabajados
                                
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                cuarto=(cuarto*total_anios)/12
                                decimo_cuarto=decimo_cuarto+cuarto
                            else:
                                cuarto = round(float(salario_base / 12), 2)
                                decimo_cuarto=decimo_cuarto+cuarto
                            
                            
                    dc=round(float(decimo_cuarto),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dc) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                
                
                #PROVISION DE VACACIONES
                if p[4]==30:
                    cursor.execute("select  sum (i.valor) from ingresos_rol_empleado i,empleados_empleado e where e.empleado_id=i.empleado_id and e.grupo_pago_id=6 and i.anio='"+str(anio)+"' and i.mes="+str(mes)+" ")
                    
                    row31 = cursor.fetchall()
                    vacaciones=0
                    if row31:
                        for d31 in row31:
                            vacaciones=vacaciones+d31[0]
                            
                    vacaciones=vacaciones/24
                    dt=round(float(vacaciones),2)
                    c=c+1
                    j = j + 1
                    html6 += '<tr><td class="eliminar"><a class="btn btn-danger remove_fields"> <i class=" glyphicon glyphicon-trash icon-white"></i></a></td><td>' + str(p[1]) + ' ' + str(p[2]) + '</td>'
                    html6 += '<td><input type="hidden" class="form-control" id="id_kitsc' + str(c) + '" name="id_kitsc' + str(c) + '" value="' + str(p[0]) + '"/>'
                    html6 += '<input type="text" class="form-control debe" id="debe_kitsc' + str(c) + '" name="debe_kitsc' + str(c) + '" value="0" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    html6 += '<td><input type="text" class="form-control haber" id="haber_kitsc' + str(c) + '" name="haber_kitsc' + str(c) + '" value="' + str(dt) + '" onkeyup="actualizarValorCuenta(' + str(c) + ')" ></td>'
                    concepto6 = '' + str(grupo_pago6.nombre) + ' Cuenta ' + str(p[1]) + ' ' + str(p[5].encode('utf8'))
                    html6 += '<td><input type="text" class="form-control" id="concepto_kitsc' + str(c) + '" name="concepto_kitsc' + str(c) + '" value="' + str(concepto6) + '/ACUMULADO" ></td>'
                    html6 += '</tr>'
                
                
                j = j + 1
                c=c+1


        return render_to_response('roles_pago/contabilizacion_rol_pago.html', {'rol_cuentas': rol_cuentas,
                                                            'roles_pago': roles_pago, 'html': html,'html2': html2,'html3': html3,'html4': html4,'html5': html5,'html6': html6,

                                                            'sueldos_unificados': sueldos_unificados,'contador':c}, RequestContext(request))




@login_required()
def RolesPagoItemsTipoIngresoEgresoListView(request):
    if request.method == 'POST':
        rol_cuentas = RolCuentacontableTipoingresoegreso.objects.all()
        return render_to_response('cuenta_contable_tipo_ingreso_egreso/index.html', {'row': rol_cuentas},
                                  RequestContext(request))
    else:
        rol_cuentas = RolCuentacontableTipoingresoegreso.objects.all()
        return render_to_response('cuenta_contable_tipo_ingreso_egreso/index.html', {'row': rol_cuentas},
                                  RequestContext(request))

class RolesPagoItemsTipoIngresoEgresoCreateView(ObjectCreateView):
    model = RolCuentacontableTipoingresoegreso
    form_class = RolCuentacontableTipoingresoegresoForm
    template_name = 'cuenta_contable_tipo_ingreso_egreso/nuevo.html'
    url_success = 'roles-pago-cuentas-contables-tipo-ingreso-egreso-list'
    url_success_other = 'roles-pago-cuentas-contables-tipo-ingreso-egreso-create'
    url_cancel = 'roles-pago-cuentas-contables-tipo-ingreso-egreso-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(RolesPagoItemsTipoIngresoEgresoCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nueva cuenta."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)



@login_required()
def RolesPagoItemsTipoIngresoEgresoUpdateView(request, pk):
    if request.method == 'POST':
        prestamo = RolCuentacontableTipoingresoegreso.objects.get(id=pk)
        form = RolCuentacontableTipoingresoegresoForm(request.POST, request.FILES, instance=prestamo)
        print form.is_valid(), form.errors, type(form.errors)

        if form.is_valid():
            new_orden = form.save()
            new_orden.save()
            context = {
                'section_title': 'Actualizar Orden Egreso',
                'button_text': 'Actualizar',
                'form': form}
            return render_to_response(
                'cuenta_contable_tipo_ingreso_egreso/nuevo.html',
                context,
                context_instance=RequestContext(request))
        else:
            form = RolCuentacontableTipoingresoegresoForm(request.POST)
            context = {
                'section_title': 'Actualizar',
                'button_text': 'Actualizar',
                'form': form}

            return render_to_response(
                'cuenta_contable_tipo_ingreso_egreso/nuevo.html',
                context,
                context_instance=RequestContext(request))
    else:
        prestamo = RolCuentacontableTipoingresoegreso.objects.get(id=pk)
        form = RolCuentacontableTipoingresoegresoForm(instance=prestamo)
        context = {
            'section_title': 'Actualizar',
            'button_text': 'Actualizar',
            'form': form}

        return render_to_response(
            'cuenta_contable_tipo_ingreso_egreso/nuevo.html',
            context,
            context_instance=RequestContext(request))



@login_required()
@csrf_exempt
def eliminarPlantilla(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        detalle = PlantillaRrhh.objects.get(id=id)
        ar = detalle.id
        try:
            rol = RolPagoPlantilla.objects.get(plantilla_rrhh_id=id)
        except RolPagoPlantilla.DoesNotExist:
            rol = None

        if rol:
            mensaje='No se puede eliminar esta plantilla'
        else:
            kits = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=ar)

            for obj in kits:
                obj.delete()

            detalle.delete()
            mensaje = 'Se elimino la plantilla satisfactoriamente'
        return HttpResponse(
            mensaje

        )
    else:
        plantillas = PlantillaRrhh.objects.order_by('id')

        return render_to_response('plantillas/index.html', {'plantillas': plantillas,}, RequestContext(request))


@login_required()
def quitarPlantillasRol(request):
    if request.method == 'POST':
        plantillas = request.POST["selected"]
        my_list = plantillas.split(",")
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        for r in my_list:
            print('valoor' + str(r))
            if r > 0:
                try:
                    plantillas_detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=r)
                except PlantillaRrhhDetalle.DoesNotExist:
                    plantillas_detalle = None

                if plantillas_detalle:
                    try:
                        rol_pago = RolPagoPlantilla.objects.filter(plantilla_rrhh_id=r).filter(mes=mes).filter(anio=anio).filter(quincena=quincena)
                    except RolPagoPlantilla.DoesNotExist:
                        rol_pago = None
                    if rol_pago:
                        print('existe')


                        for pd in plantillas_detalle:
                            if pd.tipo_ingreso_egreso_empleado.ingreso:
                                try:
                                    ingreso = IngresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(empleado_id=pd.empleado_id).filter(tipo_ingreso_egreso_empleado_id= pd.tipo_ingreso_egreso_empleado_id).filter(valor=pd.valor).order_by('-id')[0]
                                except IngresosRolEmpleado.DoesNotExist:
                                    ingreso = None

                                if ingreso:
                                    ingreso.delete()
                            if pd.tipo_ingreso_egreso_empleado.otros_ingresos:
                                try:
                                    otros_ingreso = OtrosIngresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(empleado_id=pd.empleado_id).filter(tipo_ingreso_egreso_empleado_id= pd.tipo_ingreso_egreso_empleado_id).filter(valor=pd.valor).order_by('-id')[0]
                                except OtrosIngresosRolEmpleado.DoesNotExist:
                                    otros_ingreso = None
                                if otros_ingreso:
                                    otros_ingreso.delete()

                            if pd.tipo_ingreso_egreso_empleado.egreso:
                                try:
                                    egreso = EgresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(empleado_id=pd.empleado_id).filter(tipo_ingreso_egreso_empleado_id= pd.tipo_ingreso_egreso_empleado_id).filter(valor=pd.valor).order_by('-id')[0]
                                except EgresosRolEmpleado.DoesNotExist:
                                    egreso = None
                                if egreso:
                                    egreso.delete()

                            if pd.tipo_ingreso_egreso_empleado.otros_egresos:
                                try:
                                    otros_egreso = OtrosEgresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(empleado_id=pd.empleado_id).filter(tipo_ingreso_egreso_empleado_id= pd.tipo_ingreso_egreso_empleado_id).filter(valor=pd.valor).order_by('-id')[0]
                                except OtrosEgresosRolEmpleado.DoesNotExist:
                                    otros_egreso = None
                                if otros_egreso:
                                    otros_egreso.delete()
                        rol_pago.delete()


                    html = 'Se elimino satisfactoriamente'
                else:
                    html = 'Error durante la ejecucion'

            return HttpResponse(
                html
            )
    else:
        plantillas = request.POST["selected"]
        my_list = plantillas.split(",")
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        quincena = request.POST["quincena"]
        for r in my_list:
            print('vaalor' + str(r))
            if r > 0:
                try:
                    plantillas_detalle = PlantillaRrhhDetalle.objects.filter(plantilla_rrhh_id=r)
                except PlantillaRrhhDetalle.DoesNotExist:
                    plantillas_detalle = None

                if plantillas_detalle:
                    try:
                        rol_pago = RolPagoPlantilla.objects.filter(plantilla_rrhh_id=r).filter(mes=mes).filter(
                            anio=anio).filter(quincena=quincena)
                    except RolPagoPlantilla.DoesNotExist:
                        rol_pago = None
                    if rol_pago:
                        print('existe')

                        for pd in plantillas_detalle:
                            if pd.tipo_ingreso_egreso_empleado.ingreso:
                                try:
                                    ingreso = IngresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(
                                        empleado_id=pd.empleado_id).filter(
                                        tipo_ingreso_egreso_empleado_id=pd.tipo_ingreso_egreso_empleado_id).filter(
                                        valor=pd.valor).order_by('-id')[0]
                                except IngresosRolEmpleado.DoesNotExist:
                                    ingreso = None

                                if ingreso:
                                    ingreso.delete()
                            if pd.tipo_ingreso_egreso_empleado.otros_ingresos:
                                try:
                                    otros_ingreso = OtrosIngresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(
                                        empleado_id=pd.empleado_id).filter(
                                        tipo_ingreso_egreso_empleado_id=pd.tipo_ingreso_egreso_empleado_id).filter(
                                        valor=pd.valor).order_by('-id')[0]
                                except OtrosIngresosRolEmpleado.DoesNotExist:
                                    otros_ingreso = None
                                if otros_ingreso:
                                    otros_ingreso.delete()

                            if pd.tipo_ingreso_egreso_empleado.egreso:
                                try:
                                    egreso = EgresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(
                                        empleado_id=pd.empleado_id).filter(
                                        tipo_ingreso_egreso_empleado_id=pd.tipo_ingreso_egreso_empleado_id).filter(
                                        valor=pd.valor).order_by('-id')[0]
                                except EgresosRolEmpleado.DoesNotExist:
                                    egreso = None
                                if egreso:
                                    egreso.delete()

                            if pd.tipo_ingreso_egreso_empleado.otros_egresos:
                                try:
                                    otros_egreso = OtrosEgresosRolEmpleado.objects.filter(plantilla_rrhh_id=r).filter(
                                        mes=mes).filter(anio=anio).filter(quincena=quincena).filter(
                                        empleado_id=pd.empleado_id).filter(
                                        tipo_ingreso_egreso_empleado_id=pd.tipo_ingreso_egreso_empleado_id).filter(
                                        valor=pd.valor).order_by('-id')[0]
                                except OtrosEgresosRolEmpleado.DoesNotExist:
                                    otros_egreso = None
                                if otros_egreso:
                                    otros_egreso.delete()
                        rol_pago.delete()

                    html = 'Se elimino satisfactoriamente'
                else:
                    html = 'Error durante la ejecucion'

        return HttpResponse(
            html
        )

#FUNCION QUE OBTIENE EL ROL DE PAGO PARA GENERARLO
@login_required()
@csrf_exempt
def obtenerEmpleadosMensual(request):
    if request.method == 'POST':
        empleados = Empleado.objects.filter(activo=True).order_by('nombre_empleado')
        tipopago = TipoPago.objects.all()
        formapago = FormaPagoEmpleado.objects.all()
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        otros_egresos_esposa = 0
        error=''

        try:
            rol = RolPago.objects.get(anio=anio, mes=mes)
        except RolPago.DoesNotExist:
            rol = None

        if rol:
            html += '<tr><td colspan="8"><h3>Ya se genero ese rol. Puede revisarlo en la opcion de Consultar Rol de Pago.</h3></td></tr>'
        else:
            for detal in empleados:
                i += 1
                ingresosPro = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
                #Calculo de los dias trabajados por retiro de la empres
                if detal.fecha_fin:
                    try:
                        sueldo0 = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                 empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)
                    except IngresosRolEmpleado.DoesNotExist:
                        #sueldo0 = 0
                        sueldo0 = ingresosPro[0]
                    formato_fecha = "%d-%m-%Y"
                    fecha_comparar="30-"+mes+"-"+anio
                    
                    fecha_fin_contrato = detal.fecha_fin
                    fecha_comparar_modif=date(int(anio), int(mes), 30)
                    
                    if fecha_fin_contrato:
                        diferencia=fecha_fin_contrato-fecha_comparar_modif
                    if diferencia:
                        
                        diferencia=diferencia.days* (-1)*8
                        try:
                            dias_no_t = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ausencia_id=7)
                        except DiasNoLaboradosRolEmpleado.DoesNotExist:
                            dias_no_t = None
                        
                        if dias_no_t:
                            print "s"
                        else:
                            valor2 = (sueldo0.valor_mensual / 240) * int(diferencia)
                            dias = DiasNoLaboradosRolEmpleado()
                            dias.anio = anio
                            dias.mes = mes
                            dias.empleado_id = detal.empleado_id
                            dias.dias = int(diferencia)
                            dias.tipo_ausencia_id = 7
                            dias.valor = round(float(valor2), 2)
                            dias.descontar = True
                            dias.cargar_vacaciones = True
                            dias.created_by = request.user.get_full_name()
                            dias.updated_by = request.user.get_full_name()
                            dias.created_at = datetime.now()
                            dias.updated_at = datetime.now()
                            dias.save()
                            
                    
                
                if detal.tipo_remuneracion_id == 2:
                    print "entro a tipo de renumeracion 2"
                    try:
                        sueldo0 = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                 empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)
                    except IngresosRolEmpleado.DoesNotExist:
                        #sueldo0 = 0
                        sueldo0 = ingresosPro[0]
                    periodo_trabajo=float(detal.horas_trabajo_mensual)
                    dias_parcial=(periodo_trabajo*4)
                    dias_total_no_trabajado=240-periodo_trabajo
                    print periodo_trabajo
                    sueldo_hora=sueldo0.valor_mensual/240
                    sueldo_parcial=sueldo_hora*periodo_trabajo
                    sueldo_fparcial=sueldo0.valor_mensual-sueldo_parcial
                    
                    try:
                        dias_par= DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ausencia_id=8)
                    except DiasNoLaboradosRolEmpleado.DoesNotExist:
                        dias_par = None
                        
                    if dias_par:
                        print "ya tienen esos dias parciales"
                    else:
                        dias = DiasNoLaboradosRolEmpleado()
                        dias.anio = anio
                        dias.mes = mes
                        dias.empleado_id = detal.empleado_id
                        dias.dias = int(dias_total_no_trabajado)
                        dias.tipo_ausencia_id = 8
                        dias.valor = round(float(sueldo_fparcial), 2)
                        dias.descontar = True
                        dias.cargar_vacaciones = True
                        dias.motivo = ''
                        dias.created_by = request.user.get_full_name()
                        dias.updated_by = request.user.get_full_name()
                        dias.created_at = datetime.now()
                        dias.updated_at = datetime.now()
                        dias.save()
                            
                        
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
                faltas_ingreso_egreso_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('valor'))

                vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
                dias_parciales_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=8).aggregate(Sum('valor'))
            

                descont_dias=0
                if faltas_injustificadas_valor['valor__sum']:
                    descont_dias = faltas_injustificadas_valor['valor__sum']
                
                if faltas_ingreso_egreso_valor['valor__sum']:
                    descont_dias = descont_dias+faltas_ingreso_egreso_valor['valor__sum']

                if vacaciones_justificadas_valor['valor__sum']:
                    descont_dias = descont_dias + vacaciones_justificadas_valor['valor__sum']
                
                if dias_parciales_valor['valor__sum']:
                    print 'valor dde dias parciales'+str(dias_parciales_valor['valor__sum'])
                    descont_dias = descont_dias + dias_parciales_valor['valor__sum']
                print 'descontar dias '+str(descont_dias)

                if ingresosPro:
                    for detali in ingresosPro:
                        try:
                            existe = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                     empleado_id=detal.empleado_id,
                                                                     tipo_ingreso_egreso_empleado_id=detali.tipo_ingreso_egreso_empleado_id,
                                                                     ingresos_proyectados=True)
                        except IngresosRolEmpleado.DoesNotExist:
                            existe = None

                        if existe:
                            print 'existe '


                            existe.valor = round(float(detali.valor_mensual-descont_dias), 2)
                            existe.valor_diario = round(float(detali.valor_diario), 2)
                            existe.valor_mensual = round(float(detali.valor_mensual), 2)
                            existe.nombre = detali.tipo_ingreso_egreso_empleado.nombre
                            existe.updated_by = request.user.get_full_name()
                            existe.updated_at = datetime.now()
                            existe.save()
                            #print ("sueldo es igual final="+str(existe.valor))
                        else:
                            existeNew = IngresosRolEmpleado()
                            existeNew.anio = anio
                            existeNew.mes = mes
                            existeNew.empleado_id = detal.empleado_id
                            existeNew.nombre = detali.tipo_ingreso_egreso_empleado
                            existeNew.tipo_ingreso_egreso_empleado_id = detali.tipo_ingreso_egreso_empleado_id
                            existeNew.valor = round(float(detali.valor_mensual-descont_dias), 2)
                            existeNew.valor_diario = round(float(detali.valor_diario), 2)
                            existeNew.valor_mensual = round(float(detali.valor_mensual), 2)
                            existeNew.ingresos_proyectados = True
                            existeNew.created_by = request.user.get_full_name()
                            existeNew.updated_by = request.user.get_full_name()
                            existeNew.created_at = datetime.now()
                            existeNew.updated_at = datetime.now()
                            existeNew.pagar = True
                            existeNew.save()

                egresosPro = EgresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
                if egresosPro:
                    for detale in egresosPro:
                        try:
                            existeE = EgresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                     empleado_id=detal.empleado_id,
                                                                     tipo_ingreso_egreso_empleado_id=detale.tipo_ingreso_egreso_empleado_id,
                                                                     egresos_proyectados=True)
                        except EgresosRolEmpleado.DoesNotExist:
                            existeE = None

                        if existeE:
                            existeE.valor = round(float(detale.valor), 2)
                            existeE.updated_by = request.user.get_full_name()
                            existeE.updated_at = datetime.now()
                            existeE.nombre = detale.tipo_ingreso_egreso_empleado.nombre
                            existeE.save()
                        else:
                            existeENew = EgresosRolEmpleado()
                            existeENew.anio = anio
                            existeENew.mes = mes
                            existeENew.empleado_id = detal.empleado_id
                            existeENew.tipo_ingreso_egreso_empleado_id = detale.tipo_ingreso_egreso_empleado_id
                            existeENew.valor = round(float(detale.valor), 2)
                            existeENew.egresos_proyectados = True
                            existeENew.nombre = detale.tipo_ingreso_egreso_empleado.nombre
                            existeENew.created_by = request.user.get_full_name()
                            existeENew.updated_by = request.user.get_full_name()
                            existeENew.created_at = datetime.now()
                            existeENew.updated_at = datetime.now()
                            existeENew.save()

                #CALCULO DEL SUELDO 
                try:
                    sueldo = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                             empleado_id=detal.empleado_id,
                                                             tipo_ingreso_egreso_empleado_id=24)
                except IngresosRolEmpleado.DoesNotExist:
                    sueldo = 0

                ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

                if detal.acumular_fondo_reserva:
                    fecha_comparar_modif=date(int(anio), int(mes), 30)
                    
                    if detal.fecha_ini_reconocida:
                        hoyfr=date(int(anio),int(mes), 30)
                        diferencia_entrada=hoyfr-detal.fecha_ini_reconocida

                        dias_comp= str(diferencia_entrada).split('days')
                        dias_c=dias_comp[0]
                        if int(dias_c)>=  364:
                            
                        
                            otros_ingresos_fr = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7)
                            if otros_ingresos_fr:
                                for otfr in otros_ingresos_fr:
                                    otfr.updated_by = request.user.get_full_name()
                                    otfr.tipo_ingreso_egreso_empleado_id = 7
                                    if ingresos['valor__sum']:
                                        if float(dias_c)>=394:
                                            
                                            fr_provision=ingresos['valor__sum']/12
                                            acumular_fondo=float((ingresos['valor__sum']) / 12)
                                            otfr.valor = round(acumular_fondo, 2)
                                        else:
                                            print 'total de dias'
                                            print dias_c
                                            proporcional=float(dias_c)-364
                                            print proporcional
                                            fr_provision=float((ingresos['valor__sum']) / 12)
                                            proporcionaf=float((fr_provision*proporcional)/30)
                                            otfr.valor = round(proporcionaf, 2)
                                        # comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
        
                                    otfr.nombre = 'FONDOS DE RESERVA'
                                    otfr.anio = anio
                                    otfr.mes = mes
                                    otfr.empleado_id = detal.empleado_id
                                    otfr.save()
        
                            else:
                                comprasdetalle = OtrosIngresosRolEmpleado()
                                comprasdetalle.updated_by = request.user.get_full_name()
                                comprasdetalle.tipo_ingreso_egreso_empleado_id = 7
                                if ingresos['valor__sum']:
                                    if float(dias_c)>=394:
                                        acumular_fondo=float((ingresos['valor__sum']) / 12)
                                        comprasdetalle.valor = round(acumular_fondo, 2)
                                    else:
                                        proporcional=float(dias_c)-364
                                        fr_provision=float((ingresos['valor__sum']) / 12)
                                        proporcionaf=float((fr_provision*proporcional)/30)
                                        comprasdetalle.valor = round(proporcionaf, 2)
                                    #comprasdetalle.valor = round(float((ingresos['valor__sum'] )/12),2)
                                    #comprasdetalle.valor = float((ingresos['valor__sum'] / 2) * 0.0833)
        
                                comprasdetalle.nombre = 'FONDOS DE RESERVA'
                                comprasdetalle.anio = anio
                                comprasdetalle.mes = mes
                                comprasdetalle.empleado_id = detal.empleado_id
                                comprasdetalle.save()
                        else:
                            otros_ingresos_fr = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7)
                            if otros_ingresos_fr:
                                otros_ingresos_fr.delete()

                else:
                    otros_ingresos_fr = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7)
                    if otros_ingresos_fr:
                        for otf in otros_ingresos_fr:
                            otf.delete()
                    
                if detal.acumular_decimo_tercero:
                    otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=8)
                    if otros_ingresos_dt:
                        for otdt in otros_ingresos_dt:
                            otdt.updated_by = request.user.get_full_name()
                            otdt.tipo_ingreso_egreso_empleado_id = 8
                            if ingresos['valor__sum']:
                                dtercero=float(ingresos['valor__sum'] / 12)
                                otdt.valor = round(dtercero, 2)
                            otdt.nombre = ' DECIMO 3ER SUELDO'
                            otdt.anio = anio
                            otdt.mes = mes
                            otdt.empleado_id = detal.empleado_id
                            otdt.save()
                    else:
                        comprasdetalle = OtrosIngresosRolEmpleado()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = 8
                        if ingresos['valor__sum']:
                            dtercero=float(ingresos['valor__sum'] / 12)
                            comprasdetalle.valor = round(dtercero, 2)
                        comprasdetalle.nombre = ' DECIMO 3ER SUELDO'
                        comprasdetalle.anio = anio
                        comprasdetalle.mes = mes
                        comprasdetalle.empleado_id = detal.empleado_id
                        comprasdetalle.save()
                else:
                    otros_ingresos_dt = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=8)
                    if otros_ingresos_dt:
                        for otd in otros_ingresos_dt:
                            otd.delete()
                        
                    

                if detal.acumular_decimo_cuarto:
                    dc_id = SueldosUnificados.objects.last()

                    otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=9)
                    if otros_ingresos_dc:
                        for otdct in otros_ingresos_dc:
                            otdct.updated_by = request.user.get_full_name()
                            otdct.tipo_ingreso_egreso_empleado_id = 9
                            dcuarto=float(dc_id.sueldo / 12)
                            if detal.tipo_remuneracion_id == 2:
                                mes_t=dias_trabajados/30
                                total_anios=mes_t*12
                                dcuarto=float(dc_id.sueldo/ 12)
                                dcuarto=(dcuarto*total_anios)/12
                            
                            else:
                                dcuarto=float(dc_id.sueldo/ 12)
                            otdct.valor = round(dcuarto,2)
                            otdct.nombre =' DECIMO 4TO SUELDO'
                            otdct.anio = anio
                            otdct.mes = mes
                            otdct.empleado_id = detal.empleado_id
                            otdct.save()
                    else:
                        comprasdetalle = OtrosIngresosRolEmpleado()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = 9
                        dcuarto=float(dc_id.sueldo / 12)
                        comprasdetalle.valor = round(dcuarto,2)
                        comprasdetalle.nombre = ' DECIMO 4TO SUELDO'
                        comprasdetalle.anio = anio
                        comprasdetalle.mes = mes
                        comprasdetalle.empleado_id = detal.empleado_id
                        comprasdetalle.save()
                else:
                    otros_ingresos_dc = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=9)
                    if otros_ingresos_dc:
                        for otdctf in otros_ingresos_dc:
                            otdctf.delete()
                    
                if detal.acumular_iess_asumido:
                    otros_ingresos_ia = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=27)
                    if otros_ingresos_ia:
                        for otia in otros_ingresos_ia:
                            otia.updated_by = request.user.get_full_name()
                            otia.tipo_ingreso_egreso_empleado_id = 27
                            if ingresos['valor__sum']:
                                # comprasdetalle.valor = float((ingresos['valor__sum'] / 10.5816) / 2)
                                #acumulado_iess=float(ingresos['valor__sum'] / 10.5816)
                                acumulado_iess=float(ingresos['valor__sum'] * 0.0945)
                                otia.valor = round(acumulado_iess,2)
                            otia.nombre = 'IESS ASUMIDO'
                            otia.anio = anio
                            otia.mes = mes
                            otia.empleado_id = detal.empleado_id
                            otia.save()

                    else:
                        comprasdetalle = OtrosIngresosRolEmpleado()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = 27
                        if ingresos['valor__sum']:
                            #comprasdetalle.valor = float((ingresos['valor__sum'] / 10.5816) / 2)
                            #acumulado_iess=float(ingresos['valor__sum'] / 10.5816)
                            acumulado_iess=float(ingresos['valor__sum'] * 0.0945)
                            comprasdetalle.valor = round(acumulado_iess,2)
                        comprasdetalle.nombre = 'IESS ASUMIDO'
                        comprasdetalle.anio = anio
                        comprasdetalle.mes = mes
                        comprasdetalle.empleado_id = detal.empleado_id
                        comprasdetalle.save()
                
                else:
                    otros_ingresos_ia = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=27)
                    if otros_ingresos_ia:
                        for oti in otros_ingresos_ia:
                            oti.delete()
                    
                if detal.asumir_impuesto_renta:
                    otros_ingresos_ir = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=28)
                    if otros_ingresos_ir:
                        h_at = 1
                        #print('hola5')
                    else:
                        comprasdetalle = OtrosIngresosRolEmpleado()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = 28
                        comprasdetalle.valor = 0
                        comprasdetalle.nombre = 'IR ASUMIDO'
                        comprasdetalle.anio = anio
                        comprasdetalle.mes = mes
                        comprasdetalle.empleado_id = detal.empleado_id
                        comprasdetalle.save()
                else:
                    otros_ingresos_ir = OtrosIngresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=28)
                    if otros_ingresos_ir:
                        for otiing in otros_ingresos_ir:
                            otiing.delete()
                

                if detal.extension_conyugal:
                    otros_egresos_esposa = EgresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=30)
                    if otros_egresos_esposa:
                        for otesp in otros_egresos_esposa:
                            otesp.updated_by = request.user.get_full_name()
                            otesp.tipo_ingreso_egreso_empleado_id = 30
                            if ingresos['valor__sum']:
                                # comprasdetalle.valor = float((ingresos['valor__sum'] * 0.0341) / 2)
                                ext=float(ingresos['valor__sum'] * 0.0341)
                                otesp.valor = round(ext, 2)
                            otesp.nombre = 'DESCUENTO 3.41%'
                            otesp.anio = anio
                            otesp.mes = mes
                            otesp.empleado_id = detal.empleado_id
                            otesp.save()

                        #print('hola7')
                    else:
                        comprasdetalle = EgresosRolEmpleado()
                        comprasdetalle.updated_by = request.user.get_full_name()
                        comprasdetalle.tipo_ingreso_egreso_empleado_id = 30
                        if ingresos['valor__sum']:
                            #comprasdetalle.valor = float((ingresos['valor__sum'] * 0.0341) / 2)
                            ext=float(ingresos['valor__sum'] * 0.0341)
                            comprasdetalle.valor = round(ext,2)
                        comprasdetalle.nombre = 'DESCUENTO 3.41%'
                        comprasdetalle.anio = anio
                        comprasdetalle.mes = mes
                        comprasdetalle.empleado_id = detal.empleado_id
                        comprasdetalle.save()
                else:
                    otros_egresos_esposa = EgresosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                        tipo_ingreso_egreso_empleado_id=30)
                    if otros_egresos_esposa:
                        for otes in otros_egresos_esposa:
                            otes.delete()
                            
                    
                otros_egresos_nueve = EgresosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(
                    tipo_ingreso_egreso_empleado_id=29)
                if otros_egresos_nueve:
                    for otn in otros_egresos_nueve:
                        otn.updated_by = request.user.get_full_name()
                        otn.tipo_ingreso_egreso_empleado_id = 29

                        if ingresos['valor__sum']:
                            # print('sueldoa' + str(ingresos['valor__sum']))
                            prueb=float(ingresos['valor__sum'] * 0.0945)
                            otn.valor = round(prueb, 2)
                            calc = float((ingresos['valor__sum'] * 0.0945))
                            # print('egresos' + str(calc)+'VALOR DEL SUELDO'+str(ingresos['valor__sum']))
                        otn.nombre = 'DESCUENTO 9.45%'
                        otn.anio = anio
                        otn.mes = mes
                        otn.empleado_id = detal.empleado_id
                        otn.save()
                else:

                    comprasdetalle = EgresosRolEmpleado()
                    comprasdetalle.updated_by = request.user.get_full_name()
                    comprasdetalle.tipo_ingreso_egreso_empleado_id = 29

                    if ingresos['valor__sum']:
                        #print('sueldoa' + str(ingresos['valor__sum']))
                        prueb=float(ingresos['valor__sum'] * 0.0945)
                        comprasdetalle.valor = round(prueb,2)
                        calc = float((ingresos['valor__sum'] * 0.0945))
                        #print('egresos' + str(calc)+'VALOR DEL SUELDO'+str(ingresos['valor__sum']))
                    comprasdetalle.nombre = 'DESCUENTO 9.45%'
                    comprasdetalle.anio = anio
                    comprasdetalle.mes = mes
                    comprasdetalle.empleado_id = detal.empleado_id
                    comprasdetalle.save()

                otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

                egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
                otros_egresos = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
                dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('dias'))
                dias_ingreso_egreso = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('dias'))
                dias_parciales= DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=8).aggregate(Sum('dias'))
            
                
            
                valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
                    mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))
                faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
                faltas_ingreso_egreso_valor =  DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('valor'))
                
                faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
                atrasos_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=5).aggregate(Sum('valor'))
                atrasos_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=4).aggregate(Sum('valor'))
                vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))

                total_otros_ingresos = 0
                total_otros_egresos = 0
                total_egresos = 0
                total_dias = 0
                total_desc = 0
                dias_trabajados = 30
                total_valor_dias = 0

                if ingresos['valor__sum']:
                    total_ingresos = float(ingresos['valor__sum'])
                else:
                    total_ingresos = 0

                if otros_ingresos['valor__sum']:
                    total_otros_ingresos = float(otros_ingresos['valor__sum'])
                else:
                    #print('no tiene otros ingreso'+str(detal.empleado_id))
                    total_otros_ingresos = 0

                if egresos['valor__sum']:
                    total_egresos = float(egresos['valor__sum'])


                else:
                    total_egresos = 0

                total_egreso_neto = float(total_egresos)
                mensaj=''
                mensaj+='Egresos' + str(total_egresos)
                if faltas_justificadas_valor['valor__sum']:
                    total_egresos = float(faltas_justificadas_valor['valor__sum'] + total_egresos)
                    mensaj+='Faltas justificadas'+ str(faltas_justificadas_valor['valor__sum'])
                if atrasos_justificadas_valor['valor__sum']:
                    total_egresos = float(atrasos_justificadas_valor['valor__sum'] + total_egresos)
                    mensaj += 'Atrasos justificadas' + str( atrasos_justificadas_valor['valor__sum'])
                # if atrasos_injustificadas_valor['valor__sum']:
                #     #total_egresos = float(atrasos_injustificadas_valor['valor__sum'] + total_egresos)
                #
                #     #mensaj += 'Atrasos injustificadas' + str(atrasos_injustificadas_valor['valor__sum'])
                #
                # if vacaciones_justificadas_valor['valor__sum']:
                #
                #     #total_egresos = float(vacaciones_justificadas_valor['valor__sum'] + total_egresos)
                #     #mensaj += 'Vacaciones justificadas' + str(vacaciones_justificadas_valor['valor__sum'])


                if otros_egresos['valor__sum']:
                    #print('otros_egresos' + str(otros_egresos['valor__sum']))
                    total_otros_egresos = float(otros_egresos['valor__sum'])
                    mensaj += 'Otros Egresos' + str(total_otros_egresos)

                else:
                    total_otros_egresos = 0
                total_ingreso_neto = float(total_ingresos)

                if dias['dias__sum']:
                    total_dias = float(dias['dias__sum'])
                    #dias_trabajados = float((dias_trabajados * 8) - total_dias) / 8
                else:
                    total_dias=0
                    
                if dias_ingreso_egreso['dias__sum']:
                    total_dias_ingreso_egreso=float(dias_ingreso_egreso['dias__sum'])
                else:
                    total_dias_ingreso_egreso=0
                
                if dias_parciales['dias__sum']:
                    total_dias_parciales=float(dias_parciales['dias__sum'])
                else:
                    total_dias_parciales=0
                
                dias_trabajados = float((dias_trabajados * 8) - total_dias-total_dias_ingreso_egreso-total_dias_parciales) / 8
                
                if faltas_injustificadas_valor['valor__sum']:
                    total_desc = float(faltas_injustificadas_valor['valor__sum'])
                else:
                    total_desc = 0
                    
                if faltas_ingreso_egreso_valor['valor__sum']:
                    total_desc = total_desc+float(faltas_ingreso_egreso_valor['valor__sum'])
                else:
                    total_desc = 0
                #print "total descuento:"
                #print total_desc
                #total_ingresos = float(total_ingresos - (total_desc))
                if valor_dias['valor__sum']:
                    total_valor_dias = float(valor_dias['valor__sum'])
                    # total_ingresos=float(total_ingresos-(valor_diario['valor_diario__sum']*total_dias))
                ingreso_total=0

                ingreso_total=round(float(total_ingresos+total_otros_ingresos), 2)
                total =round(float(ingreso_total-total_egresos), 2)

                if i <21:
                    error+='Fila:'+ str(i)+'TOTAL:'+str(total)
                html += ' <tr><td class="text-center">' + str(i) + '<input type="hidden" name="id_empleado' + str(
                    i) + '" id="id_empleado' + str(i) + '" value="' + str(detal.empleado_id) + '"/></td>'
                # html+='<td class="text-center"><div class="checkbox custom-checkbox custom-checkbox-primary"><input class="seleccionar" data-contextual="info" data-target="tr" data-toggle="selectrow" id="id_pago_'+str(i)+'_seleccionado" name="pago_'+str(i)+'_seleccionado" type="checkbox"><label for="id_pago_'+str(i)+'_seleccionado"></label></div></td>'
                html += '<td><input class="form-control input-sm" id="id_cedula_' + str(
                    i) + '" maxlength="10" name="cedula_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.cedula_empleado) + '" type="text"></td>'
                html += '<td><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_razon_social" maxlength="300" name="pago_' + str(
                    i) + '_razon_social" readonly="readonly" size="31" value="' + str(
                    detal.nombre_empleado.encode('utf8')) + '" type="text"><input id="id_pago_' + str(
                    i) + '_idpersona" name="pago_' + str(i) + '_idpersona" value="893721" type="hidden"></td>'
                html += '<td><input class="form-control input-sm" id="id_area_' + str(
                    i) + '" maxlength="10" name="area_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.departamento) + '" type="text"></td>'
                html += '<td><input class="form-control input-sm" id="id_cargo_' + str(
                    i) + '" maxlength="10" name="cargo_' + str(i) + '" readonly="readonly" size="10" value="' + str(
                    detal.tipo_empleado) + '" type="text"></td>'
                if sueldo:
                    html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
                        i) + '" maxlength="10" name="sueldo_' + str(
                        i) + '" readonly="readonly" size="10" value="' + str(
                        sueldo.valor_mensual) + '" type="text"></td>'
                else:
                    html += '<td><input class="form-control input-sm" id="id_sueldo_' + str(
                        i) + '" maxlength="10" name="sueldo_' + str(
                        i) + '" readonly="readonly" size="10" value="' + str(sueldo) + '" type="text"></td>'

                html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_diasagregados_ad()"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_dias" name="pago_' + str(i) + '_dias" readonly="readonly" size="5" value="' + str(
                    dias_trabajados) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_dias_valor" name="pago_valor_' + str(i) + '_dias" readonly="readonly" value="' + str(
                    total_valor_dias) + '" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_total_dias" name="pago_' + str(i) + '_valor_total_dias" readonly="readonly" value="0" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_permisos" name="pago_' + str(i) + '_valor_permisos" readonly="readonly" value="0" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_vacaciones" name="pago_' + str(i) + '_valor_vacaciones" readonly="readonly" value="0" type="hidden"></a><span class="input-group-btn input"><a href="javascript: dias_ad(' + str(
                    i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
                html += '<td><a href="javascript: ingresos(' + str(
                    i) + ')" data-toggle="modal"><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_total" name="pago_' + str(
                    i) + '_total" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    total_ingresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
                    i) + '_ingreso" name="pago_' + str(
                    i) + '_ingreso" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    total_ingreso_neto) + '" type="hidden"></td>'
                html += '<td><div class="input-group input-group-sm"><a href="#"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_otros_ingresos" maxlength="15" name="pago_' + str(
                    i) + '_otros_ingresos" readonly="readonly" size="6" value="' + str(
                    total_otros_ingresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: ingresos_ad(' + str(
                    i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'
                html += '<td><a href="javascript: egresos(' + str(
                    i) + ')" data-toggle="modal"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_total_egresos" maxlength="15" name="pago_' + str(
                    i) + '_total_egresos" readonly="readonly" size="6" value="' + str(
                    total_egresos) + '" type="text"></a><input class="form-control input-sm" id="id_pago_' + str(
                    i) + 'egreso_neto" name="pago_' + str(
                    i) + 'egreso_neto" readonly="readonly" size="7" style="text-align:right;" value="' + str(
                    total_egreso_neto) + '" type="hidden"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_otros_egresos" maxlength="10" name="pago_' + str(
                    i) + '_otros_egresos" readonly="readonly" size="6" value="0" type="hidden"></td>'
                # #html += '<td><div class="input-group input-group-sm"><a href="javascript: consultar_descuentos()"><input class="form-control input-sm text-right" id="id_pago_' + str(
                #     i) + '_otros_egresos" maxlength="10" name="pago_' + str(
                #     i) + '_otros_egresos" readonly="readonly" size="6" value="' + str(
                #     total_otros_egresos) + '" type="text"></a><span class="input-group-btn input"><a href="javascript: egresos_ad(' + str(
                #     i) + ')" class="btn btn-xs btn-default" data-toggle="modal"><i class="fa fa-plus"></i></a></span></div></td>'

                html += '<td><input class="form-control input-sm text-right" id="id_pago_' + str(i) + '_valor_a_recibir" name="pago_' + str(i) + '_valor_a_recibir" readonly="readonly" size="10" value="' + str(total) + '" type="text"><input class="form-control input-sm text-right" id="id_pago_' + str(
                    i) + '_valor_a_recibir_hidden" name="pago_' + str(
                    i) + '_valor_a_recibir_hidden" readonly="readonly" size="10" value="'+str(total)+'" type="hidden"></td>'
                html += '<td><select class="tipopago form-control input-sm" id="id_pago_' + str(
                    i) + '_tipo_pago" maxlength="15" name="pago_' + str(
                    i) + '_tipo_pago" onchange="mostrarComprobante(this);">'
                for am in formapago:
                    html += '<option value="' + str(am.id)+'"'
                    if am.id==detal.forma_pago_empleado_id:
                        html+=' selected'
                    html+='>' + str(am.nombre) + '</option>'
                html += '</select><div class="num_comprobante"><div class="pull-right"><input placeholder="# Cheque" class="form-control input-sm" id="id_pago_' + str(
                    i) + '_numero_comprobante" maxlength="40" name="pago_' + str(
                    i) + '_numero_comprobante" size="12" type="text"></div></div></td>'
                html += '<td><select class="select-input form-control input-sm" id="id_pago_' + str(
                    i) + '_cuenta_bancaria" name="pago_' + str(i) + '_cuenta_bancaria">'
                for b in banco:
                    bnombre = (b.nombre).encode('ascii', 'ignore').decode('ascii')
                    html += '<option value="' + str(b.id) + '"'
                    if b.id == detal.banco_id:
                        html += ' selected'
                    html+='>' + str(bnombre) + '</option>'
                html += '</select></td></tr>'
                final_ingresos = final_ingresos + total_ingresos
                final_otros_ingresos = final_otros_ingresos + total_otros_ingresos
                final_egresos = final_egresos + total_egresos
                final_otros_egresos = final_otros_egresos + total_otros_egresos
                final_total = final_total + total

            html += '<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td style="text-align:right">' + str(
                final_ingresos) + '</td><td >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + str(
                final_otros_ingresos) + '</td><td style="text-align:right">' + str(
                final_egresos) + '</td><td style="text-align:right">' + str(
                final_total) + '</td><td></td><td></td></tr>'
            html += '<input type="hidden" id="columnas_receta_roles" name="columnas_receta_roles" value="' + str(
                i) + '" />'
            print (error)
        return HttpResponse(
            html
        )
    else:
        print('get entro')
        html=''
        
        return HttpResponse(
            html
        )



def RolesPagoConfiguracionesView(request):
    if request.method == 'POST':
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')

        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/configuraciones.html', { 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado, 'banco': banco,
                                                            'roles_pago': roles_pago,
                                                            'sueldos_unificados': sueldos_unificados,
                                                            'clasificacion': clasificacion}, RequestContext(request))


    else:
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()
        banco = Banco.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        sueldos_unificados = SueldosUnificados.objects.order_by('-anio')
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/configuraciones.html', { 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado, 'banco': banco,
                                                            'roles_pago': roles_pago,
                                                            'sueldos_unificados': sueldos_unificados,
                                                            'clasificacion': clasificacion}, RequestContext(request))


@login_required()
def guardarRolesConfiguracionView(request):
    if request.method == 'POST':
        mensual = request.POST.get("mensual", False)
        quincenal = request.POST.get("quincenal", False)
        dia_pago = request.POST["dia_pago"]
        porcentaje_primera_quincena = request.POST["porcentaje_primera_quincena"]
        porcentaje_iess = request.POST["porcentaje_iess"]
        porcentaje_ext_conyugal = request.POST["porcentaje_ext_conyugal"]
        cuenta_bancaria_rrhh = request.POST["cuenta_bancaria_rrhh"]

        rol = RolPagoConfiguraciones()
        rol.dia_pago = dia_pago
        rol.porcentaje_primera_quincena = porcentaje_primera_quincena
        rol.mensual = mensual
        rol.quincenal = quincenal
        rol.porcentaje_iess = porcentaje_iess
        rol.extension_conyugal_iess = porcentaje_ext_conyugal
        rol.banco_id = cuenta_bancaria_rrhh
        rol.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/config')


    else:
        id_cargo = request.POST["id_cargo"]
        nombre = request.POST["nombre"]
        sueldo = request.POST["salario_min_sectorial"]

        cargo = TipoEmpleado.objects.get(tipo_empleado_id=id_cargo)
        cargo.cargo_empleado = nombre
        cargo.sueldo = float(sueldo)
        cargo.save()
        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return render_to_response('roles_pago/configuraciones.html', {'rol_cuentas': rol_cuentas, 'departamentos': departamentos,
                                                            'tipoempleado': tipoempleado}, RequestContext(request))


def RolesPagoConfiguracionesCuentaView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.order_by('id')
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/configuraciones_cuentas.html', {'rol_cuentas': rol_cuentas,
                                                            'roles_pago': roles_pago,'plan': plan,
                                                            'clasificacion': clasificacion}, RequestContext(request))


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        roles_pago = RolPagoConfiguraciones.objects.latest('id')
        plan = PlanDeCuentas.objects.all()
        clasificacion = ClasificacionCuenta.objects.order_by('orden')

        return render_to_response('roles_pago/configuraciones_cuentas.html', {'rol_cuentas': rol_cuentas,
                                                            'roles_pago': roles_pago, 'plan': plan,
                                                            'clasificacion': clasificacion}, RequestContext(request))




@login_required()
def guardarCuentasContablesConfiguracionesView(request):
    if request.method == 'POST':
        rol_cuentas = RolPagoCuentaContable.objects.all()
        for r in rol_cuentas:
            if 'cuentas' + str(r.id) in request.POST:
                id_cuenta = request.POST['cuentas' + str(r.id)]
                cuent = RolPagoCuentaContable.objects.get(id=r.id)
                cuent.plandecuentas_id = id_cuenta
                cuent.updated_at = datetime.now()
                cuent.updated_by = request.user.get_full_name()
                cuent.save()

        plan = PlanDeCuentas.objects.all()

        rol_cuentas = RolPagoCuentaContable.objects.all()
        departamentos = Departamento.objects.all()
        tipoempleado = TipoEmpleado.objects.all()

        return HttpResponseRedirect('/recursos_humanos/roles_pago/config_cuentas')


    else:
        rol_cuentas = RolPagoCuentaContable.objects.all()
        for r in rol_cuentas:
            if 'cuentas' + r.id in request.POST:
                id_cuenta = request.POST['cuentas' + r.id]
                cuent = RolPagoCuentaContable.objects.get(id=r.id)
                cuent.plandecuentas_id = id_cuenta
                cuent.updated_at = datetime.now()
                cuent.updated_by = request.user.get_full_name()
                cuent.save()

        plan = PlanDeCuentas.objects.all()
        rol_cuentas = RolPagoCuentaContable.objects.all()

        return render_to_response('roles_pago/configuraciones_cuentas.html', {'rol_cuentas': rol_cuentas, 'plan': plan},
                                  RequestContext(request))



def imprimirRolIndividual(request, idrol,iddepartamento):
    # vista de ejemplo con un hipot?tico modelo Libro

    detalles = RolPago.objects.get(id=idrol)
    departamento = Departamento.objects.get(id=iddepartamento)
    nombre=''
    if departamento:
        nombre=departamento.nombre
    mes = detalles.mes
    anio = detalles.anio
    quincena = detalles.quincena
    i = 0
    html_final= ''
    final_ingresos = 0
    final_otros_ingresos = 0
    final_egresos = 0
    final_otros_egresos = 0
    final_total = 0
    tipopago = TipoPago.objects.all()
    if mes == 1:
        mes_string = 'ENERO'
    if mes == 2:
        mes_string = 'FEBRERO'
    if mes == 3:
        mes_string = 'MARZO'
    if mes == 4:
        mes_string = 'ABRIL'
    if mes == 5:
        mes_string = 'Mayo'
    if mes == 6:
        mes_string = 'JUNIO'
    if mes == 7:
        mes_string = 'JULIO'
    if mes == 8:
        mes_string = 'AGOSTO'
    if mes == 9:
        mes_string = 'SEPTIEMBRE'
    if mes == 10:
        mes_string = 'OCTUBRE'
    if mes == 11:
        mes_string = 'NOVIEMBRE'
    if mes == 12:
        mes_string = 'DICIEMBRE'

    if detalles:
        roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).filter(empleado__departamento_id=iddepartamento).order_by('id')

    for detal in roles:
        i += 1
        html=''

        html += '<table border="1"><tr><td style="text-align:left">'
        html += 'MUEBLES Y DIVERSIDADES MUEDIRSA S.A. <br />RUC: 0992128372001<br /><b>ROL DE PAGO MUEDIRSA DE '

        if quincena == '1Q':
            html += ' PRIMERA QUINCENA '
        else:
            html += ' SEGUNDA QUINCENA '

        html += 'DE ' + str(mes_string) + ' ' + str(anio)
        html += '</td><td width="150"><img src="'+settings.MEDIA_ROOT+'imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td></tr>'
        html += '</table>'


        dia = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            tipo_ausencia_id=3).aggregate(Sum('dias'))
        valor_dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).aggregate(Sum('valor'))

        if dia['dias__sum']:
            t_dias = (240 - dia['dias__sum']) / 8
        else:
            t_dias = 30
        

        ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(pagar=True)
        total_ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))

        html += '<table border="1"><tr><td ><b>Trabajador:</b></td><td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td></tr>'
        html += ''
        html += '<tr><td ><b>Cargo:</b></td><td>' + str(
            detal.empleado.tipo_empleado) + '&nbsp;&nbsp;&nbsp;<b>Area:</b>' + str(
            detal.empleado.departamento) + '</td></tr><tr><td><b>D&iacute;as trabajados</b>' + str(t_dias) + '</td></tr>'
        try:
            sueldo = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                     empleado_id=detal.empleado_id,
                                                     tipo_ingreso_egreso_empleado_id=24)
        except IngresosRolEmpleado.DoesNotExist:
            sueldo = 0

        html += ''

        html += '<table border="1">'
        # html += '<tr><td colspan="2"><b>INGRESOS:</b></td><td colspan="2"><b>EGRESOS:</b></td></tr>'
        html += '<tr><td colspan="2">'
        html += '<table>'
        t_otros_ingresos = 0
        t_ingresos = 0
        t_egresos = 0
        t_otros_egresos = 0
        tipo_ingreso = TipoIngresoEgresoEmpleado.objects.exclude(egreso=True).order_by('orden')
        for tip in tipo_ingreso:
            if tip:
                if tip.ingreso== True :
                    ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True)
                    total_ingresos = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True).aggregate(Sum('valor'))
                    faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                        anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                        tipo_ausencia_id=3).aggregate(Sum('valor'))

                    if faltas_injustificadas_valor['valor__sum']:
                        total_desc = float(faltas_injustificadas_valor['valor__sum'])
                        # html += '<tr><td>AUSENCIAS INSJUSTIFICADAS</td><td style="text-align:right">' + str(round(total_desc, 2)) + '</td></tr>'
                    else:
                        total_desc = 0


                    if ingresos:
                        if tip.id==5 or tip.id==25 or tip.id==26:
                            total_horas = IngresosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(pagar=True).aggregate(Sum('horas'))
                            html += '<tr><td  width="220">' + str(tip.nombre) + '&nbsp;&nbsp;&nbsp;' +str(round(total_horas['horas__sum'], 2))+'</td><td style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
                        else:
                            if tip.id==24 and  faltas_injustificadas_valor['valor__sum']:
                                s_descontado=total_ingresos['valor__sum']-faltas_injustificadas_valor['valor__sum']
                                html += '<tr><td>' + str(tip.nombre) + '</td><td   style="text-align:right">' + str(round(s_descontado, 2)) + '</td></tr>'

                            else:
                                html += '<tr><td>' + str(tip.nombre) + '</td><td  style="text-align:right">' + str(round(total_ingresos['valor__sum'], 2)) + '</td></tr>'
                    else:
                        html += '<tr><td width="220">' + str(tip.nombre) + '</td><td style="text-align:right">0</td></tr>'


                    if total_ingresos['valor__sum']:
                        t_ingresos += total_ingresos['valor__sum']
                    else:
                        t_ingresos += 0

                if tip.otros_ingresos == True:
                    otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True)
                    total_otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                        mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tip.id).filter(
                        pagar=True).aggregate(Sum('valor'))
                    if otros_ingresos:
                        valor_otros_ingresos=total_otros_ingresos['valor__sum']
                    else:
                        valor_otros_ingresos=0
                    html += '<tr><td width="220">' + str(tip.nombre) + '</td><td width="50" style="text-align:right">' + str(
                            round(valor_otros_ingresos, 2)) + '</td></tr>'

                    if total_otros_ingresos['valor__sum']:
                        t_otros_ingresos += total_otros_ingresos['valor__sum']
                    else:
                        t_otros_ingresos += 0



        t_ingresos = float(t_ingresos - (total_desc))
        total_i = t_ingresos + t_otros_ingresos


        html += '</table></td>'
        html += '<td colspan="2">'
        html += '<table>'
        tipo_egreso = TipoIngresoEgresoEmpleado.objects.filter(egreso=True).order_by('orden')
        for tipe in tipo_egreso:
            egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id)
            total_egresos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipe.id).aggregate(
                Sum('valor'))
            if egresos:
                valor_egresos=total_egresos['valor__sum']
            else:
                valor_egresos=0
            html += '<tr><td width="220">' + str(tipe.nombre) + '</td><td style="text-align:right">' + str(valor_egresos) + '</td></tr>'

            if total_egresos['valor__sum']:
                t_egresos += total_egresos['valor__sum']
            else:
                t_egresos += 0

        tipo_otros_egreso = TipoIngresoEgresoEmpleado.objects.filter(otros_egresos=True)
        for tipoe in tipo_otros_egreso:
            otros_egresos = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id)
            total_otros_egresos = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado=tipoe.id).aggregate(
                Sum('valor'))
            if otros_egresos:
                valor_otros_egresos=total_otros_egresos['valor__sum']
            else:
                valor_otros_egresos =0





            html += '<tr><td>' + str(tipoe.nombre) + '</td><td style="text-align:right">' + str(round(float(valor_otros_egresos), 2)) + '</td></tr>'

            if total_otros_egresos['valor__sum']:
                t_otros_egresos += total_otros_egresos['valor__sum']
            else:
                t_otros_egresos += 0

        dias_j = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
            tipo_ausencia_id=1)
        total_dias_je = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
        if dias_j:


            total_dias_j = total_dias_je['valor__sum']

        else:
            total_dias_j = 0

        html += '<tr><td>PERMISOS</td><td style="text-align:right">' + str(round(float(total_dias_j), 2)) + '</td></tr>'
        dias_p = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(
            empleado_id=detal.empleado_id).filter(descontar=True).filter(cargar_vacaciones=False).filter(
            tipo_ausencia_id=2)
        total_dias_pe = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
        if dias_p:


            total_dias_p = total_dias_pe['valor__sum']
        else:
            total_dias_p = 0

       # html += '<tr><td>VACACIONES</td><td style="text-align:right">' + str(round(float(total_dias_p), 2)) + '</td></tr>'
        total_e = float(t_egresos) + float(t_otros_egresos) + float(total_dias_j) + float(total_dias_p)

        total_dias_valor = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))
        if total_dias_valor['valor__sum']:
            t_dias_valor = total_dias_valor['valor__sum']
        else:
            t_dias_valor = 0


        # total_cobrar=total_i-total_e-t_dias_valor
        if detal.ingresos:
            ingresos_total = detal.ingresos
        else:
            ingresos_total = 0
        if detal.otros_ingresos:
            oingresos_total = detal.otros_ingresos
        else:
            oingresos_total = 0
        if detal.egresos:
            egresos_total = detal.egresos
        else:
            egresos_total = 0
        if detal.otros_egresos:
            oegresos_total = detal.otros_egresos
        else:
            oegresos_total = 0
        if detal.descuento_dias:
            dias = detal.descuento_dias
        else:
            dias = 0
        total_cobrar = float(ingresos_total) + float(oingresos_total) - float(egresos_total)
        html += '</table></td></tr>'
        html += '<tr><td width="220"><b>**TOTAL INGRESOS**</b></td><td style="text-align:right">' + str(
            round(total_i, 2)) + '</td>'
        html += '<td width="200"><b>**TOTAL EGRESOS **&nbsp;&nbsp;&nbsp</b></td><td style="text-align:right">' + str(
            round(float(total_e), 2)) + '</td></tr>';
        html += '<tr><td colspan="2" style="text-align:right;vertical-align:middle"></td><td  style="text-align:right;vertical-align:middle"><b>** A RECIBIR **</b></td><td style="text-align:right">$' + str(
            round(total_cobrar, 2)) + '</td></tr>';
        html += '<tr><td colspan="4"><table border="0"><tr><td colspan="2">ENTREGA</td><td colspan="2">RECIBI CONFORME</td></tr>';
        html += '<tr><td colspan="2">&nbsp;</td><td colspan="2">NOMBRE:' + str(
            detal.empleado.nombre_empleado.encode('utf8')) + '<br />NUM. CEDULA: 0' + str(
            detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>';
        html += '<tr><td colspan="2" style="text-align:center;"><br />_______________________________________<br /> FIRMA</td><td colspan="2"  style="text-align:center;"><br />_______________________________________<br /> FIRMA</td></tr>';
        #html += '<tr><td  style="text-align:center;" ><img src="media/imagenes/general/firma_nomina.jpg"  width="100" height="50"><br />-------------------<br />ELABORADO</td><td style="text-align:center">-------------------<br />AUTORIZADO</td><td colspan="2" style="text-align:center">-------------------<br />Recibi Conforme: EMPLEADO</td></tr>';
        # html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>' + str(
        #     detal.empleado.nombre_empleado.encode('utf8')) + '</td><td >' + str(
        #     detal.empleado.tipo_empleado) + '</td></tr>';
        # html += '<tr><td colspan="1">&nbsp;&nbsp;&nbsp;</td><td>&nbsp;&nbsp;&nbsp;</td><td>C.C.NO</td><td >' + str(
        #     detal.empleado.cedula_empleado.encode('utf8')) + '</td></tr>';
        #
        # html += '<tr><td colspan="4">***Nota: Declaro haber recibido conforme el importe del Rol de Pago, sin derecho a reclamo por ning&uacute;n concepto en lo posterior.</td></tr>'
        html += '</table></td></tr></table>'
        html_final+=html
        html_final += ' <br />'
        html_final += html

        #COPIA DEL ROL DE PAGO


        html_final += ' <pdf:nextpage />'
    html1 = render_to_string('roles_pago/imprimir_individual.html', {'pagesize': 'A4', 'html': html_final,'nombre':nombre},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)

    #         'ordenproduccion':ordenproduccion,
    #         }

    # return render_to_response(
    #         'ordenproduccion/imprimir.html',
    #         context,
    #         context_instance=RequestContext(request))


def indexMenuImprimirIndividual(request, pk):
    # vista de ejemplo con un hipot?tico modelo Libro
    cursor = connection.cursor()
    sql = 'select distinct d.id,d.codigo,d.nombre from departamento d,empleados_empleado e, rol_pago_detalle rpd  where rpd.empleado_id=e.empleado_id and e.departamento_id=d.id and rpd.rol_pago_id='+str(pk)

    sql += ';'
    cursor.execute(sql)
    rol = cursor.fetchall()
    html=''

    # try:
    #   rol = DiasNoLaboradosRolEmpleado.objects.filter(quincena=quincena,anio=anio,mes=mes)
    # except DiasNoLaboradosRolEmpleado.DoesNotExist:
    #   rol = None

    if rol:

        for r in rol:
            html+='<div><a href="/recursos_humanos/imprimirRolIndividual/'+str(pk)+'/'+str(r[0])+'/"><button type="button" class="bt-selec-centro-costo btn btn-info btn-xs"><i class="fa fa-print"></i> '+str(r[2])+'</button></a></div><br />'


        #COPIA DEL ROL DE PAGO

    return render_to_response('roles_pago/menu_imprimir_individual.html', {'html': html},
                              RequestContext(request))




@login_required()
@csrf_exempt
def verRolGlobalActualizado(request, pk):
    if request.method == 'POST':
        html = ''

    else:
        detalles = RolPago.objects.get(id=pk)
        mes = detalles.mes
        anio = detalles.anio
        quincena = detalles.quincena
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        if detalles:
            roles = RolPagoDetalle.objects.filter(rol_pago_id=detalles.id).order_by('id')
            id = detalles.id
        for detal in roles:
            i += 1
            try:
                sueldo = IngresosRolEmpleado.objects.filter( anio=anio).filter( mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).first()
            except IngresosRolEmpleado.DoesNotExist:
                sueldo = 0
            html += '<tr>'
            html += '<td>' + str(i) + '</td>'
            html += '<td>' + str(detal.empleado.nombre_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.empleado.cedula_empleado) + '</td>'
            html += '<td>' + str(detal.empleado.departamento) + '</td>'
            html += '<td>' + str(detal.empleado.tipo_empleado) + '</td>'
            html += '<td>' + str(detal.empleado.fecha_ini_reconocida) + '</td>'
            html += '<td>' + str(detal.empleado.fecha_fin) + '</td>'
            if detal.empleado.acumular_decimo_tercero:
                html += '<td>NO</td>'
            else:
                html += '<td>SI</td>'

            #hoy = date.today()  # Asigna fecha actual
            hoy=date(int(anio),int(mes), 30)
            ayer = detal.empleado.fecha_ini_reconocida
            if ayer:
                diferencia_en_dias = hoy-ayer

                dias_comp= str(diferencia_en_dias).split('days')
                dias_c=dias_comp[0]
            else:
                diferencia_en_dias=0
                dias_c=0

            html += '<td>'
            if int(dias_c)>=  364:
                html+='SI'
            else:
                html += 'NO'

            #html+=str(diferencia_en_dias)
            html+='</td>'
            if detal.empleado.acumular_fondo_reserva:
                html += '<td>NO</td>'
            else:
                html += '<td>SI</td>'

            html += '<td>30</td>'
            if sueldo:
                html += '<td>' + str(sueldo.valor_mensual) + '</td>'

            else:
                html += '<td>0</td>'

            dias_trabajados = 30
            # total_dias=1
            # dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #     mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #     tipo_ausencia_id=3).aggregate(Sum('dias'))
            # 
            # diasf = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #     mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #     tipo_ausencia_id=7).aggregate(Sum('dias'))
            # 
            # diasp = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #     mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #     tipo_ausencia_id=8).aggregate(Sum('dias'))
            # 
            # diasv = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(
            #     mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
            #     tipo_ausencia_id=1).aggregate(Sum('dias'))
            # 
            # 
            # 
            # 
            # if dias['dias__sum']:
            #     total_dias = float(dias['dias__sum'])
            # 
            # # if dias1['dias__sum']:
            # #     total_dias = total_dias+float(dias1['dias__sum'])
            # #     
            # if diasf['dias__sum']:
            #     total_dias = total_dias+float(diasf['dias__sum'])
            # 
            # if diasp['dias__sum']:
            #     total_dias = total_dias+float(diasp['dias__sum'])
            #     
            # dias_trabajados = float((dias_trabajados * 8) - total_dias) / 8
            # 
            
            dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(Sum('dias'))
            dias_ingreso_egreso = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=7).aggregate(Sum('dias'))
            dias_parciales= DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=8).aggregate(Sum('dias'))
            if dias['dias__sum']:
                total_dias = float(dias['dias__sum'])
            else:
                total_dias=0
                    
            if dias_ingreso_egreso['dias__sum']:
                total_dias_ingreso_egreso=float(dias_ingreso_egreso['dias__sum'])
            else:
                total_dias_ingreso_egreso=0
                
            if dias_parciales['dias__sum']:
                total_dias_parciales=float(dias_parciales['dias__sum'])
            else:
                total_dias_parciales=0
                
            dias_trabajados = float((dias_trabajados * 8) - total_dias-total_dias_ingreso_egreso-total_dias_parciales) / 8

            #DIAS DEL MES TRABAJADOS
            html += '<td>' + str(dias_trabajados) + '</td>'
            if sueldo:
                html += '<td>' + str(sueldo.valor) + '</td>'

            else:
                html += '<td>0</td>'


            otros_ingresos_vacaciones = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=6).aggregate(Sum('valor'))
            if otros_ingresos_vacaciones['valor__sum']:
                html += '<td>' + str(otros_ingresos_vacaciones['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            otros_ingresos_comisiones = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=4).aggregate(Sum('valor'))

            otros_ingresos_bonificaciones = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=3).aggregate(Sum('valor'))


            otros_ingresos_alimentacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=1).aggregate(Sum('valor'))

            otros_ingresos_horas_extra_dom = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('valor'))

            otros_ingresos_horas_extra_sab = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('valor'))

            otros_ingresos_horas_suple = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('valor'))






            if otros_ingresos_comisiones['valor__sum']:
                html += '<td>' + str(otros_ingresos_comisiones['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_bonificaciones['valor__sum']:
                html += '<td>' + str(otros_ingresos_bonificaciones['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_alimentacion['valor__sum']:
                html += '<td>' + str(otros_ingresos_alimentacion['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_suple['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_suple['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_extra_sab['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_extra_sab['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_horas_extra_dom['valor__sum']:
                html += '<td>' + str(otros_ingresos_horas_extra_dom['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'



            ingresos_total = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if ingresos_total['valor__sum']:
                t_ingresoT = ingresos_total['valor__sum']
            else:
                t_ingresoT = 0

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                total_desc = float(faltas_injustificadas_valor['valor__sum'])
            else:
                total_desc = 0

            # total_ingresos = float(t_ingresoT - (total_desc))
            total_ingresos = float(t_ingresoT)


            sueldo_valor = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).aggregate(
                Sum('valor'))

            # if sueldo_valor['valor__sum']:
            #     html += '<td>' + str(sueldo_valor['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'

            otros_ingresos_total = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_ingresos_movilizacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=2).aggregate(Sum('valor'))

            otros_ingresos_freserva = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7).aggregate(Sum('valor'))



            otros_ingresos_dtercero = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))

            otros_ingresos_dcuarto = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))

            otros_ingresos_iasumido = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=27).aggregate(Sum('valor'))

            otros_ingresos_irenta = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))



            #TOTAL INGRESOS BASE IESS
            html += '<td><b>' + str(total_ingresos) + '</b></td>'

            #OTROS INGRESOS
            if otros_ingresos_dtercero['valor__sum']:
                html += '<td>' + str(otros_ingresos_dtercero['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_ingresos_dcuarto['valor__sum']:
                html += '<td>' + str(otros_ingresos_dcuarto['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_ingresos_freserva['valor__sum']:
                html += '<td>' + str(otros_ingresos_freserva['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'


            if otros_ingresos_movilizacion['valor__sum']:
                html += '<td>' + str(otros_ingresos_movilizacion['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_irenta['valor__sum']:
                html += '<td>' + str(otros_ingresos_irenta['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_iasumido['valor__sum']:
                html += '<td>' + str(otros_ingresos_iasumido['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_ingresos_total['valor__sum']:
                suma_ingresos_otros_ingresos = total_ingresos + float(
                    otros_ingresos_total['valor__sum'])
            else:
                suma_ingresos_otros_ingresos = total_ingresos

            html += '<td>' + str(suma_ingresos_otros_ingresos) + '</td>'

            #EGRESOS TOTALES
            egresos_total = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_total = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_nueve = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))
            otros_egresos_tres = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=30).aggregate(Sum('valor'))

            otros_egresos_atraso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_descir = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=20).aggregate(Sum('valor'))

            otros_egresos_falta = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_multa = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=21).aggregate(Sum('valor'))

            otros_egresos_hipotecario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=13).aggregate(Sum('valor'))

            otros_egresos_permiso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=40).aggregate(Sum('valor'))

            otros_egresos_quirografario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))


            otros_egresos_anticipo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))

            otros_egresos_anticipo_semanal = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=37).aggregate(Sum('valor'))

            otros_egresos_movistar = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

            otros_egresos_ptmo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))


            otros_egresos_otros = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

            otros_egresos_consumo_alimentos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=17).aggregate(Sum('valor'))

            otros_egresos_rfm_impuesto= EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=11).aggregate(Sum('valor'))


            otros_egresos_retenciones_judiciales = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=35).aggregate(Sum('valor'))

            otros_egresos_anticipo_funcionarios= EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=38).aggregate(Sum('valor'))


            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=3).aggregate(Sum('valor'))


            if faltas_injustificadas_valor['valor__sum']:
                faltas = float(faltas_injustificadas_valor['valor__sum'])
            else:
                faltas = 0

            if otros_egresos_nueve['valor__sum']:
                html += '<td>' + str(otros_egresos_nueve['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'


            if otros_egresos_anticipo_semanal['valor__sum']:
                html += '<td>' + str(otros_egresos_anticipo_semanal['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_anticipo['valor__sum']:
                html += '<td>' + str(otros_egresos_anticipo['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'





            if otros_egresos_rfm_impuesto['valor__sum']:
                html += '<td>' + str(otros_egresos_rfm_impuesto['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_tres['valor__sum']:
                html += '<td>' + str(otros_egresos_tres['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'



            if otros_egresos_quirografario['valor__sum']:
                html += '<td>' + str(otros_egresos_quirografario['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_hipotecario['valor__sum']:
                html += '<td>' + str(otros_egresos_hipotecario['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'


            if otros_egresos_retenciones_judiciales['valor__sum']:
                html += '<td>' + str(otros_egresos_retenciones_judiciales['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_anticipo_funcionarios['valor__sum']:
                html += '<td>' + str(otros_egresos_anticipo_funcionarios['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'





            atrasos = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).exclude(tipo_ausencia_id=2).exclude(tipo_ausencia_id=3).exclude(
                tipo_ausencia_id=1).aggregate(Sum('valor'))
            if atrasos['valor__sum']:
                atras = float(atrasos['valor__sum'])
            else:
                atras = 0


            # if otros_egresos_atraso['valor__sum']:
            #     html += '<td>' + str(otros_egresos_atraso['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'


            #html += '<td>' + str(faltas) + '</td>'
            if otros_egresos_movistar['valor__sum']:
                html += '<td>' + str(otros_egresos_movistar['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            if otros_egresos_ptmo['valor__sum']:
                html += '<td>' + str(otros_egresos_ptmo['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'


            if otros_egresos_multa['valor__sum']:
                html += '<td>' + str(otros_egresos_multa['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'

            if otros_egresos_consumo_alimentos['valor__sum']:
                html += '<td>' + str(otros_egresos_consumo_alimentos['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'



            faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
            permisos = 0
            permiso2 = 0
            
            if faltas_justificadas_valor['valor__sum']:
                permisos = float(faltas_justificadas_valor['valor__sum'])
            else:
                permisos = 0
            
            if otros_egresos_permiso['valor__sum']:
                permiso2 = float(permisos)+float(otros_egresos_permiso['valor__sum'])





            html += '<td>' + str(permiso2) + '</td>'


            # if otros_egresos_descir['valor__sum']:
            #     html += '<td>' + str(otros_egresos_descir['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'
            #
            # if otros_egresos_contribucion['valor__sum']:
            #     html += '<td>' + str(otros_egresos_contribucion['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'

            if otros_egresos_otros['valor__sum']:
                html += '<td>' + str(otros_egresos_otros['valor__sum']) + '</td>'
            else:
                html += '<td>0</td>'
            # if otros_egresos_falta['valor__sum']:
            #     html += '<td>' + str(otros_egresos_falta['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'


            # html+='<td>'+str(total_desc)+'</td>'

            if egresos_total['valor__sum']:
                egres_t = egresos_total['valor__sum']
            else:
                egres_t = 0

            if otros_egresos_total['valor__sum']:

                # html += '<td>' + str(otros_egresos_total['valor__sum']) + '</td>'
                otros_egre_t = otros_egresos_total['valor__sum']
            else:
                # html += '<td>0</td>'
                otros_egre_t = 0

            #suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos + total_desc
            suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos 
            html += '<td>' + str(suma_egresos_otros_egresos) + '</td>'
            # html+='<td>'+str(detal.otros_egresos)+'</td>'
            if suma_ingresos_otros_ingresos:
                suma_ingresos_otros_ingresos = suma_ingresos_otros_ingresos

            else:
                suma_ingresos_otros_ingresos = 0

            total_ingresos_base_sin_sueldo= IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).exclude(tipo_ingreso_egreso_empleado_id=24).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if total_ingresos_base_sin_sueldo['valor__sum']:
                t_ingreso_base_sin_sueldoT = total_ingresos_base_sin_sueldo['valor__sum']
            else:
                t_ingreso_base_sin_sueldoT = 0
                
            total_recibir_mensual = suma_ingresos_otros_ingresos - suma_egresos_otros_egresos
            html += '<td>' + str(total_recibir_mensual) + '</td>'
            html += '<td>' + str(detal.forma_pago_empleado) + '</td>'
            html += '<td>'+str(dias_trabajados)+'</td>'
            if sueldo:
                html += '<td>' + str(sueldo.valor) + '</td>'
                total_benef = round(float(t_ingreso_base_sin_sueldoT +sueldo.valor),2)

            else:
                html += '<td>0</td>'
                total_benef = round(float(t_ingreso_base_sin_sueldoT),2)
            html+='<td>'+str(t_ingreso_base_sin_sueldoT)+ '</td>'
            html += '<td>' + str(total_benef) + '</td>'
            decimo_tercer_provision=round(float(total_benef/12),2)
            
            
            # if detal.empleado.tipo_remuneracion_id == 2:
            #     mes_t=dias_trabajados/30
            #     total_anios=mes_t*12
            #     dcuarto=float(detalles.salario_base / 12)
            #     cuarto=(dcuarto*total_anios)/12
            #     
            # 
            # else:
            #     cuarto = round(float(detalles.salario_base / 12), 2)
            cuarto = round(float(detalles.salario_base / 12), 2)
        

            
            iess_provision = round(float(total_benef * 12.15 / 100), 2)
            decimo_tercer_provision_actual=0
            decimo_cuarto_provision_actual=0
            iess_provision_actual=0
            dvacaciones=float(total_benef/24)
            vacaciones = round(dvacaciones, 2)
            vacaciones_provision_actual=0
            fondo_reserva_actual=0
            
            
            fr_provision=0
            if detal.empleado.acumular_decimo_tercero:
                html += '<td>-</td>'
            else:
                html += '<td style="text-align:right">'+ str("%0.2f" % decimo_tercer_provision).replace('.', ',') + '</td>'
                decimo_tercer_provision_actual=decimo_tercer_provision
                

            if detal.empleado.acumular_decimo_cuarto:
                html += '<td>-</td>'
            else:
                if detal.empleado.tipo_remuneracion_id == 2:
                    mes_t=dias_trabajados/30
                    total_anios=mes_t*12
                    cuarto=(cuarto*total_anios)/12
                html += '<td style="text-align:right">'+ str("%0.2f" % cuarto).replace('.', ',') + '</td>'
                decimo_cuarto_provision_actual=cuarto
            
            html += '<td style="text-align:right">' + str("%0.2f" % vacaciones).replace('.', ',') + '</td>'

            if detal.empleado.acumular_fondo_reserva:
                print('NO ACUMULA')
                html += '<td>0</td>'
            else:
                if float(dias_c) >= 364:
                    if float(dias_c)>=394:
                        fr_provision=total_benef/12
                        html += '<td style="text-align:right">'+ str("%0.2f" % fr_provision).replace('.', ',') + '</td>'
                        fondo_reserva_actual=fr_provision
                    else:
                        proporcional=float(dias_c)-364
                        fr_provision=total_benef/12
                        proporcionaf=(fr_provision*proporcional)/30
                        html += '<td style="text-align:right">'+ str("%0.2f" % proporcionaf).replace('.', ',') + '</td>'
                        fr_provision=proporcionaf
                        fondo_reserva_actual=proporcionaf
                        
                
                else:
                    html += '<td style="text-align:right">0</td>'

            html += '<td style="text-align:right">' + str(iess_provision) + '</td>'
            provision_total=decimo_tercer_provision_actual+decimo_cuarto_provision_actual+iess_provision+fondo_reserva_actual+vacaciones
            html += '<td style="text-align:right">' + str(provision_total) + '</td>'




        context = {
            'html': html,
            'anio': anio,
            'mes': mes,
            'id': pk,

        }
        return render_to_response('roles_pago/verRolGlobalActual.html', context, context_instance=RequestContext(request))

@login_required()
def DeudaEmpleadoListView(request):
    row = DeudasEmpleado.objects.all().order_by('fecha_emision')
    return render_to_response('deudas_empleado/index.html', {'row': row}, RequestContext(request))
    
    
@login_required()
def DeudaEmpleadoCreateview(request):
    if request.method == 'POST':
        form =DeudasEmpleadoForm(request.POST)
        try:
            if form.is_valid():

                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    movimiento = DeudasEmpleado()
                    movimiento.empleado_id = int(cleaned_data.get('empleado').empleado_id)
                    movimiento.tipo_ingreso_egreso_empleado_id = int(request.POST['tipo_egreso'])
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    desp=cleaned_data.get('descripcion')
                    movimiento.descripcion = desp.replace("\n", " ")
                    movimiento.valor_mensual = request.POST['monto']
                    movimiento.valor_total = request.POST['monto']
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = datetime.now()
                    movimiento.updated_at = datetime.now()
                    movimiento.activo=True
                    movimiento.save()
                    
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        print 'anio ='+str (datetime.now().year)
                        asiento = Asiento()
                        asiento.codigo_asiento = "RRHH"+str(datetime.now().year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE DEUDAS EMPLEADO  ' 
                        asiento.modulo='RRHH-DEUDAS EMPLEADO'
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.updated_by = request.user.get_full_name()
                        asiento.created_at = datetime.now()
                        asiento.updated_at = datetime.now()
                        
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']

                            asiento_detalle.save()
                    
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
        
        
        item = {
            'id': movimiento.id,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")

    else:
        print 'entro'
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        tipo_egresos = TipoIngresoEgresoEmpleado.objects.filter(egreso = True)
        empleados = Empleado.objects.filter(activo = True)
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        centros = CentroCosto.objects.all()
        form = DeudasEmpleadoForm
        template = loader.get_template('deudas_empleado/create.html')
        context = RequestContext(request, {'form': form, 'tipo_egresos': tipo_egresos, 'empleados': empleados,'centros_defecto':centros_defecto,
                                           'centros':centros,
                                           'cuentas': cuentas,})
        return HttpResponse(template.render(context))



@login_required()
def deudaEmpleadoEliminarByPkView(request, pk):
    obj = DeudasEmpleado.objects.get(id=pk)

    if obj:
        obj.activo = False
        obj.save()
       
        try:
            asiento = Asiento.objects.filter(asiento_id=obj.asiento_id)
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            for a in asiento:
                a.anulado= True
                a.save()
            

    return HttpResponseRedirect('/recursos_humanos/deuda_empleado')



@login_required()
def imprimirComprobanteDeuda(request, pk):
    form = DeudasEmpleado.objects.get(id=pk)
    html = ''
    html += '<table border="0"><tr><td width="150"><img src="media/imagenes/general/cesa_logo.jpg" alt="logo producto" width="150" height="50"></td><td style="text-align:center"colspan="6" >'
    html += 'MUEBLES Y DIVERSIDADES<br />MUEDIRSA S.A. <br /></td></tr>'
    html += '<tr><td colspan="8"></td></tr>'
    html += '<tr><td colspan="8"><b>DATOS</b> </td></tr>'
    html += '<tr><td colspan="2"><b>Fecha de solicitud:</b></td><td colspan="6" style="text-align:left">' + str(form.fecha_emision) + '</td></tr>'
    html += '<tr><td colspan="2"><b>Nombre del colaborador:</b></td><td colspan="3">' + str(form.empleado.nombre_empleado.encode('utf8')) + '</td><td colspan="2">Fecha de Ingreso:</td><td colspan="2">' + str(form.empleado.fecha_ini_reconocida) + '</td></tr>'
    html += '<tr><td colspan="2"><b>Cargo/Area:</b></td><td colspan="3">' + str(form.empleado.tipo_empleado.cargo_empleado) + '</td><td colspan="2"></td><td colspan="2"></td></tr>'
    html += '<tr><td colspan="2"><b>Valor del Anticipo:</b></td><td colspan="3">' + str(form.valor_mensual) + '</td><td colspan="4"></tr>'
    html += '<tr><td colspan="2"><b>MOTIVO DEL ANTICIPO</b></td>'
    html += '<td colspan="6" style="text-align:left">' + str(form.tipo_ingreso_egreso_empleado.nombre) + '</td></tr>'
    html += '<tr><td colspan="8" style="text-align:left">' + str(form.descripcion) + '</td></tr>'
    html += '</tbody></table>'
    html += '<br><br><table><tr><td>-----------------<br>Elaborado por</td><td>-----------------<br>Visto Bueno</td><td>-----------------<br>Aprobado por</td></tr></table>'


    html1 = render_to_string('deudas_empleado/imprimir.html', {'pagesize': 'A4', 'html': html,},
                             context_instance=RequestContext(request))
    return generar_pdf(html1)




@login_required()
def PagoDeudaEmpleadoListView(request):
    row = DeudasEmpleado.objects.all().order_by('fecha_emision')
    return render_to_response('deudas_empleado/pago_index.html', {'row': row}, RequestContext(request))
    
    
@login_required()
def PagodeDeudaEmpleadoCreateview(request):
    if request.method == 'POST':
        form =DeudasEmpleadoForm(request.POST)
        try:
            if form.is_valid():

                with transaction.atomic():
                    cleaned_data = form.cleaned_data
                    movimiento = DeudasEmpleado()
                    movimiento.empleado_id = int(cleaned_data.get('empleado').empleado_id)
                    movimiento.tipo_ingreso_egreso_empleado_id = int(request.POST['tipo_egreso'])
                    movimiento.fecha_emision = cleaned_data.get('fecha_emision')
                    desp=cleaned_data.get('descripcion')
                    movimiento.descripcion = desp.replace("\n", " ")
                    movimiento.valor_mensual = request.POST['monto']
                    movimiento.valor_total = request.POST['monto']
                    movimiento.created_by = request.user.get_full_name()
                    movimiento.updated_by = request.user.get_full_name()
                    movimiento.created_at = datetime.now()
                    movimiento.updated_at = datetime.now()
                    movimiento.activo=True
                    movimiento.save()
                    
                    asientos = json.loads(request.POST['arreglo_asientos'])
                    print asientos
                    if len(asientos) > 0:
                        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
                        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
                        print 'secuencial = %s' % (codigo_asiento)
                        print 'anio ='+str (datetime.now().year)
                        asiento = Asiento()
                        asiento.codigo_asiento = "RRHH"+str(datetime.now().year)+"00"+str(codigo_asiento)
                        asiento.fecha = cleaned_data.get('fecha_emision')
                        asiento.glosa = 'MOVIMIENTO MÓDULO DE DEUDAS EMPLEADO  ' 
                        asiento.modulo='RRHH-DEUDAS EMPLEADO'
                        asiento.gasto_no_deducible = False
                        asiento.secuencia_asiento = codigo_asiento
                        total_debe=request.POST['total_debe']
                        total_haber=request.POST['total_haber']
                        asiento.total_debe = total_debe
                        asiento.total_haber = total_haber
                        asiento.created_by = request.user.get_full_name()
                        asiento.updated_by = request.user.get_full_name()
                        asiento.created_at = datetime.now()
                        asiento.updated_at = datetime.now()
                        
                        asiento.save()
                        movimiento.asiento_id=asiento.asiento_id
                        movimiento.save()
                        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
                        print 'total_debe = %s' %(total_debe)
                        print 'total_haber = %s' %(total_haber)
                        for item_asiento in asientos:
                            print item_asiento['id_plancuenta']
                            print item_asiento['debe']
                            print item_asiento['haber']
                            print asiento.asiento_id
                            asiento_detalle = AsientoDetalle()
                            asiento_detalle.asiento_id = asiento.asiento_id
                            asiento_detalle.cuenta_id = item_asiento['id_plancuenta']
                            asiento_detalle.debe = item_asiento['debe']
                            asiento_detalle.haber = item_asiento['haber']
                            asiento_detalle.concepto = item_asiento['concepto']
                            asiento_detalle.centro_costo_id = item_asiento['centro']

                            asiento_detalle.save()
                    
            else:
                form_errors = form.errors
                print form_errors
        except Exception as e:
            print (e.message)
        
        
        item = {
            'id': movimiento.id,
        }
        json_resultados = json.dumps(item)
   
        return HttpResponse(json_resultados, content_type="application/json")

    else:
        print 'entro'
        cuentas = PlanDeCuentas.objects.filter(activo=True).exclude(categoria='GENERAL')
        tipo_egresos = TipoIngresoEgresoEmpleado.objects.filter(egreso = True)
        empleados = Empleado.objects.filter(activo = True)
        centros_defecto = CentroCosto.objects.filter(por_defecto=True).first()
        centros = CentroCosto.objects.all()
        form = DeudasEmpleadoForm
        row = DeudasEmpleado.objects.all()
        template = loader.get_template('deudas_empleado/pago_empleado.html')
        context = RequestContext(request, {'form': form, 'tipo_egresos': tipo_egresos, 'empleados': empleados,'centros_defecto':centros_defecto,
                                           'centros':centros,'row':row,
                                           'cuentas': cuentas,})
        return HttpResponse(template.render(context))



@login_required()
@csrf_exempt
def verRolGlobalPrevio(request, pk,ck):
    if request.method == 'POST':
        html=''
    else:
        empleados = Empleado.objects.filter(activo=True).order_by('nombre_empleado')
        mes = ck
        anio = pk
        i = 0
        html = ''
        final_ingresos = 0
        final_otros_ingresos = 0
        final_egresos = 0
        final_otros_egresos = 0
        final_total = 0
        
        for detal in empleados:
            i += 1
            try:
                sueldo = IngresosRolEmpleado.objects.filter( anio=anio).filter( mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).first()
            except IngresosRolEmpleado.DoesNotExist:
                sueldo = 0
            html += '<tr>'
            html += '<td>' + str(i) + '</td>'
            html += '<td>' + str(detal.nombre_empleado.encode('utf8')) + '</td>'
            html += '<td>' + str(detal.cedula_empleado) + '</td>'
            html += '<td>' + str(detal.departamento) + '</td>'
            html += '<td>' + str(detal.tipo_empleado) + '</td>'
            html += '<td>' + str(detal.fecha_ini_reconocida) + '</td>'
            html += '<td>' + str(detal.fecha_fin) + '</td>'
            
            if detal.acumular_decimo_tercero:
                html += '<td>NO</td>'
            else:
                html += '<td>SI</td>'

            #hoy = date.today()  # Asigna fecha actual
            hoy=date(int(anio),int(mes), 30)
            ayer = detal.fecha_ini_reconocida
            if ayer:
                diferencia_en_dias = hoy-ayer

                dias_comp= str(diferencia_en_dias).split('days')
                dias_c=dias_comp[0]
            else:
                diferencia_en_dias=0
                dias_c=0

            html += '<td>'
            if int(dias_c)>=  364:
                html+='SI'
            else:
                html += 'NO'

            #html+=str(diferencia_en_dias)
            html+='</td>'
            if detal.acumular_fondo_reserva:
                html += '<td>NO</td>'
            else:
                html += '<td>SI</td>'

            html += '<td>30</td>'
            i += 1
            ingresosPro = IngresosProyectadosEmpleado.objects.filter(empleado_id=detal.empleado_id)
            try:
                sueldo0 = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                 empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)
            except IngresosRolEmpleado.DoesNotExist:
                sueldo0 = ingresosPro[0]
                
            if detal.fecha_fin:
                try:
                    sueldo0 = IngresosRolEmpleado.objects.get(anio=anio, mes=mes,
                                                                 empleado_id=detal.empleado_id,
                                                                 tipo_ingreso_egreso_empleado_id=24)
                except IngresosRolEmpleado.DoesNotExist:
                    sueldo0 = ingresosPro[0]
                formato_fecha = "%d-%m-%Y"
                echa_comparar="30-"+mes+"-"+anio
                    
                fecha_fin_contrato = detal.fecha_fin
                fecha_comparar_modif=date(int(anio), int(mes), 30)
                    
                if fecha_fin_contrato:
                    diferencia=fecha_fin_contrato-fecha_comparar_modif
                if diferencia:
                    diferencia=diferencia.days* (-1)*8
                    try:
                        dias_no_t = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ausencia_id=7)
                    except DiasNoLaboradosRolEmpleado.DoesNotExist:
                        dias_no_t = None
                        
                   
                            
                        
            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=3).aggregate(Sum('valor'))
            faltas_ingreso_egreso_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=7).aggregate(Sum('valor'))

            vacaciones_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    cargar_vacaciones=False).filter(tipo_ausencia_id=1).aggregate(Sum('valor'))
            dias_parciales_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                    anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                    tipo_ausencia_id=8).aggregate(Sum('valor'))
            

            descont_dias=0
            if faltas_injustificadas_valor['valor__sum']:
                descont_dias = faltas_injustificadas_valor['valor__sum']
                
            if faltas_ingreso_egreso_valor['valor__sum']:
                descont_dias = descont_dias+faltas_ingreso_egreso_valor['valor__sum']

            if vacaciones_justificadas_valor['valor__sum']:
                descont_dias = descont_dias + vacaciones_justificadas_valor['valor__sum']
                
            if dias_parciales_valor['valor__sum']:
                descont_dias = descont_dias + dias_parciales_valor['valor__sum']
                


            if sueldo:
                html += '<td>' + str(sueldo0.valor_mensual) + '</td>'

            else:
                html += '<td>0</td>'

            dias_trabajados = 30
            dias = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=3).aggregate(Sum('dias'))
            dias_ingreso_egreso = DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=7).aggregate(Sum('dias'))
            dias_parciales= DiasNoLaboradosRolEmpleado.objects.filter(anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(tipo_ausencia_id=8).aggregate(Sum('dias'))
            if dias['dias__sum']:
                total_dias = float(dias['dias__sum'])
            else:
                total_dias=0
                    
            if dias_ingreso_egreso['dias__sum']:
                total_dias_ingreso_egreso=float(dias_ingreso_egreso['dias__sum'])
            else:
                total_dias_ingreso_egreso=0
                
            if dias_parciales['dias__sum']:
                total_dias_parciales=float(dias_parciales['dias__sum'])
            else:
                total_dias_parciales=0
                
            dias_trabajados = float((dias_trabajados * 8) - total_dias-total_dias_ingreso_egreso-total_dias_parciales) / 8
                
                
            html += '<td>' + str(dias_trabajados) + '</td>'
            try:
                sueldofinal = IngresosRolEmpleado.objects.filter( anio=anio).filter( mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).first()
            except IngresosRolEmpleado.DoesNotExist:
                sueldofinal = 0
            if sueldofinal:
                html += '<td style="text-align:right">' +str("%0.2f" % sueldofinal.valor).replace('.', ',') + '</td>'

            else:
                html += '<td style="text-align:right">0</td>'


            otros_ingresos_vacaciones = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=6).aggregate(Sum('valor'))
            if otros_ingresos_vacaciones['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" % otros_ingresos_vacaciones['valor__sum']).replace('.', ',')  + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            otros_ingresos_comisiones = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=4).aggregate(Sum('valor'))

            otros_ingresos_bonificaciones = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=3).aggregate(Sum('valor'))


            otros_ingresos_alimentacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=1).aggregate(Sum('valor'))

            otros_ingresos_horas_extra_dom = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=26).aggregate(
                Sum('valor'))

            otros_ingresos_horas_extra_sab = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=25).aggregate(
                Sum('valor'))

            otros_ingresos_horas_suple = IngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(pagar=True).filter(tipo_ingreso_egreso_empleado_id=5).aggregate(
                Sum('valor'))






            if otros_ingresos_comisiones['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" % otros_ingresos_comisiones['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_bonificaciones['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" % otros_ingresos_bonificaciones['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_alimentacion['valor__sum']:
                html += '<td> style="text-align:right">'+str("%0.2f" % otros_ingresos_alimentacion['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_horas_suple['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" % otros_ingresos_horas_suple['valor__sum']).replace('.', ',')+ '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_horas_extra_sab['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" % otros_ingresos_horas_extra_sab['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_horas_extra_dom['valor__sum']:
                html += '<td style="text-align:right">'+str("%0.2f" %otros_ingresos_horas_extra_dom['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'



            ingresos_total = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if ingresos_total['valor__sum']:
                t_ingresoT = ingresos_total['valor__sum']
            else:
                t_ingresoT = 0

            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                tipo_ausencia_id=3).aggregate(Sum('valor'))

            if faltas_injustificadas_valor['valor__sum']:
                total_desc = float(faltas_injustificadas_valor['valor__sum'])
            else:
                total_desc = 0

            # total_ingresos = float(t_ingresoT - (total_desc))
            total_ingresos = float(t_ingresoT)


            sueldo_valor = IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=24).aggregate(
                Sum('valor'))

            # if sueldo_valor['valor__sum']:
            #     html += '<td>' + str(sueldo_valor['valor__sum']) + '</td>'
            # else:
            #     html += '<td>0</td>'

            otros_ingresos_total = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_ingresos_movilizacion = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=2).aggregate(Sum('valor'))

            otros_ingresos_freserva = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=7).aggregate(Sum('valor'))



            otros_ingresos_dtercero = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=8).aggregate(Sum('valor'))

            otros_ingresos_dcuarto = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=9).aggregate(Sum('valor'))

            otros_ingresos_iasumido = OtrosIngresosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=27).aggregate(Sum('valor'))

            otros_ingresos_irenta = OtrosIngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))



            #TOTAL INGRESOS BASE IESS
            html += '<td style="text-align:right"><b>' + str("%0.2f" % total_ingresos).replace('.', ',') + '</b></td>'

            #OTROS INGRESOS
            if otros_ingresos_dtercero['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_dtercero['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_ingresos_dcuarto['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_dcuarto['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_ingresos_freserva['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_freserva['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'


            if otros_ingresos_movilizacion['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_movilizacion['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_irenta['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_irenta['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_iasumido['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_ingresos_iasumido['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_ingresos_total['valor__sum']:
                suma_ingresos_otros_ingresos = total_ingresos + float(
                    otros_ingresos_total['valor__sum'])
            else:
                suma_ingresos_otros_ingresos = total_ingresos

            html += '<td style="text-align:right">' + str("%0.2f" % suma_ingresos_otros_ingresos).replace('.', ',') + '</td>'

            #EGRESOS TOTALES
            egresos_total = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_total = OtrosEgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).aggregate(Sum('valor'))

            otros_egresos_nueve = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=29).aggregate(Sum('valor'))
            otros_egresos_tres = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=30).aggregate(Sum('valor'))

            otros_egresos_atraso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_descir = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=20).aggregate(Sum('valor'))

            otros_egresos_falta = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=28).aggregate(Sum('valor'))

            otros_egresos_multa = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=21).aggregate(Sum('valor'))

            otros_egresos_hipotecario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=13).aggregate(Sum('valor'))

            otros_egresos_permiso = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=40).aggregate(Sum('valor'))

            otros_egresos_quirografario = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=14).aggregate(Sum('valor'))


            otros_egresos_anticipo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=12).aggregate(Sum('valor'))

            otros_egresos_anticipo_semanal = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=37).aggregate(Sum('valor'))

            otros_egresos_movistar = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=19).aggregate(Sum('valor'))

            otros_egresos_ptmo = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=15).aggregate(Sum('valor'))


            otros_egresos_otros = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=23).aggregate(Sum('valor'))

            otros_egresos_consumo_alimentos = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=17).aggregate(Sum('valor'))

            otros_egresos_rfm_impuesto= EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=11).aggregate(Sum('valor'))


            otros_egresos_retenciones_judiciales = EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=35).aggregate(Sum('valor'))

            otros_egresos_anticipo_funcionarios= EgresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(
                empleado_id=detal.empleado_id).filter(tipo_ingreso_egreso_empleado_id=38).aggregate(Sum('valor'))


            faltas_injustificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=3).aggregate(Sum('valor'))


            if faltas_injustificadas_valor['valor__sum']:
                faltas = float(faltas_injustificadas_valor['valor__sum'])
            else:
                faltas = 0

            if otros_egresos_nueve['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_nueve['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'


            if otros_egresos_anticipo_semanal['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_anticipo_semanal['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_anticipo['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_anticipo['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'





            if otros_egresos_rfm_impuesto['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_rfm_impuesto['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_tres['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_tres['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'



            if otros_egresos_quirografario['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_quirografario['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_hipotecario['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_hipotecario['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'


            if otros_egresos_retenciones_judiciales['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_retenciones_judiciales['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_anticipo_funcionarios['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_anticipo_funcionarios['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'





            atrasos = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).exclude(tipo_ausencia_id=2).exclude(tipo_ausencia_id=3).exclude(
                tipo_ausencia_id=1).aggregate(Sum('valor'))
            if atrasos['valor__sum']:
                atras = float(atrasos['valor__sum'])
            else:
                atras = 0


            
            if otros_egresos_movistar['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_movistar['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            if otros_egresos_ptmo['valor__sum']:
                html += '<td style="text-align:right">' +str("%0.2f" % otros_egresos_ptmo['valor__sum']).replace('.', ',')+ '</td>'
            else:
                html += '<td style="text-align:right">0</td>'


            if otros_egresos_multa['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_multa['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'

            if otros_egresos_consumo_alimentos['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_consumo_alimentos['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'



            faltas_justificadas_valor = DiasNoLaboradosRolEmpleado.objects.filter(
                anio=anio).filter(mes=mes).filter(empleado_id=detal.empleado_id).filter(descontar=True).filter(
                cargar_vacaciones=False).filter(tipo_ausencia_id=2).aggregate(Sum('valor'))
            permisos=0
            permisos2=0
            
            
            if faltas_justificadas_valor['valor__sum']:
                permisos = float(faltas_justificadas_valor['valor__sum'])
            else:
                permisos = 0
                
                
            if otros_egresos_permiso['valor__sum']:
                permisos2 = float(permisos)+float(otros_egresos_permiso['valor__sum'])
            




            html += '<td>' + str(permisos2) + '</td>'


            

            if otros_egresos_otros['valor__sum']:
                html += '<td style="text-align:right">' + str("%0.2f" % otros_egresos_otros['valor__sum']).replace('.', ',') + '</td>'
            else:
                html += '<td style="text-align:right">0</td>'
            
            if egresos_total['valor__sum']:
                egres_t = egresos_total['valor__sum']
            else:
                egres_t = 0

            if otros_egresos_total['valor__sum']:

                # html += '<td>' + str(otros_egresos_total['valor__sum']) + '</td>'
                otros_egre_t = otros_egresos_total['valor__sum']
            else:
                # html += '<td>0</td>'
                otros_egre_t = 0

            #suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos + total_desc
            suma_egresos_otros_egresos = egres_t + otros_egre_t + permisos 
            html += '<td style="text-align:right">' + str("%0.2f" % suma_egresos_otros_egresos).replace('.', ',') + '</td>'
            # html+='<td>'+str(detal.otros_egresos)+'</td>'
            if suma_ingresos_otros_ingresos:
                suma_ingresos_otros_ingresos = suma_ingresos_otros_ingresos

            else:
                suma_ingresos_otros_ingresos = 0

            total_ingresos_base_sin_sueldo= IngresosRolEmpleado.objects.filter(anio=anio).filter(
                mes=mes).filter(empleado_id=detal.empleado_id).exclude(tipo_ingreso_egreso_empleado_id=24).filter(pagar=True).aggregate(Sum('valor'))
            # html += '<td>' + str(detal.dias) + '</td>'

            if total_ingresos_base_sin_sueldo['valor__sum']:
                t_ingreso_base_sin_sueldoT = total_ingresos_base_sin_sueldo['valor__sum']
            else:
                t_ingreso_base_sin_sueldoT = 0
                
            total_recibir_mensual = suma_ingresos_otros_ingresos - suma_egresos_otros_egresos
            html += '<td style="text-align:right">' + str("%0.2f" % total_recibir_mensual).replace('.', ',') + '</td>'
            html += '<td >' + str(detal.forma_pago_empleado) + '</td>'
            html += '<td >'+str(dias_trabajados)+'</td>'
            if sueldo:
                html += '<td style="text-align:right">' + str("%0.2f" % sueldo.valor).replace('.', ',') + '</td>'
                total_benef = round(float(t_ingreso_base_sin_sueldoT +sueldo.valor),2)

            else:
                html += '<td style="text-align:right">0</td>'
                total_benef = round(float(t_ingreso_base_sin_sueldoT),2)
            html+='<td style="text-align:right">'+str("%0.2f" % t_ingreso_base_sin_sueldoT).replace('.', ',')+ '</td>'
            html += '<td style="text-align:right">' + str("%0.2f" % total_benef).replace('.', ',') + '</td>'
            dterceroprov=float(total_benef/12)
            decimo_tercer_provision=round(dterceroprov,2)
            dc_id = SueldosUnificados.objects.last()
            
            if detal.tipo_remuneracion_id == 2:
                mes_t=dias_trabajados/30
                total_anios=mes_t*12
                dcuarto=float(dc_id.sueldo/ 12)
                dcuarto=(dcuarto*total_anios)/12
            
            else:
                dcuarto=float(dc_id.sueldo/ 12)
            cuarto = round(dcuarto, 2)
            diess_provision=float(total_benef * 12.15 / 100)
            iess_provision = round(diess_provision, 2)
            dvacaciones=float(total_benef/24)
            vacaciones = round(dvacaciones, 2)
            decimo_tercer_provision_actual=0
            decimo_cuarto_provision_actual=0
            iess_provision_actual=0
            vacaciones_provision_actual=0
            fondo_reserva_actual=0
            
            fr_provision=0
            if detal.acumular_decimo_tercero:
                html += '<td>-</td>'
            else:
                html += '<td style="text-align:right">' + str("%0.2f" % decimo_tercer_provision).replace('.', ',') + '</td>'
                decimo_tercer_provision_actual=decimo_tercer_provision

            if detal.acumular_decimo_cuarto:
                html += '<td>-</td>'
            else:
                
                html += '<td style="text-align:right">' + str("%0.2f" % cuarto).replace('.', ',') + '</td>'
                decimo_cuarto_provision_actual=cuarto
            
            html += '<td style="text-align:right">' + str("%0.2f" % vacaciones).replace('.', ',') + '</td>'

            if detal.acumular_fondo_reserva:
                html += '<td style="text-align:right">0</td>'
            else:
                if float(dias_c) >= 364:
                    if float(dias_c)>=394:
                        fr_provision=total_benef/12
                        html += '<td style="text-align:right">'+ str("%0.2f" % fr_provision).replace('.', ',') + '</td>'
                        fondo_reserva_actual=fr_provision
                    else:
                        proporcional=float(dias_c)-364
                        fr_provision=total_benef/12
                        proporcionaf=(fr_provision*proporcional)/30
                        html += '<td style="text-align:right">'+ str("%0.2f" % proporcionaf).replace('.', ',') + '</td>'
                        fr_provision=proporcionaf
                        fondo_reserva_actual=proporcionaf
                        
                else:
                    html += '<td style="text-align:right">0</td>'

            html += '<td style="text-align:right">' + str("%0.2f" % iess_provision).replace('.', ',') + '</td>'
            provision_total=decimo_tercer_provision_actual+decimo_cuarto_provision_actual+iess_provision+fondo_reserva_actual+vacaciones
            html += '<td style="text-align:right">' + str("%0.2f" % provision_total).replace('.', ',') + '</td>'




        context = {
            'html': html,
            'anio': anio,
            'mes': mes,
            'id': pk,

        }
        return render_to_response('roles_pago/verRolGlobalPrevio.html', context, context_instance=RequestContext(request))


@login_required()
def SueldosUnificadosListView(request):
    sueldos = SueldosUnificados.objects.all()
    return render_to_response('sueldos/index.html', {'sueldos': sueldos}, RequestContext(request))
   

# =====================================================#

class SueldosUnificadosCreateView(ObjectCreateView):
    model = SueldosUnificados
    form_class = SueldosUnificadosForm
    template_name = 'sueldos/create.html'
    url_success = 'sueldos-list'
    url_success_other = 'sueldos-create'
    url_cancel = 'sueldos-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.created_at = datetime.now()
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(SueldosUnificadosCreateView, self).form_valid(form)

    def get_success_url(self):
        mensaje = "Ha ingresado 1 nuevo sueldo."
        messages.success(self.request, mensaje)

        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


# =====================================================#

class SueldosUnificadosUpdateView(ObjectUpdateView):
    model = SueldosUnificados
    form_class = SueldosUnificadosForm
    template_name = 'sueldos/create.html'
    url_success = 'sueldos-list'
    url_cancel = 'sueldos-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.updated_by = self.request.user
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Sueldo actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)


@login_required()
@csrf_exempt
def eliminarTipoRolView(request):

        tipos= TipoIngresoEgresoEmpleado.objects.exclude(id=24).exclude(id=6).order_by('nombre')
        anio=Anio.objects.all()
        return render_to_response('roles_pago/eliminarTipoIngresoEgresoRol.html',
                                  {'tipos': tipos, 'anio': anio}, RequestContext(request))

@login_required()
@csrf_exempt
def eliminarTipoRol(request):
    if request.method == 'POST':
       
        banco = Banco.objects.all()
        mes = request.POST["mes"]
        anio = request.POST["anio"]
        tipo = request.POST["tipo"]
        i = 0
        html = ''
        
        error=''

        try:
            rol = RolPago.objects.get(anio=anio, mes=mes)
        except RolPago.DoesNotExist:
            rol = None

        if rol:
            html += '<h3>No  se puede eliminar porque ya se genero ese rol. Puede revisarlo en la opcion de Consultar Rol de Pago.</h3>'
        else:
            count=0
            
            try:
                tipo = TipoIngresoEgresoEmpleado.objects.get(id=tipo)
            except IngresosRolEmpleado.DoesNotExist:
                tipo=None
                
            if tipo:
                print tipo.id
                if tipo.ingreso:
                    print 'entro a ingreso'
                    try:
                        ingresos = IngresosRolEmpleado.objects.filter(anio=anio, mes=mes,
                                                                 tipo_ingreso_egreso_empleado_id=tipo)
                    except IngresosRolEmpleado.DoesNotExist:
                        ingresos=None
                    count=0
                    if ingresos:
                        for ing in ingresos:
                            ing.delete()
                            count=count+1
                    
                
                if tipo.otros_ingresos:
                    print 'entro a otros ingreso'
                    try:
                        otros_ingresos = OtrosIngresosRolEmpleado.objects.filter(anio=anio, mes=mes,
                                                                 tipo_ingreso_egreso_empleado_id=tipo)
                    except OtrosIngresosRolEmpleado.DoesNotExist:
                        otros_ingresos=None
                    count=0
                    if otros_ingresos:
                        for oing in otros_ingresos:
                            oing.delete()
                            count=count+1
                            
                    
                    
                
                if tipo.egreso:
                    print 'entro a egreso'
                    try:
                        egresos = EgresosRolEmpleado.objects.filter(anio=anio, mes=mes,
                                                                 tipo_ingreso_egreso_empleado_id=tipo)
                    except EgresosRolEmpleado.DoesNotExist:
                        egresos=None
                    if egresos:
                        for eg in egresos:
                            eg.delete()
                            count=count+1
                
                
                try:
                    plantillas_detalle = PlantillaRrhhDetalle.objects.filter(tipo_ingreso_egreso_empleado_id=tipo)
                except PlantillaRrhhDetalle.DoesNotExist:
                    plantillas_detalle = None

                if plantillas_detalle:
                    for p in plantillas_detalle:
                        
                    
                        try:
                            rol_pago = RolPagoPlantilla.objects.filter(plantilla_rrhh_id=p.plantilla_rrhh_id).filter(mes=mes).filter(anio=anio)
                        except RolPagoPlantilla.DoesNotExist:
                            rol_pago = None
                        if rol_pago:
                            print 'se elimino'
                            rol_pago.delete()

            html += '<h3>Se eliminaron '+str(count)+' registros</h3>'
        return HttpResponse(
            html
        )
    