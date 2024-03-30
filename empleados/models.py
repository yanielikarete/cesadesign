from django.db import models
from os.path import basename
from django.contrib.auth.models import User, Group, Permission
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from clientes.models import Cliente
from config.models import *

from contabilidad.models import PlanDeCuentas
from bancos.models import *



# Create your models here.
class Departamento(models.Model):
    codigo = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    produccion = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'departamento'

    def __unicode__(self):
        return "%s" % (self.nombre)


class GrupoPago(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grupo_pago'

    def __unicode__(self):
        return "%s" % (self.nombre)


class TipoEmpleado(models.Model):
    tipo_empleado_id = models.AutoField(primary_key=True)
    cargo_empleado = models.CharField(max_length=20)
    descripcion_tipo = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.cargo_empleado)


class TipoContrato(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_contrato'

    def __unicode__(self):
        return "%s" % (self.nombre)


class PagoFondosReserva(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pago_fondos_reserva'

    def __unicode__(self):
        return "%s" % (self.nombre)


class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    codigo_empleado = models.CharField(max_length=10, blank=True, null=True)
    cedula_empleado = models.CharField(max_length=10, blank=True, null=True)
    nombre_empleado = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    tipo_empleado = models.ForeignKey(TipoEmpleado, blank=True, null=True)
    direccion = models.CharField(max_length=80, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField()
    fecha_fin = models.DateField(blank=True, null=True)
    fecha_ini = models.DateField(blank=True, null=True)
    fecha_ini_reconocida = models.DateField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    OBJETO_CHOICES = (
        ("Femenino", "Femenino"),
        ("Masculino", "Masculino"),
    )
    sexo = models.CharField(max_length=20, blank=True, choices=OBJETO_CHOICES)
    estado_civil = models.ForeignKey(EstadoCivil, blank=True, null=True)
    DOC_CHOICES = (
        ("Cedula", "Cedula"),
        ("Pasaporte", "Pasaporte"),

    )
    tipo_documento = models.CharField(max_length=250, blank=True, choices=DOC_CHOICES)
    pais = models.ForeignKey(Pais, blank=True, null=True)
    cargas_familiares = models.IntegerField(blank=True, null=True)
    telefono = models.CharField(max_length=100, blank=True)
    provincia = models.ForeignKey(Provincia, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True)
    imagen = models.ImageField(null=True, blank=True, upload_to="imagenes/producto/")
    gastos_vivienda = models.FloatField(blank=True, null=True)
    gastos_educacion = models.FloatField(blank=True, null=True)
    gastos_salud = models.FloatField(blank=True, null=True)
    gastos_alimentacion = models.FloatField(blank=True, null=True)
    gastos_vestimenta = models.FloatField(blank=True, null=True)
    rebajada_discapacidad = models.FloatField(blank=True, null=True)
    rebajas_tercera_edad = models.FloatField(blank=True, null=True)
    situacion_previsional = models.CharField(max_length=250, blank=True)
    iess = models.CharField(max_length=250, blank=True)
    numero_afiliacion = models.CharField(max_length=50, blank=True)
    sociedad_medica = models.CharField(max_length=250, blank=True)
    numero_sociedad_medica = models.CharField(max_length=100, blank=True)
    impuesto_renta_cargo_empleador = models.BooleanField()
    forma_pago_cliente_id = models.IntegerField(blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    tipo_cuenta = models.ForeignKey(TipoCuenta, blank=True, null=True)
    cuenta_contable = models.CharField(max_length=100, blank=True)
    aportacion_conyugal = models.BooleanField()
    horas_trabajo_semanal = models.CharField(max_length=250, blank=True)
    relacion_laboral = models.ForeignKey(RelacionLaboral, blank=True, null=True)
    tipo_remuneracion = models.ForeignKey(TipoRemuneracion, blank=True, null=True)
    compensacion = models.FloatField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    forma_pago_empleado = models.ForeignKey(FormaPagoEmpleado, blank=True, null=True)
    tipo_contrato = models.ForeignKey(TipoContrato, blank=True, null=True)
    discapacidad = models.BooleanField()
    grupo_pago = models.ForeignKey(GrupoPago, blank=True, null=True)
    acumular_decimo_tercero = models.BooleanField()
    extension_conyugal = models.BooleanField()
    pago_fondos_reserva = models.ForeignKey(PagoFondosReserva, blank=True, null=True)
    nota = models.TextField(blank=True)
    acumular_fondo_reserva = models.BooleanField()
    acumular_decimo_cuarto = models.BooleanField()
    acumular_iess_asumido = models.BooleanField()
    asumir_impuesto_renta = models.BooleanField()
    codigo_reloj = models.CharField(max_length=255, blank=True, null=True)
    habilitado_recibe_fondo_reserva=models.BooleanField(default=True)
    codigo_sectorial_iess = models.CharField(max_length=500, blank=True, null=True)
    horas_trabajo_mensual= models.CharField(max_length=250, blank=True)

    class Meta:
        managed = False
        ordering = ['nombre_empleado']
        db_table = 'empleados_empleado'

    def __unicode__(self):
        return self.nombre_empleado


class TipoIngresoEgresoEmpleado(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    ingreso = models.BooleanField(blank=True)
    egreso = models.BooleanField(blank=True)
    otros_ingresos = models.BooleanField(blank=True)
    otros_egresos = models.BooleanField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    calcular_ingreso = models.BooleanField(blank=True)
    parte_ingreso = models.BooleanField(blank=True)
    orden = models.IntegerField(blank=True, null=True)
    contabilizar_rol = models.BooleanField(blank=True)

    class Meta:
        managed = False
        db_table = 'tipo_ingreso_egreso_empleado'

    def __unicode__(self):
        return self.nombre


class IngresosProyectadosEmpleado(models.Model):
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    valor_diario = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingresos_proyectados_empleado'


class EgresosProyectadosEmpleado(models.Model):
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    valor_diario = models.FloatField(blank=True, null=True)
    deducible = models.NullBooleanField()
    aportaciones = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egresos_proyectados_empleado'


# class Vendedor(models.Model):
#     vendedor_id = models.AutoField(primary_key=True)
#     codigo_vendedor = models.CharField(max_length=10)
#     empleado = models.ForeignKey(Empleado)
#     comision = models.DecimalField(max_digits=8, decimal_places=2)
#     created_by = models.CharField(max_length=255)
#     updated_by = models.CharField(max_length=255)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()
#     activo = models.BooleanField(default=True)
#     externo = models.BooleanField(default=True)
#
#
# def __unicode__(self):
#     return "%s" % (self.empleado)


class Chofer(models.Model):
    chofer_id = models.AutoField(primary_key=True)
    codigo_chofer = models.CharField(max_length=10)
    empleado = models.ForeignKey(Empleado)
    nombre = models.CharField(max_length=255,blank=True, null=True)
    ruc = models.CharField(max_length=20,blank=True, null=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.empleado)


class Vehiculo(models.Model):
    vehiculo_id = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=30)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)
    descripcion = models.TextField(blank=True)
    codigo = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.descripcion)
