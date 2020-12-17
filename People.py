import pymongo

from Friends import Friends


class People:

    @staticmethod
    def lista_amigos(_id):
        conjunto = Friends.conjunto_amigos(_id)
        lista = list(conjunto)
        #lista.sort(_id)
        return lista

    @staticmethod
    def lista_disponibles(_id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]
        mydoc = mycol.find()
        conjunto = set()

        for x in mydoc:
            p = People(x.get("_id"))
            conjunto.add(p)

        conjuntoamigos = Friends.conjunto_amigos(_id)
        conjuntodis = conjunto.difference(conjuntoamigos)

        #Quitamos a la misma persona
        conjuntodis.remove(People(_id))

        listadispo = list(conjuntodis)
        return listadispo

    def __init__(self, _id):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]
        query = {"_id": _id}
        mydoc = mycol.find_one(query)
        self._id = mydoc.get("_id")
        self.firstname = mydoc.get("firstname")
        self.lastname = mydoc.get("lastname")

    def __init__(self, _id, firstname, lastname):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]
        mydict = {"_id": _id, "firstname": firstname, "lastname": lastname}
        mycol.insert_one(mydict)
        self._id = _id
        self.firstname = firstname
        self.lastname = lastname

    def get_id(self):
        return self._id

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def delete(self):
        client = pymongo.MongoClient("mongodb+srv://Gestionpymongo:Gestionpymongo@cluster0.iixvr.mongodb.net"
                                     "/Gestiondb?retryWrites=true&w=majority")
        mydb = client["Gestiondb"]
        mycol = mydb["People"]
        query = {"_id": self._id}
        mycol.delete_one(query)
        self._id = None
        self.firstname = None
        self.lastname = None

    def __str__(self):
        return self._id + "; " + self.firstname + "; " + self.lastname

