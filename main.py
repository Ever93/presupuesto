from tkinter import *
from tkinter import messagebox
import tkinter as tk
import subprocess
from tkinter import ttk
from ventana2 import CRMApp

class PresupuestoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Presupuesto')
        self.root.geometry('1100x650')

        self.create_menu()
        self.create_widgets()

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
        combo = ttk.Combobox(combo_frame)
        combo.pack(side=tk.LEFT)

        btn_dolar = tk.Button(frame1, text='Dolar', command=self.dolar_clicked)
        btn_dolar.grid(column=1, row=1)
        Label(frame1, text='Cotizacion:').grid(column=1, row=0)

        btn_porcentaje = tk.Button(frame1, text='%', command=self.porcentaje_clicked)
        btn_porcentaje.grid(column=2, row=1)
        Label(frame1, text='Interes:').grid(column=2, row=0)

        btn_eliminar_producto = tk.Button(frame1, text='Eliminar Producto', command=self.eliminar_producto_clicked)
        btn_eliminar_producto.grid(column=3, row=1)

        btn_agregar_producto = tk.Button(frame1, text='Agregar Producto', command=self.agregar_producto_clicked)
        btn_agregar_producto.grid(column=4, row=1)

        self.total_guarani = 0
        self.total_label = Label(frame1, text='Total:', font=('Arial', 12, 'bold'), anchor="w")
        self.total_label.grid(column=0, row=3)
        btn_guardar_pedido = tk.Button(frame1, text='Guardar', command=self.guardar_pedido_clicked)
        btn_guardar_pedido.grid(column=2, row=3)

        btn_generar_pedido = tk.Button(frame1, text='Pedio', command=self.generar_pedido_clicked)
        btn_generar_pedido.grid(column=3, row=3)

        btn_generar_presupuesto = tk.Button(frame1, text='Presupuesto', command=self.generar_presupuesto_clicked)
        btn_generar_presupuesto.grid(column=4, row=3)

        tree_frame = tk.Frame(frame1)
        tree_frame.grid(column=0, row=2, columnspan=5)
        tree_label = ttk.Label(tree_frame, text='Presupuesto')
        tree_label.pack()

        self.tree = ttk.Treeview(tree_frame)
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

    def abrir_explorador_archivos(self):
        subprocess.run(["explorer.exe"])
        
    def abrir_ventana_crm(self):
        self.crm_app = CRMApp()  # Crear una instancia de CRMApp
        self.crm_app.mainloop()  # Mostrar la ventana CRMApp

    def opcion_cliente(self):
        pass

    def opcion_empresa(self):
        pass

    def dolar_clicked(self):
        pass

    def porcentaje_clicked(self):
        pass

    def eliminar_producto_clicked(self):
        pass

    def agregar_producto_clicked(self):
        top = Toplevel()
        top.title('Cargar producto')
        #ancho por alto
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

        # Insertar los valores en el Treeview
            self.tree.insert('', END, values=(codigo_val, cantidad_val, producto_val, precio_guarani_val, precio_dolar_val))
            # Actualizar el total
            self.total_guarani += float(precio_guarani_val)
            #prueba
            if self.total_guarani == 0:
                self.total_label.config(text='Total: ')
            else:
                total_formatted = '{:,.0f}'.format(self.total_guarani)
                self.total_label.config(text=f'Total: {total_formatted}')
        # Cerrar la ventana
            top.destroy()

        btn_cargar = Button(top, text='Cargar', command=cargar)
        btn_cargar.grid(row=5, column=1)

            # Creamos el main loop para nuestra segunda ventana
        top.mainloop()
        

    def guardar_pedido_clicked(self):
        pass

    def generar_pedido_clicked(self):
        pass

    def generar_presupuesto_clicked(self):
        pass

root = Tk()
app = PresupuestoApp(root)
root.mainloop()
