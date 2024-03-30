from django.db import models
from datetime import datetime
from decimal import Decimal

class EjercicioContable(models.Model):
    ejercicio_id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    abierto = models.BooleanField()
    cierreMensual = models.BooleanField()
    dia_cierre = models.IntegerField(null=True, blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s %s" % (self.fecha_inicio, self.fecha_fin)

class PlanDeCuentas(models.Model):
    CATEGORIA = (
        ('GENERAL', 'GENERAL'),
        ('DETALLE', 'DETALLE'),
    )
    CATEGORIA_ESPECIAL = (
        ('CAJA', 'CAJA'),
        ('BANCO', 'BANCO'),
        ('CLIENTE', 'CLIENTE'),
        ('INVENTARIO', 'INVENTARIO'),
    )
    plan_id = models.AutoField(primary_key=True)
    grupo = models.ForeignKey('PlanDeCuentas', null=True, blank=True)
    nombre_plan = models.CharField(max_length=50)
    tipo_cuenta = models.ForeignKey('TipoCuenta')
    codigo_plan = models.CharField(max_length=20)
    created_by = models.CharField(max_length=255,null=True, blank=True)
    updated_by = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    nivel = models.IntegerField(default=4,null=False, blank=False)
    descripcion = models.CharField(max_length=255,null=True, blank=True)
    #nivel_padre = models.CharField(max_length=255,null=True, blank=True)
    nivel_padre = models.CharField(max_length=255)
    calificacion = models.CharField(max_length=250,null=True, blank=True)
    categoria = models.CharField(max_length=25, choices=CATEGORIA,null=True, blank=True)
    categoria_especial = models.CharField(max_length=25, choices=CATEGORIA_ESPECIAL,null=True, blank=True)
    saldo_inicial = models.DecimalField(max_digits=18, decimal_places=2)

    def __unicode__(self):
        return "%s %s" % (self.codigo_plan, self.nombre_plan)

class TipoCuenta(models.Model):
    tipo_id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)
    acreedora = models.BooleanField(default=False)
    deudora = models.BooleanField(default=False)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.nombre_tipo)

class CentroCosto(models.Model):
    centro_id = models.AutoField(primary_key=True)
    nombre_centro = models.CharField(max_length=50)  
    padre = models.ForeignKey('CentroCosto', null=True, blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo = models.BooleanField(default=True)
    codigo = models.CharField(max_length=50,null=True, blank=True,default='')
    secuencia_subcentro= models.IntegerField(default=0,null=True, blank=True)
    por_defecto = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % (self.nombre_centro)

class Asiento(models.Model):
    asiento_id = models.AutoField(primary_key=True)
    codigo_asiento = models.CharField(max_length=30)
    fecha = models.DateField(default=datetime.now, blank=True)
    glosa = models.CharField(max_length=500)
    gasto_no_deducible = models.BooleanField()
    secuencia_asiento= models.IntegerField(default=0,null=True, blank=True)
    total_debe = models.DecimalField(max_digits=18, decimal_places=2)
    total_haber = models.DecimalField(max_digits=18, decimal_places=2)
    anulado = models.BooleanField(default=False)
    modulo = models.CharField(max_length=255,null=True, blank=True,default='')
    codigo= models.CharField(max_length=30,null=True, blank=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    anulado_por = models.CharField(max_length=255, blank=True, null=True)
    anulado_at = models.DateTimeField(blank=True, null=True)
    motivo_anulacion =models.TextField(blank=True, null=True)
    inicial = models.BooleanField(default=False)


    def __unicode__(self):
        return "%s %s" % (self.fecha, self.glosa)

class AsientoDetalle(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    asiento = models.ForeignKey('Asiento')
    cuenta = models.ForeignKey('PlanDeCuentas')
    debe = models.DecimalField(max_digits=18, decimal_places=2)
    haber = models.DecimalField(max_digits=18, decimal_places=2)
    centro_costo = models.ForeignKey('CentroCosto', null=True, blank=True)
    concepto = models.CharField(max_length=255,default='')
    tipo = models.CharField(max_length=255,null=True, blank=True)
    subtipo = models.CharField(max_length=255,null=True, blank=True)

    

# class AsientoPredefinido(models.Model):
#     asiento_predef_id = models.AutoField(primary_key=True)
#     codigo_predef = models.CharField(max_length=10)
#     descripcion_predef = models.CharField(max_length=100)
#     cuenta_contable = models.CharField(max_length=20)
#     debe_haber = models.CharField(max_length=1)
#     cantidad = models.DecimalField(max_digits=18, decimal_places=4)
#     libro_id = models.IntegerField()
#     explicacion_asiento = models.CharField(db_column='Explicacion_asiento', max_length=100)  # Field name made lowercase.
#     referencia_por_cta = models.CharField(db_column='referencia_por_Cta', max_length=100)  # Field name made lowercase.
#     dcto_id = models.IntegerField()
#     fuente_id = models.IntegerField()
#     nro_nit = models.CharField(max_length=30)
#     centro_costo_id = models.IntegerField()
#     ultimo_posteo = models.CharField(max_length=10)

#     class Meta:
#         db_table = 'Asiento_predefinido'


# class Asiento(models.Model):
#     asiento_id = models.AutoField(primary_key=True)
#     codigo_asiento = models.IntegerField()
#     fecha_asiento = models.CharField(max_length=10)  # Field name made lowercase.
#     nro_consecutivo = models.IntegerField()
#     cuenta_contable = models.CharField(max_length=20)
#     debe_haber = models.CharField(max_length=1)
#     cantidad = models.DecimalField(max_digits=18, decimal_places=4)
#     libro = models.ForeignKey(LibroAuxiliar)
#     explicacion_asiento = models.CharField(max_length=100)  # Field name made lowercase.
#     referencia_por_cta = models.CharField(max_length=100)  # Field name made lowercase.
#     nro_comprobante = models.CharField(max_length=40)
#     fuente = models.ForeignKey(Fuente)
#     nro_nit = models.CharField(max_length=30)
#     centro_costo_id = models.IntegerField()
#     modulo_origen = models.CharField(max_length=3)  # Field name made lowercase.
#     dcto_origen_id = models.IntegerField()
#     nro_documento = models.CharField(max_length=10)
#     valor_base = models.DecimalField(max_digits=18, decimal_places=4)  # Field name made lowercase.
#     dcto = models.ForeignKey(DctoContable)
#     estado = models.IntegerField()
#     motivo_anulacion = models.CharField(max_length=100)

#     class Meta:
#         db_table = 'asientos'

# class DctoContable(models.Model):
#     dcto_id = models.AutoField(primary_key=True)
#     codigo_dcto = models.CharField(max_length=4)
#     descripcion_dcto = models.CharField(max_length=60)
#     contador_dcto = models.DecimalField(max_digits=18, decimal_places=0)
#     incremento_dcto = models.DecimalField(max_digits=18, decimal_places=0)
#     usa_contador = models.IntegerField()
#     generado_por = models.IntegerField()

#     class Meta:
#         db_table = 'Dcto_contable'

# class Fuente(models.Model):
#     fuente_id = models.AutoField(primary_key=True)
#     codigo_fuente = models.CharField(max_length=4)
#     nombre_fuente = models.CharField(max_length=30)  # Field name made lowercase.

#     class Meta:
#         db_table = 'Fuentes'

# class LibroAuxiliar(models.Model):
#     libro_id = models.AutoField(primary_key=True)
#     nombre_libro = models.CharField(max_length=80)
#     secuencial = models.IntegerField()
#     incremento = models.IntegerField()
#     iniciales_libro = models.CharField(max_length=3)
#     generado_por = models.IntegerField()
#     usa_contador_mes = models.IntegerField()

#     class Meta:
#         db_table = 'Libro_auxiliar'

class Banco(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banco'

    def __unicode__(self):
       return self.nombre
    
class PeriodoAnterior(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=500, blank=True)
    anio = models.IntegerField(null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)
    plan = models.ForeignKey('PlanDeCuentas', null=True, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    saldo_periodo = models.FloatField(blank=True, null=True)
    saldo_anterior = models.FloatField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'periodo_anterior'


