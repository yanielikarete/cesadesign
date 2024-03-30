
# Create your models here.
from django.db import models
from proveedores.models import Proveedor
from clientes.models import *
from inventario.models import Producto,Bodega,Unidades
from datetime import datetime
from subordenproduccion.models import OrdenProduccionReceta

# Create your models here.
class ConceptoAjustes(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    observacion = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    op = models.BooleanField(default=False)
    contabilizacion = models.BooleanField(default=False)
    class Meta:
        managed = False
        db_table = 'concepto_ajustes'

    def __unicode__(self):
        return "%s" % (self.nombre)

class Ajustes(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    tipo = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(default=datetime.now,blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)
    moneda = models.CharField(max_length=255, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    comentario_detalle = models.CharField(max_length=255, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    anulado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    imprimir = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega,blank=True, null=True)
    concepto_ajustes = models.ForeignKey(ConceptoAjustes, blank=False, null=False)
    class Meta:
        managed = False
        db_table = 'ajustes'

class AjustesDetalle(models.Model):
    ajustes = models.ForeignKey(Ajustes, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    bodega_id = models.IntegerField(blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'ajustes_detalle'

#class IngresoOrdenIngreso(models.Model):
#    codigo = models.CharField(max_length=255, blank=True)
#    orden_ingreso = models.ForeignKey(OrdenIngreso, blank=True, null=True)
#    terminos_id = models.IntegerField(blank=True, null=True)
#    fecha = models.DateTimeField(blank=True, null=True)
#    subtotal = models.FloatField(blank=True, null=True)
#    total = models.FloatField(blank=True, null=True)
#    dscto_pciento = models.FloatField(blank=True, null=True)
#    dscto_monto = models.FloatField(blank=True, null=True)
#    iva = models.FloatField(blank=True, null=True)
#    comentario = models.CharField(max_length=255, blank=True)
#    kardex_id = models.IntegerField(blank=True, null=True)
#    recibida = models.CharField(max_length=255, blank=True)
#    impto_en_precio = models.FloatField(blank=True, null=True)
#    retefuente_pciento = models.FloatField(blank=True, null=True)
#    retefuente_monto = models.FloatField(blank=True, null=True)
#    reteiva_pciento = models.FloatField(blank=True, null=True)
#    reteiva_monto = models.FloatField(blank=True, null=True)
#    reteica_pciento = models.FloatField(blank=True, null=True)
#    reteica_monto = models.FloatField(blank=True, null=True)
#    monto_base = models.FloatField(blank=True, null=True)
#    anulado = models.NullBooleanField()
#    compra_cancelada = models.NullBooleanField()
#    actualizado = models.NullBooleanField()
#    created_by = models.CharField(max_length=255, blank=True)
#    updated_by = models.CharField(max_length=255, blank=True)
#    created_at = models.DateTimeField(blank=True, null=True)
#    updated_at = models.DateTimeField(blank=True, null=True)
#    class Meta:
#        managed = False
#        db_table = 'ingreso_orden_ingreso'
