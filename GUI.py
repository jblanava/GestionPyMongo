import tkinter
from tkinter import *
#PRECAUCION -> PONER EL ORDEN DE LOS COMPONENTES SEGUN SE VAYAN A MOSTRAR, ejecutar este script y cambiar de lugar el
# codigo del label, vereis que pasa
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

root = Tk()
app = Window(root) #crea una ventana

# set window title
root.wm_title("Tkinter window") #pone el titulo a la ventana
root.geometry('350x200') #tamaño de la ventana
lbl = Label(root, text="Label") #crea un label e indica en que ventana esta el label -> root
lbl.grid(column=0, row=0) #especifica la posicion
lbl.pack()
B = tkinter.Button(root, text ="Hello", font=("Arial Bold", 20)) #crea un boton y pone un texto y un tamaño
B.pack() #empaqueta al boton
listbox = Listbox() #crea un listbox donde mostrar los datos
listbox.insert(0, "Python") #en la pos 0 pon al elemento...
listbox.insert(1, "use")
listbox.insert(2, "c++")
listbox.insert(END, "Java") #en la ultima posicion pon el elemento...
listbox.pack() #empaquetar la lista


root.mainloop() # show window