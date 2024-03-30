from django.db import models
from contabilidad.models import *
from empleados.models import *

# Create your models here.
class RolPagoConfiguraciones(models.Model):
    dia_pago = models.IntegerField(blank=True, null=True)
    porcentaje_primera_quincena = models.FloatField(blank=True, null=True)
    mensual = models.BooleanField(blank=True)
    quincenal = models.BooleanField(blank=True)
    porcentaje_iess = models.FloatField(blank=True, null=True)
    extension_conyugal_iess = models.FloatField(blank=True, null=True)
    plan_cuentas = models.ForeignKey(PlanDeCuentas, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol_pago_configuraciones'

class RolCuentacontableItems(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_cuentacontable_items'
    def __unicode__(self):
        return "%s" % (self.nombre)

class RolCuentacontableTipoingresoegreso(models.Model):
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    rol_cuentacontable_items = models.ForeignKey(RolCuentacontableItems, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_cuentacontable_tipoingresoegreso'



class ClasificacionCuenta(models.Model):
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'clasificacion_cuenta'
    def __unicode__(self):
        return "%s" % (self.nombre)

class RolPagoCuentaContable(models.Model):
    rol_pago_configuraciones = models.ForeignKey(RolPagoConfiguraciones, blank=True, null=True)
    grupo_pago = models.ForeignKey(GrupoPago, blank=True, null=True)
    clave = models.CharField(max_length=255, blank=True)
    plandecuentas = models.ForeignKey(PlanDeCuentas, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    tipo_cuenta = models.ForeignKey(TipoCuenta, blank=True, null=True)
    clasificacion_cuenta = models.ForeignKey(ClasificacionCuenta, blank=True, null=True)
    rol_cuentacontable_items = models.ForeignKey(RolCuentacontableItems, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_cuenta_contable'

class SueldosUnificados(models.Model):
    anio = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'sueldos_unificados'

class RolPago(models.Model):
    anio = models.CharField(max_length=250, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    salario_base = models.FloatField(blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago'

class RolPagoDetalle(models.Model):
    rol_pago = models.ForeignKey(RolPago, blank=True, null=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    ingresos = models.FloatField(blank=True, null=True)
    egresos = models.FloatField(blank=True, null=True)
    otros_ingresos = models.FloatField(blank=True, null=True)
    otros_egresos = models.FloatField(blank=True, null=True)
    dias = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    tipo_pago = models.ForeignKey(TipoPago, blank=True, null=True)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    numero_comprobante = models.CharField(max_length=255, blank=True)
    fondo_reserva = models.FloatField(blank=True, null=True)
    decimo_tercero = models.FloatField(blank=True, null=True)
    decimo_cuarto = models.FloatField(blank=True, null=True)
    iess_asumido = models.FloatField(blank=True, null=True)
    impuesto_renta = models.FloatField(blank=True, null=True)
    nueve_cuarenta_cinco = models.FloatField(blank=True, null=True)
    tres_cuarenta_uno = models.FloatField(blank=True, null=True)
    descuento_dias= models.FloatField(blank=True, null=True)
    forma_pago_empleado = models.ForeignKey(FormaPagoEmpleado, blank=True, null=True)
    pagar_fondo_reserva = models.BooleanField(default=False,)
    pagar_decimo_cuarto = models.BooleanField(default=False,)
    pagar_iess_asumido = models.BooleanField(default=False,)
    pagar_decimo_tercero = models.BooleanField(default=False,)
    pagar_extension_conyugal = models.BooleanField(default=False,)
    pagar_impuesto_renta= models.BooleanField(default=False,)
    fecha_ini_reconocida= models.DateField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'rol_pago_detalle'


class PlantillaRrhh(models.Model):
    codigo = models.CharField(max_length=10, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    abreviatura = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'plantilla_rrhh'

class PlantillaRrhhDetalle(models.Model):
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'plantilla_rrhh_detalle'

class OtrosIngresosRolEmpleado(models.Model):
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    rol_pago_detalle = models.ForeignKey(RolPagoDetalle, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    deducible = models.BooleanField(blank=True,)
    aportaciones = models.BooleanField(blank=True,)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    pagar = models.BooleanField(blank=True,)

    class Meta:
        managed = False
        db_table = 'otros_ingresos_rol_empleado'

class OtrosEgresosRolEmpleado(models.Model):
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    rol_pago_detalle = models.ForeignKey(RolPagoDetalle, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado= models.ForeignKey(Empleado, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    memo = models.BooleanField(blank=True,)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'otros_egresos_rol_empleado'

class TipoAusencia(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_ausencia'

class DiasNoLaboradosRolEmpleado(models.Model):
    tipo_ausencia = models.ForeignKey(TipoAusencia, blank=True, null=True)
    rol_pago_detalle = models.ForeignKey(RolPagoDetalle, blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado= models.ForeignKey(Empleado, blank=True, null=True)
    dias = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    descontar = models.BooleanField(blank=True, )
    cargar_vacaciones = models.BooleanField(blank=True, )
    motivo= models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'dias_no_laborados_rol_empleado'


class RolPagoPlantilla(models.Model):
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    rol_pago = models.ForeignKey(RolPago, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    anio = models.CharField(max_length=250, blank=True)
    quincena = models.CharField(max_length=255, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'rol_pago_plantilla'

class TipoSolicitud(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_solicitud'
    def __unicode__(self):
       return self.descripcion

class Permiso(models.Model):
    empleados_empleado = models.ForeignKey(Empleado, blank=True, null=True)
    tipo_solicitud = models.ForeignKey(TipoSolicitud, blank=True, null=True)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    permisos_dias = models.NullBooleanField()
    permisos_horas = models.NullBooleanField()
    licencia_dias = models.NullBooleanField()
    descanso_iess_dias = models.NullBooleanField()
    cita_iess_horas = models.NullBooleanField()
    fecha_desde = models.DateTimeField(blank=True, null=True)
    fecha_hasta = models.DateTimeField(blank=True, null=True)
    hora_desde = models.TimeField(blank=True, null=True)
    hora_hasta = models.TimeField(blank=True, null=True)
    total_dias_ausencia = models.IntegerField(blank=True, null=True)
    total_horas_ausencia = models.IntegerField(blank=True, null=True)
    motivo_trabajo = models.NullBooleanField()
    motivo_personal = models.NullBooleanField()
    motivo_calamidad = models.NullBooleanField()
    motivo_enfermedad = models.NullBooleanField()
    cargo_vacaciones = models.NullBooleanField()
    activo = models.NullBooleanField()
    observacion = models.CharField(max_length=255, blank=True)
    nombre_empleado = models.CharField(max_length=255, blank=True)
    cargo_empleado = models.CharField(max_length=255, blank=True)
    area_empleado = models.CharField(max_length=255, blank=True)
    vacaciones = models.NullBooleanField()
    periodo = models.NullBooleanField()
    total_dias_pendientes = models.IntegerField(blank=True, null=True)
    periodo_dias_pendiente = models.IntegerField(blank=True, null=True)
    total_horas_laboradas = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total_dias_gozados= models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'permiso'


class DiasFeriados(models.Model):
    fecha = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dias_feriados'


class IngresosRolEmpleado(models.Model):
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    rol_pago_detalle = models.ForeignKey(RolPagoDetalle, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    deducible = models.BooleanField(blank=True)
    aportaciones = models.BooleanField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    fecha = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    pagar = models.BooleanField(blank=True)
    valor_diario = models.FloatField(blank=True, null=True)
    ingresos_proyectados = models.BooleanField(blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ingresos_rol_empleado'

class EgresosRolEmpleado(models.Model):
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    rol_pago_detalle = models.ForeignKey(RolPagoDetalle, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    anio = models.CharField(max_length=10, blank=True)
    mes = models.IntegerField(blank=True, null=True)
    quincena = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    memo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plantilla_rrhh = models.ForeignKey(PlantillaRrhh, blank=True, null=True)
    egresos_proyectados = models.BooleanField(blank=True)
    class Meta:
        managed = False
        db_table = 'egresos_rol_empleado'


class AnalisisPrestamo(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    fecha = models.DateField(blank=True, null=True)
    sueldo_fijo = models.FloatField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    tipoempleado = models.ForeignKey(TipoEmpleado, blank=True, null=True)
    tiempo_servicio = models.CharField(max_length=255, blank=True)
    motivo_anticipo = models.TextField(blank=True, null=True)
    monto_solicitado = models.FloatField(blank=True, null=True)
    plazo_solicitar = models.CharField(max_length=255, blank=True)
    monto_neto_promedio = models.FloatField(blank=True, null=True)
    monto_promedio_fin_mes = models.FloatField(blank=True, null=True)
    monto_disponible_descuento = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo'

class AnalisisPrestamoDescuentos(models.Model):
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    quincena = models.IntegerField(blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    analisis_prestamo = models.ForeignKey(AnalisisPrestamo, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    iess1 = models.FloatField(blank=True, null=True)
    iess2 = models.FloatField(blank=True, null=True)
    iess3 = models.FloatField(blank=True, null=True)
    salud1 = models.FloatField(blank=True, null=True)
    salud2 = models.FloatField(blank=True, null=True)
    salud3 = models.FloatField(blank=True, null=True)
    telefonia1 = models.FloatField(blank=True, null=True)
    telefonia2 = models.FloatField(blank=True, null=True)
    telefonia3 = models.FloatField(blank=True, null=True)
    ptmo1 = models.FloatField(blank=True, null=True)
    ptmo2 = models.FloatField(blank=True, null=True)
    ptmo3 = models.FloatField(blank=True, null=True)
    donaciones1 = models.FloatField(blank=True, null=True)
    donaciones2 = models.FloatField(blank=True, null=True)
    donaciones3 = models.FloatField(blank=True, null=True)
    otros1 = models.FloatField(blank=True, null=True)
    otros2 = models.FloatField(blank=True, null=True)
    otros3 = models.FloatField(blank=True, null=True)
    quirografario1 = models.FloatField(blank=True, null=True)
    quirografario2 = models.FloatField(blank=True, null=True)
    quirografario3 = models.FloatField(blank=True, null=True)
    total_descuento1 = models.FloatField(blank=True, null=True)
    total_descuento2 = models.FloatField(blank=True, null=True)
    total_descuento3 = models.FloatField(blank=True, null=True)
    total_ingresos1 = models.FloatField(blank=True, null=True)
    total_ingresos2 = models.FloatField(blank=True, null=True)
    total_ingresos3 = models.FloatField(blank=True, null=True)
    anticipo1 = models.FloatField(blank=True, null=True)
    anticipo2 = models.FloatField(blank=True, null=True)
    anticipo3 = models.FloatField(blank=True, null=True)
    sueldo_mensual1 = models.FloatField(blank=True, null=True)
    sueldo_mensual2 = models.FloatField(blank=True, null=True)
    sueldo_mensual3 = models.FloatField(blank=True, null=True)
    neto_recibir1 = models.FloatField(blank=True, null=True)
    neto_recibir2 = models.FloatField(blank=True, null=True)
    neto_recibir3 = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo_descuentos'

class AnalisisPrestamoPromedio(models.Model):
    mes = models.IntegerField(blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    quincena = models.IntegerField(blank=True, null=True)
    total_ingreso = models.FloatField(blank=True, null=True)
    analisis_prestamo = models.ForeignKey(AnalisisPrestamo, blank=True, null=True)
    anticipo = models.FloatField(blank=True, null=True)
    sueldo_mensual = models.FloatField(blank=True, null=True)
    total_descuento = models.FloatField(blank=True, null=True)
    neto_recibir = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_prestamo_promedio'

class Prestamo(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    concepto = models.TextField(blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    plazos = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    saldo_deuda_anterior=models.FloatField(blank=True, null=True)
    total_pagar = models.FloatField(blank=True, null=True)
    aprobado = models.NullBooleanField()
    analisis_prestamo = models.ForeignKey(AnalisisPrestamo, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'prestamo'


class PrestamoDetalle(models.Model):
    fecha = models.DateField(blank=True, null=True)
    abono = models.FloatField(blank=True, null=True)
    cuota = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    descuento = models.CharField(max_length=255, blank=True)
    prestamo = models.ForeignKey(Prestamo, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'prestamo_detalle'


class LiquidacionLaboral(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    fecha = models.DateField(blank=True, null=True)
    sueldo_fijo = models.FloatField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    tipoempleado = models.ForeignKey(TipoEmpleado, blank=True, null=True)
    tiempo_servicio = models.CharField(max_length=255, blank=True)
    fecha_salida = models.DateField(blank=True, null=True)
    motivo = models.CharField(max_length=500, blank=True)
    desahucio = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    sueldo_pendiente_cantidad = models.FloatField(blank=True, null=True)
    sueldo_pendiente_total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    antiguedad_cantidad = models.FloatField(blank=True, null=True)
    total_antiguedad = models.FloatField(blank=True, null=True)
    total_desahucio = models.FloatField(blank=True, null=True)
    total_beneficio = models.FloatField(blank=True, null=True)
    total_vacaciones = models.FloatField(blank=True, null=True)
    total_otros_ingresos = models.FloatField(blank=True, null=True)
    total_descuentos = models.FloatField(blank=True, null=True)
    ptmo = models.FloatField(blank=True, null=True)
    iess = models.FloatField(blank=True, null=True)
    quirografario = models.FloatField(blank=True, null=True)
    adendum_telefonia = models.FloatField(blank=True, null=True)
    consumo_telefonia = models.FloatField(blank=True, null=True)
    bonificacion_in = models.FloatField(blank=True, null=True)
    bonificacion = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_laboral'


class LiquidacionVacaciones(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    fecha = models.DateField(blank=True, null=True)
    sueldo_fijo = models.FloatField(blank=True, null=True)
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, blank=True, null=True)
    tipoempleado = models.ForeignKey(TipoEmpleado, blank=True, null=True)
    fecha_salida = models.DateField(blank=True, null=True)
    fecha_entrada = models.DateField(blank=True, null=True)
    vacaciones = models.FloatField(blank=True, null=True)
    antiguedad_cantidad = models.FloatField(blank=True, null=True)
    antiguedad = models.FloatField(blank=True, null=True)
    total_ingresos = models.FloatField(blank=True, null=True)
    iess = models.FloatField(blank=True, null=True)
    anticipo_vacaciones = models.FloatField(blank=True, null=True)
    total_egresos = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    observacion = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_vacaciones'


class Vacaciones(models.Model):
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    anio = models.IntegerField(blank=True, null=True)
    dias_pagados = models.FloatField(blank=True, null=True)
    dias_descontados = models.FloatField(blank=True, null=True)
    anticipos = models.FloatField(blank=True, null=True)
    total_dias = models.FloatField(blank=True, null=True)
    pagadas = models.BooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    antiguedad = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vacaciones'




class DeudasEmpleado(models.Model):
    empleado = models.ForeignKey(Empleado, blank=True, null=True)
    tipo_ingreso_egreso_empleado = models.ForeignKey(TipoIngresoEgresoEmpleado, blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    valor_mensual = models.FloatField(blank=True, null=True)
    valor_total = models.FloatField(blank=True, null=True)
    activo = models.BooleanField(blank=True)
    aportaciones = models.BooleanField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'deudas_empleado'