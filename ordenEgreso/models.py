from django.db import models

# Create your models here.
from django.db import models
from proveedores.models import Proveedor
from inventario.models import Producto,Bodega,Unidades,Areas
from contabilidad.models import Asiento
from datetime import datetime
from subordenproduccion.models import OrdenProduccionReceta


class ConceptoOrdenEgreso(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    observacion = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    op = models.BooleanField(default=False)
    cuenta = models.CharField(max_length=20, blank=True)
    class Meta:
        managed = False
        db_table = 'concepto_orden_egreso'

    def __unicode__(self):
        return "%s" % (self.nombre)

class OrdenEgreso(models.Model):
    #codigo = models.CharField(max_length=255, blank=True)
    codigo = models.CharField(max_length=255, blank=False)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    supl_direccion1 = models.CharField(max_length=255, blank=True)
    supl_direccion2 = models.CharField(max_length=255, blank=True)
    supl_direccion3 = models.CharField(max_length=255, blank=True)
    supl_direccion4 = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    enviar = models.NullBooleanField()
    enviar_direccion1 = models.CharField(max_length=255, blank=True)
    enviar_direccion2 = models.CharField(max_length=255, blank=True)
    enviar_direccion3 = models.CharField(max_length=255, blank=True)
    enviar_direccion4 = models.CharField(max_length=255, blank=True)
    nro_fact_proveedor = models.CharField(max_length=255, blank=True)
    tipo_envio = models.CharField(max_length=255, blank=True)
    vendedor = models.CharField(max_length=255, blank=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(default=datetime.now,blank=True, null=True)
    hora = models.DateTimeField(blank=True, null=True)
    fecha_vcmto = models.DateTimeField(blank=True, null=True)
    pagos = models.CharField(max_length=255, blank=True)
    computador = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    impuesto_pciento = models.FloatField(blank=True, null=True)
    impuesto_monto = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    dscto_parcial_monto = models.FloatField(blank=True, null=True)
    impuesto2_pciento = models.FloatField(blank=True, null=True)
    impuesto2_monto = models.FloatField(blank=True, null=True)
    miscelaneos = models.CharField(max_length=255, blank=True)
    miscelaneos_pciento = models.CharField(max_length=255, blank=True)
    comentario = models.CharField(max_length=255, blank=True)
    comentario_detalle = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    OBJETO_CHOICES=(
        ("Egreso por Despacho a Tercero","Egreso por Despacho a Tercero"),
        ("Egreso por Devolucion de Compra","Egreso por Devolucion de Compra"),
        ("Egresos DIMID","Egresos DIMID"),
        ("Egresos Filadelfia","Egresos Filadelfia"),
        ("Egresos Fundacion Hogar de Jesus","Egresos Fundacion Hogar de Jesus"),
        ("Egresos Orden Produccion","Egresos por Orden de Produccion"),
        ("Egresos Mireya Dalmau","Egresos Mireya Dalmau"),
    )
    #notas = models.CharField(max_length=255, blank=True, choices=OBJETO_CHOICES)
    notas = models.CharField(max_length=255, blank=True)
    asiento_id = models.IntegerField(blank=True, null=True)
    docs_cp_id = models.IntegerField(blank=True, null=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    tipo_compra = models.CharField(max_length=255, blank=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    tipo_registracion = models.CharField(max_length=255, blank=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    ncf = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    aprobada = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    facturada = models.NullBooleanField()
    orden_produccion_codigo= models.CharField(max_length=255, blank=True)
    concepto_orden_egreso = models.ForeignKey(ConceptoOrdenEgreso, blank=True, null=True)
    aprobado_por = models.CharField(max_length=255, blank=True)
    aprobado_at = models.DateTimeField(blank=True, null=True)
    anulado_por = models.CharField(max_length=255, blank=True)
    anulado_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'orden_egreso'

class OrdenEgresoDetalle(models.Model):
    orden_egreso = models.ForeignKey(OrdenEgreso, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    proveedor_id = models.IntegerField(blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    bodega= models.ForeignKey(Bodega, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    recibido = models.NullBooleanField()
    unidad_id = models.IntegerField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    impto_pciento = models.FloatField(blank=True, null=True)
    impto_monto = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    descto_monto = models.FloatField(blank=True, null=True)
    impto2_pciento = models.FloatField(blank=True, null=True)
    impto2_monto = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    tipo_cambio = models.CharField(max_length=255, blank=True)
    moneda = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    despachar = models.BooleanField()
    disminuir_kardex = models.BooleanField()
    unidad_medida = models.CharField(max_length=255, blank=True)
    op = models.BooleanField(default=False)
    orden_produccion_receta = models.ForeignKey(OrdenProduccionReceta, blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden_egreso_detalle'

class EgresoOrdenEgreso(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    orden_egreso = models.ForeignKey(OrdenEgreso, blank=True, null=True)
    terminos_id = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(default=datetime.now,blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    kardex_id = models.IntegerField(blank=True, null=True)
    recibida = models.CharField(max_length=255, blank=True)
    impto_en_precio = models.FloatField(blank=True, null=True)
    retefuente_pciento = models.FloatField(blank=True, null=True)
    retefuente_monto = models.FloatField(blank=True, null=True)
    reteiva_pciento = models.FloatField(blank=True, null=True)
    reteiva_monto = models.FloatField(blank=True, null=True)
    reteica_pciento = models.FloatField(blank=True, null=True)
    reteica_monto = models.FloatField(blank=True, null=True)
    monto_base = models.FloatField(blank=True, null=True)
    anulado = models.NullBooleanField()
    compra_cancelada = models.NullBooleanField()
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'egreso_orden_egreso'

