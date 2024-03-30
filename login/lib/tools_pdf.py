# -*- coding: utf-8 -*-
#!/usr/bin/env python
import cStringIO as StringIO
# import ho.pisa as pisa
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from datetime import datetime

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        ###response['Content-Disposition'] = 'attachment; filename=%s-%s.pdf' % ("informe medico", datetime.now().strftime('%d-%m-%Y'))
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))