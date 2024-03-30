#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tools
# Requires: Python >= 2.4
# Versions:
# tools_model.py 1.0
#
from django.db import models
from .tools import Tools
from main.middlewares import ThreadLocal

#=====================================================#
# Filtros de Modelos
#=====================================================#

class FilterByPerfilManager(models.Manager):
    def get_queryset(self):
        try:
            user_session = ThreadLocal.get_current_user()
            if not(user_session.is_superuser):
                return super(FilterByPerfilManager, self).get_queryset().filter(activo=True, created_by=user_session)
        except Exception as e:
            #Tools.manejadorErrores(e)
            pass
        return super(FilterByPerfilManager, self).get_queryset()