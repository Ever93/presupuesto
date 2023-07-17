import sqlite3
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import subprocess
from tkinter import ttk
from ventana2 import CRMApp
import locale
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog
import datetime
import decimal
import re

def conectar():
    conn = sqlite3.connect('crm.db')
    c = conn.cursor()
    return conn, c

def obtener_nombres_clientes():
    conn, c = conectar()
    c.execute("SELECT nombre FROM clientes")
    nombres = c.fetchall()
    conn.close()
    return nombres

# Establecer la configuración local para el separador de miles
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class PresupuestoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Presupuesto')
        self.root.geometry('1100x650')

        self.create_menu()
        self.create_widgets()
        self.render_clientes()
    
    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.abrir_explorador_archivos)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)

        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Cliente", command=self.abrir_ventana_crm)
        options_menu.add_command(label="Empresa", command=self.opcion_empresa)

        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Opciones", menu=options_menu)

        self.root.config(menu=menu_bar)

    def create_widgets(self):
        
        frame = tk.Frame(self.root)
        frame.pack()
        Label(frame, text='Sistema', font=('Arial', 14, 'bold'), anchor="w").grid(column=0, row=0)

        frame1 = tk.LabelFrame(self.root, text='Presupuesto', padx=10, pady=10, borderwidth=5)
        frame1.pack(padx=10, pady=10)

        combo_frame = tk.Frame(frame1)
        combo_frame.grid(column=0, row=1)
        combo_label = ttk.Label(combo_frame, text='Cliente')
        combo_label.pack(side=tk.LEFT)
        self.combo = ttk.Combobox(combo_frame, values=[], postcommand=self.actualizar_coincidencias)  # Utiliza self.combo directamente
        self.combo.set('')  # Establecer el valor seleccionado en blanco
        self.combo.pack(side=tk.LEFT)
        
        self.combo.bind('<Down>', self.desplegar_lista)  # Agregar el evento 'Down' para desplegar la lista
        
        btn_dolar = tk.Button(frame1, text='Dolar', command=self.dolar_clicked)
        btn_dolar.grid(column=1, row=1)
        self.lbl_cotizacion = Label(frame1, text='Cotización: ')
        self.lbl_cotizacion.grid(column=1, row=0)

        btn_porcentaje = tk.Button(frame1, text='%', command=self.porcentaje_clicked)
        btn_porcentaje.grid(column=2, row=1)
        self.lbl_interes = Label(frame1, text='Interés:')
        self.lbl_interes.grid(column=2, row=0)

        btn_eliminar_producto = tk.Button(frame1, text='Eliminar Producto', command=self.eliminar_producto_clicked)
        btn_eliminar_producto.grid(column=3, row=1)

        btn_agregar_producto = tk.Button(frame1, text='Agregar Producto', command=self.agregar_producto_clicked)
        btn_agregar_producto.grid(column=4, row=1)

        self.total_guarani = 0
        self.total_label = Label(frame1, text='Total:', font=('Arial', 12, 'bold'), anchor="w")
        self.total_label.grid(column=0, row=3)
        
        observacion_label = Label(self.root, font=('Arial', 12, 'bold'), text='Observación:')
        observacion_label.pack(anchor='w')
        
        btn_observacion = tk.Button(frame1, text='Observacion', command=self.abrir_ventana_observacion)
        btn_observacion.grid(column=2, row=3)
        
        btn_guardar_pedido = tk.Button(frame1, text='Guardar', command=self.guardar_pedido_clicked)
        btn_guardar_pedido.grid(column=1, row=3)
        
        

        btn_generar_pedido = tk.Button(frame1, text='Pedio', command=self.generar_pedido_clicked)
        btn_generar_pedido.grid(column=3, row=3)

        btn_generar_presupuesto = tk.Button(frame1, text='Presupuesto', command=self.generar_presupuesto_clicked)
        btn_generar_presupuesto.grid(column=4, row=3)

        tree_frame = tk.Frame(frame1)
        tree_frame.grid(column=0, row=2, columnspan=5)
        tree_label = ttk.Label(tree_frame, text='Presupuesto')
        tree_label.pack()

        self.tree = ttk.Treeview(tree_frame, selectmode='browse')
        self.tree['columns'] = ('Codigo', 'Cantidad', 'Producto', 'Guarani', 'Dolar')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Codigo')
        self.tree.column('Cantidad')
        self.tree.column('Producto')
        self.tree.column('Guarani')
        self.tree.column('Dolar')

        self.tree.heading('Codigo', text='Codigo')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Producto', text='Producto')
        self.tree.heading('Guarani', text='Guarani')
        self.tree.heading('Dolar', text='Dolar')
        self.tree.pack()

    def abrir_ventana_observacion(self):
        top = tk.Toplevel()
        top.title('Observación')
        top.geometry('300x200')

        observacion_text = tk.Text(top)
        observacion_text.pack(fill=tk.BOTH, expand=True)

        btn_cargar = tk.Button(top, text='Cargar', command=self.cargar_observacion)
        btn_cargar.pack(side=tk.BOTTOM, pady=10)

        top.transient(self.root)
        top.grab_set()
        self.root.wait_window(top)

    def abrir_ventana_observacion(self):
        top = tk.Toplevel()
        top.title('Observación')
        top.geometry('300x300')

        frame = tk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True)

        observacion_text = tk.Text(frame, width=30, height=10)
        observacion_text.pack(fill=tk.BOTH, expand=True)
        observacion_text.focus_set()  # Mantener el enfoque en el cuadro de texto

        btn_cargar = tk.Button(top, text='Cargar', command=lambda: self.cargar_observacion(observacion_text.get("1.0", tk.END).strip(), top))
        btn_cargar.pack(side=tk.BOTTOM, pady=10)

        top.transient(self.root)
        top.grab_set()
        self.root.wait_window(top)

    def cargar_observacion(self, observacion, top):
        print("Observación:", observacion)
    # Haz algo con la observación (por ejemplo, cargarla en otro lugar)
        top.destroy()



    def render_clientes(self):
        nombres_clientes = obtener_nombres_clientes()
        self.clientes = [nombre[0] for nombre in nombres_clientes]
        self.combo['values'] = self.clientes

    def abrir_explorador_archivos(self):
        subprocess.run(["explorer.exe"])
        
    def abrir_ventana_crm(self):
        self.crm_app = CRMApp(self)  # Pasar self como argumento
        self.actualizar_nombres_clientes()  # Actualizar los nombres de clientes en el Combobox
        self.crm_app.mainloop()  # Mostrar la ventana CRMApp


    def opcion_empresa(self):
        pass
    
    def dolar_clicked(self):
        top = tk.Toplevel()
        top.title('Cargar Cotización')
        top.geometry('250x100')

        lbl_cotizacion = tk.Label(top, text='Cotización:')
        lbl_cotizacion.pack()

        entry_cotizacion = tk.Entry(top)
        entry_cotizacion.pack()
        entry_cotizacion.focus_set()  # Establecer el foco en el campo de entrada

        def on_enter(event):
            self.guardar_cotizacion(entry_cotizacion.get(), top)
            
        entry_cotizacion.bind('<Return>', on_enter)  # Ejecutar guardar_cotizacion al presionar Enter
        btn_guardar = tk.Button(top, text='Guardar', command=lambda: self.guardar_cotizacion(entry_cotizacion.get(), top))
        btn_guardar.pack()
        top.mainloop()

    def porcentaje_clicked(self):
        top = tk.Toplevel()
        top.title('Cargar Porcentaje')
        top.geometry('250x100')

        lbl_porcentaje = tk.Label(top, text='Porcentaje:')
        lbl_porcentaje.pack()

        entry_porcentaje = tk.Entry(top)
        entry_porcentaje.pack()
        entry_porcentaje.focus_set()  # Establecer el foco en el campo de entrada

        def on_enter(event):
            self.guardar_porcentaje(entry_porcentaje.get(), top)
            
        entry_porcentaje.bind('<Return>', on_enter)  # Ejecutar guardar_cotizacion al presionar Enter

        btn_guardar = tk.Button(top, text='Guardar', command=lambda: self.guardar_porcentaje(entry_porcentaje.get(), top))
        btn_guardar.pack()

        top.mainloop()

    def eliminar_producto_clicked(self):
        # Obtener el elemento seleccionado en el Treeview
        selection = self.tree.selection()
        if selection:
        # Eliminar el elemento de la lista y del Treeview
            self.tree.delete(selection)
        # Actualizar el total
            self.actualizar_total()


    def agregar_producto_clicked(self):
        top = Toplevel()
        top.title('Cargar producto')
        top.geometry('350x140')

        lcodigo = Label(top, text='Codigo')
        codigo = Entry(top, width=40)
        lcodigo.grid(row=0, column=0)
        codigo.grid(row=0, column=1)

        lcantidad = Label(top, text='Cantidad')
        cantidad = Entry(top, width=40)
        lcantidad.grid(row=1, column=0)
        cantidad.grid(row=1, column=1)
        
        lproducto = Label(top, text='Producto')
        producto = Entry(top, width=40)
        lproducto.grid(row=2, column=0)
        producto.grid(row=2, column=1)
        
        lprecio_dolar = Label(top, text='Precio Dolar')
        precio_dolar = Entry(top, width=40)
        lprecio_dolar.grid(row=3, column=0)
        precio_dolar.grid(row=3, column=1)
        
        lprecio_guarani = Label(top, text='Precio Guarani')
        precio_guarani = Entry(top, width=40)
        lprecio_guarani.grid(row=4, column=0)
        precio_guarani.grid(row=4, column=1)
        
        def cargar():
            # Obtener los valores de los campos
            codigo_val = codigo.get()
            cantidad_val = cantidad.get()
            producto_val = producto.get()
            precio_dolar_val = precio_dolar.get()
            precio_guarani_val = precio_guarani.get()
            # Cálculos
            cotizacion = float(self.lbl_cotizacion.cget("text").split(': ')[1])  # Obtener el valor de la cotización
            porcentaje = float(self.lbl_interes.cget("text").split(': ')[1].strip('%'))  # Obtener el valor del porcentaje

            precio_dolar_val = float(precio_dolar_val) if precio_dolar_val else 0.0  # Convertir el precio en dólares a un número
            precio_guarani_val = float(precio_guarani_val) if precio_guarani_val else 0.0  # Convertir el precio en guaraníes a un número
            cantidad_val = int(cantidad_val)  # Convertir la cantidad a un número entero

            costo_venta = (precio_dolar_val * cotizacion) * (1 + (porcentaje / 100))  # Calcular el costo de venta
            costo_venta = round(costo_venta, 2)  # Redondear el costo de venta a 2 decimales

            costo_total_guarani = costo_venta * cantidad_val  # Calcular el costo total en guaraníes

            if precio_guarani_val:
                self.total_guarani += costo_total_guarani
            # Formatear el valor de costo_total_guarani con separador de miles y sin decimales
            costo_total_guarani_str = locale.format_string("%.0f", costo_total_guarani, grouping=True)
            costo_total_guarani_str = costo_total_guarani_str.replace(',', '.')
    
            # Insertar los valores en el Treeview
            self.tree.insert('', END, values=(codigo_val, cantidad_val, producto_val, costo_total_guarani_str, f"{precio_dolar_val:.2f}"))
            # Actualizar el total
            self.actualizar_total()
            # Cerrar la ventana
            top.destroy()

        btn_cargar = Button(top, text='Cargar', command=cargar)
        btn_cargar.grid(row=5, column=1)

        # Creamos el main loop para nuestra segunda ventana
        top.mainloop()

    def actualizar_total(self):
        total_guarani = sum(decimal.Decimal(str(self.tree.item(item)['values'][3].replace('.', ''))) for item in self.tree.get_children())
        total_formatted = '{:,.0f}'.format(total_guarani).replace(',', '.')
        self.total_label.config(text=f'Total: {total_formatted}')


    def guardar_pedido_clicked(self):
        pass

    def generar_pedido_clicked(self):
        pass

    def generar_presupuesto_clicked(self):
        # Obtener el nombre del cliente seleccionado del Combobox
        cliente = self.combo.get()
        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        # Sugerir el nombre de archivo con la fecha y el nombre del cliente
        nombre_archivo = f"Presupuesto_{cliente}_{fecha_actual}.pdf"
        # Solicitar la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")],
                                                initialfile=nombre_archivo)
        if not file_path:
            return  # El usuario canceló la selección o no ingresó un nombre de archivo

        # Crear el lienzo del PDF
        pdf = canvas.Canvas(file_path, pagesize=letter)

        # Configuración de fuentes
        pdf.setFont("Times-Bold", 14)
        pdf.setFont("Times-Bold", 12)

        # Título
        pdf.drawCentredString(300, 700, "Presupuesto Equipo de Computo")

        # Cliente
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(50, 650, f"Cliente: {cliente}")

        # Subtítulo Equipo
        pdf.setFont("Times-Bold", 12)
        pdf.drawString(50, 620, "Equipo")

        # Obtener los productos del Treeview
        productos = [self.tree.set(item, "Producto") for item in self.tree.get_children()]

        # Imprimir los productos como párrafos
        y = 600
        for producto in productos:
            pdf.setFont("Times-Bold", 12)
            pdf.drawString(70, y, producto)
            y -= 20

        # Precio total
        pdf.drawString(50, y - 40, "Precio:")
        total = self.total_label.cget("text").split(": ")[1]
        pdf.drawString(100, y - 40, total + " contado con IVA incluido")

        # Guardar el PDF y cerrar el lienzo
        pdf.save()
        # Mostrar mensaje de éxito
        messagebox.showinfo("PDF Generado", "El PDF se generó correctamente.")

    def guardar_cotizacion(self, cotizacion, top):
        self.lbl_cotizacion.config(text='Cotización: ' + cotizacion)
        top.destroy()

    def guardar_porcentaje(self, porcentaje, top):
        self.lbl_interes.config(text='Interés: ' + porcentaje + '%')
        top.destroy()

    def actualizar_nombres_clientes(self):
        nombres_clientes = obtener_nombres_clientes()
        self.clientes = [nombre[0] for nombre in nombres_clientes]
        self.combo['values'] = self.clientes
        self.combo.current(0)  # Establecer la selección en el primer elemento de la lista

    def actualizar_coincidencias(self):
        texto_ingresado = self.combo.get()
        coincidencias = [cliente for cliente in self.clientes if re.search(texto_ingresado, cliente, re.IGNORECASE)]
        self.combo['values'] = coincidencias[:5]  # Mostrar solo las primeras 5 coincidencias
        
    def desplegar_lista(self, event):
        self.combo.event_generate('<<ComboboxSelected>>')  # Generar el evento '<<ComboboxSelected>>' para desplegar la lista

root = Tk()
app = PresupuestoApp(root)
root.mainloop()
