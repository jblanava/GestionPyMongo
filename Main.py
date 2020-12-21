import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import pymongo

client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
mydb = client["Gestiondb"]
seleccionado = -1

class People:

    @staticmethod
    def tuplas_personas():
        mycol = mydb["People"]
        mydoc = mycol.find()
        lista = []

        for x in mydoc:
            id_person = x.get("_id")
            firstname_person = x.get("firstname")
            lastname_person = x.get("lastname")
            tupla = (id_person, firstname_person, lastname_person)
            lista.append(tupla)

        lista.sort()
        return lista

    @staticmethod
    def lista_amigos(_id):
        conjunto = Friends.conjunto_amigos(_id)
        lista = list(conjunto)
        lista.sort()
        return lista

    @staticmethod
    def lista_disponibles(_id):
        mycol = mydb["People"]
        mydoc = mycol.find()
        conjunto = set()

        for x in mydoc:
            index = x.get("_id")
            if index != _id:
                person = People(index)
                conjunto.add(person)

        conjuntoamigos = Friends.conjunto_amigos(_id)
        conjuntodis = conjunto.difference(conjuntoamigos)

        #Quitamos a la misma persona
        listadispo = list(conjuntodis)
        listadispo.sort()
        return listadispo

    def __init__(self, _id):
        mycol = mydb["People"]

        query = {"_id": _id}
        mydoc = mycol.find_one(query)
        self._id = mydoc.get("_id")
        self.firstname = mydoc.get("firstname")
        self.lastname = mydoc.get("lastname")

    def get_id(self):
        return self._id

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def __str__(self):
        return str(self._id) + "; " + self.firstname + "; " + self.lastname

    def __lt__(self, other):
        return self.get_id() < other.get_id()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __hash__(self):
        return self.get_id()


class Friends:

    @staticmethod
    def conjunto_amigos(_id):
        mycol = mydb["Friends"]
        query = {"$or": [{"_id1": _id}, {"_id2": _id}]}
        mydoc = mycol.find(query)
        res = set()

        for x in mydoc:
            if x.get("_id1") == _id:
                p = People(x.get("_id2"))
                res.add(p)
            else:
                p = People(x.get("_id1"))
                res.add(p)

        return res

    def __init__(self, _id1, _id2):
        mycol = mydb["Friends"]

        query = {"$or": [{"_id1": _id1, "_id2": _id2}, {"_id1": _id2, "_id2": _id1}]}
        mydoc = mycol.find_one(query)

        if mydoc is None:
            mydict = {"_id1": _id1, "_id2": _id2}
            mycol.insert_one(mydict)
            self._id1 = _id1
            self._id2 = _id2
        else:
            self._id1 = mydoc.get("_id1")
            self._id2 = mydoc.get("_id2")

    def get_id1(self):
        return self._id1

    def get_id2(self):
        return self._id2

    def delete(self):
        mycol = mydb["Friends"]
        query = {"$or": [{"_id1": self._id1, "_id2": self._id2}, {"_id1": self._id2, "_id2": self._id1}]}
        mycol.delete_one(query)
        self._id1 = None
        self._id2 = None


#GUI

#PRECAUCION -> PONER EL ORDEN DE LOS COMPONENTES SEGUN SE VAYAN A MOSTRAR, ejecutar este script y cambiar de lugar el

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master


#CREAR TABLA
class Table(tk.Frame):
    def __init__(self, parent=None, title="", headers=[], height=10, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._title = tk.Label(self, text=title, font=("Trebuchet MS", 20), bg="#51d1f6")
        self._headers = headers
        self._tree = ttk.Treeview(self,
                                  height=height,
                                  columns=self._headers,
                                  show="headings", selectmode=tk.BROWSE, style="mystyle.Treeview")
        self._title.pack(side=tk.TOP, fill="x")

        # Agregamos dos scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')

        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.pack(side="left")
        #MANEJADOR DE TREE
        self._tree.tag_bind("mytag", "<<TreeviewSelect>>", self.item_selected)

        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(header, stretch=True,
                              width=tkFont.Font().measure(header.title()))

    def add_row(self, row):
        self._tree.insert('', 'end', values=row, tags=("mytag",))
        for i, item in enumerate(row):
            col_width = 75
            if self._tree.column(self._headers[i], width=None) < col_width:
                    self._tree.column(self._headers[i], width=col_width)

    def item_selected(self, event):
        item = self._tree.selection()[0]
        tupla = self._tree.item(item, option="values")
        global seleccionado
        seleccionado = int(tupla[0])
        refresh()

def insertFriend():
    try:
        #id de la tabla seleccionado
        table_selected = personas_tab._tree.selection()[0]
        table_tupla = personas_tab._tree.item(table_selected, option="values")
        table_index = int(table_tupla[0])

        #id de la lista disponibles
        dis_selected = lDisponibles.selection_get()
        dis_id = int(dis_selected.split(";")[0])

        #insertar en la bd si se han seleccionado
        if table_index is not None and dis_id is not None:
            Friends(table_index, dis_id)
            refresh()

    except:
        messagebox.showwarning(message="No se ha seleccionado un usuario", title="Error")

def deleteFriend():
    # id de la tabla seleccionado
    try:
        table_selected = personas_tab._tree.selection()[0]
        table_tupla = personas_tab._tree.item(table_selected, option="values")
        table_index = int(table_tupla[0])

        # id de la lista disponibles
        amigos_selected = lAmigos.selection_get()
        amigos_id = int(amigos_selected.split(";")[0])

        #Si los seleccionados no son vacios se borra
        if table_index is not None and amigos_id is not None:
            f = Friends(table_index, amigos_id)
            f.delete()
            refresh()
    except:
        messagebox.showwarning(message="No se ha seleccionado un usuario", title="Error")

def refresh():
    lAmigos.delete('0', 'end')
    lDisponibles.delete('0', 'end')
    listaAmigos = People.lista_amigos(seleccionado)
    listaDisponibles = People.lista_disponibles(seleccionado)

    cont = 1
    for x in listaAmigos:
        lAmigos.insert(cont, x)
        cont = cont + 1
    cont = 1
    for y in listaDisponibles:
        lDisponibles.insert(cont, y)
        cont = cont + 1


root = tk.Tk()
root.config(bg="#51d1f6")
Window(root)

# set window title
root.wm_title("Rastreator") #pone el titulo a la ventana
root.geometry('1200x700') #tamaño de la ventana

personas_headers = (u"ID", u"FIRSTNAME", u"LASTNAME")

personas_tab = Table(root, title="Personas", headers=personas_headers)
personas_tab.place(x=475, y=0)

cursor = People.tuplas_personas()

for row in cursor:
    personas_tab.add_row(row)

#LISTA DE AMIGOS
#label
labelAmigos = tk.Label(root, text="Amigos", font=("Trebuchet MS", 14), bg="#51d1f6")
labelAmigos.place(x=300, y=320)

#listbox
lAmigos = tk.Listbox(font=("Trebuchet MS", 12)) #crea un listbox donde mostrar los datos
lAmigos.config(width=40, height=12)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=lAmigos.yview)
scrollbar.place(x=500, y=350, height=280)

lAmigos.configure(yscrollcommand=scrollbar.set)
lAmigos.place(x=175, y=350)

#BOTONES
#boton de insertar
canvas = tk.Canvas(root, width=50, height=50)

imagetest = tk.PhotoImage(file="flecha_verde.png")
canvas.create_image(50, 50, image=imagetest)

bIns = tk.Button(root, image=imagetest, command=insertFriend) #crea un boton y pone un texto y un tamaño
bIns.config(width=50, height=50)
bIns.place(x = 575, y = 400)

#boton de eliminar
canvas2 = tk.Canvas(root, width=50, height=50)

imagetest2 = tk.PhotoImage(file="flecha_roja.png")
canvas2.create_image(50, 50, image=imagetest2)

bDel = tk.Button(root, image=imagetest2, command=deleteFriend) #crea un boton y pone un texto y un tamaño
bDel.config(width=50, height=50)
bDel.place(x = 575, y = 500)

#LISTA DE DISPONIBLES
#label
labelDis = tk.Label(root, text="Disponibles", font=("Trebuchet MS", 14), bg="#51d1f6")
labelDis.place(x=825, y=320)

#listbox
lDisponibles = tk.Listbox(font=("Trebuchet MS", 12))
lDisponibles.config(width=40, height=12)

scrollbar1 = ttk.Scrollbar(root, orient="vertical", command=lDisponibles.yview)
scrollbar1.place(x=1025, y=350, height=280)

lDisponibles.configure(yscrollcommand=scrollbar1.set)
lDisponibles.place(x=700, y=350)

root.mainloop() # show window
