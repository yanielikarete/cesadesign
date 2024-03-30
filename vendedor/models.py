from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
# Create your models here.

# Create your models here.
class Vendedor(models.Model):
    codigo = models.CharField(max_length=250, blank=True)
    nombre = models.CharField(max_length=250, blank=True)
    created_by = models.CharField(max_length=255, blank=True)
    updated_by = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    activo = models.NullBooleanField()
    externo = models.NullBooleanField()
    class Meta:
        managed = False
        db_table = 'vendedor'
    def __unicode__(self):
        return '%s' % (self.nombre)
    def __str__(self):
        return '%s' % (self.nombre)
