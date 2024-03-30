from django.db import models
from proveedores.models import Proveedor
from inventario.models import Producto, Unidades

# Create your models here.



class Devolucion(models.Model):
    devolucion_id = models.AutoField(primary_key=True)
    nro_devolucion = models.CharField(max_length=10)
    proveedor = models.ForeignKey(Proveedor)
    supl_direccion1 = models.CharField(max_length=80)
    supl_direccion2 = models.CharField(max_length=80)
    supl_direccion3 = models.CharField(max_length=80)
    supl_direccion4 = models.CharField(max_length=80)
    registro_tributario = models.CharField(max_length=80)
    envia = models.CharField(max_length=80)
    enviar_direccion1 = models.CharField(max_length=80)
    enviar_direccion2 = models.CharField(max_length=80)
    enviar_direccion3 = models.CharField(max_length=80)
    enviar_direccion4 = models.CharField(max_length=80)
    nro_fact_proveedor = models.CharField(db_column='Nro_fact_proveedor', max_length=30)  # Field name made lowercase.
    tipo_envio = models.CharField(max_length=80)
    vendedor = models.CharField(max_length=80)
    terminos_id = models.IntegerField()
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=16)
    fecha_vcmto = models.CharField(max_length=10)
    computador = models.TextField()
    moneda = models.IntegerField()
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    dscto_parcial_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impuesto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos = models.DecimalField(max_digits=18, decimal_places=4)
    miscelaneos_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.CharField(max_length=100)
    comentario_detalle = models.TextField(db_column='comentario_Detalle')  # Field name made lowercase.
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    notas = models.TextField()
    asiento_id = models.IntegerField()
    docs_cp_id = models.IntegerField()
    kardex_id = models.IntegerField()
    impto_en_precio = models.IntegerField()
    actualizado = models.DateTimeField()
    pago = models.DecimalField(max_digits=18, decimal_places=4)
    devolucion_cancelada = models.NullBooleanField()

    class Meta:
        db_table = 'devolucion'


class DevolucionDetalle(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    devolucion = models.ForeignKey('Devolucion')
    fecha = models.CharField(max_length=10)
    proveedor_id = models.IntegerField()
    producto = models.ForeignKey(Producto)
    bodega_id = models.IntegerField()
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    unidad = models.ForeignKey(Unidades)
    precio_compra = models.DecimalField(max_digits=18, decimal_places=4)
    impto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    descto_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    descto_monto = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_pciento = models.DecimalField(max_digits=18, decimal_places=4)
    impto2_monto = models.DecimalField(max_digits=18, decimal_places=4)
    comentario = models.TextField()
    tipo_cambio = models.DecimalField(max_digits=18, decimal_places=4)
    moneda = models.IntegerField()
    nro_item = models.IntegerField()

    class Meta:
        db_table = 'devolucion_Detalle'
