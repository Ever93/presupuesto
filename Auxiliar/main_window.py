import tkinter as tk
from second_window import SecondWindow

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal")
        
        
        open_button = tk.Button(self.root, text="Abrir Segunda Ventana", command=self.open_window)
        open_button.pack()
    
    def open_window(self):
        SecondWindow()

root = tk.Tk()
app = MainWindow(root)
root.mainloop()