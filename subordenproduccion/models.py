from django.db import models
from inventario.models import *
from config.models import *
from proforma.models import *
from reunion.models import *
from ordenEgreso.models import *
from pedido.models import *
from ordenproduccion.models import *
from empleados.models import Empleado

# Create your models here.
class SubordenProduccion(models.Model):
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    secuencia= models.CharField(max_length=255, blank=True)
    observaciones = models.TextField(blank=True)
    finalizada = models.BooleanField(blank=True)
    reproceso= models.BooleanField(default=False,blank=True)
    horas = models.FloatField(blank=True, null=True)
    costo_horas = models.FloatField(blank=True, null=True)
    costo_materiales = models.FloatField(blank=True, null=True)
    porcentaje_costo = models.FloatField(blank=True,default=0)
    class Meta:
        managed = False
        db_table = 'suborden_produccion'

class SubordenProduccionDetalle(models.Model):
    suborden_produccion = models.ForeignKey(SubordenProduccion, blank=True, null=True)
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
    fecha = models.DateField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    tipo_hora = models.CharField(max_length=255, blank=True)
    externo= models.BooleanField(default=False)
    empleado_interno = models.ForeignKey(Empleado, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'suborden_produccion_detalle'
class OrdenProduccionReceta(models.Model):
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    areas = models.ForeignKey(Areas, blank=True, null=True)
    suborden_produccion = models.ForeignKey(SubordenProduccion, blank=True, null=True)
    material = models.CharField(max_length=255, blank=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    otros_costos = models.BooleanField(default=False)
    fecha = models.DateField(blank=True, null=True)
    egresos = models.FloatField(blank=True, null=True,default=0)
    ingresos = models.FloatField(blank=True, null=True,default=0)
    aprobacion_despachar= models.BooleanField(default=False)
    aprobado_por = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'orden_produccion_receta'
class OrdenProduccionBodega(models.Model):
    producto = models.ForeignKey(Producto, blank=True, null=True)
    cantidad = models.FloatField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    medida = models.CharField(max_length=255, blank=True)
    ambiente = models.ForeignKey(Ambiente, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    observaciones = models.TextField(blank=True)
    cantidad_recibida = models.FloatField(blank=True, null=True)
    bodega = models.ForeignKey(Bodega, blank=True, null=True)
    suborden_produccion = models.ForeignKey(SubordenProduccion, blank=True, null=True)
    largo = models.CharField(max_length=255, blank=True, null=True)
    fondo = models.CharField(max_length=255, blank=True, null=True)
    alto = models.CharField(max_length=255, blank=True, null=True)
    codigo= models.CharField(max_length=255, blank=True, null=True)
    imagen = models.ImageField(null=True,blank=True,upload_to = "imagenes/producto/")
    ingresado_bodega = models.BooleanField(blank=True)
    numero_orden_ingreso=models.IntegerField(blank=True,default=0)
    cantidad_despachada = models.DecimalField(max_digits=18, decimal_places=2,blank=True)
    cantidad_sobrante = models.DecimalField(max_digits=18, decimal_places=2,blank=True)

    class Meta:
        managed = False
        db_table = 'orden_produccion_bodega'



# Create your models here.
class CostoFabricacion(models.Model):
    fecha = models.CharField(max_length=255, blank=True, null=True)
    mes =models.IntegerField(blank=True,default=0)
    anio=models.IntegerField(blank=True,default=0)
    anulado = models.BooleanField(default=False)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'costo_fabricacion'
        

class CostoFabricacionDetalle(models.Model):
    costo_fabricacion = models.ForeignKey(CostoFabricacion, blank=True, null=True)
    orden_produccion = models.ForeignKey(OrdenProduccion, blank=True, null=True)
    horas_subop  =  models.FloatField(blank=True, null=True,default=0)
    factor_horas  =  models.FloatField(blank=True, null=True,default=0)
    horas_nomina  =  models.FloatField(blank=True, null=True,default=0)
    mod   =  models.FloatField(blank=True, null=True,default=0)
    nomina_mod  =  models.FloatField(blank=True, null=True,default=0)
    bodega   =  models.FloatField(blank=True, null=True,default=0)
    factor_calculo_horas  =  models.FloatField(blank=True, null=True,default=0)
    moi   =  models.FloatField(blank=True, null=True,default=0)
    bs_mod  =  models.FloatField(blank=True, null=True,default=0)
    bs_moi  =  models.FloatField(blank=True, null=True,default=0)
    alimentacion   =  models.FloatField(blank=True, null=True,default=0)
    otros_prod  =  models.FloatField(blank=True, null=True,default=0)
    serv_planta   =  models.FloatField(blank=True, null=True,default=0)
    mantenimiento   =  models.FloatField(blank=True, null=True,default=0)
    depreciacion  =models.FloatField(blank=True, null=True,default=0)
    aport_patronal=models.FloatField(blank=True, null=True,default=0)
    fondo_reserva = models.FloatField(blank=True, null=True,default=0)
    impto_renta = models.FloatField(blank=True, null=True,default=0)
    iess_asumido = models.FloatField(blank=True, null=True,default=0)
    total_cf = models.FloatField(blank=True, null=True,default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'costo_fabricacion_detalle'
