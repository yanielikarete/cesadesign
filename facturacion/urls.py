# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

#=================GuiaRemision===========================#
	url(
		r'^guiaremision/$',
		'facturacion.views.GuiaRemisionListView',
		name='guiaremision-list',
	),
	url(
		r'^guiaremision/nuevo$',
		'facturacion.views.GuiaRemisionCreateView',
		name='guiaremision-create',
	),
	url(
		r'^guiaremision/(?P<pk>\d+)/editar/$',
		'facturacion.views.GuiaRemisionUpdateView',
		name='guiaremision-update',
	),
	url(
		r'^guiaremision/(?P<pk>\d+)/detalle/$',
		GuiaRemisionDetailView.as_view(),
		name='guiaremision-detail',
	),
	url(
		r'^guiaremision/eliminar/$',
		'facturacion.views.guiaremisionEliminarView',
		name='guiaremision-delete',
	),
	url(
		r'^guiaremision/(?P<pk>\d+)/eliminar/$',
		'facturacion.views.guiaremisionEliminarByPkView',
		name='guiaremision-delete-pk',
	),
	 url(
        r'^guiaremision/(?P<pk>\d+)/crearproforma/$',
        'facturacion.views.GuiaRemisionCrearProformaView',
        name='crear-guiaremision-proforma',
    ),
	url(
        r'^obtenerTipo/$',
        'facturacion.views.obtenerTipo',
        name='obtener-tipo',
    ),
    url(
        r'^guiaremisionAprobar/$',
        'facturacion.views.GuiaremisionListAprobarView',
        name='guiaremision-list-aprobada',
    ),

    url(
        r'^guiaremision/(?P<pk>\d+)/aprobar/$',
        'facturacion.views.GuiaRemisionAprobarByPkView',
        name='aprobar-guiaremision',
    ),
     url(
        r'^obtenerDetalleGuia/$',
        'facturacion.views.obtenerDetalleGuia',
        name='obtener-detalle-guia',
    ),
     url(
        r'^guiaremision/(?P<pk>\d+)/anular/$',
        'facturacion.views.GuiaremisionAnularByPkView',
        name='anular-guiaremision',
    ),
#      url(
# 		r'^factura/$',
# 		FacturaListView.as_view(),
# 		name='factura-list',
# 	),
# 	url(
# 		r'^factura/nuevo$',
# 		'facturacion.views.FacturaCreateView',
# 		name='factura-create',
# 	),
# 	url(
# 		r'^factura/(?P<pk>\d+)/editar/$',
# 		FacturaUpdateView.as_view(),
# 		name='factura-update',
# 	),
# 
# 	url(
# 		r'^factura/eliminar/$',
# 		'facturacion.views.facturaEliminarView',
# 		name='factura-delete',
# 	),
# 	url(
# 		r'^factura/(?P<pk>\d+)/eliminar/$',
# 		'facturacion.views.facturaEliminarByPkView',
# 		name='factura-delete-pk',
# 	),
# 	url(
#         r'^obtenerDetalleProformaFactura/$',
#         'facturacion.views.obtenerDetalleProformaFactura',
#         name='obtener-detalleproforma-factura',
#     ),
# 
#     url(
# 		r'^nota_credito/$',
# 		NotaCreditoListView.as_view(),
# 		name='nota-credito-list',
# 	),
# 	url(
# 		r'^nota_credito/nuevo$',
# 		'facturacion.views.NotaCreditoCreateView',
# 		name='nota-credito-create',
# 	),
# 	url(
# 		r'^nota_credito/(?P<pk>\d+)/editar/$',
# 		NotaCreditoUpdateView.as_view(),
# 		name='nota-credito-update',
# 	),
# 
# 	url(
# 		r'^nota_credito/eliminar/$',
# 		'facturacion.views.notaCreditoEliminarView',
# 		name='nota-credito-delete',
# 	),
# 	url(
# 		r'^nota_credito/(?P<pk>\d+)/eliminar/$',
# 		'facturacion.views.notaCreditoEliminarByPkView',
# 		name='nota-credito-delete-pk',
# 	),
# 	url(
#         r'^obtenerDetalleFactura/$',
#         'facturacion.views.obtenerDetalleFactura',
#         name='obtener-detalle-factura',
#     ),
    url(
        r'^obtenerFactura/$',
        'facturacion.views.obtenerFactura',
        name='obtener-factura',
    ),
 url(
        r'^imprimir/(?P<pk>\d+)/$',
        'facturacion.views.index',
        name='guiaremision-imprimir',
    ),

 url(
		r'^registrarCobroPago/$',
		'facturacion.views.RegistrarCobroPagoListView',
		name='registrar-cobro-pago-list',
	),
	url(
		r'^registrarCobroPago/nuevo$',
		'facturacion.views.RegistrarCobroPagoCreateView',
		name='registrar-cobro-pago-create',
	),
	url(
		r'^registrarCobroPago/(?P<pk>\d+)/editar/$',
		RegistrarCobroPagoUpdateView.as_view(),
		name='registrar-cobro-pago-update',
	),
	 url(
        r'^mostrar_documento/$',
        'facturacion.views.MostrarDocumentoView',
        name='mostrar_documento',
    ),

url(
        r'^mostrar_documento_general/$',
        'facturacion.views.MostrarDocumentoGeneralView',
        name='mostrar_documento_general',
    ),
	url(
        r'^mostrar_personas/$',
        'facturacion.views.MostrarPersonasView',
        name='mostrar_personas',
    ),

url(
		r'^cruceDocumento/nuevo$',
		'facturacion.views.CruceDocumentosCreateView',
		name='cruce-documentos-create',
	),
url(
		r'^cruceDocumento/$',
		'facturacion.views.CruceDocumentoListView',
		name='cruce-documento-list',
	),

url(
        r'^mostrar_cuenta/$',
        'facturacion.views.MostrarCuentaView',
        name='mostrar_cuenta',
    ),

url(
        r'^mostrar_cuenta_persona/$',
        'facturacion.views.MostrarCuentaPersonaView',
        name='mostrar_cuenta_persona',
    ),
url(
        r'^mostrar_op/$',
        'facturacion.views.MostrarOPView',
        name='mostrar_op',
    ),
	url(
        r'^cargarDireccionBodega/$',
        'facturacion.views.cargarDireccionBodega',
        name='cargar-direccion-bodega',
    ),
url(
        r'^cargarDireccionCliente/$',
        'facturacion.views.cargarDireccionCliente',
        name='cargar-direccion-cliente',
    ),


	url(
		r'^tipoguias/$',
		'facturacion.views.TipoGuiasListView',
		name='tipoguias-list',
	),
	url(
		r'^tipoguias/nuevo$',
		TipoGuiasCreateView.as_view(),
		name='tipoguias-create',
	),
	url(
		r'^tipoguias/(?P<pk>\d+)/editar/$',
		TipoGuiasUpdateView.as_view(),
		name='tipoguias-update',
	),
	
		url(r'^consultar_guia_electronica/$','facturacion.views.consultar_guia_remision_electronica', name='consultar-guia-electronica', ),

)
