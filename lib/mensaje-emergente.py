import tkinter
from tkinter import messagebox

def aparece_perrito():
    messagebox.showwarning("PROCESO DETENIDO","se reanuda en 1 minuto")

mi_ventana = tkinter.Tk()
mi_ventana.geometry("640x480")

mi_boton = tkinter.Button(text="PROCESO DETENIDO", command = aparece_perrito)
mi_boton.pack()

mi_ventana.mainloop()
