from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from db import conectar  # Importa el archivo db.py (o el nombre correcto de tu archivo)

class ConfigCuotasApp(Tk):
    def __init__(self, parent):
        super().__init__()
        self.title('Configuracion de cuotas')
        self.parent = parent

        self.conn, self.c = conectar()

        def render_cuotas():
            rows = self.c.execute("SELECT * FROM cuotas").fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, row[0], values=(row[1], row[2]))
                

        def insertar(cuotas):
            self.c.execute("""
                INSERT INTO cuotas (cantidadcuotas, tasainteres) VALUES (?, ?)
                """, (cuotas['cantidadcuotas'], cuotas['tasainteres']))
            self.conn.commit()
            render_cuotas()

        def nueva_cuota():
            def guardar():
                
                if not cantidadcuotas.get():
                    messagebox.showerror('Error', 'La cantidad de cuotas es obligatorio')
                    return
                if not tasainteres.get():
                    messagebox.showerror('Error', 'La tasa de interes es obligatorio')
                    return
                # Validar que cantidad y tasa sean valores numéricos
                if not cantidadcuotas.isnumeric():
                    messagebox.showerror('Error', 'La cantidad de cuotas debe ser un valor numérico')
                    return
                if not tasainteres.replace('.', '', 1).isdigit():
                    messagebox.showerror('Error', 'La tasa de interés debe ser un valor numérico')
                    return

                cuotas = {
                    'cantidadcuotas': cantidadcuotas.get(),
                    'tasainteres': tasainteres.get()
                }

                insertar(cuotas)
                top.destroy()

            # Definimos una subventana
            top = Toplevel()
            top.title('Nueva Cuota')

            lcantidadcuotas = Label(top, text='Cantidad:')
            cantidadcuotas = Entry(top, width=40)
            lcantidadcuotas.grid(row=0, column=0, padx=5, pady=5)
            cantidadcuotas.grid(row=0, column=1, padx=5, pady=5)

            ltasainteres = Label(top, text='Tasa de Interes:')
            tasainteres = Entry(top, width=40)
            ltasainteres.grid(row=1, column=0, padx=5, pady=5)
            tasainteres.grid(row=1, column=1, padx=5, pady=5)

            btn_guardar = Button(top, text='Guardar', command=guardar)
            btn_guardar.grid(row=3, column=1)

            # Creamos el main loop para nuestra segunda ventana
            top.mainloop()

        def editar_cuotas():
            pass
        
        def eliminar_cuotas():
            id = self.tree.selection()[0]
            cuotas = self.c.execute("SELECT * FROM cuotas where id = ?", (id,)).fetchone()
            respuesta = messagebox.askokcancel('Seguro', 'Estas seguro de querer eliminar el proveedor ' + cuotas[1] + '?')
            if respuesta:
                self.c.execute("DELETE FROM cuotas where id = ?", (id,))
                self.conn.commit()
                render_cuotas()
            else:
                pass
            
        btn_nueva_cuota = Button(self, text='Nueva cuota', command=nueva_cuota)
        btn_nueva_cuota.grid(column=0, row=0)

        btn_editar_cuota = Button(self, text='Editar Cuota', command=editar_cuotas)
        btn_editar_cuota.grid(column=1, row=0)

        btn_eliminar_cuota = Button(self, text='Eliminar Cuota', command=eliminar_cuotas)
        btn_eliminar_cuota.grid(column=2, row=0)

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('cantidadcuotas', 'tasainteres')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('cantidadcuotas')
        self.tree.column('tasainteres')

        self.tree.heading('cantidadcuotas', text='Cantidad de Cuotas')
        self.tree.heading('tasainteres', text='Tasa de Interes')
        self.tree.grid(column=0, row=1, columnspan=4)

        render_cuotas()

if __name__ == '__main__':
    app = ConfigCuotasApp()
    app.mainloop()
