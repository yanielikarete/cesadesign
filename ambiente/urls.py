from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',
url(
        r'^ambiente/$',
    'ambiente.views.ambientesListView',
        name='ambientes-list',
    ),

   url(
        r'^ambiente/nuevo$',
       'ambiente.views.ambientesCreateView',
        name='ambientes-create',
    ),
   url(
         r'^ambiente/(?P<pk>\d+)/editar/$',
         ambientesUpdateView.as_view(),
         name='ambientes-update',
    ),
   url(
        r'^ambiente/(?P<pk>\d+)/detalle/$',
        ambientesDetailView.as_view(),
        name='ambientes-detail',
    ),
    url(
        r'^ambiente/eliminar/$',
        'ambiente.views.ambientesEliminarView',
        name='ambientes-delete',
    ),
    url(
        r'^ambiente/(?P<pk>\d+)/eliminar/$',
        'ambiente.views.ambientesEliminarByPkView',
        name='ambientes-delete-pk',
    ),
url(
        r'^migrar/$',
        'ambiente.views.MigracionPlanCuentas',
        name='migracion-plan-cuentas',
    ),

url(
        r'^migrarProductos/$',
        'ambiente.views.MigracionProducto',
        name='migracion-productos',
    ),



url(
        r'^MigracionProveedores/$',
        'ambiente.views.MigracionProveedores',
        name='migracion-proveedores',
    ),
url(
        r'^MigracionRazonSocial/$',
        'ambiente.views.MigracionRazonSocial',
        name='migracion-razon-social',
    ),
url(
        r'^MigracionClienetRazonSocial/$',
        'ambiente.views.MigracionClienetRazonSocial',
        name='migracion-razon-social-clientes',
    ),

url(
        r'^MigracionProductoInventario/$',
        'ambiente.views.MigracionProductoInventario',
        name='migracion-producto-inventario',
    ),

url(
        r'^MigracionEmpleadoArea/$',
        'ambiente.views.MigracionEmpleadoArea',
        name='migracion-empleado-area',
    ),


url(
        r'^NivelarInventarioView/$',
        'ambiente.views.NivelarInventarioView',
        name='nivelar-inventario',
    ),
url(
        r'^MigrarInventarioView/$',
        'ambiente.views.MigrarInventarioView',
        name='migrar-inventario',
    ),

url(
        r'^corregirRetencionFacturas/$',
        'ambiente.views.CorregirFacturaView',
        name='corregir-retencion-facturas',
    ),
url(
        r'^corregirRetencionesVentaView/$',
        'ambiente.views.CorregirRetencionesVentaView',
        name='corregir-retencion-venta',
    ),

url(
        r'^CrearFacturaCompraView/(?P<pk>\d+)/crear/$',
        'ambiente.views.CrearFacturaCompraView',
        name='corregir-creacion-factura-compra',
    ),
url(
        r'^migrarCheque/$',
        'ambiente.views.MigracionCheques',
        name='migracion-cheques',
    ),

url(
        r'^migracionBalanceFinanciero/$',
        'ambiente.views.MigracionBalanceFinanciero',
        name='migracion-balance-financiero',
    ),
url(
        r'^migracionAfectaSaldoInicial/$',
        'ambiente.views.MigracionAfectaSaldoInicial',
        name='migracion-afecta-saldo-inicial',
    ),

url(
        r'^CorregirAsientoView/$',
        'ambiente.views.CorregirAsientoView',
        name='corregir-asiento',
    ),

url(
        r'^migrarAsientoRRHH/$',
        'ambiente.views.MigracionAsientoRrhh',
        name='migracion-asiento-rrhh',
    ),
url(
        r'^actualizarRetencionElectronica/$',
        'ambiente.views.CorregirRetencionesElectronicasView',
        name='migactualizar-retencion-electronica'
    ),
url(
        r'^actualizarFacturacionElectronica/$',
        'ambiente.views.CorregirFacturacionElectronicaView',
        name='migactualizar-facturacion-electronica'
    ),
url(
        r'^corregirFechaRetencionesElectronicas/$',
        'ambiente.views.CorregirFechaRetencionesElectronicasView',
        name='corregir-fecha-retenciones-electronica'
    ),
)