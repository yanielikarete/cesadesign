from django.conf.urls import patterns, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',
                       # =================Codigo de Retenciones===========================#
                       url(r'^codigoRetenciones$', 'mantenimiento.views.retenciones_list_view',
                           name='retenciones-list', ),
                       url(r'^codigoRetenciones/nuevo$', 'mantenimiento.views.RetencionCreateView',
                           name='retenciones-nuevo', ),
                       url(r'^codigoRetenciones/crear$', 'mantenimiento.views.retenciones_crear_view',
                           name='retenciones-crear', ),
                       url(r'^codigoRetenciones/(?P<pk>\d+)/editar/', RetencionUpdateView.as_view(),
                           name='retenciones-editar', ),
                       url(r'^codigoRetenciones/(?P<pk>\d+)/update/', 'mantenimiento.views.retenciones_update_view',
                           name='retenciones-update', ),

                       # =================Formas de Pagos===========================#
                       url(r'^formasPagos$', 'mantenimiento.views.formaspagos_list_view', name='formaspagos-list', ),
                       url(r'^formasPagos/nuevo$', 'mantenimiento.views.formaspagos_nuevo_view',
                           name='formaspagos-nuevo', ),
                       url(r'^formasPagos/crear$', 'mantenimiento.views.formaspagos_crear_view',
                           name='formaspagos-crear', ),
                       url(r'^formasPagos/(?P<pk>\d+)/editar/', 'mantenimiento.views.formaspagos_edit_view',
                           name='formaspagos-editar', ),
                       url(r'^formasPagos/(?P<pk>\d+)/update/', 'mantenimiento.views.formaspagos_update_view',
                           name='formaspagos-update', ),

                       url(r'^sustento_tributario/$', 'mantenimiento.views.SustentoTributarioListView',
                           name='sustento-list', ),

                       url(
                           r'^sustento_tributario/nuevo$',
                           'mantenimiento.views.SustentoTributarioCreateView',
                           name='sustento-create',
                       ),
                       url(
                           r'^sustento_tributario/(?P<pk>\d+)/editar/$',
                           'mantenimiento.views.SustentoTributarioUpdateView',
                           name='sustento-update',
                       ),
                        url(r'^contabilidad/$', 'mantenimiento.views.ConfiguracionContabilidad',
                           name='contabilidad-config', ),
                       )
