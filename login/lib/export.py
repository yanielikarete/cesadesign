# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Export
# Requires: Python >= 2.4
# Versions:
# export.py 1.0

# Import
import csv
import xlwt
from datetime import datetime, date
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from login.lib.tools_pdf import render_to_pdf
from tools import Tools

from muedirsa.models import *

import sys;
reload(sys);
sys.setdefaultencoding("utf8")

class Export:

    ########################################################################################
	##
	## Funciones para Exportar Data en CSV
	##
	########################################################################################

    @staticmethod
    def export_to_csv(model_queryset,headers_queryset):

        response = Export.add_head("text/csv; charset=utf-8","csv",model_queryset.model.__name__)
        writer = csv.writer(response)
        writer.writerow(headers_queryset)
        # Write data rows

        for obj in model_queryset:
            try:
                writer.writerow([str(getattr(obj, field)).encode("iso-8859-1") for field in headers_queryset])
            except Exception as e:
                writer.writerow([str(getattr(obj, field)).decode('utf-8', 'ignore') for field in headers_queryset])
                Tools.manejadorErrores(e)
        return response

    @staticmethod
    def export_to_excel(model_queryset, headers_queryset):
        response = Export.add_head("application/ms-excel","xls",model_queryset.model.__name__)
        wb = xlwt.Workbook(encoding='UTF-8')
        ws = wb.add_sheet(model_queryset.model.__name__)
        default_style = xlwt.Style.default_style
        #datetime_style = xlwt.easyxf(num_format_str='dd/mm/yyyy hh:mm')
        date_style = xlwt.easyxf(num_format_str='dd/mm/yyyy')

        #for field in model._meta.fields:
        #   headers.append(field.name)

        for col, rowdata in enumerate(headers_queryset):
            ws.write(0, col, rowdata)

        for row, rowdata in enumerate(model_queryset):
            print rowdata
            filas = [getattr(rowdata, field) for field in headers_queryset]
            for col, coldata in enumerate(filas):
                if isinstance(coldata, datetime):
                    val = coldata.strftime("%d/%m/%Y %H:%S")
                elif isinstance(coldata, date):
                    style = date_style
                    val = coldata
                else:
                    style = default_style
                    val = str(coldata)

                ws.write(row + 1, col, val, style)

        wb.save(response)
        return response

    @staticmethod
    def add_head(mimetype_str,type_file,model_name):
        response = HttpResponse(content_type = mimetype_str)
        date = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        data_file = "%s-%s.%s" % (model_name,date,type_file)
        response["Content-Disposition"] = ('attachment; filename="%s"' %
                                               data_file)
        return response

    @staticmethod
    def export_to_pdf(model_queryset, docente):

        reporte = Export.dibujarReporteParcial(docente)
        index = 1

        table = """<table border="1" cellpadding="0" cellspacing="0" class="tabla" style="border-collapse: collapse;table-layout:fixed;">
            		<thead>
            			<tr>
            				<th>No</th><th>Menu</th><th>Grupo</th>
            			</tr>
            		</thead>
            	<tbody>"""

        # for obj in model_queryset:
        #     table = '%s<tr><td class="text-center sx">%s</td><td class="sxl">%s</td><td>%s</td></tr>' % (table, index, str(obj.cedula), str(obj))
        #     index += 1

        table = "%s</tbody></table>" % (table)
        reporte['contenido'] = table


        return render_to_pdf('reporte/reporte.html',
                        {'pagesize':'A4','header_height':'3cm','footer_height':'2cm','reporte':reporte,})

    #=====================================================#
    @staticmethod
    def htmlHeader():
        contenido = """
            <table>
                <tr>
                    <td class="text-center">
                        
                    </td>
                <tr>
                <tr>
        		    <td>
        		       <br>
        		    </td>
        		</tr>
            </table>
            """
        return contenido

    #=====================================================#
    @staticmethod
    def dibujarReporteParcial(docente):
        #paralelo = Paralelo.objects.get(docente=docente)
        #anio_lectivo = AnioLectivo.objects.get(id=1)

        header_contenido = Export.htmlHeader()
        contenido = ""
        #institucion = docente.unidad_educativa()
        #institucion_str = "%s %s" % (institucion.tipo, institucion)
        institucion=""
        institucion_str=""
        paralelo=""
        anio_lectivo=""
        header_contenido = header_contenido.replace('[[UNIDAD EDUCATIVA]]', institucion_str)
        header_contenido = header_contenido.replace('[[PARALELO]]', str(paralelo))
        header_contenido = header_contenido.replace('[[ANIO LECTIVO]]', str(anio_lectivo))

        return {'header_contenido':header_contenido,'contenido':contenido,'footer_contenido':''}