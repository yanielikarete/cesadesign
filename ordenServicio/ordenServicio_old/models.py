from django.db import models
from clientes.models import Cliente
from pedido.models import Pedido
from ordenproduccion.models import OrdenProduccion
from facturacion.models import GuiaRemision
from empleados.models import Empleado

# Create your models here.

class OrdenServicio(models.Model):
    orden_id = models.AutoField(primary_key=True)
    nro_orden = models.CharField(max_length=30, blank=True,)
    ciudad = models.CharField(max_length=30, blank=True,)
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, null=True, blank=True,)
    direccion =  models.TextField(blank=True,)
    GARAN="GARAN"
    REPAR="REPAR"
    INSTA="INSTA"
    IMPLE="IMPLE"
    VENTA="VENTA"
    OBJETO_CHOICES=(
        ("Garantia","Garantia"),
        ("Reparacion","Reparacion"),
        ("Instalacion","Instalacion"),
        ("Implementos Seguridad","Implementos Seguridad"),
        ("Venta","Venta"),
    )
    objeto_orden = models.CharField(max_length=250,blank=True,choices=OBJETO_CHOICES)
    hora_salida_fabrica = models.TimeField(blank=True, null=True)
    hora_llegada_obra = models.TimeField(blank=True, null=True)
    hora_salida_obra = models.TimeField(blank=True, null=True)
    hora_llegada_fabrica = models.TimeField(blank=True, null=True)
    novedades =  models.TextField( blank=True,)
    pedido = models.ForeignKey(Pedido, null=True, blank=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, null=True, blank=True)
    guia_remision = models.ForeignKey(GuiaRemision, null=True, blank=True)
    reporte_visita =  models.TextField(blank=True,)
    trabajos_realizar =  models.TextField(blank=True,)
    observaciones = models.TextField(blank=True)
    maestros_responsables = models.ManyToManyField(Empleado, related_name='maestros_responsables', blank=True,null=True)
    maestro_encargado = models.ForeignKey(Empleado, related_name='maestro_encargado', blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.BooleanField(default=True, blank=True,)
    codigo_pedido = models.CharField(max_length=250, blank=True, null=True)
    codigo_orden_produccion = models.CharField(max_length=255, blank=True, null=True)
    maestro =  models.TextField( blank=True)

