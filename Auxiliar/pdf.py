from reportlab.pdfgen import canvas

def test_reportlab():
    pdf = canvas.Canvas("test.pdf")
    pdf.drawString(100, 100, "Hello, ReportLab!")
    pdf.save()
    print("PDF generado correctamente.")

test_reportlab()
