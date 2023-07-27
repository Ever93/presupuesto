from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from db import conectar  # Importa el archivo db.py (o el nombre correcto de tu archivo)

class ProveedoresApp(Tk):
    def __init__(self, parent):
        super().__init__()
        self.title('Proveedores')
        self.parent = parent

        self.conn, self.c = conectar()

        self.nombre_var = StringVar(value="")
        self.telefono_var = StringVar(value="")
        self.direccion_var = StringVar(value="")

        # Función para renderizar los proveedores en el árbol
        def render_proveedores():
            rows = self.c.execute("SELECT * FROM proveedores").fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

        def insertar(proveedor):
            self.c.execute("""
                INSERT INTO proveedores (nombre, telefono, direccion) VALUES (?, ?, ?)
                """, (proveedor['nombre'], proveedor['telefono'], proveedor['direccion']))
            self.conn.commit()
            render_proveedores()

        def nuevo_proveedor():
            def guardar():
                nombre = self.nombre_var.get()
                telefono = self.telefono_var.get()
                direccion = self.direccion_var.get()

                if not nombre:
                    messagebox.showerror('Error', 'El nombre es obligatorio')
                    return
                if not telefono:
                    messagebox.showerror('Error', 'El teléfono es obligatorio')
                    return
                if not direccion:
                    messagebox.showerror('Error', 'La dirección es obligatoria')
                    return

                proveedor = {
                    'nombre': nombre,
                    'telefono': telefono,
                    'direccion': direccion
                }

                insertar(proveedor)
                top.destroy()

            # Definimos una subventana
            top = Toplevel()
            top.title('Nuevo Proveedor')

            label_nombre = Label(top, text='Nombre:')
            label_nombre.grid(row=0, column=0, padx=5, pady=5)
            entry_nombre = Entry(top, textvariable=self.nombre_var, width=40)
            entry_nombre.grid(row=0, column=1, padx=5, pady=5)

            label_telefono = Label(top, text='Teléfono:')
            label_telefono.grid(row=1, column=0, padx=5, pady=5)
            entry_telefono = Entry(top, textvariable=self.telefono_var, width=40)
            entry_telefono.grid(row=1, column=1, padx=5, pady=5)

            label_direccion = Label(top, text='Dirección:')
            label_direccion.grid(row=2, column=0, padx=5, pady=5)
            entry_direccion = Entry(top, textvariable=self.direccion_var, width=40)
            entry_direccion.grid(row=2, column=1, padx=5, pady=5)

            btn_guardar = Button(top, text='Guardar', command=guardar)
            btn_guardar.grid(row=3, column=1)

            # Creamos el main loop para nuestra segunda ventana
            top.mainloop()

        def eliminar_proveedor():
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror('Error', 'Selecciona un proveedor para eliminar')
                return
            
            respuesta = messagebox.askokcancel('Seguro', 'Estás seguro de querer eliminar el proveedor seleccionado?')
            if respuesta:
                id_proveedor = self.tree.item(selected_item, 'text')
                self.c.execute("DELETE FROM proveedores WHERE id = ?", (id_proveedor,))
                self.conn.commit()
                render_proveedores()

        btn_nuevo_proveedor = Button(self, text='Nuevo proveedor', command=nuevo_proveedor)
        btn_nuevo_proveedor.grid(column=0, row=0)

        btn_eliminar_proveedor = Button(self, text='Eliminar proveedor', command=eliminar_proveedor)
        btn_eliminar_proveedor.grid(column=1, row=0)

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Nombre', 'Teléfono', 'Dirección')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('Nombre')
        self.tree.column('Teléfono')
        self.tree.column('Dirección')

        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Teléfono', text='Teléfono')
        self.tree.heading('Dirección', text='Dirección')
        self.tree.grid(column=0, row=1, columnspan=4)

        render_proveedores()

if __name__ == '__main__':
    app = ProveedoresApp()
    app.mainloop()
