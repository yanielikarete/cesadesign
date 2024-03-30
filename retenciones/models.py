from django.db import models

# Create your models here.

class TipoRetencion(models.Model):
	tipo_retencion_id = models.AutoField(primary_key=True)
	codigo = models.CharField(max_length=20)
	descripcion = models.CharField(max_length=255)
	porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
	impuesto = models.CharField(max_length=20)

