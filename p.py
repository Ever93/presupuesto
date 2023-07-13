import tkinter as tk

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana principal")
        self.btn_abrir = tk.Button(self, text="Abrir ventana secundaria", command=self.abrir_ventana_secundaria)
        self.btn_abrir.pack()

    def abrir_ventana_secundaria(self):
        self.withdraw()  # Ocultar la ventana principal
        self.ventana_secundaria = tk.Toplevel()
        self.ventana_secundaria.title("Ventana secundaria")
        self.ventana_secundaria.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_secundaria)

    def cerrar_ventana_secundaria(self):
        self.ventana_secundaria.destroy()  # Cerrar la ventana secundaria
        self.deiconify()  # Mostrar nuevamente la ventana principal

ventana_principal = VentanaPrincipal()
ventana_principal.mainloop()