from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def create_pdf_with_table(pdf_filename, data):
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []
    
    # Crear una tabla con tres columnas y la data proporcionada
    table = Table(data, colWidths=100, rowHeights=30)
    
    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado con fondo gris
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear contenido al centro
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para el encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para el contenido
    ])
    table.setStyle(style)
    
    # Agregar la tabla al documento
    elements.append(table)
    
    # Compilar y guardar el PDF
    doc.build(elements)
    
    print(f"El archivo PDF '{pdf_filename}' se ha generado exitosamente con la tabla.")

# Ejemplo de data para la tabla (lista de listas)
data = [
    ['Columna 1', 'Columna 2', 'Columna 3'],
    ['Dato 1', 'Dato 2', 'Dato 3'],
    ['Dato 4', 'Dato 5', 'Dato 6'],
    ['Dato 7', 'Dato 8', 'Dato 9']
]

# Crear el archivo PDF con la tabla
create_pdf_with_table('tabla_ejemplo.pdf', data)
