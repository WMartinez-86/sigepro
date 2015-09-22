from django.shortcuts import render
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, landscape, portrait, A4
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from apps.sprints.views import graficar
from django.contrib.auth.models import User
# Create your views here.


def hello_pdf(request):
    # Creamos el objeto HttpResponse con las cabeceras PDF apropiadas.
    respuesta = HttpResponse(content_type = 'application/pdf')
    respuesta['Content-Disposition'] = 'attachment; filename=hola.pdf'

    buffer = StringIO()

    # Crea el objeto PDF, usando el objeto StringIO como su "fichero".
    p = canvas.Canvas(buffer)


    # Dibujamos cosas en el PDF. Aqui es donde ocurre la generacion del PDF.
    # Lea en la documentacion de ReportLab la lista completa de funcionalidad.
    p.drawString(100, 100, "Hello world.")

    # Cerramos el objeto PDF.
    p.showPage()
    p.save()

    # Tomamos el valor del bufer StringIO y lo escribimos en la respuesta.
    respuesta.write(buffer.getvalue())
    return respuesta



def generar_pdf(request):
    print "Genero el PDF"
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "clientes.pdf"  # llamado clientes
    # esta linea es por si deseas descargar directo el pdf a tu computadora
    #response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    clientes = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Clientes", styles['Heading1'])
    clientes.append(header)
    headings = ('Nombre', 'Email')
    allclientes = [(p.username, p.email) for p in User.objects.all()]
    print allclientes

    t = Table([headings] + allclientes)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    clientes.append(t)
    doc.build(clientes)
    response.write(buff.getvalue())
    buff.close()
    return response