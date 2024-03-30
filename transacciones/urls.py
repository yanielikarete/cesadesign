# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *
from .forms import *

urlpatterns = patterns('',

	#=================Proforma===========================#
	# url(r'^proforma/$', ProformaListView.as_view(),name='transacciones-proforma-list',),
	# url(r'^transaccionesproforma/nuevo$','transacciones.views.ProformaCreateView',name='transacciones-proforma-create',),
	# url(r'^transaccionesproforma/(?P<pk>\d+)/editar/$','transacciones.views.ProformaUpdateView',name='transacciones-proforma-update',),
	# url(r'^transaccionesproforma/(?P<pk>\d+)/detalle/$',ProformaDetailView.as_view(),name='transacciones-proforma-detail',),
	# url(r'^ptransaccionesroforma/eliminar/$','transacciones.views.proformaEliminarView',name='transacciones-proforma-delete',),
	# url(r'^transaccionesproforma/(?P<pk>\d+)/eliminar/$','transacciones.views.proformaEliminarByPkView',name='transacciones-proforma-delete-pk',),
	# url(r'^proformafactura/registrar$', 'transacciones.views.transacciones_register_proforma', name='transacciones-register-proforma',),
	# url(r'^proformafactura/consultar$', 'transacciones.views.transacciones_consult_proforma', name='transacciones-consult-proforma',),
	# url(r'^proformafactura/consultar/editar/(?P<id_proforma>\d+)$', 'transacciones.views.transacciones_update_proforma', name='transacciones-update-proforma',),

	#=================RegistroDocumento===========================#
	url(
		r'^registrodocumento/$',
		RegistroDocumentoListView.as_view(),
		name='registrodocumento-list',
	),
	url(
		r'^registrodocumento/nuevo$',
		'transacciones.views.RegistroDocumentoCreateView',
		name='registrodocumento-create',
	),
	url(
		r'^registrodocumento/(?P<pk>\d+)/editar/$',
		'transacciones.views.RegistroDocumentoUpdateView',
		name='registrodocumento-update',
	),
	url(
		r'^registrodocumento/(?P<pk>\d+)/detalle/$',
		RegistroDocumentoDetailView.as_view(),
		name='registrodocumento-detail',
	),
	url(
		r'^registrodocumento/eliminar/$',
		'transacciones.views.registroDocumentoEliminarView',
		name='registrodocumento-delete',
	),
	url(
		r'^registrodocumento/(?P<pk>\d+)/eliminar/$',
		'transacciones.views.registroDocumentoEliminarByPkView',
		name='registrodocumento-delete-pk',
	),

   #=================Deposito===========================#
	url(r'^deposito/$','transacciones.views.deposito_list_view', name='deposito-list', ),
	url(r'^deposito/nuevo$', 'transacciones.views.deposito_nuevo_view', name='deposito-nuevo', ),
	url(r'^deposito/crear$', 'transacciones.views.deposito_crear_view', name='deposito-crear', ),
	url(r'^deposito/(?P<pk>\d+)/editar/', 'transacciones.views.deposito_edit_view', name='deposito-edit', ),
	url(r'^deposito/(?P<pk>\d+)/update/', 	'transacciones.views.deposito_update_view', name='deposito-update', ),

   #=================Documento===========================#
	#Compra
	url(r'^documento/compra$','transacciones.views.documento_list_view', name='documento-list', ),
	url(r'^documento/compra/api$','transacciones.views.documento_list_api_view', name='documento-list-api', ),
	url(r'^documento/compra/apiNuevo$','transacciones.views.documento_compra_api_view', name='documento-compra-api', ),
	url(r'^documento/compra/nuevo$', 'transacciones.views.documento_nuevo_view', name='documento-nuevo', ),
	url(r'^documento/compra/crear$', 'transacciones.views.documento_compra_crear_view', name='documento-compra-crear', ),
	url(r'^documento/compra/(?P<pk>\d+)/editar/', 'transacciones.views.documento_compra_edit_view', name='documento-compra-edit', ),
	url(r'^documento/compra/(?P<pk>\d+)/update/', 'transacciones.views.documento_compra_update_view', name='documento-compra-update', ),
	#url(r'^documento/compra/(?P<pk>\d+)/update/', 'transacciones.views.documento_update_view', name='documento-update', ),
	url(r'^documento/compra/consultar/facturas', 'transacciones.views.documento_compra_consultar_facturas', name='documento-compra-consultar-facturas', ),
	url(r'^documento/compra/asiento$', 'transacciones.views.consultar_documento_asiento_view', name='consultar-documento-asiento', ),
	url(r'^documento/compra/retencion$', 'transacciones.views.consultar_documento_retencion_view', name='consultar-documento-retencion', ),
	url(r'^documento/compra/retencion/(?P<pk>\d+)/imprimir', 'transacciones.views.imprimir_retencion_compra_view', name='documento-compra-retencion-imprimir', ),
	url(r'^documento/compra/asiento/(?P<pk>\d+)/imprimir', 'transacciones.views.imprimir_asiento_compra_view', name='documento-compra-asiento-imprimir', ),
	url(r'^documento/compra/(?P<pk>\d+)/consultar/', 'transacciones.views.documento_compra_consultar_view', name='documento-compra-consultar', ),

	#Liq Compra
	# url(r'^documento/lcompra$','transacciones.views.lcdocumento_list_view', name='documento-list', ),
	# url(r'^documento/compra/apiNuevolc$', 'transacciones.views.documento_lcompra_api_view', name='documento-compra-api', ),
	# url(r'^documento/compra/consultar/liquidaciones', 'transacciones.views.documento_compra_consultar_liquidaciones', name='documento-compra-consultar-liquidaciones', ),


	#Compra retencion
	url(r'^documento/compra/retencion$','transacciones.views.documento_retencion_list_view', name='documento-list', ),
	url(r'^documento/compra/retencion/nuevo$', 'transacciones.views.documento_nuevo_retencion_view', name='docuento-compra-retencion'),
	url(r'^documento/compra/retencion/crear$', 'transacciones.views.documento_compra_retencion_crear_view', name='documento-compra-retencion-crear', ),
    url(r'^documento/compra/(?P<pk>\d+)/eliminar', 'transacciones.views.documentoCompraEliminarByPkView', name='documento-compra-eliminar', ),


    url(r'^documento/consulta/$', 'transacciones.views.consultar_orden_compra', name='consultar-orden-compra'),
	url(r'^documento/consulta/retencion$', 'transacciones.views.consultar_retencion', name='consultar-retencion'),
	url(r'^documento/consulta/razonsocial', 'transacciones.views.consultar_razon_social',name='consultar-razon-social'),
	url(r'^documento/consulta/proforma-cliente', 'transacciones.views.consultar_proforma_cliente',name='consultar-proforma-cliente'),
	url(r'^documento/consulta/proforma-detalle-cliente', 'transacciones.views.consultar_proforma_detalle_cliente',name='consultar-proforma-detalle-cliente'),
	url(r'^documento/compra/consulta/cuenta$', 'transacciones.views.compra_consultar_cuenta', name='consultar-cuenta-compra'),
	url(r'^documento/compra/consulta/cuentaByCodigo$', 'transacciones.views.compra_consultar_cuenta_by_codigo', name='consultar-cuenta-compra-by-codigo'),
	url(r'^documento/consulta/items$', 'transacciones.views.consultar_items_orden', name='consultar-items-orden'),
	url(r'^documento/consulta/razonsocialId', 'transacciones.views.consultar_razon_social_id',name='consultar-razon-social-id'),



	#Venta
	url(r'^documento/venta$','transacciones.views.documento_venta_list_view', name='documento-venta-list', ),
	url(r'^documento/venta/nuevo$', 'transacciones.views.documento_venta_nuevo_view', name='documento-venta-nuevo', ),
	url(r'^documento/venta/crear$', 'transacciones.views.documento_venta_crear_view', name='documento-venta-crear', ),
	url(r'^documento/venta/consultar/proformas$', 'transacciones.views.documento_consultar_proforma', name='consultar-proforma'),
	url(r'^documento/venta/consultar/items$', 'transacciones.views.documento_consultar_proforma_detalle', name='consultar-proforma-detalle'),
	url(r'^documento/venta/consultar/facturas$', 'transacciones.views.documento_venta_consultar_facturas', name='documento-venta-consultar-facturas', ),
	url(r'^documento/venta/consultar/cuenta$', 'transacciones.views.consultar_cuenta_contable', name='consultar-cuenta-contable'),
	url(r'^documento/venta/consultar/cuenta_codigo$', 'transacciones.views.consultar_cuenta_contable_by_codigo', name='consultar-cuenta-contable-by-codigo'),
	url(r'^documento/venta/factura/(?P<pk>\d+)/imprimir', 'transacciones.views.imprimir_factura_venta_view', name='documento-venta-factura-imprimir', ),
    url(r'^documento/venta/facturas/(?P<pk>\d+)/imprimirPdf', 'transacciones.views.imprimir_factura_venta_pdf_view', name='documento-venta-factura-imprimir-pdf', ),
	url(r'^documento/venta/factura/(?P<pk>\d+)/imprimir_prueba', 'transacciones.views.impresion_factura_venta_prueba_view', name='documento-venta-factura-prueba', ),
    url(r'^documento/(?P<pk>\d+)/eliminar/$','transacciones.views.documentoVentaEliminarByPkView',name='documento-venta-delete-pk',),
	url(r'^documento/venta/factura/(?P<pk>\d+)/consultar', 'transacciones.views.consultar_factura_venta_view', name='documento-venta-consultar-factura', ),

	#Venta retencion
	url(r'^documento/venta/retencion$','transacciones.views.documento_venta_retencion_list_view', name='documento-list', ),
	url(r'^documento/venta/retencion/nuevo$', 'transacciones.views.documento_nuevo_retencion_venta_view', name='docuento-retencion-venta'),
	url(r'^documento/venta/retencion/crear$', 'transacciones.views.documento_venta_retencion_crear_view', name='documento-venta-retencion-crear', ),
	url(r'^documento/venta/retencion/(?P<pk>\d+)/imprimir', 'transacciones.views.imprimir_retencion_venta_view', name='documento-venta-retencion-imprimir', ),
	url(r'^documento/venta/retencion/(?P<pk>\d+)/eliminar/$','transacciones.views.retencionVentaEliminarByPkView', name='retencion-venta-delete-pk', ),
	url(r'^documento/venta/retencion/(?P<pk>\d+)/consultar', 'transacciones.views.retencion_venta_consultar_view', name='documento-venta-retencion-consultar', ),

	#Cruces
	url(r'^documento/venta/cruces$','transacciones.views.cruces_list_view', name='cruces-list', ),
	url(r'^documento/venta/cruces/nuevo$', 'transacciones.views.documento_nuevo_cruces_view', name='documento-cruces-venta'),
	url(r'^documento/venta/cruces/crear$', 'transacciones.views.documento_nuevo_cruces_crear_view', name='documento-cruces-crear', ),

	url(r'^documento/venta/consultar/anticipos$', 'transacciones.views.documento_venta_consultar_anticipos', name='documento-venta-consultar-anticipos', ),
	url(r'^documento/venta/consultar/deudas$', 'transacciones.views.documento_venta_consultar_deudas', name='documento-venta-consultar-deudas', ),

    url(
        r'^documento/venta/imprimirArchivoPdf/(?P<pk>\d+)/$',
        'transacciones.views.index',
        name='factura-imprimir-pdf',
    ),
   url(r'^documento/consulta/plan_cuenta_retencion_detalle$', 'transacciones.views.consultar_plan_cuentas_retencion_detalle_view', name='consultar-plan-cuentas-retencion-detalle'),
   url(r'^export_to_excel_fatura/(?P<pk>\d+)/$',
         'transacciones.views.export_to_excel_factura', name='export_to_excel_factura'),
   
   url(r'^export_to_pdf_fatura/(?P<pk>\d+)/$',
         'transacciones.views.export_to_pdf_factura', name='export_to_pdf_factura'),
   
    url(r'^factura/validarFactura/$','transacciones.views.validarFactura',name='factura-validar',),
	url(r'^retencion/(?P<pk>\d+)/imprimirpdf', 'transacciones.views.imprimir_pdf_retencion_view', name='retencion-imprimir-pdf', ),
	url(r'^documento/venta/api$','transacciones.views.documento_venta_api_view', name='documento-venta-api', ),
	url(r'^documento/consulta/guias-remision-cliente', 'transacciones.views.consultar_guias_remision_cliente',name='consultar-guias-remision-cliente'),
	
	url(r'^consultar_facturacion_electronica/$','transacciones.views.consultar_facturacion_electronica', name='documento-facturacion-electronica', ),
	url(r'^consultar_retencion_electronica/$','transacciones.views.consultar_retencion_electronica', name='documento-retencion-electronica', ),
	url(r'^consultar_retencion_electronica_actual/$','transacciones.views.consultar_retencion_electronica_actual', name='documento-retencion-electronica-actual', ),
	url(r'^consultar_datos_facturacion_electronica/(?P<pk>\d+)/', 'transacciones.views.consultar_datos_facturacion_electronica', name='consultar-datos-facturacion-electronica', ),
	url(r'^consultar_datos_retencion_electronica/(?P<pk>\d+)/', 'transacciones.views.consultar_datos_retencion_electronica', name='consultar-datos-retencion-electronica', ),
	url(r'^listado_retencion_electronica', 'transacciones.views.listado_retencion_electronica', name='listado-retencion-electronica', ),


)
