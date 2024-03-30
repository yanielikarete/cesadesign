# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',
                       url(r'^consultar/$', 'ats.views.index', name='ats-index', ),
                       url(r'^generar$', 'ats.views.generarXmlAts', name='ats-generar-xml', ),

                       )
