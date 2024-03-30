from django.db import models
from clientes.models import *
from inventario.models import *
from empleados.models import *
from datetime import datetime
from config.models import *
from vendedor.models import *
from proforma.models import *
from contabilidad.models import *
from vendedor.models import *
#from transacciones.models import RegistroDocumento,DocumentoVenta
from bancos.models import Movimiento,TipoNotaCredito

# Create your models here.
#verificar

class FormaCobro(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'forma_cobro'
    def __unicode__(self):
       return self.descripcion


class TipoGuia(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    accion = models.CharField(max_length=250, blank=True)
    activo = models.BooleanField()
    cuenta_contable_acreedora = models.ForeignKey(PlanDeCuentas, related_name="cuenta_contable_acreedora", null=True,blank=True)
    cuenta_contable_deudora = models.ForeignKey(PlanDeCuentas, related_name="cuenta_contable_deudora", null=True,blank=True)
    class Meta:
        managed = False
        db_table = 'tipo_guia'
    def __unicode__(self):
        return '%s' % (self.descripcion)

class GuiaRemision(models.Model):
    guia_id = models.AutoField(primary_key=True)
    nro_guia = models.IntegerField()
    fecha_inicio = models.DateField(default=datetime.now,blank=True, null=True)
    fecha_fin = models.DateField(default=datetime.now,blank=True, null=True)
    tipo_documento = models.CharField(max_length=20,blank=True, null=True)
    #fecha_emision = models.DateField(default=datetime.now,blank=True, null=True)
    fecha_emision = models.DateField(default=datetime.now)
    nro_autorizacion = models.CharField(max_length=30,blank=True,)
    nro_comprobante = models.CharField(max_length=30,blank=True,)
    VENTA='VENTA'
    COMPRA='COMPRA'
    TRASNF='TRASNF'
    CONSIG='CONSIG'
    DEVOLU='DEVOLU'
    IMPORT='IMPORT'
    EXPORT='EXPORT'
    TRASLE='TRASLE'
    TRASLF='TRASLF'
    OTROS='OTROS'
    MOTIVO_CHOICES=(
        (VENTA,'Venta'),
        (COMPRA,'Compra'),
        (TRASNF,'Transformacion'),
        (CONSIG,'Consignacion'),
        (DEVOLU,'Devolucion'),
        (IMPORT,'Importacion'),
        (EXPORT,'Exportacion'),
        (TRASLE,'Traslado entre establecimientos de la misma empresa'),
        (TRASLF,'Traslado por emisor itinerante de facturas'),
        (OTROS,'Otros'),
    )
    partida = models.CharField(max_length=256,blank=True, null=True)
    destino = models.CharField(max_length=256,blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    chofer = models.ForeignKey(Chofer, blank=True, null=True)
    vehiculo = models.ForeignKey(Vehiculo, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True,blank=True)
    tipo_guia = models.ForeignKey(TipoGuia,blank=True, null=True)
    aprobada = models.BooleanField(blank=True)
    ingreso = models.BooleanField(blank=True)
    egreso = models.BooleanField(blank=True)
    parcial = models.BooleanField(blank=True)
    puntos_venta = models.ForeignKey(PuntosVenta,default=1,blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    anulada = models.BooleanField(default=False,blank=True)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    facturacion_eletronica = models.BooleanField(default=False,blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.nro_guia, self.fecha_inicio, self.tipo_guia)


class GuiaDetalle(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    guia= models.ForeignKey(GuiaRemision)
    producto = models.ForeignKey(Producto)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    descripcion = models.CharField(max_length=500, blank=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    nro_documento=models.IntegerField(blank=True,default=0)
    precio_compra = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2)



# class NotaCredito(models.Model):
#     nro_nota_credito = models.CharField(max_length=10, blank=True)
#     tipo_factura = models.IntegerField(blank=True, null=True)
#     cliente = models.ForeignKey(Cliente, blank=True, null=True)
#     clte_direccion1 = models.CharField(max_length=80, blank=True)
#     clte_direccion2 = models.CharField(max_length=80, blank=True)
#     clte_direccion3 = models.CharField(max_length=80, blank=True)
#     clte_direccion4 = models.CharField(max_length=80, blank=True)
#     registro_tributario = models.CharField(max_length=80, blank=True)
#     enviar = models.CharField(max_length=80, blank=True)
#     enviar_direccion1 = models.CharField(max_length=80, blank=True)
#     enviar_direccion2 = models.CharField(max_length=80, blank=True)
#     enviar_direccion3 = models.CharField(max_length=80, blank=True)
#     enviar_direccion4 = models.CharField(max_length=80, blank=True)
#     refer_cliente = models.CharField(max_length=20, blank=True)
#     tipo_envio = models.CharField(max_length=80, blank=True)
#     vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
#     hora = models.CharField(max_length=16, blank=True)
#     fecha_vcmto = models.CharField(max_length=10, blank=True)
#     computador = models.TextField(blank=True)
#     subtotal = models.FloatField(blank=True, null=True)
#     total = models.FloatField(blank=True, null=True)
#     iva_pciento = models.FloatField(blank=True, null=True)
#     iva_monto = models.FloatField(blank=True, null=True)
#     dscto_pciento = models.FloatField(blank=True, null=True)
#     dscto_monto = models.FloatField(blank=True, null=True)
#     dscto_parcial_monto = models.FloatField(blank=True, null=True)
#     impuesto2_pciento = models.FloatField(blank=True, null=True)
#     impuesto2_monto = models.FloatField(blank=True, null=True)
#     miscelaneos = models.FloatField(blank=True, null=True)
#     miscelaneos_pciento = models.FloatField(blank=True, null=True)
#     observacion = models.TextField(blank=True)
#     comentario_detalle = models.TextField(db_column='comentario_Detalle', blank=True) # Field name made lowercase.
#     tipo_cambio = models.FloatField(blank=True, null=True)
#     notas = models.TextField(blank=True)
#     tipo_documento = models.CharField(max_length=40, blank=True)
#     retefuente_pciento = models.FloatField(blank=True, null=True)
#     retefuente_monto = models.FloatField(blank=True, null=True)
#     reteiva_pciento = models.FloatField(blank=True, null=True)
#     reteiva_monto = models.FloatField(blank=True, null=True)
#     reteica_pciento = models.FloatField(blank=True, null=True)
#     reteica_monto = models.FloatField(blank=True, null=True)
#     monto_base = models.FloatField(blank=True, null=True)
#     nro_estimado = models.CharField(max_length=10, blank=True)
#     actualizado = models.DateTimeField(blank=True, null=True)
#     ncf = models.CharField(max_length=50, blank=True)
#     en_anexo = models.CharField(max_length=2, blank=True)
#     campo1 = models.CharField(max_length=30, blank=True)
#     campo2 = models.FloatField(blank=True, null=True)
#     campo3 = models.CharField(max_length=20, blank=True)
#     asiento_id = models.IntegerField(blank=True, null=True)
#     pagos = models.FloatField(blank=True, null=True)
#     causa_anulacion = models.TextField(blank=True)
#     fecha = models.DateField(blank=True, null=True)
#     puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
#     ruc = models.CharField(max_length=20, blank=True)
#     bodega = models.ForeignKey(Bodega, blank=True, null=True)
#     
#     razon_social = models.ForeignKey(RazonSocial, blank=True, null=True)
#     factura_codigo = models.CharField(max_length=20, blank=True)
#     tipo_nota_credito = models.ForeignKey(TipoNotaCredito, blank=True, null=True)
#     
#     class Meta:
#         managed = False
#         db_table = 'nota_credito'
# 
# class NotaCreditoDetalle(models.Model):
#     nota_credito = models.ForeignKey(NotaCredito, blank=True, null=True)
#     fecha = models.DateTimeField(blank=True, null=True)
#     nombre = models.CharField(max_length=255, blank=True)
#     producto = models.ForeignKey(Producto, blank=True, null=True)
#     cantidad = models.FloatField(blank=True, null=True)
#     precio_compra = models.FloatField(blank=True, null=True)
#     descto_pciento = models.FloatField(blank=True, null=True)
#     medida = models.CharField(max_length=255, blank=True)
#     observaciones = models.CharField(max_length=255, blank=True)
#     created_by = models.CharField(max_length=255, blank=True)
#     updated_by = models.CharField(max_length=255, blank=True)
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     total = models.FloatField(blank=True, null=True)
#     detalle = models.TextField(blank=True, null=True)
#     codigo_produccion = models.CharField(max_length=255, blank=True)
#     documento_venta = models.ForeignKey(DocumentoVenta, blank=True, null=True)
#     class Meta:
#         managed = False
#         db_table = 'nota_credito_detalle'


class TipoTransaccion(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_transaccion'
    def __unicode__(self):
       return self.nombre 

class TransaccionesFormapago(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'transacciones_formapago'
    def __unicode__(self):
       return self.descripcion

class RegistrarCobroPago(models.Model):
    numero_documento = models.CharField(max_length=250,blank=True, null=True)
    tipo_transaccion = models.ForeignKey(TipoTransaccion,default=1)
    forma_cobro = models.ForeignKey(FormaCobro, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    cuenta_pago_cobro = models.CharField(max_length=255, blank=True, null=True)
    numero_comprobante = models.CharField(max_length=255, blank=True, null=True)
    efectivo = models.BooleanField(blank=True, default=False)
    descripcion = models.TextField( blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    plan_cuenta = models.ForeignKey(PlanDeCuentas, blank=True, null=True)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    transacciones_forma_pago = models.ForeignKey(TransaccionesFormapago, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    paguese_a = models.CharField(max_length=500, blank=True)
    numero_cheque = models.CharField(max_length=20, blank=True)
    fecha_cheque = models.DateField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'registrar_cobro_pago'

class RegistrarCobroPagoDetalle(models.Model):
    codigo = models.CharField(max_length=250,blank=True, null=True)
    documento = models.CharField(max_length=250,blank=True, null=True)
    fecha_emision = models.DateField(blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    tipo_documento = models.CharField(max_length=250, blank=True)
    valor = models.FloatField(blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    valor_a_pagar = models.FloatField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    #proforma_factura = models.ForeignKey(ProformaFactura, blank=True, null=True)
    #factura = models.ForeignKey(Factura, blank=True, null=True)
    registrar_cobro_pago = models.ForeignKey(RegistrarCobroPago, blank=True, null=True)
    fecha_pago = models.DateField(blank=True, null=True)
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    #registro_documento = models.ForeignKey(RegistroDocumento, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'registrar_cobro_pago_detalle'


class CruceDocumento(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha_emision = models.DateField(blank=True, null=True)
    persona_id = models.IntegerField(blank=True, null=True)
    #registro_documento= models.ForeignKey(RegistroDocumento, blank=True, null=True)
    saldo = models.FloatField(blank=True, null=True)
    tipo_transaccion = models.ForeignKey(TipoTransaccion, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cruce_documento'


class CruceDocumentoDetalle(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    #registro_documento = models.ForeignKey(RegistroDocumento, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    anticipo_id = models.IntegerField(blank=True, null=True)
    valor_anticipo = models.FloatField(blank=True, null=True)
    plan_cuentas = models.ForeignKey(PlanDeCuentas, blank=True, null=True)
    valor_cuentas_contable = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cruce_documento_detalle'