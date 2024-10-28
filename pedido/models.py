from django.db import models
from os.path import basename
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from clientes.models import Cliente
from config.models import TipoMueb,EstadosPro,Notificaciones
from proforma.models import Proforma,ProformaDetalle
from empleados.models import *
from config.models import *
from empleados.models import *
from vendedor.models import *
from inventario.models import *
from proforma.models import *

# Create your models here.

class Pedido(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    fechacord = models.DateField(blank=True, null=True)
    fechapedido = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    subtotal = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    val_descuento = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    val_iva = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    incompleto = models.NullBooleanField()
    observacion = models.TextField(blank=True)
    abono = models.DateField(blank=True, null=True)
    pago = models.NullBooleanField()
    abona = models.BooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    fuera_ciudad = models.BooleanField()
    tiempo_respuesta = models.CharField(max_length=250, blank=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    fechaentrega = models.DateField(blank=True, null=True)
    condiciones_fisicas = models.CharField(max_length=500, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    maqueteado = models.BooleanField()
    proforma_codigo = models.CharField(max_length=250, blank=True)
    aprobada = models.BooleanField()
    direccion_entrega = models.CharField(max_length=250, blank=True)
    forma_pago =models.ForeignKey(FormaPago, blank=True, null=True)
    aprobadavendedor = models.BooleanField()
    terminado_maqueteado_pedido = models.BooleanField()
    anulada = models.BooleanField()
    tipo_lugar = models.ForeignKey(TipoLugar)
    porcentaje_descuento = models.FloatField(blank=True, null=True)
    puntos_venta = models.ForeignKey(PuntosVenta,default=1)
    abreviatura_codigo = models.CharField(max_length=10, blank=True)
    porcentaje_iva = models.FloatField(blank=True, null=True)
    finalizar_maqueteado = models.BooleanField(default=False)
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'pedido'
    def __unicode__(self):
        return "%s" %(self.codigo)
        
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    precio_compra = models.FloatField(blank=True, null=True)
    descto_pciento = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/pedido_detalle/")
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    detalle = models.TextField(blank=True)
    ambiente =models.ForeignKey(Ambiente, blank=True, null=True)
    reparacion = models.NullBooleanField()
    almacen = models.NullBooleanField()
    largo = models.CharField(max_length=255, blank=True)
    fondo = models.CharField(max_length=255, blank=True)
    alto = models.CharField(max_length=255, blank=True)
    codigo_produccion= models.CharField(max_length=255, blank=True)
    no_producir = models.BooleanField(default=False)
    proforma_detalle = models.ForeignKey(ProformaDetalle, blank=True, null=True)
    render = models.BooleanField(default=False)
    class Meta:
        db_table = 'pedido_detalle'


class ImagenesPedido(models.Model):
    descripcion = models.TextField(blank=True)
    pedido_detalle = models.ForeignKey(PedidoDetalle, blank=True, null=True)
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/render_pedido_detalle/")
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'imagenes_pedido'