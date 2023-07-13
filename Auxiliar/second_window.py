import tkinter as tk
from tkinter import ttk


class SecondWindow:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Segunda Ventana")
        
        # Agregar un Treeview con nombre y teléfono
        tree = tk.ttk.Treeview(self.window, columns=("Nombre", "Teléfono"))
        tree.heading("#0", text="")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Teléfono", text="Teléfono")
        tree.pack()