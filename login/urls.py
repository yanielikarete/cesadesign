# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.defaults import *
from .views import *

urlpatterns = patterns('',

                       url(r'^inicio/$', 'login.views.homeEmpresa', name='home-empresa'),
                       ########################################################
                       # LOGIN
                       ########################################################
                        url(r'^$', 'login.views.ingresar', name='login-index'),
                       url(r'^iniciar/$', 'login.views.ingresar', name='iniciar'),
                       url(r'^logout/$', 'login.views.salir', name='logout'),
                       url(
                           r'^accounts/password-change$',
                           'django.contrib.auth.views.password_change',
                           {'template_name': 'user/password_change_form.html'},
                           name='password_change',
                       ),
                       url(
                           r'^accounts/password-change-done$',
                           'login.views.userPasswordChangeDone',
                           name='password_change_done',
                       ),

                       ########################################################
                       # PASSWORD RESET
                       ########################################################
                       url(
                           r'^user/password/reset/$',
                           'django.contrib.auth.views.password_reset',
                           {
                               'template_name': 'registration/password_reset_form_login.html',
                               'post_reset_redirect': reverse_lazy('password_reset_done')
                           },
                           name='password_reset',
                       ),
                       url(
                           r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
                           {'template_name': 'registration/password_reset_done_login.html'},
                           name='password_reset_done',
                       ),
                       url(
                           r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {
                               'template_name': 'registration/password_reset_confirm_login.html',
                               'post_reset_redirect': reverse_lazy('password_reset_done')
                           },
                       ),
                       url(
                           r'^user/password/done/$', 'django.contrib.auth.views.password_reset_complete',
                           {'template_name': 'registration/password_reset_complete_login.html'},
                       ),
                        url(r'^getMessages/$', 'login.views.getMessages', name='get-messages'),
                       )
