# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from login.lib.tools_view import ObjectListView, ObjectCreateView, ObjectDetailView, ObjectUpdateView, eliminarView, eliminarByPkView,cambiarEstadoByPkView
from django.core.urlresolvers import reverse_lazy
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
from config.models import *
from inventario.models import *
from datetime import datetime, timedelta
from proveedores.models import *
from empleados.models import *
from django.db import connection, transaction
from transacciones.models import *
import pyodbc
from django.utils.encoding import smart_str, smart_unicode



from login.lib.tools import Tools

from config.models import Mensajes
from django.template import RequestContext
from django.forms.extras.widgets import *
from django.contrib import auth


@login_required()
def ambientesListView(request):
    ambientes = Ambiente.objects.all().order_by('id')


    return render_to_response('ambientes/index.html', {'ambientes': ambientes}, RequestContext(request))

#=====================================================#
class ambientesDetailView(ObjectDetailView):
    model = Ambiente
    template_name = 'ambientes/detail.html'

#=====================================================#
@login_required()
def ambientesCreateView(request):
    if request.method == 'POST':
        proforma_form = AmbienteForm(request.POST)

        if proforma_form.is_valid():
            new_orden = proforma_form.save()
            new_orden.created_by = request.user.get_full_name()
            new_orden.updated_by = request.user.get_full_name()
            new_orden.created_at = datetime.now()
            new_orden.updated_at = datetime.now()
            new_orden.save()
            try:
                secuencial = Secuenciales.objects.get(modulo='ambiente')
                secuencial.secuencial=secuencial.secuencial+1
                secuencial.created_by = request.user.get_full_name()
                secuencial.updated_by = request.user.get_full_name()
                secuencial.created_at = datetime.now()
                secuencial.updated_at = datetime.now()
                secuencial.save()
            except Secuenciales.DoesNotExist:
                secuencial = None


            return HttpResponseRedirect('/ambiente/ambiente')
        else:
            print 'error'
            print proforma_form.errors, len(proforma_form.errors)
    else:
        proforma_form = AmbienteForm

    return render_to_response('ambientes/create.html', {'form': proforma_form, }, RequestContext(request))


#=====================================================#
class ambientesUpdateView(ObjectUpdateView):
    model = Ambiente
    form_class = AmbienteForm
    template_name = 'ambientes/create.html'
    url_success = 'ambientes-list-list'
    url_cancel = 'ambientes-list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.updated_at = datetime.now()
        self.object.save()

        return super(ObjectUpdateView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Ambiente actualizada con exito')
        if '_addanother' in self.request.POST and self.request.POST['_addanother']:
            return reverse_lazy(self.url_success_other)
        else:
            return reverse_lazy(self.url_success)
#=====================================================#
@login_required()
def ambientesEliminarView(request):
    return eliminarView(request, Ambiente, 'ambientes-list')

#=====================================================#
@login_required()
def ambientesEliminarByPkView(request, pk):
    objetos = Ambiente.objects.filter(id__in = pk)
    for obj in objetos:
        if obj.activo:
            obj.activo = False
        else:
            obj.activo= True

        obj.save()

    return HttpResponseRedirect('/ambiente/ambiente')

def MigracionPlanCuentas(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                s=x[1]

                try:
                    cliente = PlanDeCuentas.objects.get(codigo_plan=x[0])

                except PlanDeCuentas.DoesNotExist:
                    cliente = None
                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    #row = cursor.execute();


                    cliente.codigo_plan=x[0]
                    cliente.nombre_plan=x[1].decode('unicode-escape')
                    try:
                        padre = PlanDeCuentas.objects.get(codigo_plan=x[2])

                    except PlanDeCuentas.DoesNotExist:
                        padre = None
                    if padre:
                        cliente.grupo_id=padre.plan_id
                    cliente.nivel_padre = x[2]
                    cliente.descripcion=x[3]
                    if x[4].isdigit():
                        cliente.nivel = int(x[4])
                    cliente.calificacion=x[5]
                    cliente.created_by = request.user.get_full_name()
                    cliente.updated_by = request.user.get_full_name()
                    cliente.created_at = datetime.now()
                    cliente.updated_at = datetime.now()
                    cliente.activo=True
                    cliente.tipo_cuenta_id = 1
                    cliente.save()

                else:

                    cliente= PlanDeCuentas()
                    cliente.codigo_plan = x[0]
                    cliente.nombre_plan = x[1].decode('unicode-escape')
                    cliente.nivel_padre = x[2]
                    cliente.descripcion = x[3]
                    try:
                        padre = PlanDeCuentas.objects.get(codigo_plan=x[2])

                    except PlanDeCuentas.DoesNotExist:
                        padre = None
                    if padre:
                        cliente.grupo_id=padre.plan_id
                    if x[4].isdigit():
                        cliente.nivel = int(x[4])
                    cliente.calificacion = x[5]
                    cliente.tipo_cuenta_id = 1
                    cliente.created_by = request.user.get_full_name()
                    cliente.updated_by = request.user.get_full_name()
                    cliente.created_at = datetime.now()
                    cliente.updated_at = datetime.now()
                    cliente.activo = True
                    cliente.save()
                    print('entroNOempleado')

            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


def MigracionProducto(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                s=x[1]

                try:
                    cliente = Producto.objects.get(codigo_producto=x[0])

                except Producto.DoesNotExist:
                    cliente = None
                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    #row = cursor.execute();


                    cliente.codigo_producto=x[0]
                    cliente.descripcion_producto=x[4].decode('unicode-escape').strip()
                    cliente.tipo_producto_id = x[6]
                    cliente.linea_id = x[7]
                    cliente.categoria_id = x[9]
                    cliente.sub_categoria_id = x[10]
                    cliente.unidad=x[12]
                    cliente.peso = x[13]
                    cliente.medida_peso = x[14]
                    if x[17]=='1':
                        cliente.acepta_iva = True
                    else:
                        cliente.acepta_iva = False
                    if x[18]=='0':
                        cliente.activo = True
                    else:
                        cliente.activo = False


                    if x[19]=='1':
                        cliente.servicio = True
                    else:
                        cliente.servicio = False

                    cliente.precio1 = float(x[20].replace(',','.'))
                    cliente.precio2 = float(x[21].replace(',','.'))
                    cliente.precio3 = float(x[22].replace(',','.'))
                    cliente.precio4 = float(x[23].replace(',','.'))
                    cliente.precio5 = float(x[24].replace(',','.'))
                    cliente.costo = float(x[27].replace(',','.'))
                    cliente.cant_minimia = float(x[29].replace(',','.'))
                    cliente.cant_maxima = float(x[31].replace(',','.'))
                    #falta el 44
                    cliente.fecha_ult_vta = datetime.strptime(x[32], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    cliente.fecha_ult_com =  datetime.strptime(x[33], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    cliente.cant_venta =float(x[34].replace(',','.'))
                    cliente.cant_compra = float(x[35].replace(',','.'))
                    cliente.comentario=x[61]
                    cliente.notas = x[86]

                    if x[89]=='1':
                        cliente.ice = True
                    else:
                        cliente.ice = False
                    cliente.irbp=x[90]

                    cliente.created_by = x[91].decode('unicode-escape')
                    cliente.updated_by = x[92].decode('unicode-escape')
                    cliente.created_at = x[93]
                    cliente.updated_at = x[94]
                    cliente.precio_de_compra_max= float(x[102].replace(',','.'))
                    cliente.uat =float(x[95].replace(',', '.'))
                    cliente.val_uat1 = x[96]
                    cliente.val_uat2 = x[97]
                    cliente.val_uat3 = x[98]
                    cliente.val_uat4 = x[99]
                    cliente.val_uat5 = x[100]
                    cliente.val_uat6 = x[101]
                    cliente.base=True
                    cliente.save()


                    try:
                        presupuesto = PresupuestoProducto.objects.get(producto_id=cliente.producto_id)

                    except PresupuestoProducto.DoesNotExist:
                        presupuesto = None

                    if presupuesto:
                        presupuesto.enero=x[74]
                        presupuesto.febrero = x[75]
                        presupuesto.marzo = x[76]
                        presupuesto.abril = x[77]
                        presupuesto.mayo = x[78]
                        presupuesto.junio = x[79]
                        presupuesto.julio = x[80]
                        presupuesto.agosto = x[81]
                        presupuesto.septiembre = x[82]
                        presupuesto.octubre = x[83]
                        presupuesto.noviembre = x[84]
                        presupuesto.diciembre = x[85]
                        presupuesto.save()
                    else:
                        presupuesto=PresupuestoProducto()
                        presupuesto.enero = x[74]
                        presupuesto.febrero = x[75]
                        presupuesto.marzo = x[76]
                        presupuesto.abril = x[77]
                        presupuesto.mayo = x[78]
                        presupuesto.junio = x[79]
                        presupuesto.julio = x[80]
                        presupuesto.agosto = x[81]
                        presupuesto.septiembre = x[82]
                        presupuesto.octubre = x[83]
                        presupuesto.noviembre = x[84]
                        presupuesto.diciembre = x[85]
                        presupuesto.save()







                    # try:
                    #     padre = PlanDeCuentas.objects.get(codigo_plan=x[2])
                    #
                    # except PlanDeCuentas.DoesNotExist:
                    #     padre = None
                    # if padre:
                    #     cliente.grupo_id=padre.plan_id








                else:

                    cliente=Producto()
                    cliente.codigo_producto = x[0]
                    cliente.descripcion_producto = x[4].decode('unicode-escape').strip()
                    cliente.tipo_producto_id = x[6]
                    cliente.linea_id = x[7]
                    cliente.categoria_id = x[9]
                    cliente.sub_categoria_id = x[10]
                    cliente.unidad = x[12]
                    cliente.peso = x[13]
                    cliente.medida_peso = x[14]
                    if x[17] == '1':
                        cliente.acepta_iva = True
                    else:
                        cliente.acepta_iva = False
                    if x[18] == '0':
                        cliente.activo = True
                    else:
                        cliente.activo = False

                    if x[19] == '1':
                        cliente.servicio = True
                    else:
                        cliente.servicio = False

                    cliente.precio1 = float(x[20].replace(',', '.'))
                    cliente.precio2 = float(x[21].replace(',', '.'))
                    cliente.precio3 = float(x[22].replace(',', '.'))
                    cliente.precio4 = float(x[23].replace(',', '.'))
                    cliente.precio5 = float(x[24].replace(',', '.'))
                    cliente.costo = float(x[27].replace(',', '.'))
                    cliente.cant_minimia = float(x[29].replace(',', '.'))
                    cliente.cant_maxima = float(x[31].replace(',', '.'))
                    # falta el 44
                    cliente.fecha_ult_vta = datetime.strptime(x[32], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    cliente.fecha_ult_com = datetime.strptime(x[33], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                    cliente.cant_venta = float(x[34].replace(',', '.'))
                    cliente.cant_compra = float(x[35].replace(',', '.'))
                    cliente.comentario = x[61]
                    cliente.notas = x[86]

                    if x[89] == '1':
                        cliente.ice = True
                    else:
                        cliente.ice = False
                    cliente.irbp = x[90]

                    cliente.created_by = x[91].decode('unicode-escape')
                    cliente.updated_by = x[92].decode('unicode-escape')
                    cliente.created_at = x[93]
                    cliente.updated_at = x[94]
                    cliente.precio_de_compra_max = float(x[102].replace(',', '.'))
                    cliente.uat = float(x[95].replace(',', '.'))
                    cliente.val_uat1 = x[96]
                    cliente.val_uat2 = x[97]
                    cliente.val_uat3 = x[98]
                    cliente.val_uat4 = x[99]
                    cliente.val_uat5 = x[100]
                    cliente.val_uat6 = x[101]
                    cliente.base = True
                    cliente.save()
                    try:
                        presupuesto = PresupuestoProducto.objects.get(producto_id=cliente.producto_id)

                    except PresupuestoProducto.DoesNotExist:
                        presupuesto = None

                    if presupuesto:
                        presupuesto.enero = x[74]
                        presupuesto.febrero = x[75]
                        presupuesto.marzo = x[76]
                        presupuesto.abril = x[77]
                        presupuesto.mayo = x[78]
                        presupuesto.junio = x[79]
                        presupuesto.julio = x[80]
                        presupuesto.agosto = x[81]
                        presupuesto.septiembre = x[82]
                        presupuesto.octubre = x[83]
                        presupuesto.noviembre = x[84]
                        presupuesto.diciembre = x[85]
                        presupuesto.save()
                    else:
                        presupuesto = PresupuestoProducto()
                        presupuesto.enero = x[74]
                        presupuesto.febrero = x[75]
                        presupuesto.marzo = x[76]
                        presupuesto.abril = x[77]
                        presupuesto.mayo = x[78]
                        presupuesto.junio = x[79]
                        presupuesto.julio = x[80]
                        presupuesto.agosto = x[81]
                        presupuesto.septiembre = x[82]
                        presupuesto.octubre = x[83]
                        presupuesto.noviembre = x[84]
                        presupuesto.diciembre = x[85]
                        presupuesto.save()



            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


def MigracionProveedores(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            if len(x[0]):
                s=x[1]

                try:
                    cliente = Proveedor.objects.get(codigo_proveedor=x[1])

                except Proveedor.DoesNotExist:
                    cliente = None

                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    #row = cursor.execute();


                    cliente.codigo_proveedor=x[1]
                    cliente.nombre_proveedor=x[2].decode('unicode-escape')
                    cliente.fecha_nacimiento = x[5]

                    cliente.contacto = x[7].decode('unicode-escape')
                    cliente.direccion1=x[8].decode('unicode-escape')
                    cliente.telefono1 = x[9]
                    cliente.fax=x[10]
                    if x[11].isdigit():
                        cliente.clase_id = int(x[11])

                    print('Categoria:')
                    print str(x[12])
                    if x[12].isdigit():
                        cliente.categoria_cliente_id =int(x[12])
                    if x[15].isdigit():
                        cliente.ciudad_id = int(x[15])

                    if x[17].isdigit():
                        cliente.tipo_vta_id = int(x[17])


                    cliente.ruc = x[20]
                    cliente.e_mail1 = x[22]

                    try:
                        cliente.cupo = float(x[11])
                        cliente.descuento = float(x[25])

                    except:
                        print ('n')

                    cliente.created_by = x[29].decode('unicode-escape')
                    cliente.updated_by = x[30].decode('unicode-escape')
                    cliente.created_at = x[31]
                    cliente.updated_at = x[32]
                    if x[34].isdigit():
                        cliente.cuenta_contable=int(x[34])

                    cliente.serie = x[35]
                    if x[36].isdigit():
                        cliente.esnatural = x[36]
                    cliente.hasnfac = x[37]
                    cliente.descnfac = x[38]
                    if x[39] == '1':
                        cliente.obligcont = True
                    else:
                        cliente.obligcont = False

                    cliente.autoriza = x[40]
                    cliente.validez = x[41]
                    if x[42].isdigit():
                        cliente.ret_fue = x[42]
                    if x[43].isdigit():
                        cliente.ret_iva = x[43]

                    if x[44] == '1':
                        cliente.pag_cheque = True
                    else:
                        cliente.pag_cheque = False

                    if x[49] == '1':
                        cliente.incluye_ice = True
                    else:
                        cliente.incluye_ice = False

                    cliente.convenio_hasta = x[50]
                    if x[51] == '1':
                        cliente.consignacion = True
                    else:
                        cliente.consignacion = False

                    if x[52].isdigit():
                        cliente.prod_usr = x[52]
                    if x[53].isdigit():
                        cliente.cod_local = x[53]


                    cliente.celular = x[54]

                    if x[55] == '1':
                        cliente.pasaporte = True
                    else:
                        cliente.pasaporte = False
                    cliente.base = True
                    cliente.save()

                else:

                    cliente= Proveedor()
                    cliente.codigo_proveedor = x[1]
                    cliente.nombre_proveedor = x[2].decode('unicode-escape')
                    cliente.fecha_nacimiento = x[5]

                    cliente.contacto = x[7].decode('unicode-escape')
                    cliente.direccion1 = x[8].decode('unicode-escape')
                    cliente.telefono1 = x[9]
                    cliente.fax = x[10]
                    if x[11].isdigit():
                        cliente.clase_id = int(x[11])

                    print('Categoria:')
                    print str(x[12])
                    if x[12].isdigit():
                        cliente.categoria_cliente_id = int(x[12])
                    if x[15].isdigit():
                        cliente.ciudad_id = int(x[15])

                    if x[17].isdigit():
                        cliente.tipo_vta_id = int(x[17])

                    cliente.ruc = x[20]
                    cliente.e_mail1 = x[22]
                    try:
                        cliente.cupo = float(x[11])
                        cliente.descuento = float(x[25])

                    except:
                        print ('n')




                    cliente.created_by = x[29].decode('unicode-escape')
                    cliente.updated_by = x[30].decode('unicode-escape')
                    cliente.created_at = x[31]
                    cliente.updated_at = x[32]
                    if x[34].isdigit():
                        cliente.cuenta_contable = int(x[34])

                    cliente.serie = x[35]
                    if x[36].isdigit():
                        cliente.esnatural = x[36]
                    cliente.hasnfac = x[37]
                    cliente.descnfac = x[38]
                    if x[39] == '1':
                        cliente.obligcont = True
                    else:
                        cliente.obligcont = False

                    cliente.autoriza = x[40]
                    cliente.validez = x[41]
                    if x[42].isdigit():
                        cliente.ret_fue = x[42]
                    if x[43].isdigit():
                        cliente.ret_iva = x[43]

                    if x[44] == '1':
                        cliente.pag_cheque = True
                    else:
                        cliente.pag_cheque = False

                    if x[49] == '1':
                        cliente.incluye_ice = True
                    else:
                        cliente.incluye_ice = False

                    cliente.convenio_hasta = x[50]
                    if x[51] == '1':
                        cliente.consignacion = True
                    else:
                        cliente.consignacion = False

                    if x[52].isdigit():
                        cliente.prod_usr = x[52]
                    if x[53].isdigit():
                        cliente.cod_local = x[53]

                    cliente.celular = x[54]

                    if x[55] == '1':
                        cliente.pasaporte = True
                    else:
                        cliente.pasaporte = False
                    cliente.base = True
                    cliente.save()
                    print('entroNOempleado')

            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))



def MigracionRazonSocial(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print "validando..."

            if len(x[0]):

                codigo = x[0].strip()
                #nombre = x[1].decode('unicode-escape')
                #direccion = x[3].decode('unicode-escape')
                #print x[1].decode("utf-8", "replace")
                #print x[1].decode('string_escape')
                print codigo


                try:
                    cliente = RazonSocial.objects.get(codigo_razon_social=codigo)
                    print('entro')

                except RazonSocial.DoesNotExist:
                    cliente = None
                    print('entro2')
                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    cliente.codigo_razon_social = x[0].strip()
                    print('entro3')
                    cliente.nombre = x[1].decode('unicode-escape')

                    if x[2] != '0':
                        print ('contacto ')
                        cliente.contacto = x[2].decode('unicode-escape')

                    else:
                        print ('contacto no')

                    if x[3] != '0':
                        print ('direccion si ')
                        cliente.direccion1 = x[3].decode('unicode-escape')
                    else:
                        print ('direccion no')

                    if x[4] != '0':
                        print ('direccion si ')
                        cliente.ruc = x[4].strip()
                    else:
                        print ('direccion no')


                    cliente.created_by = request.user.get_full_name()
                    cliente.updated_by = request.user.get_full_name()
                    cliente.created_at = datetime.now()
                    cliente.updated_at = datetime.now()
                    cliente.base = True
                    cliente.save()

                else:


                    cliente= RazonSocial()
                    cliente.codigo_razon_social = x[0].strip()
                    print('entro3')
                    cliente.nombre = x[1].decode('unicode-escape')

                    if x[2] != '0':
                        print ('contacto ')
                        cliente.contacto = x[2].decode('unicode-escape')

                    else:
                        print ('contacto no')

                    if x[3] != '0':
                        print ('direccion si ')
                        cliente.direccion1 = x[3].decode('unicode-escape')
                    else:
                        print ('direccion no')

                    if x[4] != '0':
                        print ('direccion si ')
                        cliente.ruc = x[4].strip()
                    else:
                        print ('direccion no')

                    cliente.created_by = request.user.get_full_name()
                    cliente.updated_by = request.user.get_full_name()
                    cliente.created_at = datetime.now()
                    cliente.updated_at = datetime.now()
                    cliente.base = True
                    cliente.save()
                    print('entroNOempleado')

            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


def MigracionClienetRazonSocial(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            if len(x[0]):
                s=x[1]

                try:
                    razon = RazonSocial.objects.get(codigo_razon_social=x[0])

                except RazonSocial.DoesNotExist:
                    razon = None



                if razon:


                    try:
                        codigo=x[5].decode('unicode-escape')
                        cliente = Cliente.objects.get(codigo_cliente=codigo)

                    except Cliente.DoesNotExist:
                        cliente = None


                    if cliente:
                        try:
                            razon_cliente = RazonSocialClientes.objects.filter(cliente_id=cliente.id_cliente).filter(razon_social_id=razon.id)

                        except RazonSocialClientes.DoesNotExist:
                            razon_cliente = None


                        if razon_cliente:
                            print('hola')
                            razon_cliente[0].created_by = request.user.get_full_name()
                            razon_cliente[0].updated_by = request.user.get_full_name()
                            razon_cliente[0].created_at = datetime.now()
                            razon_cliente[0].updated_at = datetime.now()
                            razon_cliente[0].base = True
                            razon_cliente[0].save()
                        else:
                            razon_cliente=RazonSocialClientes()
                            razon_cliente.created_by = request.user.get_full_name()
                            razon_cliente.updated_by = request.user.get_full_name()
                            razon_cliente.created_at = datetime.now()
                            razon_cliente.updated_at = datetime.now()
                            razon_cliente.cliente_id=cliente.id_cliente
                            razon_cliente.razon_social_id = razon.id
                            razon_cliente.base = True
                            razon_cliente.save()
                    else:

                        print('datos:')
                        print x[0]
                        print (':')
                        print x[1]




                else:

                    print('datos:')
                    print x[0]
                    print (':')
                    print x[1]

            else:
                print('datos:')
                print x[0]
                print (':')
                print x[1]

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


def MigracionProductoInventario(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                s=x[1]

                try:
                    cliente = Producto.objects.get(codigo_producto=x[0])

                except Producto.DoesNotExist:
                    cliente = None
                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    #row = cursor.execute();


                    #cliente.codigo_producto=x[0]
                    #cliente.descripcion_producto=x[4].decode('unicode-escape').strip()
                    cliente.tipo_producto_id = x[2]
                    cliente.unidad=x[4]
                    cliente.costo = float(x[5].replace(',','.'))

                    cliente.base=True
                    cliente.save()


                    # try:
                    #     inventario = ProductoEnBodega.objects.get(producto_id=cliente.producto_id)
                    #
                    # except ProductoEnBodega.DoesNotExist:
                    #     inventario = None
                    #
                    # if x[3]!='0':
                    #     inventarioBodega = ProductoEnBodega()
                    #     inventarioBodega.bodega_id=1
                    #     inventarioBodega.producto_id=cliente.producto_id
                    #     inventarioBodega.cantidad=float(x[3].replace(',','.'))
                    #     inventarioBodega.created_by = request.user.get_full_name()
                    #     inventarioBodega.updated_by = request.user.get_full_name()
                    #     inventarioBodega.created_at = datetime.now()
                    #     inventarioBodega.updated_at = datetime.now()
                    #     inventarioBodega.save()
                    #
                    #
                    #
                    #     ingreso = Kardex()
                    #     ingreso.nro_documento=cliente.producto_id
                    #     ingreso.producto_id=cliente.producto_id
                    #     ingreso.cantidad=float(x[3].replace(',','.'))
                    #     ingreso.created_by = request.user.get_full_name()
                    #     ingreso.updated_by = request.user.get_full_name()
                    #     ingreso.created_at = datetime.now()
                    #     ingreso.updated_at = datetime.now()
                    #     ingreso.descripcion='Ingreso a inventario'
                    #     ingreso.bodega_id=1
                    #     ingreso.fecha_ingreso=datetime.now()
                    #     ingreso.costo=float(x[5].replace(',','.'))
                    #     ingreso.modulo='Migracion de inventario'
                    #     ingreso.save()
                    #
                    # # if inventario:
                    # #     if inventario.bodega_id==1:
                    # #
                    # # else:
                    # #     inventarioBodega=ProductoEnBodega()
                    # #     presupuesto.enero = x[74]
                    # #     presupuesto.febrero = x[75]
                    # #     presupuesto.marzo = x[76]
                    # #     presupuesto.abril = x[77]
                    # #     presupuesto.mayo = x[78]
                    # #     presupuesto.junio = x[79]
                    # #     presupuesto.julio = x[80]
                    # #     presupuesto.agosto = x[81]
                    # #     presupuesto.septiembre = x[82]
                    # #     presupuesto.octubre = x[83]
                    # #     presupuesto.noviembre = x[84]
                    # #     presupuesto.diciembre = x[85]
                    # #     presupuesto.save()
                    # #
                    # #
                    # #
                    # #
                    # #
                    # #
                    # #
                    # # # try:
                    # # #     padre = PlanDeCuentas.objects.get(codigo_plan=x[2])
                    # # #
                    # # # except PlanDeCuentas.DoesNotExist:
                    # # #     padre = None
                    # # # if padre:
                    # # #     cliente.grupo_id=padre.plan_id
                    #
                    #
                    #





                else:
                    print('hola')

                    # cliente=Producto()
                    # cliente.codigo_producto = x[0]
                    # cliente.descripcion_producto = x[1].decode('unicode-escape').strip()
                    # cliente.tipo_producto_id = x[2]
                    # cliente.linea_id = 1
                    # cliente.categoria_id = 1
                    # cliente.sub_categoria_id = 1
                    # cliente.unidad = x[4]
                    # cliente.activo = True
                    # cliente.costo = float(x[5].replace(',', '.'))
                    #
                    # cliente.created_by = request.user.get_full_name()
                    # cliente.updated_by = request.user.get_full_name()
                    # cliente.created_at = datetime.now()
                    # cliente.updated_at =datetime.now()
                    #
                    # cliente.base = True
                    # cliente.save()
                    # try:
                    #     inventario = ProductoEnBodega.objects.get(producto_id=cliente.producto_id)
                    #
                    # except ProductoEnBodega.DoesNotExist:
                    #     inventario = None
                    #
                    # if x[3]!='0':
                    #     inventarioBodega = ProductoEnBodega()
                    #     inventarioBodega.bodega_id = 1
                    #     inventarioBodega.producto_id = cliente.producto_id
                    #     inventarioBodega.cantidad = float(x[3].replace(',', '.'))
                    #     inventarioBodega.created_by = request.user.get_full_name()
                    #     inventarioBodega.updated_by = request.user.get_full_name()
                    #     inventarioBodega.created_at = datetime.now()
                    #     inventarioBodega.updated_at = datetime.now()
                    #     inventarioBodega.save()
                    #
                    #     ingreso = Kardex()
                    #     ingreso.nro_documento = cliente.producto_id
                    #     ingreso.producto_id = cliente.producto_id
                    #     ingreso.cantidad = float(x[3].replace(',', '.'))
                    #     ingreso.created_by = request.user.get_full_name()
                    #     ingreso.updated_by = request.user.get_full_name()
                    #     ingreso.created_at = datetime.now()
                    #     ingreso.updated_at = datetime.now()
                    #     ingreso.descripcion = 'Ingreso a inventario'
                    #     ingreso.bodega_id = 1
                    #     ingreso.fecha_ingreso = datetime.now()
                    #     ingreso.costo = float(x[5].replace(',', '.'))
                    #     ingreso.modulo = 'Migracion de inventario'
                    #     ingreso.save()



            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))



def MigracionEmpleadoArea(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                s=x[1]

                try:
                    cliente = Empleado.objects.get(cedula_empleado=x[0])

                except Empleado.DoesNotExist:
                    cliente = None

                usern=request.user.get_full_name()
                fecha=datetime.now()

                if cliente:

                    cliente.grupo_pago_id=x[1]
                    if x[2] == "0":
                        print('entroNOempleado Pruebaaa')
                    else:
                        cliente.areas_id = x[2]
                        print x[2]
                        print('HOOOOOOOOOOOO')

                    cliente.save()



                else:


                    print('entroNOempleado')

            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))



@login_required()
def NivelarInventarioView(request):

    cursor = connection.cursor()
    cursor.execute(
        "SELECT p.producto_id,p.descripcion_producto,SUM(e.cantidad) as egresos FROM producto p,orden_egreso_detalle e, egreso_orden_egreso eoe, orden_egreso oe where p.producto_id=e.producto_id and e.orden_egreso_id=oe.id and oe.id=eoe.orden_egreso_id and eoe.created_at>='2017-01-01 00:00:00' and eoe.created_at<='2017-01-07 00:00:00' group by p.producto_id,p.descripcion_producto order by p.producto_id;")
    row_egreso= cursor.fetchall()

    cursor.execute("SELECT p.producto_id,p.descripcion_producto,SUM(e.cantidad) as compras FROM producto p,compras_detalle e, compras_locales eoe, orden_compra oe where p.producto_id=e.producto_id and e.compra_id=oe.compra_id and oe.compra_id=eoe.orden_compra_id and eoe.created_at>='2017-01-01 00:00:00' and eoe.created_at<='2017-01-07 00:00:00' group by p.producto_id,p.descripcion_producto order by p.producto_id;")
    row_compras = cursor.fetchall()
    html=''
    html+='<table>'
    for p in row_egreso:
        html+='<tr>'
        html += '<td>'+str(p[1].encode('utf8'))+'</td>'
        html += '<td>' + str(p[2]) + '</td>'
        try:

            product_bod = ProductoEnBodega.objects.get(producto_id=p[0],bodega_id=1)
            html += '<td>EXISTE</td>'

        except ProductoEnBodega.DoesNotExist:
            product_bod = None
            html += '<td>NO EXISTE</td>'


        if product_bod:
            html += '<td>'+str(product_bod.cantidad_migrada)+'</td>'
            product_bod.egresos=float(p[2])
            product_bod.save()

        html += '</tr>'

    html += '</table>'
    html+='<h1>Compras</h1>'
    html += '<table>'
    for p1 in row_compras:
        html += '<tr>'
        html += '<td>' + str(p1[1].encode('utf8')) + '</td>'
        html += '<td>' + str(p1[2]) + '</td>'
        try:
            product_boding = ProductoEnBodega.objects.get(producto_id=p1[0],bodega_id=1)
            html += '<td>EXISTE</td>'

        except ProductoEnBodega.DoesNotExist:
            product_boding = None
            html += '<td>NO EXISTE</td>'

        if product_boding:
            html += '<td>' + str(product_boding.cantidad_migrada) + '</td>'
            product_boding.ingresos = float(p1[2])
            product_boding.save()
        html += '</tr>'

    html += '</table>'
    html+='<h2>TOTAL</h2>'
    html+='<table>'
    html += '<tr><td>producto</td><td>cantidad migrada</td><td>ingresos</td><td>egresos</td><td>cantidad inicial</td></tr>'
    productos_bodega = ProductoEnBodega.objects.filter(bodega_id=1)
    for pb in productos_bodega:
        html+='<tr>'
        if pb.cantidad_migrada:
            cantidad_migrada = pb.cantidad_migrada
        else:
            cantidad_migrada = 0
            #pb.cantidad_migrada=0


        if pb.ingresos:
            ingresos = pb.ingresos
        else:
            ingresos = 0
            pb.ingresos = 0

        if pb.egresos:
            egresos = pb.egresos

        else:
            egresos = 0
            pb.egresos=0

        cantidad_inicial=cantidad_migrada+egresos-ingresos
        pb.cantidad_inicial=cantidad_inicial

        pb.save()
        html += '<td>' + str(pb.producto.descripcion_producto.encode('utf8')) + '</td>'
        html += '<td>'+str(pb.cantidad_migrada)+'</td>'
        html += '<td>' + str(pb.ingresos) + '</td>'
        html += '<td>' + str(pb.egresos) + '</td>'
        html += '<td>' + str(pb.cantidad_inicial) + '</td>'
        html += '</tr>'
    html += '</table>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_inventario.html', {'html': html}, RequestContext(request))

@login_required()
def MigrarInventarioView(request):


    html=''
    html+='<table>'
    html += '<tr><td>producto</td><td>cantidad migrada</td><td>ingresos</td><td>egresos</td><td>cantidad inicial</td></tr>'
    productos_bodega = ProductoEnBodega.objects.filter(bodega_id=1)
    for pb in productos_bodega:
        inventario = Inventario()
        #html+='<tr>'
        inventario.producto_id=pb.producto_id
        inventario.bodega_id = pb.bodega_id
        inventario.anio=2017
        inventario.cantidad=pb.cantidad_inicial
        inventario.created_by = request.user.get_full_name()
        inventario.updated_by = request.user.get_full_name()
        inventario.created_at = datetime.now()
        inventario.updated_at = datetime.now()
        inventario.save()


    html += '</table>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_inventario.html', {'html': html}, RequestContext(request))







@login_required()
def CorregirFacturaView(request):

    cursor = connection.cursor()
    cursor.execute("select * from documento_compra where anulado is not true and updated_by like '%Isabel%' and id not in (select documento_compra_id from documento_retencion_compra) order by id ;")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        html+='<tr>'
        html += '<td>'+str(p[0])+'</td>'
        try:

            product_bod=DocumentoCompra.objects.get(id=p[0])
            html += '<td>EXISTEn</td>'

        except DocumentoCompra.DoesNotExist:
            product_bod = None
            html += '<td>NO EXISTE</td>'

        if product_bod:
            html+='<td>'+str(product_bod.proveedor)+'</td>'
            html += '<td>'+str(product_bod.establecimiento)+'</td>'
            html += '<td>'+str(product_bod.punto_emision)+'</td>'
            html += '<td>'+str(product_bod.secuencial)+'</td>'
            product_bod.retenido=True
            product_bod.save()
            documento_retencion = DocumentosRetencionCompra()
            documento_retencion.documento_compra_id=p[0]
            documento_retencion.fecha_emision=product_bod.fecha_emision
            documento_retencion.establecimiento=product_bod.establecimiento
            documento_retencion.punto_emision=product_bod.punto_emision
            documento_retencion.secuencial="00000000"
            documento_retencion.autorizacion="11192754445"
            documento_retencion.descripcion=product_bod.descripcion
            documento_retencion.valor_retenido=0
            documento_retencion.migrado=True
            documento_retencion.save()
            
            documento_retencion_detalle=DocumentosRetencionDetalleCompra()
            documento_retencion_detalle.retencion_detalle_id=14
            documento_retencion_detalle.base_imponible=product_bod.base_iva
            documento_retencion_detalle.porcentaje_retencion=0
            documento_retencion_detalle.valor_retenido=0
            documento_retencion_detalle.documento_retencion_compra_id=documento_retencion.id
            documento_retencion_detalle.migrado=True
            documento_retencion_detalle.save()

            cont=cont+1
            
            

        html += '</tr>'

    html += '</table>'
    html+='<p>total:'+str(cont)+'</p>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_inventario.html', {'html': html}, RequestContext(request))


@login_required()
def CorregirRetencionesVentaView(request):

    cursor = connection.cursor()
    cursor.execute("select * from documento_retencion_venta where asiento_id is null;")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        documento_retencion = DocumentoRetencionVenta.objects.get(id=p[0])
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        asiento = Asiento()
        asiento.codigo_asiento = int(codigo_asiento)
        asiento.fecha = p[2]
        asiento.glosa = 'RT de factura de cliente de la rt#'+str(p[0])
        asiento.gasto_no_deducible = False
        asiento.save()
        documento_retencion.asiento=asiento
        documento_retencion.save()
        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=secuenciales_id + 1)
        html+='<tr>'
        html += '<td>'+str(p[0])+'</td>'
        cursor = connection.cursor();
        sql3="select drvd.documento_retencion_venta_id,sum(drvd.valor_retenido),rd.tipo_retencion_id from documento_retencion_detalle_venta drvd,retencion_detalle rd where drvd.documento_retencion_venta_id=" + str(p[0])+ " and rd.id=drvd.retencion_detalle_id group by drvd.documento_retencion_venta_id,rd.tipo_retencion_id"
        print sql3
        cursor.execute(sql3)
        row3 = cursor.fetchall()
        total=0

        if row3:
            for d in row3:
                if d[2]==1:
                    asiento_detalle = AsientoDetalle()
                    asiento_detalle.asiento_id = int(asiento.asiento_id)
                    asiento_detalle.cuenta_id = 623
                    asiento_detalle.debe = d[1]
                    asiento_detalle.haber = 0
                    asiento_detalle.save()
                    total=total+d[1]
                    
                if d[2]==2:
                    asiento_detalle = AsientoDetalle()
                    asiento_detalle.asiento_id = int(asiento.asiento_id)
                    asiento_detalle.cuenta_id = 622
                    asiento_detalle.debe = d[1]
                    asiento_detalle.haber = 0
                    asiento_detalle.save()
                    total=total+d[1]
        asiento_detalle = AsientoDetalle()
        asiento_detalle.asiento_id = int(asiento.asiento_id)
        asiento_detalle.cuenta_id = 22
        asiento_detalle.debe = 0
        asiento_detalle.haber = total
        asiento_detalle.save()
           

            

        html += '</tr>'

    html += '</table>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_inventario.html', {'html': html}, RequestContext(request))
@login_required()
def CrearFacturaCompraView(request,pk):
    new_orden = ComprasLocales.objects.get(id=pk)
    with transaction.atomic():
        if new_orden:
            documento = DocumentoCompra()
            documento.created_by = new_orden.created_by
            documento.updated_by = new_orden.updated_by
            documento.created_at = new_orden.created_at
            documento.updated_at = new_orden.updated_at
            documento.fecha_emision = new_orden.fecha
            documento.fecha_vencimiento = new_orden.fecha
            documento.proveedor = new_orden.proveedor
            documento.orden_compra_id = new_orden.orden_compra_id
            documento.establecimiento = new_orden.proveedor.establecimiento
            documento.punto_emision = new_orden.proveedor.establecimiento
            if new_orden.nro_fact_proveedor:
                documento.secuencial = new_orden.nro_fact_proveedor
            else:
                documento.secuencial = new_orden.recibida
            documento.autorizacion = new_orden.proveedor.autorizacion_sri
            documento.descripcion = new_orden.comentario
            # documento.base_iva_0 =
            # documento.base_iva =
            documento.base_iva = new_orden.subtotal
            documento.valor_iva = new_orden.iva
            documento.porcentaje_iva = new_orden.iva_pciento
            # documento.base_ice =
            # documento.valor_ice =
            # documento.porcentaje_ice =
            documento.descuento = new_orden.dscto_monto
            documento.total = new_orden.total
            # documento.tipo_provision = cleaned_data.get('tipo_provision')
            documento.pagado = False
            documento.generada = True
            documento.compra_id=new_orden.id
            documento.save()


            objet = OrdenCompra.objects.filter(compra_id=new_orden.orden_compra_id)
            for ob in objet:
                ob.facturada = True
                ob.save()



            objetos = ComprasDetalle.objects.filter(compra_id=new_orden.orden_compra_id)
            print('Cantidad de objetos en la compra detalle')
            print len(objetos)
            for obj in objetos:
                obj.recibido = True
                obj.save()
                documento_detalle = DocumentosCompraDetalle()
                documento_detalle.documento_compra_id = int(documento.id)
                documento_detalle.producto_id = obj.producto_id
                documento_detalle.descripcion = obj.producto.descripcion_producto
                documento_detalle.base_ice = 0
                documento_detalle.valor_ice = 0
                documento_detalle.porcentaje_ice = 0
                documento_detalle.descuento = 0
                documento_detalle.cantidad = obj.cantidad
                documento_detalle.save()

                id = obj.compras_detalle_id
                print id

                try:
                    product = Producto.objects.get(producto_id=obj.producto_id)
                except Producto.DoesNotExist:
                    product = None
                    # if product:
                    #     product.costo=obj.precio_compra
                    #     product.save()
                    #     print ("Se actualizo el producto")

                new_orden_compra = OrdenCompra.objects.get(compra_id=obj.compra_id)
                try:
                    kardez = Kardex.objects.filter(modulo=id).filter(nro_documento=new_orden_compra.nro_compra).filter(producto_id=obj.producto_id).filter(fecha_ingreso=datetime.now())
                except Kardex.DoesNotExist:
                    kardez = None

                if kardez:
                    print('ya existe')
                    print len(kardez)
                else:
                    print ('No existe cardex del detalle_id' + str(id)+'CCompra No.'+str(new_orden_compra.nro_compra))
                    k = Kardex()
                    k.nro_documento = new_orden_compra.nro_compra
                    k.producto = obj.producto
                    k.cantidad = obj.cantidad
                    k.descripcion = 'Ingreso a Bodega de Materia Prima'
                    k.costo = obj.precio_compra
                    k.bodega = new_orden_compra.bodega
                    k.modulo = id
                    k.un_doc_soporte='Orden de Compra No.'+str(new_orden_compra.nro_compra)+' Compra Local No.'+str(new_orden.codigo)
                    k.fecha_ingreso = datetime.now()
                    k.save()

                    # prod1 = ProductoEnBodega.objects.filter(producto_id=obj.producto_id).filter(bodega_id=obj.bodega_id)
                    # 
                    # if prod1:
                    #     for prod in prod1:
                    #         prod.cantidad = float(prod.cantidad) + float(obj.cantidad)
                    #         prod.updated_at = datetime.now()
                    #         prod.updated_by = request.user.get_full_name()
                    #         prod.save()
                    # else:
                    #     k = ProductoEnBodega()
                    #     k.producto_id = obj.producto_id
                    #     k.bodega_id = obj.bodega_id
                    #     k.cantidad = obj.cantidad
                    #     k.created_by = request.user.get_full_name()
                    #     k.updated_by = request.user.get_full_name()
                    #     k.created_at = datetime.now()
                    #     k.updated_at = datetime.now()
                    #     k.save()
                # try:
                #     secuencial = Secuenciales.objects.get(modulo='compraslocales')
                #     secuencial.secuencial = secuencial.secuencial + 1
                #     secuencial.created_by = request.user.get_full_name()
                #     secuencial.updated_by = request.user.get_full_name()
                #     secuencial.created_at = datetime.now()
                #     secuencial.updated_at = datetime.now()
                #     secuencial.save()
                # except Secuenciales.DoesNotExist:
                #     secuencial = None

                
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))

def MigracionCheques(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[3]):
                

                try:
                    proveedor = Proveedor.objects.get(codigo_proveedor=x[3])

                except Proveedor.DoesNotExist:
                    proveedor = None
                usern=request.user.get_full_name()
                fecha=datetime.now()
                movimiento = Movimiento()
                movimiento.tipo_anticipo_id = 1
                movimiento.tipo_documento_id = 1
                movimiento.fecha_emision = x[0]
                movimiento.banco_id = 2
                if proveedor:
                    movimiento.proveedor = proveedor
                else:
                    text='No hay proveedor'
                movimiento.paguese_a = x[5].decode('unicode-escape')
                
                movimiento.numero_cheque = x[1]
                movimiento.fecha_cheque = x[0]
                movimiento.descripcion = x[8].decode('unicode-escape')
                movimiento.monto = x[7]
                movimiento.monto_cheque = x[6]
                movimiento.save()
                movimiento.numero_comprobante = 'M2017000'+str(movimiento.id)
                movimiento.save()
                    

           
            else:
                print('hola')

        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


def MigracionBalanceFinanciero(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        text=""
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                try:
                    plan = PlanDeCuentas.objects.get(codigo_plan=x[0],activo=True)
                except PlanDeCuentas.DoesNotExist:
                    plan = None
                if plan:
                    usern=request.user.get_full_name()
                    fecha=datetime.now()
                    periodo = PeriodoAnterior()
                    periodo.anio = 2016
                    periodo.plan = plan
                    periodo.fecha = fecha
                    periodo.saldo_periodo = float(x[3].replace(',','.'))
                    periodo.saldo= float(x[4].replace(',','.'))
                    periodo.saldo_anterior= float(x[2].replace(',','.'))
                    periodo.descripcion= x[1]
                    periodo.codigo= x[0]
                    periodo.tipo= x[5]
                    periodo.created_at = fecha
                    periodo.updated_at = fecha
                    periodo.created_by = usern
                    periodo.updated_by = usern
                    periodo.save()
                else:
                    text+="<br>"
                    text+="El plan no existe"+str(x[0])
                    text1="El plan no existe"+str(x[0])
                    print text1
                    
                    
                    

           
            else:
                print('hola')
                

        texto = text
        print text
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))



def MigracionAfectaSaldoInicial(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        text=""
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            if len(x[0]):
                numero_cheque=str(x[4])
                cursor = connection.cursor()
                sql="select * from movimiento where numero_cheque='"+str(x[4])+"' and tipo_documento_id=1"
                cursor.execute(sql)
                mov1= cursor.fetchall()
                if mov1:
                    
                    try:
                        
                        mov = Movimiento.objects.get(id=mov1[0][0])
                    except Movimiento.DoesNotExist:
                        mov = None
                    if mov:
                        abono=DocumentoAbono()
                        #abono.documento_compra_id=item_factura['id']
                        abono.movimiento_id = mov.id
                        abono.abono=float(x[6])
                        abono.observacion = str(x[5].encode('utf8'))
                        abono.created_by = request.user.get_full_name()
                        abono.updated_by = request.user.get_full_name()
                        abono.created_at = datetime.now()
                        abono.updated_at = datetime.now()
                        abono.saldo_inicial=True
                        abono.proveedor_id=mov.proveedor_id
                        abono.save()
                    else:
                        text+="<br>"
                        text+="El movimiento no existe"+str(x[0])+' del cheque '+str(x[4])
                        text1="El movimiento no existe"+str(x[0])+' del cheque '+str(x[4])
                else:
                    t2="El movimiento no existe"+str(x[0])+' del cheque '+str(x[4])
                    print t2
            
                

        texto = text
        print text
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))



@login_required()
def CorregirAsientoView(request):

    cursor = connection.cursor()
    cursor.execute("select codigo_asiento,secuencia_asiento,asiento_id from contabilidad_asiento order by asiento_id;")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    consec=1
    for p in row_egreso:
        codigo_secuencial=p[0]
        cod=codigo_secuencial.split('2017')
        html+='<tr>'
        html += '<td>'+str(cod[0])+'</td>'
        longitud=len(str(consec))
        if longitud== 1:
            ceros='00000'
        if longitud== 2:
            ceros='0000'
        if longitud== 3:
            ceros='000'
        if longitud== 4:
            ceros='00'
        
        if longitud== 5:
            ceros='0'
       
        prue=str(cod[0])+'2017'+str(ceros)+''+str(consec)
        html += '<td>'+str(prue)+'</td>'
        
        try:
            asiento = Asiento.objects.get(asiento_id=p[2])
        except Asiento.DoesNotExist:
            asiento = None
        if asiento:
            asiento.secuencia_asiento=consec
            asiento.codigo_asiento=prue
            asiento.save()

            consec=consec+1
            
            

        html += '</tr>'

    html += '</table>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_asiento.html', {'html': html}, RequestContext(request))



def MigracionAsientoRrhh(request):
    if request.method == 'POST':
        archivos = request.FILES['archivo']
        paramFile = request.FILES['archivo'].read()
        #portfolio = csv.DictReader(paramFile)
        users = []
        lineas = paramFile.split('\n')
        usern=request.user.get_full_name()
        fecha=datetime.now()
        codigo_asiento = Secuenciales.objects.get(modulo='asiento').secuencial
        secuenciales_id = Secuenciales.objects.get(modulo='asiento').id
        
        
        asiento = Asiento()
        asiento.codigo_asiento = "RRHH"+str(codigo_asiento)
        asiento.fecha = fecha
        asiento.glosa = 'RRHH'
        asiento.gasto_no_deducible = False
        asiento.save()
        cont=0
        
        for linea in lineas:
            x = linea.split(";")
            print x[0]
            cont=cont+1
            if len(x[0]):
                try:
                    plan = PlanDeCuentas.objects.get(codigo_plan=x[0])

                except PlanDeCuentas.DoesNotExist:
                    plan = None
                

                if plan:
                    

                    asiento_detalle = AsientoDetalle()
                    asiento_detalle.asiento_id = int(asiento.asiento_id)
                    asiento_detalle.cuenta_id = plan.plan_id
                    asiento_detalle.debe = float(x[3].replace(',','.'))
                    asiento_detalle.haber = float(x[4].replace(',','.'))
                    asiento_detalle.concepto=x[2].decode('unicode-escape')
                    asiento_detalle.save()
                    
                    
                    if cont == 1 or  cont == '1':
                        asiento.glosa=x[2].decode('unicode-escape')
                        asiento.total_debe=float(x[5].replace(',','.'))
                        asiento.total_haber=float(x[5].replace(',','.'))
                        asiento.modulo='RRHH'
                        asiento.secuencia_asiento=codigo_asiento
                        asiento.save()

                else:

                    print('No existe plan contable'+str(x[0]))

            else:
                print('hola')

        Secuenciales.objects.filter(pk=secuenciales_id).update(secuencial=codigo_asiento + 1)
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))


    else:
        texto = "text"
        return render_to_response('migracion/migracion.html', {'texto': texto}, RequestContext(request))




@login_required()
def CorregirFacturaView(request):

    cursor = connection.cursor()
    cursor.execute("select * from documento_compra where anulado is not true and updated_by like '%Isabel%' and id not in (select documento_compra_id from documento_retencion_compra) order by id ;")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        html+='<tr>'
        html += '<td>'+str(p[0])+'</td>'
        try:

            product_bod=DocumentoCompra.objects.get(id=p[0])
            html += '<td>EXISTEn</td>'

        except DocumentoCompra.DoesNotExist:
            product_bod = None
            html += '<td>NO EXISTE</td>'

        if product_bod:
            html+='<td>'+str(product_bod.proveedor)+'</td>'
            html += '<td>'+str(product_bod.establecimiento)+'</td>'
            html += '<td>'+str(product_bod.punto_emision)+'</td>'
            html += '<td>'+str(product_bod.secuencial)+'</td>'
            product_bod.retenido=True
            product_bod.save()
            documento_retencion = DocumentosRetencionCompra()
            documento_retencion.documento_compra_id=p[0]
            documento_retencion.fecha_emision=product_bod.fecha_emision
            documento_retencion.establecimiento=product_bod.establecimiento
            documento_retencion.punto_emision=product_bod.punto_emision
            documento_retencion.secuencial="00000000"
            documento_retencion.autorizacion="11192754445"
            documento_retencion.descripcion=product_bod.descripcion
            documento_retencion.valor_retenido=0
            documento_retencion.migrado=True
            documento_retencion.save()
            
            documento_retencion_detalle=DocumentosRetencionDetalleCompra()
            documento_retencion_detalle.retencion_detalle_id=14
            documento_retencion_detalle.base_imponible=product_bod.base_iva
            documento_retencion_detalle.porcentaje_retencion=0
            documento_retencion_detalle.valor_retenido=0
            documento_retencion_detalle.documento_retencion_compra_id=documento_retencion.id
            documento_retencion_detalle.migrado=True
            documento_retencion_detalle.save()

            cont=cont+1
            
            

        html += '</tr>'

    html += '</table>'
    html+='<p>total:'+str(cont)+'</p>'
    #html='Se guardo satisfactoriamente'
    return render_to_response('migracion/nivelar_inventario.html', {'html': html}, RequestContext(request))


@login_required()
def CorregirRetencionesElectronicasView(request):

    cursor = connection.cursor()
    cursor.execute("select * from documento_compra where fecha_emision>='2018-03-01' and fecha_emision<='2018-03-16';")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        
        if p[0]:
            try:
                factura = DocumentosRetencionCompra.objects.get(documento_compra_id=p[0])
            except DocumentosRetencionCompra.DoesNotExist:
                factura = None
            if factura:
            
                if factura.id:
                    conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
                    cursor = conn.cursor()
                    sqlCommanf="select claveAcceso,estado,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial  from infoCompRetencion where id="+str(factura.id)+";"
                    cursor.execute(sqlCommanf)
                    row = cursor.fetchall()
                    conn.commit()
                    for r in row:
                        try:
                            dc = DocumentoCompra.objects.get(id=p[0])
                        except DocumentoCompra.DoesNotExist:
                            dc = None
                        factura.autorizacion=r[2]
                        factura.save()
                        dc.fecha_autorizacion=r[3]
                        dc.save()
@login_required()
def CorregirFacturacionElectronicaView(request):

    cursor = connection.cursor()
    cursor.execute("select id,id_facturacion_eletronica from documento_venta where fecha_emision>='2018-01-01'")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        
        if p[1]:
            conn = pyodbc.connect("DRIVER=FreeTDS;SERVER=104.192.6.75;PORT=1433;UID=sa;PWD=U7BKm3eayFCn9cTx;DATABASE=MuedirsaPrueba")
            cursor = conn.cursor()
            sqlCommanf="select claveAcceso,estado,numeroAutorizacion,fechaAutorizacion,msjeSRI,estadoCorreo,msjeCorreo,estadoPdf,msjePdf,secuencial  from infoDocumentoCliente where id="+str(p[1])+";"
            cursor.execute(sqlCommanf)
            row = cursor.fetchall()
            conn.commit()
            for r in row:
                try:
                    dc = DocumentoVenta.objects.get(id=p[0])
                except DocumentoVenta.DoesNotExist:
                    dc = None
                dc.autorizacion=r[2]
                dc.fecha_autorizacion=r[3]
                dc.save()
            
                                        
        

            

        
@login_required()
def CorregirFechaRetencionesElectronicasView(request):

    cursor = connection.cursor()
    cursor.execute("select dc.id,dc.fecha_emision,dc.fecha_autorizacion,dcr.id,dcr.fecha_emision,dcr.autorizacion,dc.anulado,dc.facturacion_eletronica from documento_compra dc,documento_retencion_compra dcr where dc.id=dcr.documento_compra_id and dcr.fecha_emision!=dc.fecha_autorizacion and dc.fecha_autorizacion is not Null order by dcr.fecha_emision")
    row_egreso= cursor.fetchall()


    html=''
    html+='<table>'
    cont=0
    for p in row_egreso:
        
        if p[0]:
            try:
                factura = DocumentosRetencionCompra.objects.get(id=p[3])
            except DocumentosRetencionCompra.DoesNotExist:
                factura = None
            if factura:
                if p[2]:
                    factura.fecha_emision=p[2]
                    factura.save()
                       