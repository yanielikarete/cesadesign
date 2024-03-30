from django.db import models
from inventario.models import Producto,Bodega,Unidades
from vendedor.models import *
from clientes.models import *
# Create your models here.
class Reunion(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    fecha = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    MOTIVO_CHOICES=(
        ('1','1 dia'),
        ('2','2 dias'),
        ('3','3 dias'),
        ('4','4 dias'),
        ('5','5 dias'),
        ('6','6 dias'),
        ('7','7 dias'),
        ('8','8 dias'),
        ('9','9 dias'),
        ('10','10 dias'),
        ('11','11 dias'),
        ('12','12 dias'),
        ('13','13 dias'),
        ('14','14 dia'),
        ('15','15 dias'),
        ('16','16 dias'),
        ('17','17 dias'),
        ('18','18 dias'),
        ('19','19 dias'),
        ('20','20 dias'),
        ('30','30 dias'),
        ('40','40 dias'),
        ('50','50 dias'),
        
    )
    motivo = models.CharField(max_length=250, blank=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    observacion = models.CharField(max_length=500, blank=True)
    tiempo_respuesta = models.CharField(max_length=250, blank=True,choices=MOTIVO_CHOICES)
    observacion_tiempo_respuesta = models.CharField(max_length=500, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    bodega = models.BooleanField(blank=True)
    finalizado_bodega = models.BooleanField(blank=True)
    respuesta_bodega = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    direccion = models.TextField(blank=True)

    class Meta:
        db_table = 'reunion'
class ImagenesReunion(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    imagen = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    reunion = models.ForeignKey(Reunion, blank=True, null=True)
    vendedor = models.ForeignKey(Vendedor, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imagenes_reunion'
class ImagenesReunionDetalle(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/reunion/")
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    imagenes_reunion = models.ForeignKey(ImagenesReunion, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'imagenes_reunion_detalle'
