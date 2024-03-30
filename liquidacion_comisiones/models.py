from django.db import models
from clientes.models import Cliente, TerminosPago
from inventario.models import Producto
from vendedor.models import *
from proforma.models import Proforma

from datetime import datetime
from config.models import PuntosVenta
# Create your models here.
class LiquidacionComisiones(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    retencion_fuente = models.FloatField(blank=True, null=True)
    retencion_iva = models.FloatField(blank=True, null=True)
    neto_pagar = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    valor_cancelado = models.FloatField(blank=True, null=True)
    valor_cancelado_sin_iva = models.FloatField(blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    total_retenciones = models.FloatField(blank=True, null=True)
    adelanto = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_comisiones'

class LiquidacionComisionesDetalle(models.Model):
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    #proforma_factura = models.ForeignKey(ProformaFactura, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    proforma_codigo = models.CharField(max_length=255, blank=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    detalle = models.TextField(blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    valor_cancelado = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    valor_cancelado_sin_iva = models.FloatField(blank=True, null=True)
    porcentaje_comision = models.FloatField(blank=True, null=True)
    total_comision = models.FloatField(blank=True, null=True)
    liquidacion_comisiones= models.ForeignKey(LiquidacionComisiones, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'liquidacion_comisiones_detalle'


class ProformaComision(models.Model):
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    porcentaje_comision = models.FloatField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'proforma_comision'


class ProformaComisionAbono(models.Model):
    proforma_comision = models.ForeignKey(ProformaComision, blank=True, null=True)
    abono = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proforma_comision_abono'