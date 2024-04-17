from django.db import models
from django.db import models
from config.models import *
from vendedor.models import *
from decimal import Decimal
from retenciones.models import TipoRetencion
from contabilidad.models import *

#from bancos.models import ContabilidadPlandecuentas
# Create your models here.
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
    
class CategoriasClte(models.Model):
    categoria_clte_id = models.AutoField(primary_key=True)
    descripcion_categ = models.CharField(max_length=35)
    predeterminado = models.IntegerField()

    class Meta:
        db_table = 'Categorias_clte'

    def __unicode__(self):
        return "%s" % (self.descripcion_categ)

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    codigo_cliente = models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255, blank=True)
    razon_social = models.CharField(max_length=255, blank=True)
    fecha_emision = models.CharField(max_length=255, blank=True)
    cuenta_contable_venta = models.ForeignKey(PlanDeCuentas, related_name="cuenta_contable_venta",null=True, blank=True)
    tipo_persona = models.CharField(max_length=255, blank=True)
    ruc = models.CharField(max_length=13, null=True)
    cedula = models.CharField(max_length=10, null=True, blank=True)
    telefono1 = models.CharField(max_length=255, null=True)
    cuenta_cobrar = models.ForeignKey(PlanDeCuentas,related_name="cuenta_cobrar",null=True, blank=True)
    direccion1 = models.CharField(max_length=255,null=True)
    direccion2 = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255,blank=True)
    email1 = models.CharField(max_length=255, null=True)
    vendedor = models.ForeignKey(Vendedor, null=True, blank=True)
    comentario = models.CharField(max_length=255,blank=True)
    pais = models.ForeignKey(Pais, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)
    dias_credito = models.IntegerField(blank=True, null=True)
    tipo_cliente = models.ForeignKey(TipoCliente, null=True, blank=True)
    serie = models.CharField(max_length=255,blank=True)
    retencion_iva = models.ForeignKey(RetencionDetalle, related_name="retencion_iva",null=True, blank=True)
    retencion_fuente = models.ForeignKey(RetencionDetalle, related_name="retencion_fuente",null=True, blank=True)
    activo = models.BooleanField(default=True)
    saldo_factura = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    saldo_proforma = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0'))
    zona = models.ForeignKey(Zona, null=True, blank=True)
    cupo_credito = models.FloatField(blank=True, null=True)
    banco = models.ForeignKey(Banco, null=True, blank=True)
    categoria_cliente = models.ForeignKey(CategoriaCliente, null=True, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    descuento = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'cliente'
    def __unicode__(self):
        return "%s" % (self.nombre_cliente)

class TerminosPago(models.Model):
    termino_id = models.AutoField(primary_key=True)
    codigo_termino = models.CharField(max_length=4)
    descripcion_termino = models.CharField(db_column='Descripcion_termino', max_length=40)  # Field name made lowercase.
    tipo_pago = models.CharField(max_length=2)
    monto = models.DecimalField(max_digits=18, decimal_places=2)
    dias = models.IntegerField()
    inicial = models.DecimalField(max_digits=18, decimal_places=2)
    cuotas = models.IntegerField()
    dscto_pronto_pago = models.DecimalField(max_digits=18, decimal_places=2)
    cuenta_contable = models.CharField(max_length=20)
    predeterminado = models.IntegerField()
    cuenta_corriente = models.CharField(max_length=40)
    cliente_paga_en = models.CharField(max_length=2)

    class Meta:
        db_table = 'terminos_pago'
    def __unicode__(self):
        return "%s %s" % (self.codigo_termino, self.descripcion_termino)

class FormaPagoClie(models.Model):
    forma_pago_id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=4)
    descripcion = models.CharField(max_length=50)
    tipo_cuenta = models.IntegerField()
    predeterminado = models.IntegerField()
    cta_contable = models.CharField(max_length=20)
    enlaza_id = models.IntegerField()

    class Meta:
        db_table = 'forma_pago_clie'
    def __unicode__(self):
        return "%s %s" % (self.codigo, self.descripcion)


class RazonSocial(models.Model):
    codigo_razon_social = models.CharField(max_length=20, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    telefono2 = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    contacto = models.CharField(max_length=255, blank=True)
    email1 = models.CharField(max_length=255, blank=True)
    email2 = models.CharField(max_length=255, blank=True)
    categoria_cliente = models.ForeignKey(CategoriaCliente, null=True, blank=True)
    vendedor =models.ForeignKey(Vendedor, null=True, blank=True)
    balance = models.FloatField(blank=True, null=True)
    cliente_activo = models.NullBooleanField()
    registro_empresarial = models.CharField(max_length=255, blank=True)
    registro_tributario = models.CharField(max_length=255, blank=True)
    cuenta_cont_ventas = models.CharField(max_length=255, blank=True)
    giro_id = models.IntegerField(blank=True, null=True)
    creado = models.CharField(max_length=255, blank=True)
    maximo_credito = models.FloatField(blank=True, null=True)
    descuento = models.FloatField(blank=True, null=True)
    interes_anual = models.FloatField(blank=True, null=True)
    termino_id = models.IntegerField(blank=True, null=True)
    comentario = models.CharField(max_length=255, blank=True)
    facturar_con = models.CharField(max_length=255, blank=True)
    campo1 = models.CharField(max_length=255, blank=True)
    campo2 = models.CharField(max_length=255, blank=True)
    campo3 = models.CharField(max_length=255, blank=True)
    imagen = models.CharField(max_length=255, blank=True)
    aplica_reten_impto = models.NullBooleanField()
    reten_impto = models.FloatField(blank=True, null=True)
    aplica_reten_ica = models.NullBooleanField()
    reten_ica = models.FloatField(blank=True, null=True)
    aplica_reten_fuente = models.NullBooleanField()
    reten_fuente = models.FloatField(blank=True, null=True)
    aplica_2do_impto = models.NullBooleanField()
    segundo_impto = models.FloatField(blank=True, null=True)
    aplica_impto = models.NullBooleanField()
    impto = models.FloatField(blank=True, null=True)
    primer_apellido = models.CharField(max_length=255, blank=True)
    segundo_apellido = models.CharField(max_length=255, blank=True)
    primer_nombre = models.CharField(max_length=255, blank=True)
    segundo_nombre = models.CharField(max_length=255, blank=True)
    tipo_empresa = models.CharField(max_length=255, blank=True)
    impto_incluido = models.CharField(max_length=255, blank=True)
    monto_ult_transac = models.FloatField(blank=True, null=True)
    fecha_ult_transac = models.DateTimeField(blank=True, null=True)
    descri_ult_transac = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    ruc = models.CharField(max_length=13, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=10, blank=True)
    clase_id = models.IntegerField(blank=True, null=True)
    validez = models.DateTimeField(blank=True, null=True)
    incluye_ice = models.NullBooleanField()
    convenio_hasta = models.DateTimeField(blank=True, null=True)
    consignacion = models.NullBooleanField()
    cuenta_anticipo = models.CharField(max_length=10, blank=True)
    pasaporte = models.NullBooleanField()
    tipo_precio_id = models.IntegerField(blank=True, null=True)
    zona = models.ForeignKey(Zona, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, null=True, blank=True)
    plan_de_cuentas = models.ForeignKey(PlanDeCuentas, null=True, blank=True)
    cupo_credito = models.FloatField(blank=True, null=True)
    dias_credito = models.IntegerField(blank=True, null=True)
    tipo_cliente = models.ForeignKey(TipoCliente, null=True, blank=True)
    banco = models.ForeignKey(Banco, null=True, blank=True)
    class Meta:
        managed = False
        db_table = 'razon_social'
    def __unicode__(self):
        return "%s" % (self.nombre)

class RazonSocialClientes(models.Model):
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    razon_social = models.ForeignKey(RazonSocial, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'razon_social_clientes'

