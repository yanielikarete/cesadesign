from django.db import models
from os.path import basename
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from clientes.models import Cliente
from config.models import TipoMueb,EstadosPro
from proforma.models import Proforma
from empleados.models import *
from config.models import TipoMueb,EstadosPro,FormaPago,Ambiente
from empleados.models import *
from vendedor.models import *
from inventario.models import *
from proforma.models import *
from pedido.models import *


# Create your models here.

class OrdenProduccion(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=False, null=False)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.FloatField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.BooleanField(blank=True)
    vidrio = models.BooleanField(blank=True)
    hierro = models.BooleanField(blank=True)
    marmol = models.BooleanField(blank=True)
    enchape = models.BooleanField(blank=True)
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.BooleanField(blank=True)
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.BooleanField(blank=True)
    panorama = models.BooleanField(blank=True)
    corredizo = models.BooleanField(blank=True)
    oleo = models.BooleanField(blank=True)
    conchaperla = models.BooleanField(blank=True)
    tela_almacen = models.BooleanField(blank=True)
    tela_cliente = models.BooleanField(blank=True)
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/producto/")
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.BooleanField(blank=True)
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mueb = models.ForeignKey(TipoMueb, blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.BooleanField(blank=True)
    semimate = models.BooleanField(blank=True)
    brillante = models.BooleanField(blank=True)
    pulido = models.BooleanField(blank=True)
    aluminio = models.BooleanField(blank=True)
    acero = models.BooleanField(blank=True)
    abrillantado = models.BooleanField(blank=True)
    pintado = models.BooleanField(blank=True)
    satinado = models.BooleanField(blank=True)
    acero_brillante = models.BooleanField(blank=True)
    fechacotizacion = models.BooleanField(blank=True)
    engrampe = models.BooleanField(blank=True)
    impulso = models.BooleanField(blank=True)
    poroabierto = models.BooleanField(blank=True)
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.BooleanField(blank=True)
    observacion = models.CharField(max_length=1255,blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    maqueteado_proforma = models.BooleanField(blank=True)
    terminado_maqueteado_proforma = models.BooleanField(blank=True)
    pedido_codigo = models.CharField(max_length=255, blank=True)
    pedido = models.ForeignKey(Pedido, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    codigo_item = models.CharField(max_length=255, blank=True)
    profundidad = models.CharField(max_length=255, blank=True)
    ancho = models.CharField(max_length=255, blank=True)
    patina_color = models.CharField(max_length=255, blank=True)
    pintado_mano = models.BooleanField(blank=True)
    cuero_almacen = models.BooleanField(blank=True)
    cuero_cliente = models.BooleanField(blank=True)
    fechainicio = models.DateField(blank=True, null=True)
    fechaentrega = models.DateField(blank=True, null=True)
    pedido_detalle= models.ForeignKey(PedidoDetalle, blank=True, null=True)
    aprobada = models.BooleanField(blank=True)
    finalizada = models.NullBooleanField()
    producto_creado = models.ForeignKey(Producto, blank=True, null=True)
    metal_hierro = models.BooleanField(blank=True)
    bodega_productos_blanco = models.BooleanField(blank=True)
    subop_productos_blanco = models.IntegerField(blank=True, null=True)
    imagen_global = models.ImageField(null=True,blank=True,upload_to = "imagenes/producto/")
    neumatico = models.BooleanField(blank=True)
    venta_local = models.BooleanField(blank=True)
    exportacion = models.BooleanField(blank=True)
    polyester = models.BooleanField(blank=True)
    semiabierto = models.BooleanField(blank=True)
    garantia = models.BooleanField(blank=True)
    costo = models.DecimalField(max_digits=18, decimal_places=2,blank=True, default=Decimal('0'))
    costo_directo = models.DecimalField(max_digits=18, decimal_places=2,blank=True, default=Decimal('0'))
    costo_final = models.DecimalField(max_digits=18, decimal_places=2,blank=True, default=Decimal('0'))
    porcentaje_costo = models.DecimalField(max_digits=18, decimal_places=2,blank=True, default=Decimal('0'))
    fecha_aprobacion = models.DateField(blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    despachar =models.BooleanField(default=False,)
    fecha_aprobacion_despacho= models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s" %(self.codigo)
    class Meta:
        managed = False
        db_table = 'orden_produccion'
class Rop(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    detalle = models.TextField(blank=True)
    cantidad = models.FloatField(blank=True, null=True)
    largo = models.CharField(max_length=250, blank=True)
    fondo = models.CharField(max_length=250, blank=True)
    alto = models.CharField(max_length=250, blank=True)
    madera = models.BooleanField()
    vidrio = models.BooleanField()
    hierro = models.BooleanField()
    marmol = models.BooleanField()
    enchape = models.BooleanField()
    enchape_detalle = models.CharField(max_length=250, blank=True)
    tallado = models.BooleanField()
    tallado_detalle = models.CharField(max_length=250, blank=True)
    tono = models.CharField(max_length=250, blank=True)
    retractil = models.BooleanField()
    panorama = models.BooleanField()
    corredizo = models.BooleanField()
    oleo = models.BooleanField()
    conchaperla = models.BooleanField()
    tela_almacen = models.BooleanField()
    tela_cliente = models.BooleanField()
    agarraderas = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    guia = models.IntegerField(blank=True, null=True)
    adicional = models.BooleanField()
    fechapedido = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True)
    estado = models.IntegerField(blank=True, null=True)
    tipo_mueb = models.ForeignKey(TipoMueb, blank=True, null=True)
    doc = models.IntegerField(blank=True, null=True)
    mate = models.BooleanField(blank=True)
    semimate = models.BooleanField(blank=True)
    brillante = models.BooleanField(blank=True)
    pulido = models.BooleanField(blank=True)
    aluminio = models.BooleanField(blank=True)
    acero = models.BooleanField(blank=True)
    abrillantado = models.BooleanField(blank=True)
    pintado = models.BooleanField(blank=True)
    satinado = models.BooleanField(blank=True)
    fechacotizacion = models.BooleanField(blank=True)
    engrampe = models.BooleanField(blank=True)
    impulso = models.BooleanField(blank=True)
    poroabierto = models.BooleanField(blank=True)
    ingreso = models.IntegerField(blank=True, null=True)
    cantaux = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    tiempo_respuesta = models.CharField(max_length=255, blank=True)
    fuera_ciudad = models.BooleanField()
    observacion = models.CharField(max_length=1255,blank=True)
    forma_pago = models.ForeignKey(FormaPago, blank=True, null=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    codigo_item = models.CharField(max_length=255, blank=True)
    profundidad = models.CharField(max_length=255, blank=True)
    ancho = models.CharField(max_length=255, blank=True)
    patina_color = models.CharField(max_length=255, blank=True)
    pintado_mano = models.BooleanField()
    cuero_cliente = models.BooleanField()
    cuero_almacen = models.BooleanField()
    fechainicio = models.DateField(blank=True, null=True)
    fechaentrega = models.DateField(blank=True, null=True)
    aprobada = models.BooleanField(blank=True)
    finalizada = models.BooleanField()
    bodega_productos_blanco = models.BooleanField()
    subop_productos_blanco = models.IntegerField(blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    codigo_orden_produccion = models.CharField(max_length=255, blank=True)
    metal_hierro = models.BooleanField(blank=True)
    detalle = models.TextField(blank=True)
    neumatico = models.BooleanField(blank=True)
    venta_local = models.BooleanField(blank=True)
    exportacion = models.BooleanField(blank=True)
    class Meta:
        managed = False
        db_table = 'rop'
