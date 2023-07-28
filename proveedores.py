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

        def render_proveedores():
            rows = self.c.execute("SELECT * FROM proveedores").fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, row[0], values=(row[1], row[2], row[3]))
                

        def insertar(proveedores):
            self.c.execute("""
                INSERT INTO proveedores (nombre, telefono, direccion) VALUES (?, ?, ?)
                """, (proveedores['nombre'], proveedores['telefono'], proveedores['direccion']))
            self.conn.commit()
            
            render_proveedores()

        def nuevo_proveedor():
            def guardar():
                
                if not nombre.get():
                    messagebox.showerror('Error', 'El nombre es obligatorio')
                    return
                if not telefono.get():
                    messagebox.showerror('Error', 'El teléfono es obligatorio')
                    return
                if not direccion.get():
                    messagebox.showerror('Error', 'La dirección es obligatoria')
                    return

                proveedores = {
                    'nombre': nombre.get(),
                    'telefono': telefono.get(),
                    'direccion': direccion.get()
                }

                insertar(proveedores)
                top.destroy()

            # Definimos una subventana
            top = Toplevel()
            top.title('Nuevo Proveedor')

            lnombre = Label(top, text='Nombre:')
            nombre = Entry(top, width=40)
            lnombre.grid(row=0, column=0, padx=5, pady=5)
            nombre.grid(row=0, column=1, padx=5, pady=5)

            ltelefono = Label(top, text='Teléfono:')
            telefono = Entry(top, width=40)
            ltelefono.grid(row=1, column=0, padx=5, pady=5)
            telefono.grid(row=1, column=1, padx=5, pady=5)

            ldireccion = Label(top, text='Dirección:')
            direccion = Entry(top, width=40)
            ldireccion.grid(row=2, column=0, padx=5, pady=5)
            direccion.grid(row=2, column=1, padx=5, pady=5)

            btn_guardar = Button(top, text='Guardar', command=guardar)
            btn_guardar.grid(row=3, column=1)

            # Creamos el main loop para nuestra segunda ventana
            top.mainloop()

        def eliminar_proveedor():
            id = self.tree.selection()[0]
            proveedor = self.c.execute("SELECT * FROM proveedores where id = ?", (id,)).fetchone()
            respuesta = messagebox.askokcancel('Seguro', 'Estas seguro de querer eliminar el proveedor ' + proveedor[1] + '?')
            if respuesta:
                self.c.execute("DELETE FROM proveedores where id = ?", (id,))
                self.conn.commit()
                render_proveedores()
            else:
                pass
            
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
