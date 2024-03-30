from django.db import models
from vendedor.models import *
from clientes.models import Cliente,RazonSocial
from proveedores.models import Proveedor
from contabilidad.models import *
from config.models import *
from proforma.models import Proforma

class TarjetaCredito(models.Model):
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjeta_credito'

    def __unicode__(self):
        return "%s" % self.nombre
class Ciudad(models.Model):
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

class TipoCuentaBanco(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_cuenta'

    def __unicode__(self):
        return "%s" % self.nombre


class FormatoCheque(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'formato_cheque'

    def __unicode__(self):
        return "%s" % self.descripcion


class Banco(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True, null=True)
    nombre = models.CharField(max_length=250)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    numero_cuenta = models.CharField(max_length=250)
    ciudad = models.ForeignKey(Ciudad)
    cuenta_contable = models.ForeignKey(PlanDeCuentas)
    tipo_cuenta = models.ForeignKey(TipoCuentaBanco)
    estado = models.BooleanField(default=True)
    saldo_inicial = models.DecimalField(decimal_places=2, max_digits=20)
    fecha_corte = models.DateField()
    formato_cheque = models.ForeignKey(FormatoCheque)
    macro_rrhh = models.CharField(max_length=50, blank=True)
    secuencia = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'banco'
    def __unicode__(self):
        return "%s" % self.nombre



class TipoAnticipo(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_anticipo'
    def __unicode__(self):
        return "%s" % self.descripcion


class TipoMovimiento(models.Model):
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_movimiento'


class TipoDocumento(models.Model):
    descripcion = models.CharField(max_length=250)
    cliente = models.BooleanField(default=False, blank=True)
    proveedor= models.BooleanField(default=False, blank=True)

    class Meta:
        managed = False
        db_table = 'tipo_documento'
    def __unicode__(self):
        return "%s" % self.descripcion




class SecuenciaCheque(models.Model):
    id = models.AutoField(primary_key=True)
    secuencia = models.CharField(max_length=250)
    secuencia_inicio = models.CharField(max_length=250)
    secuencia_fin = models.CharField(max_length=250)
    estado = models.BooleanField()
    banco = models.ForeignKey(Banco)

    class Meta:
        managed = False
        db_table = 'secuencia_cheque'



class TipoNotaCredito(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_nota_credito'
    def __unicode__(self):
       return self.descripcion
    
class Conciliacion(models.Model):
    fecha_corte = models.DateField()
    cuenta_banco = models.ForeignKey(Banco)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    saldo_estado_cuenta = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    estado = models.BooleanField()
    descripcion_estado = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conciliacion'

    
class Movimiento(models.Model):
    tipo_anticipo = models.ForeignKey(TipoAnticipo)
    tipo_documento = models.ForeignKey(TipoDocumento, blank=True, null=True)
    fecha_emision = models.DateField()
    banco = models.ForeignKey(Banco, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    paguese_a = models.CharField(max_length=250, blank=True, null=True)
    numero_cheque = models.IntegerField(blank=True, null=True)
    fecha_cheque = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True)
    numero_comprobante = models.CharField(max_length=250, blank=True, null=True)
    tipo_movimiento = models.ForeignKey(TipoMovimiento, blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, blank=True, null=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    activo = models.BooleanField(default=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    proforma =  models.BooleanField(default=False, blank=True)
    tarjeta_credito = models.ForeignKey(TarjetaCredito, blank=True, null=True)
    numero_lote = models.CharField(max_length=255, blank=True, null=True)
    retencion_iva= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    impuesto_renta= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    numero_ingreso = models.CharField(max_length=250, blank=True, null=True)
    puntos_venta = models.ForeignKey(PuntosVenta, blank=True, null=True)
    ruc = models.CharField(max_length=20, blank=True)    
    razon_social = models.ForeignKey(RazonSocial, blank=True, null=True)
    nro_nota_credito = models.CharField(max_length=10, blank=True)
    subtotal = models.FloatField(blank=True, null=True)
    iva = models.FloatField(blank=True, null=True)
    dscto_pciento = models.FloatField(blank=True, null=True)
    dscto_monto = models.FloatField(blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    telefono = models.CharField(max_length=250, blank=True, null=True)
    tipo_nota_credito = models.ForeignKey(TipoNotaCredito, blank=True, null=True)
    nc_establecimiento = models.CharField(max_length=3, blank=True, null=True)
    nc_punto_emision = models.CharField(max_length=3, blank=True, null=True)
    nc_secuencial = models.CharField(max_length=255, blank=True, null=True)
    nc_autorizacion = models.CharField(max_length=255, blank=True, null=True)
    porcentaje_iva= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    subtotal_0= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    rise= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    conciliacion = models.ForeignKey(Conciliacion, blank=True, null=True)
    monto_cheque= models.DecimalField(decimal_places=2, max_digits=20, blank=True, default=Decimal('0'))
    abono_saldo_inicial = models.BooleanField(default=False)
    nc_sin_persona = models.BooleanField(default=False)
    asociado_cheques_protestados = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    facturacion_eletronica = models.BooleanField(default=False)
    id_facturacion_eletronica= models.IntegerField(blank=True, null=True)
    ats = models.BooleanField(default=True)
    cruce = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'movimiento'


class ChequesProtestados(models.Model):
    fecha_emision = models.DateField()
    cliente = models.ForeignKey(Cliente)
    banco = models.ForeignKey(Banco)
    numero_cheque = models.CharField(max_length=250)
    fecha_cheque = models.DateField()
    valor_cheque = models.DecimalField(decimal_places=2, max_digits=20)
    valor_multa = models.DecimalField(decimal_places=2, max_digits=20)
    comprobante_debito = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    anulado = models.BooleanField(default=False)
    conciliacion = models.ForeignKey(Conciliacion, blank=True, null=True)
    movimiento_multa = models.ForeignKey(Movimiento, blank=True, null=True,related_name='movimiento_multa')
    movimiento_valor_cheque = models.ForeignKey(Movimiento, blank=True, null=True,related_name='movimiento_valor_cheque')
    class Meta:
        managed = False
        db_table = 'cheques_protestados'




class ChequesNoCobrados(models.Model):
    fecha_emision = models.DateField()
    nombre_proveedor = models.CharField(max_length=255,blank=True, null=True)
    banco = models.ForeignKey(Banco,blank=True, null=True)
    numero_cheque = models.CharField(max_length=250,blank=True, null=True)
    valor_cheque = models.DecimalField(decimal_places=2, max_digits=20,blank=True, null=True)
    descripcion = models.CharField(max_length=250,blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'cheques_no_cobrados'
    
    
class DocumentoAbonoCheque(models.Model):
    cheques_protestados= models.ForeignKey(ChequesProtestados, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    abono = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    anulado = models.BooleanField(default=False)
    activo = models.BooleanField(default=False)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'documento_abono_cheque'
        


class AjusteFacturaAbonoProforma(models.Model):
    proforma = models.ForeignKey(Proforma, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    movimiento = models.ForeignKey(Movimiento, blank=True, null=True)
    asiento = models.ForeignKey(Asiento, blank=True, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'ajuste_factura_abono_proforma'