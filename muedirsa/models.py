# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

from django.db import models
from inventario.models import *


class Conexion(models.Model):
    id_conexion = models.AutoField(primary_key=True)
    string_de_conexion = models.CharField(max_length=250, blank=True)
    ruta_para_data = models.CharField(max_length=250, blank=True)
    computador_base = models.CharField(max_length=250, blank=True)
    servidor_de_datos = models.CharField(max_length=250, blank=True)
    ultima_actual_sp = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'conexion'

class Empresa(models.Model):
    empresa_id = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=250, blank=True)
    base_de_datos = models.CharField(max_length=250, blank=True)
    condicion = models.CharField(max_length=255, blank=True)
    icono_asociado = models.CharField(max_length=255, blank=True)
    folder_empresa = models.CharField(max_length=255, blank=True)
    registro_tributario_empresa = models.CharField(max_length=255, blank=True)
    direccion1 = models.CharField(max_length=255, blank=True)
    direccion2 = models.CharField(max_length=255, blank=True)
    direccion3 = models.CharField(max_length=255, blank=True)
    telefono1 = models.CharField(max_length=255, blank=True)
    celular = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    correo_electronico = models.CharField(max_length=255, blank=True)
    sitio_web = models.CharField(max_length=255, blank=True)
    registro_empresarial = models.CharField(max_length=255, blank=True)
    barrio_distrito = models.CharField(max_length=255, blank=True)
    ciudad = models.CharField(max_length=255, blank=True)
    codigo_postal = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    logo = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'empresa'

class Producto(models.Model):
    producto_id = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=26)
    descripcion_producto = models.CharField(max_length=255)
    precio1 = models.FloatField()
    precio2 = models.FloatField()
    precio3 = models.FloatField()
    precio4 = models.FloatField()
    costo = models.FloatField()
    unidad_en_compra = models.IntegerField()
    equivalencia_en_compra = models.FloatField()
    cant_total = models.FloatField()
    cant_minimia = models.FloatField()
    categoria = models.ForeignKey(CategoriaProducto)
    sub_categoria = models.ForeignKey(SubCategoriaProducto)
    acepta_lote = models.NullBooleanField()
    valor_inventario = models.FloatField()
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/producto/")
    incremento1 = models.FloatField()
    incremento2 = models.FloatField()
    incremento3 = models.FloatField()
    incremento4 = models.FloatField()
    codigo_fabricante = models.CharField(max_length=20)
    producto_fisico = models.IntegerField()
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
    class Meta:
        db_table = 'producto'
        ordering = ['codigo_producto']

    def __unicode__(self):
        return "%s %s" % (self.codigo_producto, self.descripcion_producto)
