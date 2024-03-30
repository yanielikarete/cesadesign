from django.db import models
from proveedores.models import Proveedor
from clientes.models import Cliente

from os.path import basename
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class Ambiente(models.Model):
    descripcion = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    codigo = models.CharField(max_length=250, blank=True)
    orden = models.IntegerField(blank=True, null=True)
    activo = models.NullBooleanField()
    class Meta:
        db_table = 'ambiente'