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
from os.path import basename
from django.db import models
from django.contrib.auth.models import User,Group,Permission
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Mensajes(models.Model):
    codigo = models.CharField(max_length=255, blank=True)
    mensaje = models.CharField(max_length=255, blank=True) 
    activo = models.BooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mensajes'

    def __unicode__(self):
       return self.codigo

class Areas(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo= models.BooleanField()
    costo_hora = models.FloatField(blank=True, null=True)
    costo_hora_extraordinaria = models.FloatField(blank=True, null=True)
    costo_hora_suplementaria = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'areas'
    def __unicode__(self):
       return self.descripcion


class EstadosPro(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'estados_pro'
class TipoMueb(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_mueb'
        
    def __unicode__(self):
       return self.descripcion


class Vehiculo(models.Model):
    numero_serie = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    placa = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.CharField(max_length=100, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'vehiculo'
    def __unicode__(self):
        return "%s %s" % (self.descripcion, self.placa)

class Menu(models.Model):
    cod_parent = models.ForeignKey('self', db_column='cod_parent', blank=True, null=True)
    nom_option = models.CharField(max_length=40)
    num_order = models.IntegerField(blank=True, null=True)
    txt_url = models.TextField(blank=True)
    txt_description = models.TextField(blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'menu'
    def __unicode__(self):
       return self.nom_option


class MenuGroup(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    menu = models.ForeignKey(Menu, blank=True, null=True)
    sts_show = models.BooleanField(default=False)
    sts_modify = models.BooleanField(default=False)
    sts_delete = models.BooleanField(default=False)
    sts_new = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'menu_group'

class Secuenciales(models.Model):
    modulo = models.CharField(max_length=255, blank=True)
    secuencial = models.IntegerField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'secuenciales'

class Ambiente(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.BooleanField()
    class Meta:
        db_table = 'ambiente'
    def __unicode__(self):
       return self.descripcion 

class FormaPago(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        db_table = 'forma_pago'
        
    def __unicode__(self):
       return self.descripcion 

class TipoLugar(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_lugar'
    def __unicode__(self):
       return self.descripcion 

class PuntosVenta(models.Model):
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=255, blank=True)
    nro_productos = models.IntegerField(blank=True, null=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo_proforma = models.CharField(max_length=10, blank=True)
    secuencial = models.IntegerField(blank=True, null=True)
    establecimiento = models.CharField(max_length=3, blank=True)
    punto_emision = models.CharField(max_length=3, blank=True)
    autorizacion = models.CharField(max_length=500, blank=True)
    secuencial_factura_electronica = models.IntegerField(blank=True, null=True)
    secuencial_retencion_electronica = models.IntegerField(blank=True, null=True)
    secuencial_nota_credito_electronica = models.IntegerField(blank=True, null=True)
    secuencial_guia_electronica = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puntos_venta'
    def __unicode__(self):
       return self.nombre 

class Parametros(models.Model):
    clave = models.CharField(max_length=50, blank=True)
    valor = models.CharField(max_length=150, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'parametros'

class TipoCliente(models.Model):
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_cliente'
    def __unicode__(self):
       return self.nombre 

class Provincia(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'provincia'
    def __unicode__(self):
       return self.nombre 

class Zona(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    fecha_ini = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'zona'
    def __unicode__(self):
       return self.nombre 
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
       return self.nombre 

class CategoriaCliente(models.Model):
    codigo = models.CharField(max_length=26, blank=True)
    nombre = models.CharField(max_length=255, blank=True)
    activo = models.NullBooleanField()
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'categoria_cliente'
    def __unicode__(self):
       return self.nombre 

class EstadoCivil(models.Model):
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'estado_civil'
    def __unicode__(self):
       return self.nombre 

class RelacionLaboral(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'relacion_laboral'
    def __unicode__(self):
       return self.nombre
class TipoRemuneracion(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'tipo_remuneracion'
    def __unicode__(self):
       return self.nombre
class Pais(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'pais'
    def __unicode__(self):
       return self.nombre

class FormaPagoEmpleado(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'forma_pago_empleado'
    def __unicode__(self):
       return self.nombre

class TipoCuenta(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'tipo_cuenta'
    def __unicode__(self):
       return self.nombre

class TipoPago(models.Model):
    nombre = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tipo_pago'


class Notificaciones(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    mensaje = models.TextField(blank=True, null=True)
    visto = models.NullBooleanField()
    url = models.CharField(max_length=255, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    titulo = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'notificaciones'


class Anio(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'anio'
    def __unicode__(self):
       return self.nombre
    
    
class Mes(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mes'
    def __unicode__(self):
       return self.descripcion
    
class BloqueoPeriodo(models.Model):

    fecha = models.DateTimeField(blank=True, null=True)
    anio =  models.ForeignKey(Anio, blank=True, null=True)
    mes =  models.ForeignKey(Mes, blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'bloqueo_periodo'
   
