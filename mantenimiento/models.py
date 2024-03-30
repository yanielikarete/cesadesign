from django.db import models
from contabilidad.models import *

class TipoRetencion(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'tipo_retencion'

    def __unicode__(self):
        return "%s" % self.descripcion


class Retenciones(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.CharField(max_length=250)
    porcentaje = models.DecimalField(decimal_places=2, max_digits=20)
    codigo_anexo = models.CharField(max_length=250, blank=True)
    tipo_retencion = models.ForeignKey(TipoRetencion)
    campo_formulario = models.CharField(max_length=250,blank=True)
    cuenta = models.ForeignKey(PlanDeCuentas,null=True, blank=True)
    codigo_facturacion_electronica = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed  = False
        db_table = 'retencion_detalle'

class FormaPago(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=250)
    codigo = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sri_forma_pago'


class SustentoTributario(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sustento_tributario'

    def __unicode__(self):
       return self.nombre
