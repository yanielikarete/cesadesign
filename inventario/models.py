from django.db import models
from proveedores.models import Proveedor
from clientes.models import Cliente
from config.models import *
from contabilidad.models import PlanDeCuentas
from os.path import basename
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class CategoriaProducto(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    codigo_categoria = models.CharField(max_length=10)
    descripcion_categoria = models.CharField( max_length=255)
    predeterminado = models.IntegerField()
    nro_productos = models.IntegerField()
    imagen_categoria = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'categoria_producto'
        verbose_name = _(u'CategoriaProducto')

    def __unicode__(self):
        return '%s' % (self.descripcion_categoria)

    def __str__(self):
        return '%s' % (self.descripcion_categoria)

class SubCategoriaProducto(models.Model):
    sub_categoria_producto_id = models.AutoField(primary_key=True)
    codigo_sub_categ = models.CharField(max_length=10)
    categoria = models.ForeignKey(CategoriaProducto)
    descripcion_sub_categ = models.CharField(max_length=255)
    predeterminado = models.IntegerField()
    nro_productos = models.IntegerField()
    imagen_subcateg = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'sub_categoria_producto'
        verbose_name = _(u'SubCategoriaProducto')

    def __unicode__(self):
       return '%s' % (self.descripcion_sub_categ)
    def __str__(self):
       return '%s' % (self.descripcion_sub_categ)


class Bodega(models.Model):
    codigo_bodega = models.CharField(max_length=26)
    nombre = models.CharField(max_length=255)
    direccion1 = models.CharField(max_length=255)
    direccion2 = models.CharField(max_length=255,blank=True)
    direccion3 = models.CharField(max_length=255,blank=True, null=True)
    telefono = models.CharField(max_length=255,blank=True, null=True)
    predeterminado = models.CharField(max_length=255,blank=True, null=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    activo = models.NullBooleanField()
    activo_bodega = models.NullBooleanField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
    	db_table = 'bodega'
    def __unicode__(self):
        return "%s %s" % (self.codigo_bodega, self.nombre)
class Linea(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'linea'
    def __unicode__(self):
       return "%s" % (self.descripcion)

class TipoProducto(models.Model):
    codigo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    activo= models.BooleanField()
    cuenta_contable = models.ForeignKey(PlanDeCuentas, related_name="cuenta_contable", null=True,
                                               blank=True)
    cuenta_inventario_productos_proceso = models.ForeignKey(PlanDeCuentas, related_name="cuenta_inventario_productos_proceso", null=True,
                                        blank=True)
    class Meta:
        db_table = 'tipo_producto'
        ordering = ['codigo']
    def __unicode__(self):
       return "%s" % (self.descripcion)

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=26)
    descripcion_producto = models.CharField(max_length=255)
    descripcion_interna = models.CharField(max_length=500,null=True,blank=True)
    precio1 = models.FloatField(blank=True)
    precio2 = models.FloatField(blank=True)
    precio3 = models.FloatField(blank=True)
    precio4 = models.FloatField(blank=True,)
    costo = models.FloatField(blank=True)
    unidad_en_compra = models.IntegerField(blank=True)
    equivalencia_en_compra = models.FloatField()
    cant_total = models.FloatField(blank=True)
    cant_minimia = models.FloatField(blank=True)
    categoria = models.ForeignKey(CategoriaProducto)
    sub_categoria = models.ForeignKey(SubCategoriaProducto)
    acepta_lote = models.NullBooleanField()
    valor_inventario = models.FloatField()
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/producto/")
    situacion_producto = models.IntegerField()
    tipo_producto = models.ForeignKey(TipoProducto, db_column='tipo_producto')
    bodega_id = models.IntegerField()
    mostrar_componente = models.NullBooleanField()
    factura_sin_stock = models.NullBooleanField()
    avisa_expiracion = models.NullBooleanField()
    factura_con_precio = models.IntegerField()
    producto_equivalente = models.CharField(max_length=255)
    cuenta_compra = models.CharField(max_length=255)
    cuenta_venta = models.CharField(max_length=20)
    suplidor1_id = models.IntegerField()
    impuesto1_id = models.IntegerField()
    impto1_en_vtas = models.CharField(max_length=255)
    impto1_en_compras = models.CharField(max_length=255)
    ultima_venta = models.DateTimeField()
    otro_impto_id = models.IntegerField()
    otro_impto_id_vtas = models.CharField(max_length=20)
    otro_impto_id_compras = models.CharField(max_length=20)
    precio_de_compra_0 = models.DecimalField(max_digits=8, decimal_places=2)
    precio_actualizado = models.DateTimeField()
    requiere_nro_serie = models.NullBooleanField()
    costo_dolar = models.DecimalField(max_digits=8, decimal_places=2)
    comentario = models.CharField(max_length=255)
    comenta_factura = models.CharField(max_length=255)
    retencion_id = models.IntegerField()
    rete_vtas = models.CharField(max_length=255)
    rete_compras = models.CharField(max_length=255)
    notas = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(blank=True)
    linea = models.ForeignKey(Linea)
    activo = models.BooleanField()
    unidad = models.CharField(max_length=255, blank=True)
    medida_peso = models.CharField(max_length=255, blank=True)
    costo_promedio = models.FloatField(blank=True)
    acepta_iva = models.BooleanField()
    peso = models.CharField(max_length=255, blank=True)
    precio_de_compra_max = models.FloatField(blank=True)
    uat = models.FloatField(blank=True)
    codigo_produccion = models.CharField(max_length=255,blank=True)
    horas = models.FloatField(blank=True, null=True)
    costo_horas = models.FloatField(blank=True, null=True)
    costo_produccion = models.FloatField(blank=True, null=True)
    costo_material = models.FloatField(blank=True, null=True)
    costo_fijo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    servicio = models.NullBooleanField()
    precio5 = models.FloatField(blank=True, null=True)
    fecha_ult_vta = models.DateField(blank=True, null=True)
    fecha_ult_com = models.DateField(blank=True, null=True)
    descrip_tipo_producto = models.CharField(max_length=255, blank=True)
    ice = models.NullBooleanField()
    val_uat1 = models.FloatField(blank=True, null=True)
    val_uat2 = models.FloatField(blank=True, null=True)
    bloquea = models.BooleanField()
    ultimo_costo = models.FloatField(blank=True, null=True)
    cant_media = models.FloatField(blank=True, null=True)
    cant_maxima = models.FloatField(blank=True, null=True)
    cant_venta = models.FloatField(blank=True, null=True)
    cant_compra = models.FloatField(blank=True, null=True)
    irbp = models.FloatField(blank=True, null=True)
    val_uat3 = models.FloatField(blank=True, null=True,default=0)
    val_uat4 = models.FloatField(blank=True, null=True,default=0)
    val_uat5 = models.FloatField(blank=True, null=True,default=0)
    val_uat6 = models.FloatField(blank=True, null=True,default=0)
    porcentaje_precio1 = models.FloatField(blank=True,default=0)
    porcentaje_precio2 = models.FloatField(blank=True,default=0)
    porcentaje_precio3 = models.FloatField(blank=True,default=0)
    base=models.BooleanField(blank=True)
    class Meta:
        db_table = 'producto'
        ordering = ['codigo_producto']

    def __unicode__(self):
	 	return "%s %s" % (self.codigo_producto, self.descripcion_producto)

class ProductoEquivalente(models.Model):
    producto_equivalente_id = models.IntegerField(primary_key=True)
    producto_id_principal = models.ForeignKey(Producto, related_name='principal')
    comentario = models.CharField(max_length=500)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    producto_id_equivalente = models.ForeignKey(Producto, related_name='equivalente')
    class Meta:
        db_table = 'producto_equivalente'


class Impuesto(models.Model):
    impuesto_id = models.IntegerField(primary_key=True)
    abreviatura = models.CharField(max_length=255)
    descripcion_impto = models.CharField(max_length=255)
    valor_impto = models.FloatField()
    cta_cont_ventas = models.CharField(max_length=255)
    cta_cont_compras = models.CharField(max_length=255)
    predeterminado = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'impuesto'
    def __unicode__(self):
        return "%s %s" % (self.abreviatura, self.descripcion_impto)

class Lote(models.Model):
    lote_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto)
    nro_lote = models.CharField(max_length=250)
    descripcion_lote = models.CharField(max_length=250)
    bodega = models.ForeignKey(Bodega)
    fecha_ingreso = models.DateTimeField()
    fecha_expiracion = models.DateTimeField()
    ubicacion = models.CharField(max_length=250)
    cantidad = models.FloatField()
    comentario_lote = models.CharField(max_length=250)
    nro_documento = models.IntegerField()
    disponible = models.FloatField()
    agotado_en = models.DateTimeField()
    nro_item = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'lote'
    def __unicode__(self):
        return "%s %s %s" % (self.producto, self.nro_lote, self.descripcion_lote)


class ProductoEnBodega(models.Model):
    producto_bodega_id = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    cantidad = models.FloatField(blank=True, null=True)
    ubicacion = models.CharField(max_length=255,blank=True, null=True)
    created_by = models.CharField(max_length=255,blank=True, null=True)
    updated_by = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    cantidad_migrada = models.FloatField(blank=True, null=True)
    cantidad_inicial = models.FloatField(blank=True, null=True)
    ingresos = models.FloatField(blank=True, null=True)
    egresos = models.FloatField(blank=True, null=True)
    class Meta:
        db_table = 'producto_en_bodega'

class OtroSuplidor(models.Model):
    otro_suplidor_id = models.AutoField(primary_key=True)
    producto_id_principal = models.ForeignKey(Producto, db_column='producto_id_principal')
    proveedor_id_principal = models.ForeignKey(Proveedor, db_column='proveedor_id_principal')
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'otro_suplidor'

class ListaCliente(models.Model):
    lista_cliente_id = models.IntegerField(primary_key=True)
    cliente = models.ForeignKey(Cliente)
    producto = models.ForeignKey(Producto)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'lista_cliente'

class ListaPrecio(models.Model):
    lista_suplidor_id = models.IntegerField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor)
    producto = models.ForeignKey(Producto)
    precio_de_compra_1 = models.DecimalField(max_digits=8, decimal_places=2)
    precio_en_dolar_1 = models.DecimalField(max_digits=8, decimal_places=2)
    rango_inicial_1 = models.DecimalField(max_digits=8, decimal_places=2)
    rango_final_1 = models.DecimalField(max_digits=8, decimal_places=2)
    precio_de_compra_2 = models.DecimalField(max_digits=8, decimal_places=2)
    precio_en_dolar_2 = models.DecimalField(max_digits=8, decimal_places=2)
    rango_inicial_2 = models.DecimalField(max_digits=8, decimal_places=2)
    rango_final_2 = models.DecimalField(max_digits=8, decimal_places=2)
    actualizado = models.NullBooleanField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'lista_precio'

class Unidades(models.Model):
    unidad_id = models.AutoField(primary_key=True)
    abreviatura = models.CharField(max_length=255)
    descripcion_unidad = models.CharField(max_length=255)
    predeterminado_vta = models.CharField(max_length=255)
    predeterminado_com = models.CharField(max_length=255)
    nro_productos = models.FloatField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'unidades'
    def __unicode__(self):
        return "%s %s" % (self.abreviatura, self.descripcion_unidad)


class Kits(models.Model):
    padre = models.ForeignKey('Producto', related_name='padre')
    hijo = models.ForeignKey('Producto', related_name='hijo')
    cantidad = models.FloatField(blank=True)
    total = models.FloatField(blank=True)
    costo = models.FloatField(blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    areas = models.ForeignKey(Areas,blank=True)
    medida = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255 ,blank=True, null=True)
    otros_costos = models.BooleanField(default=False)

    class Meta:
        db_table = 'kits'

class Kardex(models.Model):
    kardex_id = models.AutoField(primary_key=True)
    nro_documento = models.CharField(max_length=250)
    empresa_tipo = models.CharField(max_length=250)
    empresa_id = models.IntegerField()
    producto = models.ForeignKey(Producto)
    cantidad = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=250)
    tipo = models.IntegerField()
    fecha_ingreso = models.DateTimeField()
    costo = models.FloatField(blank=True, null=True)
    cant_disponible = models.IntegerField()
    cant_dispoxbodega = models.IntegerField()
    modificable = models.NullBooleanField()
    bodega = models.ForeignKey(Bodega)
    modulo = models.CharField(max_length=250)
    documento_id = models.IntegerField()
    nro_doc_soporte = models.IntegerField()
    un_doc_soporte = models.CharField(max_length=250)
    hora = models.CharField(max_length=250)
    costo_old = models.DecimalField(max_digits=8, decimal_places=2)
    lote_id = models.IntegerField()
    ingreso = models.CharField(max_length=250)
    nro_item = models.IntegerField()
    fecha_hora = models.DateTimeField()
    cant_disponible_x = models.FloatField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    fecha_egreso = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    egreso = models.NullBooleanField()
    class Meta:
        db_table = 'kardex'


class Seriales(models.Model):
    serial_id = models.IntegerField(primary_key=True)
    producto = models.ForeignKey(Producto)
    nro_serial = models.CharField(max_length=255)
    ingresado = models.CharField(max_length=255)
    modulo_ingreso = models.CharField(max_length=255)
    nro_doc_ingreso = models.CharField(max_length=255)
    salida = models.CharField(max_length=255)
    cliente_mid = models.ForeignKey(Cliente, db_column='cliente_mid')
    modulo_salida = models.CharField(max_length=255)
    bodega = models.ForeignKey(Bodega)
    nro_item = models.IntegerField()
    nro_doc_salida = models.IntegerField()
    nro_item_s = models.IntegerField()
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    proveedor_mid = models.ForeignKey(Proveedor, db_column='proveedor_mid')
    class Meta:
        db_table = 'seriales'


class ImagenesKardex(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    nro_documento = models.CharField(max_length=10)
    imagen_dcto = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'imagenes_kardex'


class ImagenesProducto(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    producto_id = models.IntegerField()
    imagen_producto = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'imagenes_producto'


class InvFisico(models.Model):
    inv_fisico_id = models.AutoField(primary_key=True)
    fecha_inv_fisico = models.CharField(max_length=10)
    descrip_inv_fisico = models.CharField(db_column='Descrip_inv_fisico', max_length=200)  # Field name made lowercase.
    almacen_id = models.IntegerField()
    prod_cont_almacen = models.DecimalField(max_digits=18, decimal_places=4)
    total_prod_almacen = models.DecimalField(db_column='Total_prod_almacen', max_digits=18, decimal_places=4)  # Field name made lowercase.
    campo1 = models.CharField(max_length=100)
    campo2 = models.DecimalField(max_digits=18, decimal_places=4)
    campo3 = models.TextField()

    class Meta:
        db_table = 'inv_fisico'


class InvFisicoDetalle(models.Model):
    detalle_inv_fis_id = models.AutoField(primary_key=True)
    producto_id = models.CharField(max_length=30)
    bodega_id = models.IntegerField()
    unidades_contadas = models.DecimalField(max_digits=18, decimal_places=4)
    campo1 = models.CharField(max_length=100)
    campo2 = models.DecimalField(max_digits=18, decimal_places=4)
    campo3 = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'inv_fisico_detalle'

class PresupuestoProducto(models.Model):
    producto_id = models.ForeignKey(Producto, db_column='producto_id')
    enero = models.IntegerField(null=True,blank=True)
    febrero = models.IntegerField(null=True,blank=True)
    marzo = models.IntegerField(null=True,blank=True)
    abril = models.IntegerField(null=True,blank=True)
    mayo = models.IntegerField(null=True,blank=True)
    junio = models.IntegerField(null=True,blank=True)
    julio = models.IntegerField(null=True,blank=True)
    agosto = models.IntegerField(null=True,blank=True)
    septiembre = models.IntegerField(null=True,blank=True)
    octubre = models.IntegerField(null=True,blank=True)
    noviembre = models.IntegerField(null=True,blank=True)
    diciembre = models.IntegerField(null=True,blank=True)
    created_by = models.CharField(max_length=255)
    updated_by = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        db_table = 'presupuesto_producto'


class ProductoAreas(models.Model):
    producto = models.ForeignKey(Producto, blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    secuencia = models.IntegerField(blank=True, null=True)
    horas = models.FloatField(blank=True, null=True)
    costo_horas = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    costo_materiales = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo_produccion = models.FloatField(blank=True, null=True)
    costo_fijo = models.FloatField(blank=True, null=True)
    precio1 = models.FloatField(blank=True, null=True,default=0)
    precio2 = models.FloatField(blank=True, null=True,default=0)
    class Meta:
        managed = False
        db_table = 'producto_areas'

class ProductoManoObra(models.Model):
    producto_areas = models.ForeignKey(ProductoAreas, blank=True, null=True)
    operacion_unitaria = models.CharField(max_length=255, blank=True)
    empleado = models.CharField(max_length=255, blank=True)
    hora_inicio = models.CharField(max_length=255, blank=True)
    hora_fin = models.CharField(max_length=255, blank=True)
    hora_total = models.FloatField(blank=True, null=True)
    costo_hora = models.FloatField(blank=True, null=True)
    costo_total = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    tipo_hora = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'producto_mano_obra'

class AnalisisInventario(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    descripcion = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    aprobada = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'analisis_inventario'

class AnalisisInventarioDetalle(models.Model):
    analisis_inventario = models.ForeignKey(AnalisisInventario, blank=True, null=True)
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    cantidad_real = models.FloatField(blank=True, null=True)
    diferencia = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'analisis_inventario_detalle'

class ProductoGeneral(models.Model):
    codigo = models.CharField(max_length=26, blank=True)
    descripcion = models.CharField(max_length=255, blank=True)
    precio1 = models.FloatField(blank=True, null=True)
    precio2 = models.FloatField(blank=True, null=True)
    precio3 = models.FloatField(blank=True, null=True)
    precio4 = models.FloatField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    unidad_en_compra = models.IntegerField(blank=True, null=True)
    categoria = models.ForeignKey(CategoriaProducto, blank=True, null=True)
    sub_categoria = models.ForeignKey(SubCategoriaProducto, blank=True, null=True)
    tipo_producto = models.ForeignKey(TipoProducto, blank=True, null=True)
    linea = models.ForeignKey(Linea, blank=True, null=True)
    activo = models.BooleanField()
    unidad = models.CharField(max_length=255, blank=True)
    medida_peso = models.CharField(max_length=255, blank=True)
    acepta_iva = models.NullBooleanField()
    peso = models.CharField(max_length=255, blank=True)
    codigo_produccion = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'producto_general'



class Inventario(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    anio = models.IntegerField(blank=True, null=True,default=0)
    cantidad = models.FloatField(blank=True, null=True,default=0)
    created_by = models.CharField(max_length=255,blank=True, null=True)
    updated_by = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


    class Meta:
        db_table = 'inventario'