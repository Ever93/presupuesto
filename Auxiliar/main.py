from tkinter import *
from tkinter import messagebox
import sqlite3
import tkinter as tk
import subprocess
from tkinter import ttk
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
root.title('Prespuesto')
#ancho por alto
root.geometry('1100x650')

ventana_secundaria = None

def abrir_ventana_secundaria():

    global ventana_secundaria
    root.withdraw()  # Ocultar la ventana principal
    ventana_secundaria = tk.Toplevel()
    ventana_secundaria.title("Ventana secundaria")
    ventana_secundaria.geometry('600x280')
    ventana_secundaria.protocol("WM_DELETE_WINDOW", cerrar_ventana_secundaria)

    tree_label = ttk.Label(tree_frame, text='Cliente')
    tree_label.pack()
    tree = ttk.Treeview(ventana_secundaria)
    tree['columns'] = ('Nombre', 'Telefono', 'Empresa')
    tree.column('#0', width=0, stretch=NO)
    tree.column('Nombre')
    tree.column('Telefono')
    tree.column('Empresa')

    tree.heading('Nombre', text='Nombre')
    tree.heading('Telefono', text='Telefono')
    tree.heading('Empresa', text='Empresa')
    tree.grid(column=2, row=1, columnspan=4)

def cerrar_ventana_secundaria():
    global ventana_secundaria
    ventana_secundaria.destroy()  # Cerrar la ventana secundaria
    root.deiconify()  # Mostrar nuevamente la ventana principal

def abrir_explorador_archivos():
    subprocess.run(["explorer.exe"])

#Creamos las opciones de archivo y Opciones
# Crear la barra de menú
menu_bar = tk.Menu(root)
# Crear el menú "Archivo"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=abrir_explorador_archivos)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)
# Crear el menú "Opciones"
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Cliente", command=abrir_ventana_secundaria)
options_menu.add_command(label="Empresa", command='')

# Agregar los menús a la barra de menú
menu_bar.add_cascade(label="Archivo", menu=file_menu)
menu_bar.add_cascade(label="Opciones", menu=options_menu)

# Configurar la barra de menú en la ventana principal
root.config(menu=menu_bar)


#El primer Frame(esta encima de Frame1)
frame = tk.Frame(root)
frame.pack()
Label(frame, text='Sistema', font=('Arial', 14, 'bold'), anchor="w").grid(column=0, row=0)

##############

#Frame1, contiene a todo el cuadro de presupuesto y los botones
frame1 = tk.Frame(root)
frame1 = LabelFrame(root, text='Presupuesto', padx=10, pady=10, borderwidth=5)
frame1.pack(padx=10, pady=10)

#Contiene el frame de cliente que se renderiza en frame1 con el buscador
combo_frame = tk.Frame(frame1)
combo_frame.grid(column=0, row=1)
combo_label = ttk.Label(combo_frame, text='Cliente')
combo_label.pack(side=tk.LEFT)
combo = ttk.Combobox(combo_frame)
combo.pack(side=tk.LEFT)


#Se encuentra todos los botones de arriba del treeview
btn_dolar = tk.Button(frame1, text='Dolar', command='')
btn_dolar.grid(column=1, row=1)
Label(frame1, text='Cotizacion:').grid(column=1, row=0)

btn_porcentaje = tk.Button(frame1, text='%', command='')
btn_porcentaje.grid(column=2, row=1)

Label(frame1, text='Interes:').grid(column=2, row=0)

btn = tk.Button(frame1, text='Eliminar Producto', command='')
btn.grid(column=3, row=1)

btn = tk.Button(frame1, text='Agregar Producto', command='')
btn.grid(column=4, row=1)

#Footer(Etiqueta y botones de footer)
Label(frame1, text='Total:', font=('Arial', 12, 'bold'), anchor="w").grid(column=0, row=3)
btn_guardar_pedido = tk.Button(frame1, text='Guardar', command='')
btn_guardar_pedido.grid(column=2, row=3)
btn_generar_pedido = tk.Button(frame1, text='Pedio', command='')
btn_generar_pedido.grid(column=3, row=3)
btn_generar_presupuesto = tk.Button(frame1, text='Presupuesto', command='')
btn_generar_presupuesto.grid(column=4, row=3)
######################################

#Contiene el cuadro de la vista de arbol(Treeview)
tree_frame = tk.Frame(frame1)
tree_frame.grid(column=0, row=2, columnspan=5)
#Etiqueta heading del cuadro treeview
tree_label = ttk.Label(tree_frame, text='Presupuesto')
tree_label.pack()

#Cuadro con columnas y filas del treeview
tree = ttk.Treeview(tree_frame)
tree['columns'] = ('Codigo', 'Cantidad', 'Producto', 'Guarani', 'Dolar')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('Codigo')
tree.column('Cantidad')
tree.column('Producto')
tree.column('Guarani')
tree.column('Dolar')

tree.heading('Codigo', text='Codigo')
tree.heading('Cantidad', text='Cantidad')
tree.heading('Producto', text='Producto')
tree.heading('Guarani', text='Guarani')
tree.heading('Dolar', text='Dolar')

tree.pack()


root.mainloop()