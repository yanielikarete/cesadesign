from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from login.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'login.views.ingresar', name='login'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^login/$', 'muedirsa.views.login_page', name='login'),
                       url(r'^login/', include('login.urls')),
                       url(r'^inventario/', include('inventario.urls')),
                       url(r'^clientes/', include('clientes.urls')),
                       url(r'^proveedores/', include('proveedores.urls')),
                       url(r'^OrdenesdeCompra/', include('OrdenesdeCompra.urls')),
                       url(r'^config/', include('config.urls')),
                       url(r'^proforma/', include('proforma.urls')),
                       url(r'^pedido/', include('pedido.urls')),
                       url(r'^empleados/', include('empleados.urls')),
                       url(r'^reunion/', include('reunion.urls')),
                       url(r'^vendedores/', include('vendedor.urls')),
                       url(r'^ordenproduccion/', include('ordenproduccion.urls')),
                       url(r'^ambiente/', include('ambiente.urls')),
                       url(r'^facturacion/', include('facturacion.urls')),
                       url(r'^ordenServicio/', include('ordenServicio.urls')),
                       url(r'^ordenEgreso/', include('ordenEgreso.urls')),
                       url(r'^subordenproduccion/', include('subordenproduccion.urls')),
                       url(r'^ordenIngreso/', include('ordenIngreso.urls')),
                       url(r'^reporte/', include('reporte.urls')),
                       url(r'^contabilidad/', include('contabilidad.urls')),
                       url(r'^transacciones/', include('transacciones.urls')),
                       url(r'^liquidacion_comisiones/', include('liquidacion_comisiones.urls')),
                       url(r'^recursos_humanos/', include('recursos_humanos.urls')),
                       url(r'^bancos/', include('bancos.urls')),
                       url(r'^mantenimiento/', include('mantenimiento.urls')),
                       url(r'^ats/', include('ats.urls')),
                       url(r'^ajustes/', include('ajustes.urls')),

                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
