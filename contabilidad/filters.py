# coding: utf-8
import django_filters
from .models import *

class EjercicioContableFilter(django_filters.FilterSet):
	class Meta:
		model = EjercicioContable
		fields = ['fecha_inicio', 'fecha_fin', 'abierto', 'cierreMensual', 'dia_cierre',]

class PlanDeCuentasFilter(django_filters.FilterSet):
	nombre_plan = django_filters.CharFilter(lookup_type='icontains')
	class Meta():
		model = PlanDeCuentas
		fields = ['grupo', 'nombre_plan', 'tipo_cuenta', 'codigo_plan',]

class TipoCuentaFilter(django_filters.FilterSet):
	nombre_tipo = django_filters.CharFilter(lookup_type='icontains')
	class Meta:
		model = TipoCuenta
		fields = ['nombre_tipo',]
        
class CentroCostoFilter(django_filters.FilterSet):
	nombre_centro = django_filters.CharFilter(lookup_type='icontains')
	class Meta:
		model = CentroCosto
		fields = ['nombre_centro',]

class AsientoFilter(django_filters.FilterSet):
	codigo_asiento = django_filters.CharFilter(lookup_type='icontains')
	class Meta:
		model = Asiento
		fields = ['fecha', 'codigo_asiento', 'gasto_no_deducible',]