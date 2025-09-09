from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generar_pdf(registros):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Reporte de Placas Registradas")

    # Encabezados
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, "ID")
    c.drawString(100, height - 100, "Número")
    c.drawString(250, height - 100, "Fecha y Hora")

    # Contenido
    y = height - 120
    c.setFont("Helvetica", 10)

    for id_, numero, fecha_hora in registros:
        c.drawString(50, y, str(id_))
        c.drawString(100, y, numero)
        c.drawString(250, y, fecha_hora)
        y -= 20
        if y < 50:  # Salto de página
            c.showPage()
            y = height - 50

    c.save()
    buffer.seek(0)
    return buffer
