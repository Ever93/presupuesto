import sqlite3
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import tkinter as tk
import subprocess
from cliente import CRMApp
from proveedores import ProveedoresApp
from configCuotas import ConfigCuotasApp
import locale
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import decimal
import re
from tkinter import simpledialog
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



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

def obtener_nombres_proveedores():
    conn, c = conectar()
    c.execute("SELECT nombre FROM proveedores")
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
        self.observacion_texto = ""  # Variable de instancia para almacenar el texto de la observación
        self.lbl_cotizacion_value = StringVar()
        self.lbl_interes_value = StringVar()
        self.selected_cliente = ""  
        self.selected_proveedor = ""  
        self.create_menu()
        self.create_widgets()
        self.render_clientes()
        self.render_proveedores()
        self.elementos_eliminados = {}
    
    def obtener_datos_cuotas(self):
        conn, c = conectar()
        c.execute("SELECT cantidadcuotas FROM cuotas")
        cantidad = [fila[0] for fila in c.fetchall()]
        conn.close()
        return cantidad

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Abrir", command=self.abrir_explorador_archivos)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        #Menu Opciones
        options_menu = tk.Menu(menu_bar, tearoff=0)
        options_menu.add_command(label="Cliente", command=self.abrir_ventana_crm)
        options_menu.add_command(label="Proveedores", command=self.abrir_ventana_proveedores)
        options_menu.add_command(label="Empresa", command=self.opcion_empresa)
        options_menu.add_command(label="Config. Cuotas", command=self.abrir_ventana_cuotas)

        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        menu_bar.add_cascade(label="Opciones", menu=options_menu)
        self.root.config(menu=menu_bar)

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()
        Label(frame, text='Sistema', font=('Arial', 14, 'bold'), anchor="w").grid(column=0, row=0)
        frame1 = tk.LabelFrame(self.root, text='Presupuesto', padx=10, pady=10, borderwidth=5)
        frame1.pack(padx=10, pady=10)
        
        combo_frame_cliente = tk.Frame(frame1)
        combo_frame_cliente.grid(column=0, row=1)
        combo_label_cliente = ttk.Label(combo_frame_cliente, text='Cliente')
        combo_label_cliente.pack(side=tk.LEFT)
        self.combo_cliente = ttk.Combobox(combo_frame_cliente, values=[], postcommand=self.actualizar_coincidencias_cliente)
        self.combo_cliente.set('')  # Set the selected value to empty initially
        self.combo_cliente.pack(side=tk.LEFT)
        self.combo_cliente.bind('<<ComboboxSelected>>', self.cliente_selected)  # Add event handler
       
        combo_frame_proveedor = tk.Frame(frame1)
        combo_frame_proveedor.grid(column=1, row=1)
        combo_label_proveedor = ttk.Label(combo_frame_proveedor, text='Proveedor')
        combo_label_proveedor.pack(side=tk.LEFT)
        self.combo_proveedor = ttk.Combobox(combo_frame_proveedor, values=[], postcommand=self.actualizar_coincidencias_proveedor)
        self.combo_proveedor.set('')  # Set the selected value to empty initially
        self.combo_proveedor.pack(side=tk.LEFT)
        self.combo_proveedor.bind('<<ComboboxSelected>>', self.proveedor_selected)  # Add event handler

        btn_dolar = tk.Button(frame1, text='Dolar', command=self.dolar_clicked)
        btn_dolar.grid(column=2, row=1)
        self.lbl_cotizacion = Label(frame1, text='Cotización: ')
        self.lbl_cotizacion.grid(column=2, row=0)

        btn_porcentaje = tk.Button(frame1, text='%', command=self.porcentaje_clicked)
        btn_porcentaje.grid(column=3, row=1)
        self.lbl_interes = Label(frame1, text='Interés:')
        self.lbl_interes.grid(column=3, row=0)

        btn_eliminar_producto = tk.Button(frame1, text='Eliminar Producto', command=self.eliminar_producto_clicked)
        btn_eliminar_producto.grid(column=4, row=1)

        btn_agregar_producto = tk.Button(frame1, text='Agregar Producto', command=self.agregar_producto_clicked)
        btn_agregar_producto.grid(column=5, row=1)

        self.total_guarani = 0
        self.total_label = Label(frame1, text='Total:', font=('Arial', 12, 'bold'), anchor="w")
        self.total_label.grid(column=0, row=3)
        
        btn_observacion = tk.Button(frame1, text='Observacion', command=self.abrir_ventana_observacion)
        btn_observacion.grid(column=2, row=3)
        
        btn_guardar_pedido = tk.Button(frame1, text='Guardar', command=self.guardar_pedido_clicked)
        btn_guardar_pedido.grid(column=1, row=3)
        
        btn_generar_pedido = tk.Button(frame1, text='Pedido', command=self.generar_pedido_clicked)
        btn_generar_pedido.grid(column=3, row=3)

        btn_generar_presupuesto = tk.Button(frame1, text='Presupuesto', command=self.generar_presupuesto_clicked)
        btn_generar_presupuesto.grid(column=4, row=3)

        tree_frame = tk.Frame(frame1)
        tree_frame.grid(column=0, row=2, columnspan=6)
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
        #Creamos label para cargar observacion
        observacion_label = Label(self.root, font=('Arial', 12, 'bold'), text='Observación:')
        observacion_label.pack(anchor='w', padx='20')
        self.observacion_frame = Frame(self.root, bd=1, relief='solid',  width=200, height=200)  # Ajusta los valores de width y height según tu preferencia
        self.observacion_frame.pack(pady=1, padx=35, anchor='w', fill='both', expand=True)    
        #Aqui se muestra el texto cargado en observacion
        self.observacion_text_label = Label(self.observacion_frame, font=('Times New Roman', 12), text=self.observacion_texto, anchor='w', justify='left')
        self.observacion_text_label.pack(pady=5, padx=5, anchor='w')

        #Label cuotas
        cuotas_label = Label(self.root, font=('Arial', 12, 'bold'), text='Cuotas:')
        cuotas_label.pack(anchor='w', padx='20')
        # Creamos un nuevo frame para las cuotas
        cuotas_frame = Frame(self.root, bd=1, relief='solid', width=200, height=100)
        cuotas_frame.pack(pady=10, padx=35, anchor='w', fill='both', expand=True)
        # Obtener datos cantidad de la base de datos
        cantidad = self.obtener_datos_cuotas()
        # Mostrar los datos en el marco de cuotas
        for cantidad_cuotas in cantidad:
            label = tk.Label(cuotas_frame, text=f"Cantidad de Cuotas: {cantidad_cuotas}")
            label.pack(anchor='w')
    
        
    def abrir_ventana_observacion(self):
        top = Toplevel()
        top.title('Observación')
        top.geometry('300x300')

        frame = Frame(top)
        frame.pack(fill=BOTH, expand=True)

        observacion_text = Text(frame, width=30, height=3, font=('Arial', 12))
        observacion_text.pack(pady=10, padx=10)
        observacion_text.focus_set() 

        observacion_text.bind("<Return>", lambda event: self.cargar_observacion(observacion_text.get("1.0", "end-1c"), top))

        btn_cargar = Button(frame, text='Cargar', command=lambda: self.cargar_observacion(observacion_text.get("1.0", "end-1c"), top))
        btn_cargar.pack(pady=10)

        top.transient(self.root)
        top.grab_set()
        self.root.wait_window(top)

    def cargar_observacion(self, observacion, top):
        self.observacion_texto = observacion
        self.observacion_text_label.config(text=self.observacion_texto)
        top.destroy()

    def render_clientes(self):
        nombres_clientes = obtener_nombres_clientes()
        self.clientes = [nombre[0] for nombre in nombres_clientes]
        self.combo_cliente['values'] = self.clientes
    
    def render_proveedores(self):
        nombres_proveedores = obtener_nombres_proveedores()
        self.proveedores = [nombre[0] for nombre in nombres_proveedores]
        self.combo_proveedor['values'] = self.proveedores
       
    def cliente_selected(self, event):
        self.selected_cliente = self.combo_cliente.get()
        
    def proveedor_selected(self, event):
        self.selected_proveedor = self.combo_proveedor.get()
    
    def abrir_explorador_archivos(self):
        subprocess.run(["explorer.exe"])
        
    def abrir_ventana_crm(self):
        self.crm_app = CRMApp(self)  # Pasar self como argumento
        self.actualizar_nombres_clientes()  # Actualizar los nombres de clientes en el Combobox
        self.crm_app.mainloop()  # Mostrar la ventana CRMApp
        
    def abrir_ventana_proveedores(self):
        proveedores_app = ProveedoresApp(self)
        proveedores_app.mainloop()

    def opcion_empresa(self):
        pass
    
    def abrir_ventana_cuotas(self):
        configcuotas_app = ConfigCuotasApp(self)
        configcuotas_app.mainloop()
    
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
    
    def guardar_cotizacion(self, cotizacion, top):
        self.lbl_cotizacion.config(text='Cotización: ' + cotizacion)
        self.lbl_cotizacion_value.set(cotizacion)  # Actualizar el valor de lbl_cotizacion_value después de guardar la cotización
        top.destroy()

    def guardar_porcentaje(self, porcentaje, top):
        self.lbl_interes.config(text='Interés: ' + porcentaje + '%')
        self.lbl_interes_value.set(porcentaje)  # Actualizar el valor de lbl_interes_value después de guardar el porcentaje
        top.destroy()
  
    def eliminar_producto_clicked(self):
        # Obtener el elemento seleccionado en el Treeview
        selection = self.tree.selection()
        if selection:
        # Eliminar el elemento de la lista y del Treeview
            self.tree.delete(selection)
        # Actualizar el total
            self.actualizar_total()

    def agregar_producto_clicked(self):     
        cotizacion_vacia = self.lbl_cotizacion.cget("text") == "Cotización: "
        interes_vacio = self.lbl_interes.cget("text") == "Interés:"

        if cotizacion_vacia:
            messagebox.showwarning("Cotización requerida", "La cotización es requerida.")
        elif interes_vacio:
            messagebox.showwarning("Interés requerido", "El interés es requerido.")
        else:
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
            
                if precio_dolar_val:
                    costo_venta = (precio_dolar_val * cotizacion) * (1 + (porcentaje / 100))
                    costo_venta = round(costo_venta, 2)  # Redondear el costo de venta a 2 decimales
                    costo_total_guarani = costo_venta * cantidad_val  # Calcular el costo total en guaraníes
                    if precio_guarani_val:
                        self.total_guarani += costo_total_guarani
            # Formatear el valor de costo_total_guarani con separador de miles y sin decimales
                    costo_total_guarani_str = locale.format_string("%.0f", costo_total_guarani, grouping=True)
                    costo_total_guarani_str = costo_total_guarani_str.replace(',', '.')
            # Formatear el valor de costo_total_guarani con separador de miles y sin decimale
                else:
                    costo_venta = precio_guarani_val * cantidad_val
                    costo_total_guarani_str = locale.format_string("%.0f", costo_venta, grouping=True)
                    costo_total_guarani_str = costo_total_guarani_str.replace(',', '.')
                #insertar valores en el treeview
                if precio_dolar_val:
                    self.tree.insert('', END, values=(codigo_val, cantidad_val, producto_val, f'{costo_total_guarani_str}', f'{precio_dolar_val:.2f}'))
                else:
                    self.tree.insert('', END, values=(codigo_val, cantidad_val, producto_val, costo_total_guarani_str, ''))
            # Actualizar el total
                self.actualizar_total()
                top.destroy()

            btn_cargar = Button(top, text='Cargar', command=cargar)
            btn_cargar.grid(row=5, column=1)
            top.mainloop()

    def actualizar_total(self):
        total_guarani = sum(decimal.Decimal(str(self.tree.item(item)['values'][3].replace('.', ''))) for item in self.tree.get_children())
        total_formatted = '{:,.0f}'.format(total_guarani).replace(',', '.')
        self.total_label.config(text=f'Total: {total_formatted}')

    def guardar_pedido_clicked(self):
        pass
    
    def generar_pedido_clicked(self):
        items_a_imprimir_pedido = self.mostrar_cuadro_dialogo_pedido()
        if items_a_imprimir_pedido is None:
            return
        
    def mostrar_cuadro_dialogo_pedido(self):
        # Obtener los productos del Treeview
        productos = [
            (
            self.tree.set(item, "Codigo"),
            self.tree.set(item, "Cantidad"),
            self.tree.set(item, "Producto"),
            )
            for item in self.tree.get_children()
        ]
        # Mostrar el cuadro de diálogo
        dialog = tk.Toplevel()
        dialog.title("Seleccionar elementos")
        label = tk.Label(dialog, text="Seleccione los elementos que desea incluir en el pedido:")
        label.pack()

        items_var = []
        for producto in productos:
            var = tk.IntVar(value=1)  # Inicialmente, todos los elementos están marcados
            items_var.append(var)
            check_btn = tk.Checkbutton(
                dialog,
                text=producto[2],  # Usamos el nombre del producto como etiqueta
                variable=var,
                onvalue=1,
                offvalue=0
            )
            check_btn.pack(anchor=tk.W)

        def generar_pedido():
            selected_items = [
                producto for producto, var in zip(productos, items_var) if var.get() == 1
            ]
            dialog.destroy()
            self.generar_pedido_clicked_with_items(selected_items)
            
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        btn_generar_pdf = tk.Button(button_frame, text="Generar PDF", command=generar_pedido)
        btn_generar_pdf.pack(side=tk.LEFT, padx=10, pady=5)  # Ubicar a la izquierda con un espaciado
        # Hacer que el cuadro de diálogo se adapte a su contenido
        dialog.update_idletasks()
        dialog.geometry(f"{dialog.winfo_reqwidth()}x{dialog.winfo_reqheight()}")
        dialog.mainloop()

    def generar_pedido_clicked_with_items(self, items_a_imprimir_pedido):
        # Obtener el nombre del cliente seleccionado del Combobox
        cliente = self.combo_cliente.get()
        proveedor = self.combo_proveedor.get()
        fecha_actual = datetime.datetime.now().strftime("%d_%m_%y")  # Obtener la fecha actual
        # Sugerir el nombre de archivo con el título "Pedido" y la fecha actual
        nombre_archivo_sugerido = f"Pedido_{cliente}_{fecha_actual}.pdf"
        # Solicitar la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=nombre_archivo_sugerido
        )
        if not file_path:
            # El usuario canceló la selección o no ingresó un nombre de archivo
            return
        # Crear el lienzo del PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        # Estilo para el título del PDF
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title = Paragraph("Pedido", title_style)
        elements.append(title)

        # Proveedor
        elements.append(Paragraph(f"Proveedor: {proveedor}", styles['Heading1']))
        # Subtítulo Productos Seleccionados
        elements.append(Paragraph("Productos", styles['Heading2']))
        # Datos para la tabla
        columnas = ('Codigo', 'Cantidad', 'Producto')
        filas = [columnas]  # Agregar el encabezado de la tabla a las filas

        for item in items_a_imprimir_pedido:
            codigo = item[0]
            cantidad = item[1]
            producto = item[2]
            fila = (codigo, cantidad, producto)
            filas.append(fila)

        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Encabezado con fondo gris
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto del encabezado en blanco
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinear contenido al centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior para el encabezado
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para el contenido
        ])
        # Crear la tabla
        table = Table(filas, colWidths=[100, 100, 200], rowHeights=30)
        table.setStyle(style)
        # Agregar la tabla al documento
        elements.append(table)
        # Compilar y guardar el PDF
        doc.build(elements)
        # Mostrar mensaje de éxito
        messagebox.showinfo("PDF Generado", "El PDF se generó correctamente.")

    def generar_pedido_img(self, items_a_imprimir):
    # Obtener el nombre del cliente seleccionado del Combobox
        cliente = self.combo.get()
    # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    # Sugerir el nombre de archivo con el título "Pedido" y el nombre del cliente y fecha actual
        nombre_archivo_sugerido = f"Pedido_{cliente}_{fecha_actual}.png"
    # Solicitar la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Files", "*.png")], initialfile=nombre_archivo_sugerido
        )

        if not file_path:
        # El usuario canceló la selección o no ingresó un nombre de archivo
            return
 
    # Crear la imagen
        img = Image.new('RGB', (400, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 15)
    # Escribir el título
        draw.text((10, 10), f"Pedido de {cliente}", fill=(0, 0, 0), font=font)

    # Escribir los productos seleccionados
        y = 30
        for producto in items_a_imprimir:
            draw.text((20, y), producto, fill=(0, 0, 0), font=font)
            y += 20
    # Guardar la imagen
        img.save(file_path)

    # Mostrar mensaje de éxito
        messagebox.showinfo("Imagen Generada", "La imagen se generó correctamente.")

    def generar_presupuesto_clicked(self):
        # Mostrar el cuadro de diálogo para seleccionar los elementos a incluir en el PDF
        items_a_imprimir = self.mostrar_cuadro_dialogo_items()
        if items_a_imprimir is None:
        # Si el usuario cancela el cuadro de diálogo, no se genera el PDF
            return
        
    def mostrar_cuadro_dialogo_items(self):
    # Obtener los productos del Treeview
        productos = [self.tree.set(item, "Producto") for item in self.tree.get_children()]
    # Mostrar el cuadro de diálogo
        dialog = tk.Toplevel()
        dialog.title("Seleccionar elementos")

        label = tk.Label(dialog, text="Seleccione los elementos que desea incluir en el presupuesto:")
        label.pack()

        items_var = []
        for producto in productos:
            var = tk.IntVar(value=1)  # Inicialmente, todos los elementos están marcados
            items_var.append(var)
            check_btn = tk.Checkbutton(dialog, text=producto, variable=var, onvalue=1, offvalue=0)
            check_btn.pack(anchor=tk.W)

        def generar_presupuesto():
            selected_items = [
                producto for producto, var in zip(productos, items_var) if var.get() == 1
            ]
            dialog.destroy()
            self.generar_presupuesto_clicked_with_items(selected_items)

        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)

        btn_generar_pdf = tk.Button(button_frame, text="Generar", command=generar_presupuesto)
        btn_generar_pdf.pack(side=tk.LEFT, padx=10, pady=5)  # Ubicar a la izquierda con un espaciado

        btn_generar_img = tk.Button(button_frame, text="Detallar", command='')
        btn_generar_img.pack(side=tk.LEFT, padx=10, pady=5)  # Ubicar a la izquierda con un espaciado
        
        dialog.update_idletasks()
        dialog.geometry(f"{dialog.winfo_reqwidth()}x{dialog.winfo_reqheight()}")
        
        dialog.mainloop()
        
    def generar_presupuesto_clicked_with_items(self, items_a_imprimir):
    # Obtener el nombre del cliente seleccionado del Combobox
        cliente = self.combo_cliente.get()
    # Obtener la fecha actual
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    # Sugerir el nombre de archivo con la fecha y el nombre del cliente
        nombre_archivo = f"Presupuesto_{cliente}_{fecha_actual}.pdf"
    # Solicitar la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], initialfile=nombre_archivo
        )

        if not file_path:
        # El usuario canceló la selección o no ingresó un nombre de archivo
            return
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

    # Imprimir los productos seleccionados como párrafos
        y = 600
        for producto in items_a_imprimir:
            pdf.setFont("Times-Bold", 12)
            pdf.drawString(70, y, producto)
            y -= 20

    # Precio total(la x es la distancia del borde vertical y la y es la distancia del borde horizontal)
        pdf.drawString(50, y - 40, "Precio:")
        total = self.total_label.cget("text").split(": ")[1]
        pdf.drawString(90, y - 40, total + " contado con IVA incluido")
    #Observacion
        observacion_texto = self.observacion_text_label.cget("text")
        if observacion_texto:
            pdf.drawString(50, y - 60, observacion_texto)

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
        self.combo_cliente['values'] = self.clientes
        self.combo_cliente.current(0)  # Establecer la selección en el primer elemento de la lista
        
    def actualizar_nombres_proveedores(self):
        nombres_proveedores = obtener_nombres_proveedores()
        self.proveedores = [nombre[0] for nombre in nombres_proveedores]
        self.combo_proveedor['values'] = self.proveedores
        self.combo_proveedor.current(0)
        
    def actualizar_coincidencias_cliente(self):
        texto_ingresado = self.combo_cliente.get()
        coincidencias = [cliente for cliente in self.clientes if re.search(texto_ingresado, cliente, re.IGNORECASE)]
        self.combo_cliente['values'] = coincidencias[:5]  # Show only the first 5 matches

    def actualizar_coincidencias_proveedor(self):
        texto_ingresado = self.combo_proveedor.get()
        coincidencias = [proveedor for proveedor in self.proveedores if re.search(texto_ingresado, proveedor, re.IGNORECASE)]
        self.combo_proveedor['values'] = coincidencias[:5] 
        
    def desplegar_lista(self, event):
        self.combo.event_generate('<<ComboboxSelected>>')  # Generar el evento '<<ComboboxSelected>>' para desplegar la lista

root = Tk()
app = PresupuestoApp(root)
root.mainloop()