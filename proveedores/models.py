from os.path import basename
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal
# Create your models here.
from contabilidad.models import *
from retenciones.models import TipoRetencion

class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ciudad'

    def __unicode__(self):
        return "%s" % self.nombre

class Vendedor(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_at = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'vendedor'

    def __unicode__(self):
        return "%s" % self.nombre

class Provincia(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null= True)
    fecha_ini = models.DateTimeField(blank=True, null= True )
    class Meta:
        managed = False
        db_table = 'provincia'

    def __unicode__(self):
        return "%s" % self.nombre

class Pais(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'pais'

    def __unicode__(self):
        return "%s" % self.nombre

class TipoRetencion(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_retencion'

class RetencionDetalle(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    porcentaje = models.DecimalField(max_digits=18, decimal_places=2, blank=True, default=Decimal('0'))
    codigo_anexo = models.IntegerField()
    tipo_retencion = models.ForeignKey(TipoRetencion)
    campo_formulario = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'retencion_detalle'
    def __unicode__(self):
        return "%s - %s (%s)" % (self.codigo,self.descripcion,self.porcentaje)


class TipoVenta(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_venta'

    def __unicode__(self):
        return "%s" % self.descripcion

class Proveedor(models.Model):
    proveedor_id = models.AutoField(primary_key=True)
    codigo_proveedor = models.CharField(max_length=26)
    nombre_proveedor = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255, null=True, blank=True)
    razon_social = models.CharField(max_length=255, null=True, blank=True)
    fecha_emision = models.CharField(max_length=255, null=True, blank=True)
    cuenta_contable_compra = models.ForeignKey(PlanDeCuentas,related_name="cuenta_contable_compra", null=True, blank=True)
    tipo_persona = models.CharField(max_length=255, null=True, blank=True)
    tipo_proveedor = models.CharField(max_length=255, null=True, blank=True)
    ruc = models.CharField(max_length=13, null=True, blank=True)
    cedula = models.CharField(max_length=10, null=True, blank=True)
    telefono1 = models.CharField(max_length=255, null=True, blank=True)
    direccion1 = models.CharField(max_length=255, null=True, blank=True)
    cuenta_anticipo = models.ForeignKey(PlanDeCuentas,related_name="cuenta_anticipo", null=True, blank=True)
    vendedor = models.ForeignKey(Vendedor, null=True, blank=True)
    e_mail1 = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    serie = models.CharField(max_length=255, null=True, blank=True)
    dias_credito = models.IntegerField(null=True, blank=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)
    comentario = models.CharField(max_length=255, null=True, blank=True)
    retencion_iva = models.ForeignKey(RetencionDetalle, related_name="retencion_iva", null=True, blank=True)
    retencion_fuente = models.ForeignKey(RetencionDetalle, related_name="retencion_fuente", null=True, blank=True)
    activo = models.BooleanField(default=True)
    saldo_factura = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    autorizacion_imprenta = models.CharField(max_length=100, null=True, blank=True)
    autorizacion_sri = models.CharField(max_length=100, null=True, blank=True)
    factura_desde = models.IntegerField(default=0, null=True, blank=True)
    factura_hasta = models.IntegerField(default=0, null=True, blank=True)
    lleva_contabilidad = models.BooleanField(default=False)
    fecha_validez = models.DateField(default=datetime.now, blank=True)
    tipo_venta = models.ForeignKey(TipoVenta,null=True, blank=True)
    cuenta_gasto = models.ForeignKey(PlanDeCuentas, related_name="cuenta_gasto",null=True, blank=True)
    establecimiento = models.CharField(max_length=25, null=True, blank=True)
    punto_emision = models.CharField(max_length=25, null=True, blank=True)
    secuencial =  models.IntegerField(null=True, blank=True)
    sin_datos= models.BooleanField(default=False)
    class Meta:
        db_table = 'proveedor'

    def __unicode__(self):
        return "%s" % (self.nombre_proveedor)


class TerminosPagopv(models.Model):
    termino_idpv = models.IntegerField()
    codigo_terminopv = models.IntegerField()
    descripcion_terminopv = models.CharField(max_length=255)
    tipo_pago = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    dias = models.IntegerField()
    inicial = models.DecimalField(max_digits=8, decimal_places=2)
    cuotas = models.DecimalField(max_digits=8, decimal_places=2)
    dscto_pronto_pago = models.FloatField()
    cuenta_contable = models.IntegerField()
    predeterminado = models.CharField(max_length=255)
    cuenta_corriente = models.CharField(max_length=255)
    cliente_paga_en = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'terminos_pagopv'

    def __unicode__(self):
        return "%s" % (self.descripcion_terminopv)


class ImagenesPv(models.Model):
    imagen_idpv = models.AutoField(primary_key=True)
    proveedor_id = models.IntegerField()
    imagen_proveedor = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'imagenes_pv'

    def __unicode__(self):
        return "%s" % (self.imagen_proveedor)

class ProveedorPlancuenta(models.Model):
    id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor)
    plancuenta = models.IntegerField(PlanDeCuentas)

    class Meta:
        managed = False
        db_table = 'proveedor_plancuenta'

class ProveedorRetencion(models.Model):
    id = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor)
    retencion = models.ForeignKey(RetencionDetalle)

    class Meta:
        managed = False
        db_table = 'proveedor_retenciones'

