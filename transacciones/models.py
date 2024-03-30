
from django.contrib.auth.models import User
from decimal import Decimal

from OrdenesdeCompra.models import *
from clientes.models import Cliente
from contabilidad.models import *
from inventario.models import *
from empleados.models import Empleado
from retenciones.models import TipoRetencion
from bancos.models import Banco,Movimiento,AjusteFacturaAbonoProforma
from config.models import *
from vendedor.models import *
from reunion.models import *
from mantenimiento.models import *
from proforma.models import *
from facturacion.models import *
from ordenproduccion.models import *

class RegistroDocumento(models.Model):
    fecha = models.DateField(blank=True, null=True)
    fecha_emision = models.DateField(name="documento-fecha-emision")
    cliente = models.ForeignKey(Cliente, null=True)
    vendedor = models.ForeignKey(Empleado, null=True)
    vencimiento = models.IntegerField(blank=True, null=True)
    forma_de_pago = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)
    bodega = models.ForeignKey(Bodega,blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True)
    subtotal12 = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal0 = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    saldo = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    saldo_cobrar = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transacciones_registrodocumento'


class RegistroDocumentoDetalle(models.Model):
    detalle_id = models.AutoField(primary_key=True)
    registrodoc = models.ForeignKey(RegistroDocumento)
    PRODUCTO = 1
    CUENTA = 2
    TIPO_DET_CHOICES = (
        (PRODUCTO, "producto"),
        (CUENTA, "cuenta"),
    )
    tipo = models.IntegerField(choices=TIPO_DET_CHOICES, )
    cantidad = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cuenta = models.ForeignKey(PlanDeCuentas)
    centro = models.ForeignKey(CentroCosto)
    valor = models.DecimalField(max_digits=18, decimal_places=4)
    iva = models.DecimalField(max_digits=4, decimal_places=2)
    ice = models.DecimalField(max_digits=4, decimal_places=2)
    retencion_ir = models.ForeignKey(TipoRetencion, related_name='detalledoc_ir')
    retencion_iva = models.ForeignKey(TipoRetencion, related_name='detalledoc_iva')
    desc = models.DecimalField(max_digits=18, decimal_places=4)
    subtotal = models.DecimalField(max_digits=18, decimal_places=4)

    class Meta:
        managed = False
        db_table = 'transacciones_registrodocumentodetalle'


class Deposito(models.Model):
    fecha_corte = models.DateField()
    fecha = models.DateField()
    banco = models.ForeignKey(Banco)
    numero_comprobante = models.IntegerField()
    total = models.DecimalField(decimal_places=2, max_digits=20)
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'deposito'


class TransaccionTipoDocuemento(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'transaccion_tipodocumento'


class TipoRetencion(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_retencion'


class RetencionDetalle(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    porcentaje = models.DecimalField(max_digits=18, decimal_places=4, blank=True, default=Decimal('0'))
    codigo_anexo = models.IntegerField()
    tipo_retencion = models.ForeignKey(TipoRetencion)
    campo_formulario = models.IntegerField()
    cuenta = models.ForeignKey(PlanDeCuentas, null=True, blank=True)
    codigo_facturacion_electronica = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'retencion_detalle'


class SriFormaPago(models.Model):
    descripcion = models.CharField(max_length=250)
    codigo = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'sri_forma_pago'


class DocumentoCompra(models.Model):
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_emision = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    orden_compra = models.ForeignKey(OrdenCompra,blank=True, null=True)
    establecimiento = models.CharField(max_length=3)
    punto_emision = models.CharField(max_length=3)
    secuencial = models.CharField(max_length=255)
    autorizacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    base_iva = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True)
    base_ice = models.DecimalField(max_digits=18, decimal_places=4)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    retenido = models.BooleanField(default=False)
    pagado = models.BooleanField(default=True, blank=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    tipo_provision = models.CharField(max_length=100,blank=True,null=True)
    sustento_tributario = models.ForeignKey(SustentoTributario,blank=True,null=True)
    generada= models.BooleanField(default=False)
    compra = models.ForeignKey(ComprasLocales, blank=True, null=True)
    sri_forma_pago = models.ForeignKey(SriFormaPago, blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    total_pagar = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    nota_credito = models.BooleanField(default=False)
    anulado = models.BooleanField(default=False)
    valor_retenido = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    base_no_iva_factura=models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True, default=Decimal('0'));
    base_rise_factura=models.DecimalField(max_digits=18, decimal_places=4,blank=True, null=True, default=Decimal('0'));
    no_afecta= models.BooleanField(default=False)
    facturacion_eletronica = models.BooleanField(default=False)
    afecta_produccion= models.BooleanField(default=False)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)
    ats = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'documento_compra'


class DocumentosCompraDetalle(models.Model):
    documento_compra = models.ForeignKey(DocumentoCompra)
    producto = models.ForeignKey(Producto)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    base_iva = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=4)
    base_ice = models.DecimalField(max_digits=18, decimal_places=4)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'documento_compra_detalle'


class DocumentosRetencionCompra(models.Model):
    documento_compra = models.ForeignKey(DocumentoCompra)
    fecha_emision = models.DateField()
    establecimiento = models.CharField(max_length=3)
    punto_emision = models.CharField(max_length=3)
    secuencial = models.CharField(max_length=255)
    autorizacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    migrado = models.BooleanField(default=False)

    class Meta:
        db_table = 'documento_retencion_compra'


class DocumentosRetencionDetalleCompra(models.Model):
    documento_retencion_compra = models.ForeignKey(DocumentosRetencionCompra)
    retencion_detalle = models.ForeignKey(RetencionDetalle)
    base_imponible = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_retencion = models.DecimalField(max_digits=18, decimal_places=4)
    valor_retenido = models.DecimalField(max_digits=18, decimal_places=4)
    migrado = models.BooleanField(default=False)

    class Meta:
        db_table = 'documento_retencion_detalle_compra'


class DocumentoFormaPago(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    documento_compra = models.ForeignKey(DocumentoCompra, blank=True)

    class Meta:
        managed = False
        db_table = 'documento_forma_pago'

#----------------------------------------------------------
class DocumentoLCompra(models.Model):
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_emision = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    orden_compra = models.ForeignKey(OrdenCompra, blank=True, null=True)
    establecimiento = models.CharField(max_length=3)
    punto_emision = models.CharField(max_length=3)
    secuencial = models.CharField(max_length=255)
    autorizacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    base_iva = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    base_ice = models.DecimalField(max_digits=18, decimal_places=4)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    total = models.DecimalField(max_digits=18, decimal_places=4)
    retenido = models.BooleanField(default=False)
    pagado = models.BooleanField(default=True, blank=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    tipo_provision = models.CharField(max_length=100, blank=True, null=True)
    sustento_tributario = models.ForeignKey(SustentoTributario, blank=True, null=True)
    generada = models.BooleanField(default=False)
    compra = models.ForeignKey(ComprasLocales, blank=True, null=True)
    sri_forma_pago = models.ForeignKey(SriFormaPago, blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    total_pagar = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    nota_credito = models.BooleanField(default=False)
    anulado = models.BooleanField(default=False)
    valor_retenido = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    base_no_iva_factura = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True,
                                              default=Decimal('0'));
    base_rise_factura = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True,
                                            default=Decimal('0'));
    no_afecta = models.BooleanField(default=False)
    facturacion_eletronica = models.BooleanField(default=False)
    afecta_produccion = models.BooleanField(default=False)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)
    ats = models.BooleanField(default=False)

    class Meta:
        db_table = 'documento_lcompra'


class DocumentosLCompraDetalle(models.Model):
    documento_compra = models.ForeignKey(DocumentoCompra)
    producto = models.ForeignKey(Producto)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=4)
    base_iva = models.DecimalField(max_digits=18, decimal_places=4)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=4)
    base_ice = models.DecimalField(max_digits=18, decimal_places=4)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=4)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=4)
    descuento = models.DecimalField(max_digits=18, decimal_places=4)
    cantidad = models.DecimalField(max_digits=18, decimal_places=4)
    descripcion = models.CharField(max_length=255)

    class Meta:
        db_table = 'documento_lcompra_detalle'


#----------------------------------------------------------
class TipoComprobanteVentas(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'tipo_comprobante_ventas'


class DocumentoVenta(models.Model):
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_emision = models.DateField()
    establecimiento = models.CharField(max_length=3)
    punto_emision = models.CharField(max_length=3)
    secuencial = models.CharField(max_length=255)
    autorizacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255,blank=True, null=True)
    base_iva = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=2)
    base_ice = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    descuento = models.DecimalField(max_digits=18, decimal_places=2)
    total = models.DecimalField(max_digits=18, decimal_places=2)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
    retenido = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente)
    proforma = models.ForeignKey(Proforma,blank=True, null=True)
    total_en_letras = models.CharField(max_length=255,blank=True, null=True)
    razon_social = models.ForeignKey(RazonSocial,blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor)
    ruc = models.CharField(max_length=25,blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    punto_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    activo = models.BooleanField(default=True)
    nota_credito = models.BooleanField(default=False)
    guia_remision=models.ForeignKey(GuiaRemision,blank=True, null=True)
    tipo_comprobante_ventas=models.ForeignKey(TipoComprobanteVentas,blank=True, null=True)
    facturacion_eletronica = models.BooleanField(default=False)
    id_facturacion_eletronica= models.IntegerField(blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'documento_venta'




class FormaPagoVentas(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'forma_pago_ventas'

class DocumentoVentaFormaPago(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    documento_venta = models.ForeignKey(DocumentoVenta)
    forma_pago_ventas = models.ForeignKey(FormaPagoVentas)

    class Meta:
        managed = False
        db_table = 'documento_venta_forma_pago'

class DocumentosVentaDetalle(models.Model):
    documento_venta = models.ForeignKey(DocumentoVenta)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    descripcion = models.CharField(max_length=255)
    base_iva = models.DecimalField(max_digits=18, decimal_places=2)
    valor_iva = models.DecimalField(max_digits=18, decimal_places=2)
    porcentaje_iva = models.DecimalField(max_digits=18, decimal_places=2)
    base_ice = models.DecimalField(max_digits=18, decimal_places=2)
    valor_ice = models.DecimalField(max_digits=18, decimal_places=2)
    porcentaje_ice = models.DecimalField(max_digits=18, decimal_places=2)
    base_iva_0 = models.DecimalField(max_digits=18, decimal_places=2)
    valor_iva_0 = models.DecimalField(max_digits=18, decimal_places=2)
    subtotal = models.DecimalField(max_digits=18, decimal_places=2)
    cantidad = models.DecimalField(max_digits=18, decimal_places=2)
    descuento = models.DecimalField(max_digits=18, decimal_places=2)

    class Meta:
        db_table = 'documento_venta_detalle'

class DocumentoRetencionVenta(models.Model):
    documento_venta = models.ForeignKey(DocumentoVenta)
    fecha_emision = models.DateField()
    establecimiento = models.CharField(max_length=3)
    punto_emision = models.CharField(max_length=3)
    secuencial = models.CharField(max_length=255)
    autorizacion = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    anulado = models.BooleanField(default=False)
    retencion_con_tarjeta_de_credito = models.BooleanField(default=False)
    ruc_compania_tcredito = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'documento_retencion_venta'

class DocumentoRetencionDetalleVenta(models.Model):
    documento_retencion_venta = models.ForeignKey(DocumentoRetencionVenta)
    retencion_detalle = models.ForeignKey(RetencionDetalle)
    base_imponible = models.DecimalField(max_digits=18, decimal_places=4,default=Decimal('0'))
    porcentaje_retencion = models.DecimalField(max_digits=18, decimal_places=4,default=Decimal('0'))
    valor_retenido = models.DecimalField(max_digits=18, decimal_places=4,default=Decimal('0'))

    class Meta:
        db_table = 'documento_retencion_detalle_venta'

class DocumentoAbono(models.Model):
    documento_compra = models.ForeignKey(DocumentoCompra, blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    abono = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cantidad_anterior_abonada = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    diferencia = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    anulado = models.BooleanField(default=False)
    observacion= models.TextField(blank=True)
    saldo_inicial = models.BooleanField(default=False)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'documento_abono'

class DocumentoAbonoVenta(models.Model):
    documento_venta= models.ForeignKey(DocumentoVenta, blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    abono = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    cantidad_anterior_abonada = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    diferencia = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    anulado = models.BooleanField(default=False)
    abono_inicial = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    ajuste_factura_abono_proforma = models.ForeignKey(AjusteFacturaAbonoProforma, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documento_abono_venta'

class MovimientoNotaCredito(models.Model):
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    documento_compra= models.ForeignKey(DocumentoCompra, blank=True, null=True)
    documento_venta= models.ForeignKey(DocumentoVenta, blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    iva = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    proveedor = models.BooleanField(default=True)
    fecha = models.DateTimeField(blank=True, null=True)
    anulado = models.BooleanField(default=False)
    proforma= models.ForeignKey(Proforma, blank=True, null=True)
    es_proforma = models.BooleanField(default=False)
    lleva_iva = models.BooleanField(default=True)
    class Meta:
        managed = False
        db_table = 'movimiento_nota_credito'
        
        
class CosteoFabricacionFacturas(models.Model):
    documento_compra = models.ForeignKey(DocumentoCompra, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    porcentaje= models.FloatField(blank=True,default=0)
    total = models.FloatField(blank=True,default=0)
    anulado = models.BooleanField(default=False)
    comentario = models.CharField(max_length=250, blank=True, null=True)
    tipo = models.CharField(max_length=250, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    rubro = models.CharField(max_length=250, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'costeo_fabricacion_facturas'

class Cruces(models.Model):
    fecha = models.DateField(blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    documento_venta = models.ForeignKey(DocumentoVenta, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    factura = models.CharField(max_length=255, blank=True, null=True)
    valor_factura = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
        #models.DecimalField(max_digits=18, decimal_places=2, null=True)
    saldo_factura = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
        #models.DecimalField(max_digits=18, decimal_places=2, null=True)
    valor_cruce = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
        #models.DecimalField(max_digits=18, decimal_places=2, null=True)
    comprobante = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(default=False)
    anulado = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'cruces'

class CrucesDetalle(models.Model):
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    documento_venta = models.ForeignKey(DocumentoVenta, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    valor_cruce = models.DecimalField(max_digits=18, decimal_places=2,blank=True, null=True)
    comprobante = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'cruces_detalle'
