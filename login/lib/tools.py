#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tools
# Requires: Python >= 2.4
# Versions:
# tools.py 1.0

# Import
import datetime
import time
import calendar
import logging

from django.core.mail import EmailMessage
from config.models import Mensajes

class Tools:

    #=====================================================#
    @staticmethod
    def enviarEmail(id_mensaje, docente, titulo):
        fecha = datetime.datetime.now().strftime("%d de %B del %Y a las %H:%M")

        mensaje = Mensajes.objects.get(codigo=id_mensaje).mensaje
        mensaje = mensaje.replace('{USUARIO}', str(docente))
        mensaje = mensaje.replace('{FECHA}', str(fecha))

        try:
            email = EmailMessage(titulo, mensaje, 'info@pegaso.com', [docente.email])
            email.content_subtype = 'html'
            email.send(fail_silently = False)

        except Exception as e:
            print e
            pass

    #=====================================================#
    @staticmethod
    def calcularEstado(nota):
        estado = ''
        if nota>=6.99:
            estado = 'APROBADO'
        else:
            estado = 'REPROBADO'

        return estado

    #=====================================================#
    @staticmethod
    def calcularEscala(nota):
        escala = ''
        if nota>=9.00 and nota<=10.00:
            escala = 'DAR'
        elif nota>=7.00 and nota<=8.99:
            escala = 'AAR'
        elif nota>=4.01 and nota<=6.99:
            escala = 'NAAR'
        elif nota>0.00 and nota<=4.00:
            escala = 'NAAR'

        return escala

    #=====================================================#
    @staticmethod
    def calcularComportamiento(letra):
        valor = 0
        if letra == 'A':
            valor = 1
        elif letra == 'B':
            valor = 2
        elif letra == 'C':
            valor = 3
        elif letra == 'D':
            valor = 4
        elif letra == 'E':
            valor = 5

        return valor

    #=====================================================#
    @staticmethod
    def promedioComportamiento(valor):
        letra = ''
        if valor == 1:
            letra = 'A'
        elif valor == 2:
            letra = 'B'
        elif valor == 3:
            letra = 'C'
        elif valor == 4:
            letra = 'D'
        elif valor == 5:
            letra = 'E'

        return letra

    #=====================================================#
	@staticmethod
	def manejadorErrores(e):
		"""imprime el detalle del error ocurrido."""
		print ''
		print ':::::::::::::::::::::::::::::::::::::::::::'
		logging.exception('')
		print e
		print ':::::::::::::::::::::::::::::::::::::::::::'
		print ''

#=====================================================#
# Manejo de Fechas
#=====================================================#
	@staticmethod
	def checkDate(date_str, format):
		"""verifica si un String ee del tipo Date con un formato pasado como parametro.
		   :Parameters:
		   	- 'date_str': Fecha en tipo String.
		   	- 'format': formato de la fecha en tipo String.

			:return: True si es una fecha valida o False si no lo es
		"""
		try:
			time.strptime(date_str, format)
			return True
		except Exception:
			return False

	@staticmethod
	def strToDate(date_str, format):
		"""convierte un String en tipo Date con un formato pasado como parametro.
		   :Parameters:
		   	- 'date_str': Fecha en tipo String.
		   	- 'format': formato de la fecha en tipo String.

			:return: un tipo Date con al fecha convertida o si existe error con al fecha actual
		"""
		return datetime.datetime.strptime(date_str, format).date()

	@staticmethod
	def strToDateTime(date_str,format):
		"""convierte un String en tipo DateTime con un formato pasado como parametro.
		   :Parameters:
		   	- 'date_str': Fecha en tipo String.
		   	- 'format': formato de la fecha en tipo String.

			:return: un tipo Datetime con al fecha convertida o si existe error con al fecha actual
		"""
		return datetime.datetime.strptime(date_str, format)

	@staticmethod
	def js_timestamp_from_datetime(dt):
		"""convierte un DateTime en tipo Timestamp compatible con JavaScript.
		   :Parameters:
		   	- 'dt': DateTime a convertir.

			:return: mktime
		"""
		return 1000 * time.mktime(dt.timetuple())

	@staticmethod
	def fecha_inicio_fecha_final_mes():
		"""obtiene la fecha inicial y final del mes activo.

			:return: array con las fechas de inicial y final
		"""
		fecha_hoy = datetime.date.today()
		fecha_inicio_mes = datetime.date(fecha_hoy.year, fecha_hoy.month, 1)
		fecha_final_mes = datetime.date(fecha_hoy.year, fecha_hoy.month, calendar.monthrange(fecha_hoy.year, fecha_hoy.month)[1])
		return [fecha_inicio_mes, fecha_final_mes]

	@staticmethod
	def get_date_week():
		"""obtiene las fechade los dias de la semana activa.

			:return: array con las fechasde las semana espezando por el lunes
		"""
		date = datetime.date.today()
		start_week = date - datetime.timedelta(date.weekday())
		martes = start_week + datetime.timedelta(1)
		miercoles = start_week + datetime.timedelta(2)
		jueves = start_week + datetime.timedelta(3)
		viernes = start_week + datetime.timedelta(4)
		sabado = start_week + datetime.timedelta(5)
		end_week = start_week + datetime.timedelta(6)

		return [start_week,martes,miercoles,jueves,viernes,sabado,end_week]

	@staticmethod
	def get_date_actividad(fecha_actividad, num_actividades_diarias, fechas_dias_semana):
		"""compara dos fechas y si son iguales ingrementa el numero de las actididades diarias.
		   :Parameters:
		   	- 'fecha_actividad': Date de la actividad.
		   	- 'num_actividades_diarias': Array con el numero de actividades diarias.
		   	- 'fechas_dias_semana': Date con la fecha a comparar.

			:return: 'num_actividades_diarias' con el numero de actividades diarias actualizadas.
		"""
		if(fecha_actividad == fechas_dias_semana[0]):
			num_actividades_diarias[0] += 1
		elif(fecha_actividad == fechas_dias_semana[1]):
			num_actividades_diarias[1] += 1
		elif(fecha_actividad == fechas_dias_semana[2]):
			num_actividades_diarias[2] += 1
		elif(fecha_actividad == fechas_dias_semana[3]):
			num_actividades_diarias[3] += 1
		elif(fecha_actividad == fechas_dias_semana[4]):
			num_actividades_diarias[4] += 1
		return num_actividades_diarias
