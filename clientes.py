from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import TableStyle
from tkinter import filedialog

root = Tk()
root.title('CRM')

conn = sqlite3.connect('crm.db')

c = conn.cursor()

#Creamos nuestra base de datos en sqlite3
c.execute("""
        CREATE TABLE if not exists clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            Empresa TEXT NOT NULL
            
        )
        """)

#Definimos las funciones

def render_clientes():
    rows = c.execute("SELECT * FROM clientes").fetchall()
    tree.delete(*tree.get_children())
    
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

def insertar(clientes):
    c.execute("""
            INSERT INTO clientes (nombre, telefono, empresa) VALUES (?, ?, ?)
            """, (clientes['nombre'], clientes['telefono'], clientes['empresa']))
    conn.commit()
    render_clientes()

def nuevo_cliente():
    
    def guardar():
        #Validar para no cargar datos vacios
        if not nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        if not telefono.get():
            messagebox.showerror('Error', 'El telefono es obligatorio')
            return
        if not empresa.get():
            messagebox.showerror('Error', 'El nombre de empresa es obligatorio')
            return
            
        clientes = {
            'nombre': nombre.get(),
            'telefono': telefono.get(),
            'empresa': empresa.get()
        }
        
        insertar(clientes)
        top.destroy()
        
    #Definimos una subventana
    top = Toplevel()
    top.title('Nuevo cliente')
    
    lnombre = Label(top, text='Nombre')
    nombre = Entry(top, width=40)
    lnombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)
    
    
    ltelefono = Label(top, text='Telefono')
    telefono = Entry(top, width=40)
    ltelefono.grid(row=1, column=0)
    telefono.grid(row=1, column=1)
    
    lempresa = Label(top, text='Empresa')
    empresa = Entry(top, width=40)
    lempresa.grid(row=2, column=0)
    empresa.grid(row=2, column=1)
    
    guardar = Button(top, text='Guardar', command=guardar)
    guardar.grid(row=3, column=1)
    
    #Creamos el main loop para nuestra segunda ventana
    top.mainloop()


def eliminar_cliente():
    id = tree.selection()[0]
    cliente = c.execute("SELECT * FROM clientes where id = ?", (id, )).fetchone()
    respuesta = messagebox.askokcancel('Seguro', 'Estas seguro de querer eliminar el cliente ' + cliente[1] + '?')
    if respuesta:
        c.execute("DELETE FROM clientes WHERE id = ?", (id, ))
        conn.commit()
        render_clientes()
    else:
        pass


def generar_pdf():
    # Obtener los datos de los clientes
    rows = c.execute("SELECT * FROM clientes").fetchall()
    data = [['ID', 'Nombre', 'Teléfono', 'Empresa']]
    for row in rows:
        data.append([row[0], row[1], row[2], row[3]])

    # Solicitar al usuario el nombre del archivo
    filename = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF', '*.pdf')])
    if not filename:
        return  # Si el usuario cancela la selección del archivo, salimos de la función

    # Crear el documento PDF
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Crear el contenido del PDF
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Presupuesto:", styles['Title']))
    content.append(Spacer(1, 20))

    # Crear la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    content.append(table)

    # Construir el PDF
    doc.build(content)
    messagebox.showinfo('Éxito', 'Se ha generado el archivo PDF.')



btn = Button(root, text='Nuevo cliente', command=nuevo_cliente)
btn.grid(column=0, row=0)

btn_eliminar = Button(root, text='Eliminar cliente', command=eliminar_cliente)
btn_eliminar.grid(column=1, row=0)

btn_pdf = Button(root, text='Generar PDF', command=generar_pdf)
btn_pdf.grid(column=2, row=0)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre', 'Telefono', 'Empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Telefono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0, row=1, columnspan=4)


render_clientes()
root.mainloop()